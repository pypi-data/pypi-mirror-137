#!/usr/bin/python

import logging
import sys
import os

from serial.serialutil import SerialException
import serial.tools.list_ports

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.GeneralDevice import GeneralDevice

SERIALRETRIES = 3

class SerialDevice(GeneralDevice):

    _busconnectioncounter = 0
    _busconnectionerrorcounter = 0
    _interfaceidentifiers = []
    _commport = None
    _baudrate = None
    _bytesize = None
    _stopbits = None
    _parity = None
    _timeout = None
    _seperator = None
    _requestcommand = None

    def __init__(self):
        super().__init__()

    # def disconnect(self):     #todo required?
    #     if self._commport != None:
    #         self._commport.close()

    def _connect(self):
        if self._commport != None and self._commport.isOpen():
            return

        try:
            if not isinstance(self._interfaceidentifiers, list) or len(self._interfaceidentifiers) == 0:
                raise Exception("Invalid commport identifiers.", str(self._interfaceidentifiers)) 

            found_ports = []
            awailable_ports = serial.tools.list_ports.comports()
            for p, desc, hwid in sorted(awailable_ports):
                for identifier in self._interfaceidentifiers:
                    if not isinstance(identifier, str):
                        raise Exception("Invalid commport identifier.", str(identifier)) 
                    if identifier in desc:
                        found_ports.append(p)

            if len(found_ports) > 0:
                try:
                    commport = serial.Serial()
                    commport.baudrate = self._baudrate
                    commport.bytesize = self._bytesize
                    commport.stopbits = self._stopbits
                    commport.parity = self._parity
                    commport.timeout = self._timeout
                    self._commport = commport
                except Exception as e:
                    logging.error("Invalid comm port configuration for devicetype " + str(self.__class__.__name__) + str(". Error: " + str(e)))
                    raise e   

                #check on witch port the device with the suitable identity is
                i = 0
                portname = None
                for port in found_ports:
                    if self._checkid(port):
                        portname = found_ports[i]
                        break
                    i += 1

                if portname == None:
                    raise Exception("Device not found.")   

                self._commport.port = portname
                self._commport.open()
                logging.info(str(self._name) + " Found device on comm port " + str(portname) + " and connected successfully.")

            else:
                self._commport = None
                logging.info("No commports found for device " + str(self._name))

        except Exception as e:
            self._commport = None
            logging.warning(str(self._name) + " Cannot discover device. Error: " + str(e))
            raise e

    def _readserialdata(self):
        if self._commport == None:
            logging.warning("No connection established.")
            raise Exception("not connected")
        
        if self._requestcommand != None:
            try:
                self._commport.write(self._requestcommand)
            except Exception as e:
                logging.warning("Cannot send data request to device " + str(self._name) + ". " + str(e))
                raise e
        else:
            logging.error("Configuration error on device " + str(self._name) + ". Request command invalid.")
            raise Exception("Configuration error.")

        try:
            response = self._commport.readlines()
        except Exception as e:
            logging.warning("Cannot read from device " + str(self._name) + ". " + str(e))
            raise e

        key = "b'dr" # Todo Abhängig vom Gerätetyp ...
        if len(response) > 0:
            response_string = None
            for element in response:
                if str(element).startswith(key):
                    response_string = str(element)
                    break
            if response_string == None:
                raise Exception("no valid response received: " + str(response))
            
            content_string = response_string[len(key):-(len(key)+1)]      
        else:
            # raise Exception("Noting received from device " + str(self._name) + ".")
            logging.debug("Noting received from device " + str(self._name) + ".")
            return None

        if self._seperator == None:
            raise Exception("Invalid seperator: " + str(self._seperator))
        try:
            received_values = content_string.split(self._seperator)[1:]
        except Exception as e:
            raise Exception("Cannot split content_string. " + str(e))

        try:
            receivedchecksum = int(received_values[29])       # todo device specific checksume calculation
            self._checksumcheck(response_string, receivedchecksum)
        except Exception as e:
            raise Exception("Checksum check failed: " + str(e)) 

        return received_values

    def _checksumcheck(self, response_string, receivedchecksum):
        return

    def _readregister(self, registerId, registertype="serial"):
        if registertype != "serial":
            raise Exception("Register type not supportet. Only serial is supported by this device type. Register: " + str(registertype))  

        self._busconnectioncounter += 1
        try:
            for attempt in range(SERIALRETRIES):
                registers = self._readserialdata()
                if registers != None:
                    try:
                        return registers[registerId]
                    except Exception as e:
                        raise Exception("Invalid id: " + str(registerId))
            raise Exception("Serial communication failed.")
        except Exception as e:
            self._increaseBusErrorCounter()
            if self._commport != None:
                self._commport.close()
            raise Exception("Register " + str(registertype) + ":" + str(registerId) + " cannot be read. " + str(e))

    def _readregisters(self, startregisteraddress, registerstoread, registertype="serial"):
        if registertype != "serial":
            raise Exception("Register type not supportet. Only serial is supported by this device type. Register: " + str(registertype))  

        self._busconnectioncounter += 1
        try:
            for attempt in range(SERIALRETRIES):
                registersread = self._readserialdata()
                if registersread != None:
                    registers = dict()
                    for i in range(registerstoread):
                        try:
                            registers[startregisteraddress + i] = registersread[startregisteraddress + i]
                        except Exception as e:
                            raise Exception("Invalid id: " + str(startregisteraddress + i))
                    return registers
            raise Exception("Serial communication failed.")
        except Exception as e:
            self._increaseBusErrorCounter()
            if self._commport != None:
                self._commport.close()
            raise Exception("Registers " + str(registertype) + ":" + str(startregisteraddress) + ":" + str(registerstoread) + " cannot be read. " + str(e))

    def _writeserialdata(self, registerId, data):
        if self._commport == None:
            logging.warning("No connection established.")
            raise Exception("not connected")

        command = self._lookupcommand(registerId)
        request = (command + ' {}\r\n'.format(data)).encode('utf-8')
        self._busconnectioncounter += 1
        try:
            self._commport.write(request)
            self._commport.readlines()
        except Exception as e:
            logging.warning("Cannot write data to device " + str(self._name) + ". Data: " + str(data) + ". Error: " + str(e))
            raise e
    
    def _lookupcommand(self, registerId):
        raise Exception("not implemented")

    def _writeregister(self, registerId, valueToWrite):
        logging.debug(str(self._name) + " writing register " + str(registerId) + " value: " + str(valueToWrite))

        self._writeserialdata(registerId, valueToWrite)
        try:
            valuefromdevice = self._readregister(registerId)
        except Exception as e:
            logging.debug(str(self._name) + " cannot verify written data.")
            self._increaseBusErrorCounter()
            raise Exception("writing failed. Cannot verify")
        try:
            valuefromdevice = str(valuefromdevice)
        except Exception as e:
            pass
        try:
            valueToWrite = str(valueToWrite)
        except Exception as e:
            pass
        if valueToWrite != valuefromdevice:
            self._increaseBusErrorCounter()
            raise Exception("writing failed. Value missmatch. Device: " + str(valuefromdevice) + "; Setup: " + str(valueToWrite))

    # def _writeregisters(self, registerStartId, valuesToWrite):        # todo
    #     logging.debug("[ModbusRtuDevice] ID " + str(self._serial) + " writing registers " + str(registerIds) + " value: " + str(valuesToWrite))
    #     if self._unit != None:
    #         ModbusConnection.instance().writeregisters(self._unit, registerIds, valuesToWrite)
    #     else:
    #         print("Register " + str(registerIds) + " changed to " + str(valuesToWrite))

    def getcommunicationerrorscounter(self):
        return self._busconnectionerrorcounter

    def getcommunicationerrorsrate(self):
        with self._lock:
            errorRate = 0
            try:
                errorRate = round(self._busconnectionerrorcounter / self._busconnectioncounter, 2)
            except:
                logging.debug(str(self._name) + " Cannot calculate serial device error rate.")
            return errorRate

    def resetcounters(self):
        with self._lock:
            try:
                self._busconnectionerrorcounter = 0
                self._busconnectioncounter = 0
            except Exception as e:
                logging.error(str(self._name) + " Error resetting serial device connection counters. " + str(e))

    def _increaseBusErrorCounter(self):
        self._busconnectionerrorcounter += 1
        logging.debug(str(self._name) + " Communication error. Total errors: " + str(self._busconnectionerrorcounter))

    # overwride this to find the right port if device supports reading serial. Otherwise the first port will be used
    def _checkid(self, port):
        return True


