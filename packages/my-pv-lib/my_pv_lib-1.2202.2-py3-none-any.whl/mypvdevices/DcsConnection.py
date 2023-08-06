#!/usr/bin/python

import logging
from datetime import datetime, timedelta
import time
import socket
import random
import json
import threading
import queue
import string
from xtea import MODE_CBC, new
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mypvdevices.ServerConnection import ServerConnection


JOINTIMEOUT = 3
RECEIVEMQSITZE = 10
SERIALLEN = 16
CRYPTOKEYLEN = 32
ACKTIMEOUT = 0.5
BUFFERSIZE = 2048
SOCKETRETRIES = 3
SOCKETWAITTIME = 1
KEEPALIVETIMEOUT = 25
RECONNECTTIMEOUT = 5
TIDBLOCKTIME = 90
MAXIMUMSENDTIME = 1.5
MAXIMUMTRANSACTIONTIME = 3
MAXMESSAGEAGE = 5
RECEIVEMSGQUEUSIZE = 2
LOGDATABLOCKTIME = 120

class DcsConnection(ServerConnection):
    _serial = None
    __cryptoKey__ = None
    _serverAddress = None
    _serverPort = None
    _socket = None
    _connected = False
    _receiveBuffer = None
    _receiverThread = None
    _workerThread = None
    _socketLock = None
    _threadLock = None
    _messageLock = None
    _running = False
    _sentRequests = None
    _ackReceivedEvent = None
    _receivedMessageQueue = None
    _lastMessageTime = None
    _lastMessageSendTime = None
    _keepConnected = False
    _device = None
    _logdata = None
    _logdataTimeStamp = None
    
    def __init__(self, serial, cryptoKey, server, port):
        if serial != None and len(serial) == SERIALLEN:
            self._serial = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)

        if cryptoKey != None and len(cryptoKey) == CRYPTOKEYLEN and type(cryptoKey) == str:
            self.__cryptoKey__ = bytearray.fromhex(cryptoKey)
        else:
            errmsg = "Instance not created. CryptoKey invalid. CryptoKey=" + str(cryptoKey)
            logging.error(errmsg)
            raise ValueError(errmsg)

        if server != None:
            self._serverAddress = server
        else:
            errmsg = "Instance not created. Server is required"
            logging.error(errmsg)
            raise ValueError(errmsg)
        
        if port != None and port > 0 and port < 65636:
            self._serverPort = port
        else:
            errmsg = "Instance not created. Port out of range. Port=" + str(port)
            logging.error(errmsg)
            raise ValueError(errmsg)

        self._socketLock = threading.Lock()
        self._threadLock = threading.Lock()
        self._messageLock = threading.Lock()
        self._sentRequests = dict()
        self._ackReceivedEvent = threading.Event()
        self._receivedMessageQueue = queue.Queue(RECEIVEMQSITZE)

        logging.debug("DcsConnection created. Serial: " + str(self._serial))

    def __del__(self):
        self._running = False

    def getServer(self):
        return self._serverAddress

    def getsockethash(self):
        return self._socket.__hash__()

    def addDevice(self, device):
        if(device != None):
            self._device = device
            return True
        else:
            return False

    def isconnected(self):
        return self._connected

    def connect(self):
        logging.info(str(id(self)) + " connecting " + str(self._serial ) + "@" + str(self._serverAddress) + ":" + str(self._serverPort) + "...")
        if(self._connected == True):
            return True

        self._lastMessageTime = None
        if(not self._running):
            self.__start__()
        else:
            logging.debug(str(id(self)) + " threads already running")
        try:
            result = self._dcsConnect()
        except Exception as e:
            logging.warning(str(id(self)) + " Failed to open socket " + str(self._serial ) + "@" + str(self._serverAddress) + ":" + str(self._serverPort) + ". Server down or network error?")
            self._keepConnected = True
            return False
        if not result:
            logging.warning(str(id(self)) + " Failed to connect " + str(self._serial ) + "@" + str(self._serverAddress) + ":" + str(self._serverPort) + ". Check encryption key!")
        else:
            logging.info(str(id(self)) + " Successfully connected " + str(self._serial ) + "@" + str(self._serverAddress) + ":" + str(self._serverPort) + ".")
        self._keepConnected = True
        return result

    def disconnect(self):
        self._keepConnected = False
        self._connected = False
        self.__stop__()
        result = self._dcsDisconnect()
        if(result):
            logging.info(str(id(self)) + " successfully disconnected")
        else:
            logging.warning(str(id(self)) + "cannont disconnect")
        return result
        
    def reconnect(self):
        self._connected = False
        self._keepConnected = False
        result = self._dcsDisconnect()
        if(result):
            logging.info(str(id(self)) + " successfully disconnected. Ready to reconnect")
        else:
            logging.warning(str(id(self)) + "cannont disconnect")
        return self.connect()

    def __createReceiverThread__(self):
        return threading.Thread(target=self.__receive__, name="DCS-RECEIVER "+str(self._serial )+"@"+str(self._serverAddress)+":"+str(self._serverPort))

    def __createWorkerThread__(self):
        return threading.Thread(target=self.__worker__, name="DCS-WORKER "+str(self._serial )+"@"+str(self._serverAddress)+":"+str(self._serverPort))

    def __start__(self):
        logging.debug("Threads starting...")
        self._running = True
        self._receiverThread = self.__createReceiverThread__()
        self._workerThread = self.__createWorkerThread__()
        try:
            self._receiverThread.start()
            self._workerThread.start()
        except Exception as e:
            logging.warning("Threads starting with Exception " + str(e))
    
    def __stop__(self):
        logging.debug("Threads stopping...")
        self._connected = False
        with self._threadLock:
            self._running = False
            if(self._receiverThread != None and self._receiverThread.is_alive()):
                self._receiverThread.join(JOINTIMEOUT)
            logging.debug("Receiver stopped. ")
            if(self._workerThread != None and self._workerThread.is_alive()):
                self._workerThread.join(JOINTIMEOUT)
            logging.debug("Worker stopped.")

    ##receiving messages
    def __receive__(self):
        logging.debug(str(id(self)) + " Receiver running...")
        while self._running == True:
            wait = False
            with self._socketLock:
                if(self._socket != None and not self._socket._closed):
                    try:
                        rec = self._socket.recv(BUFFERSIZE)
                        self._receiveBuffer += rec
                    except BlockingIOError as e:
                        if e.errno != 10035 and e.errno != 11:
                            logging.error(str(id(self)) + " BlockingIOError: " + str(e))
                    except Exception as e:
                        logging.error(str(id(self)) + " Unknown error receiving data from socket. " + str(e))
                        wait = True     # set wait but don't wait here because mutex has to be released first

            if(wait == True):
                wait = False
                logging.warning(str(id(self)) + " Waiting for socket to recover")
                time.sleep(SOCKETWAITTIME)

            if self._receiveBuffer != None and len(self._receiveBuffer)>=32:			
                rec_serialno = self._receiveBuffer[0:SERIALLEN].decode("utf-8")
                rec_tid = int.from_bytes(self._receiveBuffer[SERIALLEN:18],"little")
                rec_msgtype = int(self._receiveBuffer[18])
                rec_paylen = int.from_bytes(self._receiveBuffer[19:21],"little")
                rec_payload = self._receiveBuffer[32:(32+rec_paylen)]
                self._receiveBuffer = self._receiveBuffer[(32+rec_paylen):]

                if(rec_serialno != self._serial ):
                    logging.warning(str(id(self)) + " Invalid serial in received data: " + str(rec_serialno))
                else:
                    logging.debug(str(id(self)) + " Received TID:" + str(rec_tid) + "; Type:" + str(rec_msgtype) + " Paylen: "+str(rec_paylen))
                    message = {
                        "tid": rec_tid,
                        "type": rec_msgtype,
                        "payload": rec_payload,
                        "receivetime": datetime.now()
                    }
                    try:
                        self._receivedMessageQueue.put_nowait(message)
                    except Exception as e:
                        logging.warning(str(id(self)) + " cannot put message in _receivedMessageQueue: " + str(e))
                    self._lastMessageTime = datetime.now()

                    if self._receivedMessageQueue.qsize() >= RECEIVEMSGQUEUSIZE:
                        logging.warning(str(id(self)) + " receivedMessageQueue size exceeded. Size: " + str(self._receivedMessageQueue.qsize()))
            else:
                logging.debug(str(id(self)) + " nothing to receive.")
                time.sleep(0.1)
 
    #handling massages
    def __worker__(self):
        logging.debug(str(id(self)) + " Worker running...")
        cleanupconter = 0
        while self._running == True:
            if cleanupconter > 50:
                try:
                    self.__cleanSentrequests__()
                    cleanupconter = 0
                except Exception as e:
                    logging.debug(str(id(self)) + " error cleaning mq: " + str(e))
            cleanupconter += 1

            try:
                message = self._receivedMessageQueue.get_nowait()
            except Exception:
                message = None
                time.sleep(0.1)

            if(message):
                logging.debug(str(id(self)) + " Handling Message: " + str(message))
                try:
                    difference = datetime.now() - message["receivetime"]
                    if(difference.total_seconds() < MAXMESSAGEAGE or message["type"] == 9):
                        self.__handlemessage__(message["type"], message["payload"], message["tid"])
                        processingtime = datetime.now() - message["receivetime"]
                        if(processingtime.total_seconds() > MAXMESSAGEAGE):
                            logging.warning(str(id(self)) + " processing time too long: " + str(processingtime.total_seconds()) + ". MsgType: " + str(message["type"]) + ", TID: " + str(message["tid"]))
                    else:
                        logging.warning(str(id(self)) + " message to old. Rejecting message. Age: " + str(difference.total_seconds()) + ". MsgType: " + str(message["type"]) + ", TID: " + str(message["tid"]))
                except Exception as e:
                    logging.error(str(id(self)) + " Error handling message. " + str(e))

    def __handlemessage__(self, msgtype, payload, tid):
        if(msgtype == 9):
            logging.debug(str(id(self)) + " TID: " + str(tid) + "; Received ACK")
            try:
                self._ackrequest(tid)    #just notify waiting messages and do nothing more
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error handling ACK")
            return

        if(msgtype == 8):
            logging.debug(str(id(self)) + " TID: " + str(tid) + "; Received Keep Alive.")
            try:
                self._send(None, 9, tid, isresponce=True)     #send ACK
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending ACK")
            return

        if(msgtype == 4):
            logging.debug(str(id(self)) + " TID: " + str(tid) + "; Received Curent Data Request.")
            try:
                self.senddata(tid=tid)
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending data." +  str(e))
            return

        if(msgtype == 5):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Received Setup Change.")
            try:
                self._changeSetup(payload)
            except Exception as e:
                logging.error(str(id(self)) + " Error applying setup changes. " + str(e))
            try:
                self.sendsetup(tid=tid)
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending setup response")
            return

        if(msgtype == 6):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Received Calc Log Data (for MSG-Type 2).")
            if payload != None:
                time = self._decryptPayload(payload)
            else:
                time = None
            nack=True
            try:
                self.loadlogdata(time)
                nack=False
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + "; Error getting logData. " +  str(e))
            try:
                self._send(None, 9, tid, isresponce=True, nack=nack)     #send ACK/NACK
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending ACK/NACK for Calc Log Data. NACK=" + str(nack))
            if nack == False:
                self.clearlogdata()
            return

        if(msgtype == 7):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Received Send Log Daten (MSG-Type 2).")
            try:
                self.sendlogdata(tid=tid)
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending logData.")
                try:
                    self._send(None, 9, tid, isresponce=True, nack=True)     #send NACK
                except Exception as sendexception:
                    logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending NACK for Send Log Data. " + str(sendexception)) 
            return

        logging.info(str(id(self)) + " TID: " + str(tid) + "; Unknown MSG-Type received: " + str(msgtype) + ".")
    
    def watchdog(self):
        logging.debug(str(id(self)) + " DCS-Watchdog running...")
        with self._threadLock:
            if(self._running != True):
                logging.warning(str(id(self)) + "DCS-Watchdog: DCS-Connection ist stopped.")
                return self._running

            if(self._receiverThread != None and not self._receiverThread.is_alive()):
                logging.warning(str(id(self)) + " Receiver thread death. Restarting...")
                try:
                    self._receiverThread = self.__createReceiverThread__()
                    self._receiverThread.start()
                except Exception as e:
                    logging.warning(str(id(self)) + " Error restarting receiver Thread: " + str(e))
            
            if(self._workerThread != None and not self._workerThread.is_alive()):
                logging.warning(str(id(self)) + " Worker thread death. Restarting...")
                try:
                    self._workerThread.join(0.1)
                    self._workerThread = self.__createWorkerThread__()
                    self._workerThread.start()
                except Exception as e:
                    logging.warning(str(id(self)) + " Error restarting worker Thread: " + str(e))
            
        if(self._lastMessageTime != None):
            difference = datetime.now() - self._lastMessageTime
            if(difference.total_seconds() > KEEPALIVETIMEOUT):
                logging.error(str(id(self)) + " No message received for more then " + str(KEEPALIVETIMEOUT) + " secunds. Reconnecting...")
                try:
                    self.reconnect()
                except Exception as e:
                    logging.warning(str(id(self)) + "Cannot reconect. " + str(e))

        if(self._keepConnected == True and self._connected != True):
            logging.info(str(id(self)) + " disconnection detected. Reconnecting...")
            try:
                self.reconnect()
            except Exception as e:
                logging.warning(str(id(self)) + "Cannot reconect. " + str(e))
        
        try:
            self._checkSocket()
        except Exception as e:
                logging.warning(str(id(self)) + "Cannot check socket. " + str(e))

        logging.debug(str(id(self)) + " MSQ-Size: " + str(self._receivedMessageQueue.qsize()))
        return self._running

    def __cleanSentrequests__(self):
        with self._messageLock:
            cleanList = []
            for request in self._sentRequests:
                try:
                    if self._sentRequests[request] != None and self._sentRequests[request]["timestamp"] < datetime.now() - timedelta(seconds=TIDBLOCKTIME):
                        cleanList.append(request)
                except Exception as e:
                    logging.debug(str(id(self)) + " request " + str(request) + " element does not exist anymore. " + str(e))

            for element in cleanList:
                try:
                    logging.debug(str(id(self)) + " Cleaning up request " + str(element) + ".")
                    del self._sentRequests[element]
                except Exception as e:
                    logging.debug(str(id(self)) + " Cannot clean request " + str(element) + ". " + str(e))

    def _dcsConnect(self):
        if not self._connected:
            self._sentRequests.clear()
            logging.debug(str(id(self)) + " preparing socket.... ")
            if(self._checkSocket()):
                try:
                    self.sendsetup(True)
                except Exception as e:
                    logging.error(str(id(self)) + " connection failed. " + str(e))
                    return False

                self._connected = True
                logging.debug(str(id(self)) + " connected " + str(self._serial ))
                return True
            else:
                logging.error(str(id(self)) + " connection failed. No socket available")
                raise Exception("socket error")

    def _checkSocket(self):
        with self._socketLock:
            result = True
            if self._socket == None or self._socket._closed:
                result = self._openSocket()
            return result

    def _openSocket(self):
        socketRetries = 0
        logging.debug(str(id(self)) + " No socket. Opening socket...")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(RECONNECTTIMEOUT)
        self._receiveBuffer = bytes()
        host = ""
        try:
            host = socket.gethostbyname(self._serverAddress)
        except Exception:
            logging.error(str(id(self)) + " Host not found.")
            self._socket = None
            return False

        while(socketRetries <= SOCKETRETRIES):
            try:
                logging.debug(str(id(self)) + " trying to connect socket " + str(host) + ":" + str(self._serverPort) + "...")
                self._socket.connect((host, self._serverPort))
                break
            except Exception:
                logging.warning(str(id(self)) + " Cannot open socket to " + str(host) + ":" + str(self._serverPort) + ".")
                socketRetries = socketRetries + 1
                time.sleep(SOCKETWAITTIME)
            if socketRetries > SOCKETRETRIES:
                self._socket = None
                
        if(self._socket != None):
            self._socket.setblocking(0)
            return True
       
        logging.info(str(id(self)) + " Opening socket failed. Too many retries: " + str(socketRetries))
        return False

    def _dcsDisconnect(self):
        try:
            if self._receivedMessageQueue != None:
                self._receivedMessageQueue.queue.clear()
        except Exception as e:
            logging.error(str(id(self)) + " cannot clear receivedMessageQueue. " + str(e))
            return False
        if self._socket == None or self._socket._closed:
            logging.info(str(id(self)) + " Socket is already closed")
            return True
        try:
            self._closeSocket()
            logging.info(str(id(self)) + " Socket closed")
            return True
        except Exception as e:
            logging.error(str(id(self)) + " closing socket failed. " + str(e))
            return False    

    def _closeSocket(self):
        self._socketLock.acquire()
        self._socket.close()
        self._socketLock.release()

    def _ackrequest(self, tid):
        with self._messageLock:
            try:
                self._sentRequests[tid]["state"] = "ACK"
                self._sentRequests[tid]["timestamp"] = datetime.now()
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + " Request not found. ACK not set. " + str(e))

            try:
                self._sentRequests[tid]["event"].set()       #wakeup request
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + " Request not found. Could not wakeup. " + str(e))

    def _send(self, payload, msgtype, tid, isresponce=False, nack=False):
        startsendtime = datetime.now()
        if self._socket == None or self._socket._closed:
            errmsg = str(id(self)) + "Cannot send. No open Socket."
            logging.error(errmsg)
            raise ConnectionError(errmsg)
        try:
            package = self._make_package(self._serial , payload, msgtype, tid, nack)
        except Exception as e:
            return False
        if package != None:
            if self._registermessage(tid, msgtype, isresponce):
                with self._socketLock:
                    try:
                        self._socket.send(package)
                        self._lastMessageSendTime = datetime.now()
                        logging.debug(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " transmitted.")
                    except Exception as e:
                        logging.error(str(id(self)) + " cannot send. " + str(e))
                        return False

                difference = datetime.now() - startsendtime
                if(difference.total_seconds() > MAXIMUMSENDTIME):
                    logging.warning(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " sending time to hight! " + str(difference.total_seconds()))
                
                if(isresponce == False):
                    if(not self._waitForAck(tid)): 
                        logging.warning(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " no ACK received.")
                        return False

                difference = datetime.now() - startsendtime
                if(difference.total_seconds() > MAXIMUMTRANSACTIONTIME):
                    logging.warning(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " transaction time to hight! " + str(difference.total_seconds()))

                logging.debug(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " successfull send. Transaction-time: " + str(difference.total_seconds()))
                return True
            else:
                return False
        else:
            logging.error(str(id(self)) + " no package to send")
            return False

    def _registermessage(self, tid, msgtype, isresponce=False):
        if msgtype == 9 or isresponce==True:
            return True;
        with self._messageLock:
            try:
                self._sentRequests[tid]
                if self._sentRequests[tid] != None:
                    logging.error("[" + self._serial + "] tid " + str(tid) + " already in use")
                    return False
            except Exception:
                pass

            event = threading.Event()
            self._sentRequests[tid] = {
                "timestamp": datetime.now(),
                "event": event,
                "state": "NEW"
            }
            return True

    def _waitForAck(self, tid):
        with self._messageLock:
            try:
                if(self._sentRequests[tid]["state"] != "ACK"):   #message has already been acked in the while
                    self._sentRequests[tid]["state"] = "SEND"
                    self._sentRequests[tid]["timestamp"] = datetime.now()
                    event = self._sentRequests[tid]["event"]
                else:
                    event = None
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + " MSG not registrated. " + str(e))
                return False

        if(event):
            event.wait(ACKTIMEOUT)

        response = False
        with self._messageLock:
            try:
                if(self._sentRequests[tid]["state"] == "ACK"):
                    response = True
                del self._sentRequests[tid]
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + " MSG not found. " + str(e))
            return response

    def _wakeUpWaitingMessages(self):
        self._socketLock.acquire()
        for item in self._sentRequests.values():
            temp = item["event"]
            temp.set()
        self._socketLock.release()

    def _make_package(self, device_serno, payl, msgtype, tid, nack=False):
        if(len(device_serno) != SERIALLEN):
            errorMsg = str(id(self)) + " invalid serial " + str(device_serno)
            logging.warning("TID: " + str(tid) + " MakePackage: " + str(errorMsg))
            raise Exception(errorMsg)

        if(msgtype == None):
            errorMsg = str(id(self)) + " no msgtype set "
            logging.warning("TID: " + str(tid) + " MakePackage: " + str(errorMsg))
            raise Exception(errorMsg)

        if(tid == None):
            errorMsg = str(id(self)) + " invalid TID " + str(tid)
            logging.warning("TID: " + str(tid) + " MakePackage: " + str(errorMsg))
            raise Exception(errorMsg)

        if(payl != None):
            try:
                payload = json.dumps(payl).encode('utf-8')
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + " Invalid Payload: " + str(payl) + ". " + str(e))
                return False
        else:
            payload = bytes()
        
        try:
            rand = self._get_random_string(8)
            iv = rand.encode('utf-8')
        except Exception as e:
            logging.error("TID: " + str(tid) + " Error generating IV: " + str(e))
            raise(e)
        xtea = new(self.__cryptoKey__, mode = MODE_CBC, IV = iv)

        missing = 8 - len(payload) % 8
        if missing < 8:
            payload = payload + B'\x00' * missing   #always multiple of 8
        if(len(payload) != 0):
            payload = random.randint(0, 2^32).to_bytes(4, byteorder="little")+random.randint(0, 2^32).to_bytes(4, byteorder="little") + payload      # add 8 bytes for initial vector
       
        payload = xtea.encrypt(payload)
        payloadLengh = len(payload).to_bytes(2, byteorder="little")    #calc payload
        Cloudsocket_tid= tid.to_bytes(2, byteorder="little")
        Cloudsocket_msgtype = bytes([msgtype])
        if nack == True:
            ackn = B'\x00'
        else:
            ackn = B'\x01'
        if self._device != None:
            try:
                healthState = self._device.gethealthstate()
            except Exception as e:
                logging.error("TID: " + str(tid) + " Cannot get healthstate: " + str(e))
                healthState = 0
        else:
            healthState = 0
        healthStateByte = healthState.to_bytes(1, byteorder="little")
        header = device_serno.encode('utf-8') + Cloudsocket_tid + Cloudsocket_msgtype + payloadLengh + ackn + healthStateByte + B'\x00'*9  #build 32 byte header
        package = header + payload
        return  package

    def _get_random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str 

    def _decryptPayload(self, payload):
        iv=payload[(len(payload)-8):]
        xtea = new(self.__cryptoKey__, mode=MODE_CBC,IV=iv)
        payload_decrypted = xtea.decrypt(payload)[8:(len(payload)-2)]
        payload_string = payload_decrypted.decode()
        payload_string_stripped = payload_string.rstrip('\x00')
        return payload_string_stripped

    def _getsetupelements(self, payload_string):
        message_string = payload_string[payload_string.find("?")+1:]
        seperator = message_string.find("/")
        if seperator != -1:
            setup_string = message_string[0:seperator]
        else:
            setup_string = message_string
        logging.debug("["+str(self._serial )+"@"+str(self._serverAddress)+":"+str(self._serverPort)+"]; Setup changes: " + str(setup_string))
        elements = setup_string.split("&")
        return elements

    def senddata(self, tid=None):
        if(self._connected):
            try:
                data = self._getCurrentData()
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + ", cannot get CurrentData: " + str(e))
            if(tid == None):
                isresponce=True
                tid = self._getTid()
            else:
                isresponce=True
                if(tid > 65535 or tid < 1):
                    raise Exception("TID out of range (1-65535)")
            logging.info(str(id(self)) + " TID: " + str(tid) + ", sending data: " + str(data))
            try:
                if(not self._send(data, 1, tid, isresponce=isresponce)):
                    raise Exception("Cannot send data. TID: " + str(tid) + ". " + str(data))
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + ", Error: " + str(e))
                raise
        else:
            errormsg = str(id(self)) + " Error sendig Data. Not connected"
            logging.error(errormsg)
            raise Exception(errormsg)

    def sendlogdata(self, tid=None):
        logData = self._logdata
        if(logData == None):
            error = str(id(self)) + " Cannot send logData. Empty Logdata."
            logging.warning(error)
            raise Exception(error)

        if(self._connected):
            if(tid == None):
                tid = self._getTid()
                isresponce = True
            else:
                isresponce = True
                if(tid > 65535 or tid < 1):
                    raise Exception("TID out of range (1-65535)")
            logging.info(str(id(self)) + " TID: " + str(tid) + ", sending logData: " + str(self._logdata))
            try:
                if(not self._send(logData, 2, tid, isresponce=isresponce)):
                    raise Exception("Error sending logData.")
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + ", Error: " + str(e))
                raise
        else:
            errormsg = "Error sendig LogData. Not connected"
            logging.error(errormsg)
            raise Exception(errormsg)

    def _getTid(self):
        with self._messageLock:
            found = None
            while found == None:
                tid = random.randint(1, 65535)
                try:
                    self._sentRequests[tid]
                except:
                    found = tid
                    self._sentRequests[tid] = None
        return found

    def sendsetup(self, forced = None, tid=None):
        if(self._connected or forced):
            setup = self._getsetup()
            if(tid == None):
                tid = self._getTid()
                isresponce = False
            else:
                isresponce = True
                if(tid > 65535 or tid < 1):
                    raise Exception("TID out of range (1-65535)")
            logging.info(str(id(self)) + " TID: " + str(tid) + ", sending setup: " + str(setup))
            try:
                if(not self._send(setup, 3, tid, isresponce=isresponce)):
                    raise Exception("Error sending setup.")
            except Exception as e:
                logging.error("TID: " + str(tid) + ", Error: " + str(e)) 
                raise
        else:
            errormsg = "Error sendig Setup. Not connected"
            logging.error(errormsg)
            raise Exception(errormsg)

    def _getsetup(self):
        if(self._device == None):
            logging.warning(str(id(self)) + " device not found. sending dummy setup")
            return {"device": "ConnectionTest", "fwversion": "1.0.0", "serialno": self._serial }
        else:
            return self._device.getsetup()

    def _getCurrentData(self):
        if(self._device == None):
            logging.warning(str(id(self)) + " device not found. getting dummy currData")
            t = datetime.now()
            return {"power": t.second * 100}
        else:
            try:
                return self._device.getdata()
            except Exception as e:
                logging.warning(str(id(self)) + " cannot get data. " + str(e))
            
    
    def loadlogdata(self, time = None):

        if self._logdataTimeStamp != None:
            difference = datetime.now() - self._logdataTimeStamp
            if(difference.total_seconds() < LOGDATABLOCKTIME): 
                logging.warning(str(id(self)) + " cannot get logdata. Minimum waiting time (" + str(LOGDATABLOCKTIME) +") not reached. " + str(difference.total_seconds()))
                raise Exception("Logdata not ready.")

        t = datetime.now()
        if time == None:
            time = t.strftime("%Y%m%d%H%M%S")
        else:
            time = str(time)
            
        if(self._device == None):
            logging.warning(str(id(self)) + " device not found. getting dummy logData")
            self._logdata = {"i_power": t.second * 100, "time": time}
        else:
            try:
                self._logdata = self._device.getlogdata(time)
            except Exception as e:
                logging.warning(str(id(self)) + " cannot get logdata. " + str(e))

        
        self._logdataTimeStamp = t

    def clearlogdata(self):
        if(self._device == None):
            logging.debug(str(id(self)) + " device not found. nothing to clean.")
        else:
            try:
                self._device.clearlog()
            except Exception as e:
                logging.warning(str(id(self)) + " cannot clean logdata.")

    def _changeSetup(self, payload):
        try:
            setupstring = self._decryptPayload(payload)
            setupChanges = self._getsetupelements(setupstring)
            logging.debug(str(id(self)) + " Changing setup: " + str(setupChanges))
        except Exception as e:
            error = str(id(self)) + " Error decoding setup changes: " + str(e)
            logging.error(error)
            setupChanges = None
            raise Exception(error)

        if(setupChanges != None):
            for elements in setupChanges:
                setting = elements.split("=")
                field = setting[0]
                value = int(setting[1])

                if(self._device == None):
                    logging.warning(str(id(self)) + " device not found. Settings not applied.")
                    print("Field:" + str(field) + "; Value=" + str(value))
                else:
                    self._device.setsetupvalue(field, value)        					