# # Entry Point     
# if __name__ == "__main__":

#     from colr import color
#     import time
#     from DcsConnection import DcsConnection

#     logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

#     #device connection tests
#     serial = "120100200505tes1"
#     serial2 = "120100200505tes2"
#     cryptoKey = "41424142414241424142414241424142"
#     server = "my-pv.live"

#     #AUTO-Tests
#     try:
#         device = SerialDevice("test")
#         print(color('ERROR: creating invalid device.', fore='red', style='bright'))
#     except:
#         print(color('SUCCESS: creating invalid device.', fore='green', style='bright'))

#     try:
#         device = SerialDevice()
#         print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: creating valid device.', fore='red', style='bright'))

#     try:
#         device.connect()
#         print(color('ERROR: connecting device.', fore='red', style='bright'))
#     except Exception as e:
#         print(color('SUCCESS: connecting device.', fore='green', style='bright'))

#     try:
#         setup = device.getsetup()
#         if(setup == None):
#             raise Exception("Setup is None")
#         print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

#     try:
#         data = device.getdata()
#         if(data == None):
#             raise Exception("Data is None")
#         print(color('SUCCESS: getting device data.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: getting device data.', fore='red', style='bright'))

#     try:
#         logdata = device.getlogdata()
#         if(logdata == None):
#             raise Exception("logdata is None")
#         print(color('SUCCESS: getting device logdata.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: getting device logdata.', fore='red', style='bright'))

#     try:
#         device.stop()
#         print(color('SUCCESS: stopping device before start.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: stopping device before start.', fore='red', style='bright'))

#     try:
#         temp = device.getstate()
#         if(temp == False):
#             print(color('SUCCESS: getting device state (before start).', fore='green', style='bright'))
#         else:
#             raise Exception("device state is not stopped.")
#     except:
#         print(color('ERROR: getting device state (before start).', fore='red', style='bright'))

#     try:
#         temp = device.getdevicetype()
#         if(temp == "SerialDevice"):
#             print(color('SUCCESS: getting device type.', fore='green', style='bright'))
#         else:
#             raise Exception("device type does not match.")
#     except:
#         print(color('ERROR: getting device type.', fore='red', style='bright'))

#     if(device != None):
#         try:
#             register = device.readregister(1234, "serial")
#             print(color('ERROR: reading register.', fore='red', style='bright'))
#         except Exception as e:
#             print(color('SUCCESS: reading register.', fore='green', style='bright'))

#     connection = DcsConnection(serial, cryptoKey, server, 50333)
#     try:
#         device.addserverconnection(connection)
#         print(color('SUCCESS: adding connection to device.', fore='green', style='bright'))
#     except Exception:
#         print(color('ERROR: adding connection to device.', fore='red', style='bright'))

#     try:
#         device.start()
#         print(color('SUCCESS: starting device.', fore='green', style='bright'))
#     except Exception:
#         print(color('ERROR: starting device.', fore='red', style='bright'))

#     try:
#         temp = device.getstate()
#         if(temp == True):
#             print(color('SUCCESS: getting device state (running).', fore='green', style='bright'))
#         else:
#             raise Exception("device state is not running.")
#     except Exception:
#         print(color('ERROR: getting device state (running).', fore='red', style='bright'))

#     time.sleep(10)
 
#     try:
#         device.stop()
#         print(color('SUCCESS: stopping device.', fore='green', style='bright'))
#     except Exception:
#         print(color('ERROR: stopping device.', fore='red', style='bright'))