# Entry Point     
if __name__ == "__main__":

    from colr import color

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    serial = "120100200505tes1"
    serial2 = "120100200505tes2"
    serial3 = "120100200505tes3"
    cryptoKey = "41424142414241424142414241424142"
    cryptoKeyInvalid = "ABABABABABABAB00ABABABABABABAB00"
    server = "my-pv.live"

    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()

    # if True:
    #     connection = DcsConnection(serial, cryptoKey, server, 50333)
    #     connection2 = DcsConnection(serial2, cryptoKey, server, 50333)
    #     connection.connect()
    #     connection2.connect()
    #     hash1 = connection.getsockethash()
    #     hash2 = connection2.getsockethash()
    #     try:
    #         while True:
    #             print(color('[DCS-Connection] Communication active. Press CTRL+C to stop', fore='blue', style='bright'))
    #             connection.watchdog()
    #             connection2.watchdog()
    #             if(hash1 != connection.getsockethash()):
    #                 print(color('[DCS-Connection] Socket of serial ' + str(serial) + ' has changed.', fore='red', style='bright'))
    #                 hash1 = connection.getsockethash()
    #             if(hash2 != connection2.getsockethash()):
    #                 print(color('[DCS-Connection] Socket of serial ' + str(serial2) + ' has changed.', fore='red', style='bright'))
    #                 hash2 = connection2.getsockethash()

    #             time.sleep(10)
    #     except KeyboardInterrupt as e:
    #         print("[DCS-Connection] Stopping Test...")
    #         connection.disconnect()
    #         connection2.disconnect()

    #AUTO-Tests
    #Constructor Tests
    try:
        DcsConnection("toShort", cryptoKey, server, 50333)
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))

    try:
        DcsConnection(serial, cryptoKey, server, None)
        print(color('ERROR: Creation without port.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without port.', fore='green', style='bright'))

    try:
        DcsConnection(serial, cryptoKey, server, 123456789)
        print(color('ERROR: Creation invalid port.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation invalid port.', fore='green', style='bright'))

    try:
        DcsConnection(serial, cryptoKey, None, 50333)
        print(color('ERROR: Creation without server.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without server.', fore='green', style='bright'))

    try:
        DcsConnection(serial, None, server, 50333)
        print(color('ERROR: Creation without CryptoKey.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without CryptoKey.', fore='green', style='bright'))

    try:
        DcsConnection(serial, "tooShortKey", server, 50333)
        print(color('ERROR: Creation with to short CryptoKey.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation with to short CryptoKey.', fore='green', style='bright'))

    try:
        DcsConnection(None, cryptoKey, server, 50333)
        print(color('ERROR: Creation without serial.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without serial.', fore='green', style='bright'))