#     try:
#         temp = device.getstate()
#         if(temp == False):
#             print(color('SUCCESS: getting device state (stopped).', fore='green', style='bright'))
#         else:
#             raise Exception("device state is not stopped.")
#     except Exception:
#         print(color('ERROR: getting device state (stopped).', fore='red', style='bright'))

#     device = SerialDevice()
#     connection = DcsConnection(serial, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     time.sleep(20)
#     device.stop()
 
#     #Bus tests
#     device = SerialDevice()
#     try:
#         device.readallregisters()
#         print(color('SUCCESS: reading registers.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: reading registers.', fore='red', style='bright'))
    
#     if(device.getregistervalue(50) == None ):
#         print(color('SUCCESS: reading unknown register.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: reading unknown register.', fore='red', style='bright'))

#     if(device.getchannelvalue("abc", True) == None ):
#         print(color('SUCCESS: getting dataset (abc).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting dataset (abc).', fore='red', style='bright'))

#     if(device.getchannelvalue(None, True) == None ):
#         print(color('SUCCESS: getting dataset (None).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting dataset (None).', fore='red', style='bright'))

#     if(device.getlogvalue(None) == None ):
#         print(color('SUCCESS: getting logvalue (None).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (None).', fore='red', style='bright'))

#     if(device.getlogvalue("abc") == None ):
#         print(color('SUCCESS: getting logvalue (abc).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (abc).', fore='red', style='bright'))

#     time.sleep(1)
#     device.readallregisters()
#     device._processchannels()

#     if( device.getlogvalue("abc") == None ):
#         print(color('SUCCESS: getting logvalue (abc) after wait.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (abc) after wait.', fore='red', style='bright'))

#     device.stop()
#     time.sleep(10)

#     device = SerialDevice()
#     device._running = True
#     avgVal0 = device.getlogvalue("test")
#     device._excecutebuscommunication()
#     avgVal1 = device.getlogvalue("test")
#     device._excecutebuscommunication()
#     avgVal2 = device.getlogvalue("test")
#     device._excecutebuscommunication()
#     avgVal3 = device.getlogvalue("test")
#     device._excecutebuscommunication()
#     avgVal4 = device.getlogvalue("test")
#     if( avgVal4 == avgVal1):
#         print(color('SUCCESS: checking calculation.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: checking calculation.', fore='red', style='bright'))

#     device.clearlog()
#     if( device.getlogvalue("abc") == None ):
#         print(color('SUCCESS: getting logvalue (abc) after clear.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (abc) after clear.', fore='red', style='bright'))

#     if( device.getlogvalue("test") == None ):
#         print(color('SUCCESS: getting logvalue (test) after clear.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (test) after clear.', fore='red', style='bright'))

#     if( device.getlogvalue("power") == None ):
#         print(color('SUCCESS: getting logvalue (power) after clear.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power) after clear.', fore='red', style='bright'))

#     device.stop()

#     try:
#         device._sethealthstate(0)
#         print(color('SUCCESS: setting healthState to 0.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: setting healthState to 0.', fore='red', style='bright'))

#     try:
#         device._sethealthstate("seppi")
#         print(color('ERROR: setting healthState to invalid.', fore='red', style='bright'))
#     except Exception as e:
#         print(color('SUCCESS: setting healthState to invalid.', fore='green', style='bright'))

#     try:
#         device._sethealthstate(None)
#         print(color('ERROR: setting healthState to None.', fore='red', style='bright'))
#     except Exception as e:
#         print(color('SUCCESS: setting healthState to None.', fore='green', style='bright'))

#     try:
#         device._sethealthstate(3)
#         print(color('SUCCESS: setting healthState to 3.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: setting healthState to 3.', fore='red', style='bright'))

#     time.sleep(5)
#     #DCS communication tests
#     device = SerialDevice()
#     connection = DcsConnection(serial2, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     try:
#         while True:
#             print(color('[SerialDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
#             print(device.getinfo())
#             device.showcommunicationerrors()
#             device.showcommunicationerrorsrate()
#             time.sleep(10)
#     except KeyboardInterrupt as e:
#         print("[DCS-Connection] Stopping Test...")
#         device.stop()
#     input("waiting...  PRESS ENTER")