# Connection Tests
    #connecting to unknown host
    connection = DcsConnection(serial, cryptoKey, "noserver.my-pv.live", 50333)
    if(connection.connect()):
        print(color('ERROR: Connecting to invalid host.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting to invalid host.', fore='green', style='bright'))
    connection.disconnect()
    
    #connecting to invalid port
    connection = DcsConnection(serial, cryptoKey, server, 1234)
    if(connection.connect()):
        print(color('ERROR: Connecting to invalid port.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting to invalid port.', fore='green', style='bright'))
    connection.disconnect()

    #regular connection
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    if(not connection.connect()):
        print(color('ERROR: Regular connection.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Regular connection.', fore='green', style='bright'))
    connection.disconnect()

    if(not connection.disconnect()):
        print(color('ERROR: disconnection.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: disconnection.', fore='green', style='bright'))
    connection.disconnect()

    #reconnecting
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    if(not connection.reconnect()):
        print(color('ERROR: reconnection.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: reconnection.', fore='green', style='bright'))
    connection.disconnect()

    #connecting to twice
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    if(not connection.connect()):
        print(color('ERROR: Connecting twice.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting twice.', fore='green', style='bright'))
    connection.disconnect()

    #connecting after disconnecting
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    connection.disconnect()
    if(not connection.connect()):
        print(color('ERROR: Connecting again.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting again.', fore='green', style='bright'))
    connection.disconnect()

    #connecting with invalid cryptoKey
    connection = DcsConnection(serial, "1"*CRYPTOKEYLEN, server, 50333)
    if(connection.connect()):
        print(color('ERROR: Connection with an invalid crypto key esteblished.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connection with an invalid crypto key failed.', fore='green', style='bright'))
    try:
        connection.senddata()
        print(color('ERROR: sending data with invalid encryption Key.', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: sending data with invalid encryption Key.', fore='green', style='bright'))
    connection.disconnect()

    #connecting unknown device
    connection = DcsConnection("0123456789ABCEFG", cryptoKey, server, 50333)
    if(connection.connect()):
        print(color('ERROR: Connection using an unknown serial esteblished.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connection using an unknown serial failed.', fore='green', style='bright'))
    try:
        connection.senddata()
        print(color('ERROR: sending data with unknown device.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending data with unknown device.', fore='green', style='bright'))
    connection.disconnect()

    #Starting/Stopping Thread
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        connection.__start__()
        time.sleep(2)
        connection.__stop__()
        print(color('SUCCESS: Starting/Stopping Thread.', fore='green', style='bright'))
    except Exception as e:
        print(e)
        print(color('ERROR: Starting/Stopping Thread.', fore='red', style='bright'))
    connection.disconnect()

    #sending using valid connection after trying to connect with an invalid connection
    #valid connection
    connection = DcsConnection(serial, cryptoKey, server, 50333) 
    state = connection.connect()
    #connection with invalid key but same serial
    connection2 = DcsConnection(serial, cryptoKeyInvalid, server, 50333) 
    state2 = connection2.connect()
    #send data using first valid connection
    try:
        connection.senddata()
        print(color('SUCCESS: sending using valid connection after trying to connect with an invalid connection.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending using valid connection after trying to connect with an invalid connection.', fore='red', style='bright'))
    connection.disconnect()
    connection2.disconnect()

#Communication Tests
    #send without beeing connected
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        connection.sendsetup()
        print(color('ERROR: sending setup without beeing connected.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending setup without beeing connected.', fore='green', style='bright'))

    try:
        connection.senddata()
        print(color('ERROR: sending data without beeing connected.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending data without beeing connected.', fore='green', style='bright'))

    try:
        connection.loadlogdata()
        connection.clearlogdata()
        connection.sendlogdata()
        print(color('ERROR: sending logData without beeing connected.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending logData without beeing connected.', fore='green', style='bright'))

    try:
        connection.connect()
    except Exception as e:
        print(color('ERROR: Cannot connect for connection tests.', fore='red', style='bright'))

    try:
        connection.senddata()
        print(color('SUCCESS: sending data.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending data.', fore='red', style='bright'))

    try:
        print("waiting...")
        time.sleep(LOGDATABLOCKTIME)
        connection.loadlogdata()
        connection.clearlogdata()
        connection.sendlogdata()
        print(color('SUCCESS: sending logData.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending logData.', fore='red', style='bright'))

    try:
        connection.loadlogdata()
        print(color('ERROR: getting logData to without waiting.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: getting logData to without waiting.', fore='green', style='bright'))

    try:
        connection.sendsetup()
        print(color('SUCCESS: sending setup.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending setup.', fore='red', style='bright'))

    connection.disconnect()

    #sending empty logData
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    try:
        connection.sendlogdata()
        print(color('ERROR: sending empty logData.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: sending empty logData.', fore='green', style='bright'))
    connection.disconnect()

    ##active/passive clients tests
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    socketHash = connection.getsockethash()
    time.sleep(15 + KEEPALIVETIMEOUT)
    if(connection.isconnected() and socketHash == connection.getsockethash()):
        print(color('SUCCESS: Check isconnected.', fore='green', style='bright'))
    else:
        print(color('ERROR: Check isconnected.', fore='red', style='bright'))

    #switch to active client by sending data
    try:
        connection.loadlogdata()
        connection.clearlogdata()
        connection.sendlogdata()
        print(color('SUCCESS: sending unexpected logData after waiting.', fore='green', style='bright'))
    except:
        print(color('ERROR: sending unexpected logData after waiting.', fore='red', style='bright'))
    #switch to active client by sending data   
    try:
        connection.senddata()
        print(color('SUCCESS: sending unexpected currData after waiting.', fore='green', style='bright'))
    except:
        print(color('ERROR: sending unexpected currData after waiting.', fore='red', style='bright'))
    
    time.sleep(10 + KEEPALIVETIMEOUT)
    if(connection.isconnected() and socketHash == connection.getsockethash()):
        print(color('SUCCESS: Check if socket has changed.', fore='green', style='bright'))
    else:
        print(color('ERROR: Check if socket has changed. Old socket-Hash: ' + str(socketHash) + ', new socket-Hash: ' + str(connection.getsockethash()), fore='red', style='bright'))
    connection.disconnect()

    ## watchdog tests
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        if(connection.watchdog() == False):
            print(color('SUCCESS: Watchdog without started connection.', fore='green', style='bright'))
        else:
            raise Exception("connection running.")
    except Exception as e:
        print(color('ERROR: Watchdog without started connection. ' + str(e), fore='red', style='bright'))
    connection.connect()
    try:
        if(connection.watchdog()):
            print(color('SUCCESS: Watchdog with started connection.', fore='green', style='bright'))
        else:
            raise Exception("connection not running.")
    except Exception as e:
        print(color('ERROR: Watchdog with started connection. ' + str(e), fore='red', style='bright'))
    connection.disconnect()

    time.sleep(10)
    try:
        if(connection.watchdog() == False):
            print(color('SUCCESS: Watchdog with after disconnecting.', fore='green', style='bright'))
        else:
            raise Exception("connection not disconnected.")
    except Exception as e:
        print(color('ERROR: Watchdog with after disconnecting. ' + str(e), fore='red', style='bright'))

    input(color('[DCS-Connection] AUTO-Tests finished. Press enter to continue...', fore='blue', style='bright'))

    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection2 = DcsConnection(serial2, cryptoKey, server, 50333)
    connection3 = DcsConnection(serial3, cryptoKey, server, 50333)
    connection.connect()
    connection2.connect()
    connection3.connect()
    hash1 = connection.getsockethash()
    hash2 = connection2.getsockethash()
    hash3 = connection3.getsockethash()
    try:
        while True:
            print(color('[DCS-Connection] Communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            connection.watchdog()
            connection2.watchdog()
            connection3.watchdog()
            if(hash1 != connection.getsockethash()):
                print(color('[DCS-Connection] Socket of serial ' + str(serial) + ' has changed.', fore='red', style='bright'))
                hash1 = connection.getsockethash()
            if(hash2 != connection2.getsockethash()):
                print(color('[DCS-Connection] Socket of serial ' + str(serial2) + ' has changed.', fore='red', style='bright'))
                hash2 = connection2.getsockethash()
            if(hash3 != connection3.getsockethash()):
                print(color('[DCS-Connection] Socket of serial ' + str(serial3) + ' has changed.', fore='red', style='bright'))
                hash3 = connection3.getsockethash()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        connection.disconnect()
        connection2.disconnect()
        connection3.disconnect()

    time.sleep(1)
    # input(color('[DCS-Connection] Press enter to exit...', fore='blue', style='bright'))
