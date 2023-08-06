#!/usr/bin/python

import logging
import threading
import time
from datetime import datetime
import sys
import os
import random

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ServerConnection import ServerConnection
from mypvdevices.Dataprocessor import Dataprocessor

BUILDNR = "1.2202.2"

JOINTIMEOUTSECONDS = 5
MONITORSLEEPTIMESECONDS = 10
DEFAULTBUSSLEEPTIMESECONDS = 15
CHANNELDATAMAXIMUMAGESECONDS = 60
ROUNDINGDIGITS = 2

class GeneralDevice:
    _firmwareversion = "3." + str(BUILDNR)
    _lock = None
    _running = False
    _monitorthread = None
    _busCommunicationThread = None
    _datasetdefinitions = None
    _data = None
    _logdata = None
    _logdataTimeStamp = None
    _logdataStartTimeStamp = None
    _logdataCounter = None
    _logdataLastValue = None
    _logdataSum = None
    _serverconnections = None
    _setup = None
    _healthState = 0
    _registers = None
    _registerTimeStamp = None
    _settingsMap = None
    _registerLastSuccessfullReadTimeStamp = None
    _busCommunicationExecuted = None
    _buscommunicationWaitTime = DEFAULTBUSSLEEPTIMESECONDS
    _registersToReadList = None
    _channels = None
    _datamaximumage = CHANNELDATAMAXIMUMAGESECONDS
    _name = None

    def __init__(self):           
        self._lock = threading.Lock()
        self._serverconnections = list()
        self._registers = dict()
        self._data = dict()
        self._logdata = dict()
        self._logdataCounter = dict()
        self._logdataLastValue = dict()
        self._logdataSum = dict()
        self._setup = {}
        self._settingsMap = {}
        self._name = self.__class__.__name__
        self._channels = {}

    def __str__(self):
        output = "Device " + self._name
        for channelId in self._channels:
            try:
                value = self.getchannelvalue(channelId)
            except Exception as e:
                value = None
            output += "\nChannel " + str(channelId) + ": " + str(value)
        return output

    def addserverconnection(self, connection):
        if connection != None and isinstance(connection, ServerConnection):
            if(connection.addDevice(self)):
                self._serverconnections.append(connection)
                logging.debug(str(self._name) + " Added server connection to device")
            else:
                logging.error(str(self._name) + " Failed adding server connection to device")
                raise Exception("cannot add server connection")
        else:
            raise TypeError("invalid connection. Has to be of type ServerConnection or a child of ServerConnection.")

    def _builddatasetdefinitions(self):
        datasets = {}
        for channelid in self._channels:
            channel = self._channels[channelid]
            if channel.datasettype != None:
                datasets[channelid] = channel.datasettype
        self._datasetdefinitions = datasets

    def start(self):
        self._running = True
        logging.debug(str(self._name) + " starting...")
        self._busCommunicationThread = threading.Thread(target=self._runbuscommunication, name="BusCommunication " + str(self._name))
        self._busCommunicationThread.start()
        time.sleep(10)
        for connection in self._serverconnections:
            connection.connect()
        time.sleep(5)
        self._monitorthread = threading.Thread(target=self._run, name="Monitor " + str(self._name))
        self._monitorthread.start()
        logging.debug(str(self._name) + " started.")
    
    def stop(self):
        self._running = False
        logging.info(str(self._name) + " stopping.")
        if(self._busCommunicationThread != None and self._busCommunicationThread.is_alive()):
            self._busCommunicationThread.join(JOINTIMEOUTSECONDS)
        for connection in self._serverconnections:
            try:
                connection.loadlogdata()
                connection.sendlogdata()
                logging.info(str(self._name) + " forced logdata sent on stopping.")
            except:
                logging.warning(str(self._name) + " cannot send logdata on stopping.")
            connection.disconnect()

    def getstate(self):
        return self._running
    
    def getdevicetype(self):
        return self.__class__.__name__

    def getsetup(self):
        setupjson = {}
        for element in self._setup:
            setupjson[element] = self._setup[element].value
        return setupjson

    def setbuscommunicationwaittime(self, waittime):
        if waittime != None and waittime >= 0 and waittime < 90000:
            self._buscommunicationWaitTime = waittime
            logging.info(str(self._name) + " communication-waittime set to " + str(self._buscommunicationWaitTime))
            return True
        else:
            logging.info(str(self._name) + " set communication-waittime failed. Out of range: " + str(waittime))
            return False

    def _run(self):
        while self._running:
            logging.debug(str(self._name) + " monitor running...")

            connectionerrors = 0
            for connection in self._serverconnections:
                try:
                    connection.watchdog()
                except:
                    logging.error(str(self._name) + " watchdog failed.")

                try:
                    if not connection.isconnected():
                        logging.info(str(self._name) + " not connected to " + str(connection.getServer()))        #todo implement __str__ in connection and change it here
                        connectionerrors += 1
                except Exception as e:
                    logging.warning(str(self._name) + " cannot check connection to " + str(connection.getServer()) + ". " + str(e))

            if connectionerrors > 0:
                logging.debug(str(self._name) + ": Connection errors: " + str(connectionerrors))

            try:
                if self._busCommunicationExecuted != None:
                    difference = datetime.now() - self._busCommunicationExecuted
                    if(difference.total_seconds() > self._buscommunicationWaitTime * 3):
                        logging.warning(str(self._name) + " modbus data too old: " + str(difference.total_seconds()))
                        if self._datasetdefinitions != None:
                            for dataset in self._datasetdefinitions:
                                self._data[dataset] = None
            except Exception as e:
                logging.warning(str(self._name) + " cleanup failed. " + str(e))

            try:
                self._supervise()
            except Exception as e:
                logging.warning(str(self._name) + " supervision failed. " + str(e))

            time.sleep(MONITORSLEEPTIMESECONDS)

    def setsetupvalue(self, key, value):
        logging.info("Setup Change: key="+str(key)+", value="+str(value))

        if key == None:
            msg="key required"
            raise TypeError(msg)

        if not isinstance(key, str):
            msg="key has to be a string"
            raise TypeError(msg)

        if value == None:
            msg="value required"
            raise TypeError(msg)

        if not isinstance(value, int):
            msg="value has to be a int"
            raise TypeError(msg)

        try:
            self._setup[key]
        except Exception as e:
            logging.warning(str(self._name) + " Setup-Element does not exist: " + str(e))
            raise Exception("setup element does not exist.")
        try:
            self._setup[key].value = value
            if self._setup[key].channelname != None:
                self.setchannelvalue(self._setup[key].channelname, value)
            else:
                logging.debug(str(self._name) + " no register mapping for key " + str(key))

        except Exception as e:
            logging.info(str(self._name) + " Setup change not successfull. " + str(e))
            raise e

    def _supervise(self):
        pass

    def _sethealthstate(self, state):
        if state != None and isinstance(state, int) and state <= 3 and state >= 0:
            if self._healthState != state:
                self._healthState = state
                logging.info(str(self._name) + ". HealthState set to " + str(state))
        else:
            logging.error(str(self._name) + ". Cannot set healthState. Invalid state: " + str(state))
            raise Exception("invalid state " + str(state))

    def gethealthstate(self):
        return self._healthState

    def _runbuscommunication(self):
        while self._running:
            buscommunicationstarttime = datetime.now()
            try:
                logging.debug(str(self._name) + ". Running bus communication...")
                self._excecutebuscommunication()
                self._busCommunicationExecuted = datetime.now()
            except Exception as e:
                logging.error(str(self._name) + ". BusCommunication Thread Error: " + str(e))
            
            executiontime = datetime.now() - buscommunicationstarttime
            logging.debug(str(self._name) + ". BusCommunication execution time: " + str(executiontime.total_seconds()))
            if(self._buscommunicationWaitTime > 0 and executiontime.total_seconds() > self._buscommunicationWaitTime):
                logging.warning(str(self._name) + ". BusCommunication execution time too high: " + str(executiontime.total_seconds()))

            time.sleep(random.random())        
            time.sleep(self._buscommunicationWaitTime)

    def _excecutebuscommunication(self):
        if self._buscommunicationWaitTime > 0:
            logging.debug(str(self._name) + ". BusCommunication running...")
            try:
                self.readallregisters()
            except Exception as e:
                logging.error(str(self._name) + ". Unknown BusCommunication register read error: " + str(e))
                self._registers = dict()
            if len(self._registers) > 0:
                try:
                    self._syncsettings()
                except Exception as e:
                    logging.warning(str(self._name) + ". Settingssync not successfull. " + str(e))
            else:
                logging.debug(str(self._name) + ". No bus communication to device.")
            
            try:
                self._processchannels()
            except Exception as e:
                logging.warning(str(self._name) + ". Processing registers not successfull. " + str(e))

    def _syncsettings(self):
        errors = 0
        if self._setup != None:
            setupchanged = False
            for name in self._setup:
                channel = self._setup[name].channelname
                if channel != None:
                    if channel in self._channels:
                        try:
                            channelvalue = self.getchannelvalue(channel)
                        except Exception as e:
                            logging.warning(str(self._name) + ". Cannot get channelvalue")
                            channelvalue = None
                        setupvalue = self._setup[name].value
                        if channelvalue != None and channelvalue != setupvalue:
                            logging.info(str(self._name) + " setting missmatch " + str(name) + " - Device: " + str(channelvalue) + "; Setup: " + str(setupvalue) + ".")
                            if self._setup[name].forced:
                                try:
                                    self.setchannelvalue(channel, setupvalue)
                                except Exception as e:
                                    logging.warning(str(self._name) + " cannot write channel while settings sync. Set " + str(name) + " to "+str(setupvalue)+". " + str(e))
                                logging.info(str(self._name) + " forced " + str(name) + " to "+str(setupvalue)+".")
                            else:
                                self._setup[name].value = channelvalue
                                setupchanged = True
                                logging.debug(str(self._name) + " changed setup. " + str(name) + "=" + str(channelvalue) + ".")
                    else:
                        logging.warning(str(self._name) + " channel for setting " + str(name) + " not found.")
                        errors += 1
            if setupchanged:
                self.sendsetup()
        if errors == 0:
            return True
        else:
            raise Exception("Errors with " + str(errors) + " setup elements")

    def sendsetup(self):
        success = True
        for connection in self._serverconnections:
            if connection.isconnected():
                try:
                    connection.sendsetup()
                except Exception:
                    logging.error(str(self._name) + " " + str(connection) + " cannot send setup change to server.")
                    success = False
        return success

    def _buildRegistersToReadList(self):
        registersToReadList = []
        for channelid in self._channels:
            channel = self._channels[channelid]
            registers = channel.registers
            registertype = channel.registertype
            currentElementStart = registers[0]
            currentElementLen = len(registers)
            currentElementEnd = currentElementStart + currentElementLen - 1
            i = 0
            skip = False
            for element in registersToReadList:
                listElementType = element[2]
                listElementStart = element[0]
                listElementLen = element[1]
                listElementEnd = listElementStart + listElementLen - 1
                if listElementType == registertype:
                    if listElementStart <= currentElementStart and listElementEnd >= currentElementEnd:     # alredy in list
                        skip = True
                    elif listElementStart >= currentElementStart and listElementEnd <= currentElementEnd:      # new element includes list element -> replace list element
                        registersToReadList[i][0] = currentElementStart
                        registersToReadList[i][1] = currentElementLen
                        skip = True
                    elif listElementEnd == currentElementStart - 1:  # attach current element to list element
                        newLen = listElementLen + currentElementLen
                        newEnd = listElementStart + newLen -1
                        registersToReadList[i][1] = newLen
                        try:    # check if there is a next element
                            nextElement = registersToReadList[i+1]
                            nextElementStart = nextElement[0]
                        except Exception:
                            nextElement = None
                        if nextElement and nextElementStart == newEnd + 1:  #check if next element is a neighbour
                            registersToReadList[i][1] = registersToReadList[i][1] + registersToReadList[i+1][1]
                            del registersToReadList[i+1]
                        skip = True
                    elif listElementStart == currentElementEnd + 1: # extend list element with new element in front
                        registersToReadList[i][0] = currentElementStart
                        registersToReadList[i][1] = listElementLen + currentElementLen
                        skip = True
                i += 1
            if not skip:
                registersToReadList.append([currentElementStart, currentElementLen, registertype])
            registersToReadList.sort()
        self._registersToReadList = registersToReadList

    def readallregisters(self):
        if self._registersToReadList == None:
            self._buildRegistersToReadList()

        allRegisters = dict()
        readerror = 0
        for element in self._registersToReadList:
            try:
                startAddress = element[0]
                registersToRead = element[1]
                registertype = element[2]
            except Exception as e:
                logging.error(str(self._name) + ". Invalid register definition: " + str(element))
                raise e
            if startAddress != None and registersToRead != None:
                logging.debug(str(self._name) + ". Reading " + str(registersToRead) + " " + str(registertype) + " registers starting with " + str(startAddress))
                try:
                    registers = self.readregisters(startAddress, registersToRead, registertype) 
                except Exception as e:
                    registers = None
                    logging.warning(e)
                if registers != None:
                    allRegisters.update(registers)                    
                if registers == None or len(registers) == 0:
                    readerror += 1
            else:
                logging.warning(str(self._name) + ". Register definition error: ", str(startAddress), str(registersToRead))
        self._registers = allRegisters
        self._registerTimeStamp = time.time()
        if readerror == 0:
            self._registerLastSuccessfullReadTimeStamp = time.time()
        else:
            logging.warning(str(self._name) + ". Reading register failed for " + str(readerror) + " blocks.")

    def readregister(self, registerId, registertype="holding"):
        if registerId == None:
            msg="registerId required"
            raise TypeError(msg)

        if not isinstance(registerId, int):
            msg="registerId has to be a int"
            raise TypeError(msg)

        if registertype == None:
            msg="registertype required"
            raise TypeError(msg)

        if not isinstance(registertype, str):
            msg="registertype has to be a str"
            raise TypeError(msg)

        with self._lock:
            self._connect()
            return self._readregister(registerId, registertype)

    def readregisters(self, registerId, registerstoread, registertype="holding"):
        if registerId == None:
            msg="registerId required"
            raise TypeError(msg)

        if not isinstance(registerId, int):
            msg="registerId has to be a int"
            raise TypeError(msg)

        if registerstoread == None:
            msg="registerstoread required"
            raise TypeError(msg)

        if not isinstance(registerstoread, int):
            msg="registerstoread has to be a int"
            raise TypeError(msg)

        if registertype == None:
            msg="registertype required"
            raise TypeError(msg)

        if not isinstance(registertype, str):
            msg="registertype has to be a str"
            raise TypeError(msg)

        with self._lock:
            self._connect()
            return self._readregisters(registerId, registerstoread, registertype)

    def writeregister(self, registerId, value):
        if registerId == None:
            msg="registerId required"
            raise TypeError(msg)

        if not isinstance(registerId, int):
            msg="registerId has to be a int"
            raise TypeError(msg)

        if value == None:
            msg="value required"
            raise TypeError(msg)

        logging.debug(str(self._name) + ": writing register " + str(registerId) +" with value "+ str(value))
        with self._lock:
            self._connect()
            self._writeregister(registerId, value)

    def writeregisters(self, registerStartId, values):
        if registerStartId == None:
            msg="registerStartId required"
            raise TypeError(msg)

        if not isinstance(registerStartId, int):
            msg="registerStartId have to be a int"
            raise TypeError(msg)

        if values == None:
            msg="values required"
            raise TypeError(msg)

        if not isinstance(values, list):
            msg="values have to be a list"
            raise TypeError(msg)

        logging.debug(str(self._name) + ": writing registers starting at" + str(registerStartId) +" with value "+ str(values))
        with self._lock:
            self._connect()
            self._writeregisters(registerStartId, values)

    def getregistervalue(self, registerId):
        with self._lock:
            try:
                if(self._registers[registerId] != None):
                    value = {
                        "time": self._registerTimeStamp,
                        "value": self._registers[registerId]
                    }
                else:
                    value = None
            except Exception:
                logging.debug(str(self._name) + " register not found. Register Id: " + str(registerId))
                value = None
        return value

    def _processchannels(self):
        if self._datasetdefinitions == None:
            self._builddatasetdefinitions()

        if self._datasetdefinitions != None:
            for dataset in self._datasetdefinitions:

                if len(self._registers) == 0:
                    # logging.debug(str(self._name) + " Cannot process channels. No data available")
                    raise Exception("No data to process")

                try:
                    value = self.getchannelvalue(dataset, False)
                except Exception as e:
                    logging.debug(str(self._name) + ", dataset=" + str(dataset) + ", cannot get data from channel")
                    value = None
                if value != None:
                    element = {
                        "time": self._registerTimeStamp,
                        "value": value
                    }
                    self._addtologdata(dataset, element)
                    logging.debug(str(self._name) + ", dataset=" + str(dataset) + ", value=" + str(value) + " processed")
                else:
                    logging.debug(str(self._name) + " no value for dataset " + str(dataset))
        else:
            logging.warning(str(self._name) + " no datasets defined")
        self._logdataTimeStamp = self._registerTimeStamp

        if self._logdataStartTimeStamp == None:
            self._logdataStartTimeStamp = datetime.now()
    
    def getlogdataage(self):
        if self._logdataStartTimeStamp != None:
            difference = datetime.now() - self._logdataStartTimeStamp
            return difference.total_seconds()
        else:
            return 0

    def _addtologdata(self, datasetname, element):
        datasettype = self._datasetdefinitions[datasetname]
        value = None
        if element["value"] != None:
            if(datasettype == "avg"):
                try:
                    self._logdataCounter[datasetname] = self._logdataCounter[datasetname] + 1
                except Exception:
                    self._logdataCounter[datasetname] = 1
                try:
                    self._logdataSum[datasetname] = self._logdataSum[datasetname] + element["value"]
                except Exception:
                    self._logdataSum[datasetname] = element["value"]
                value = self._logdataSum[datasetname] / self._logdataCounter[datasetname]
            if(datasettype == "sum"):
                try:
                    oldvalue = self._logdata[datasetname]
                except Exception:
                    oldvalue = 0
                try:
                    x0 = self._logdataLastValue[datasetname]
                except Exception:
                    x0 = 0
                if(x0 == None):
                    x0 = 0
                t0 = self._logdataTimeStamp
                if(t0 == None):
                    t0 = element["time"]
                x1 = element["value"]
                t1 = element["time"]
                dt = (t1 - t0)/3600
                newvalue = dt * ((x1 + x0)/2)
                value = oldvalue + newvalue
                self._logdataLastValue[datasetname] = x1
                # print(str(self._name) + " Integrating " + str(datasetname) + ": dt="+str(round(dt, 4))+" x1="+str(round(x1, 4))+" x0="+str(round(x0, 4))+" oldvalue="+str(round(oldvalue, 4))+" newvalue="+str(round(newvalue, 4))+"  value="+str(round(value, 4)))
            self._logdata[datasetname] = value

    def getlogvalue(self, datasetname, casttype=None, scale=None):
        if self._logdata == None or len(self._logdata) == 0:
            return None

        if casttype not in ["int"] and scale != None:
            logging.error("Scaling only supported for numbers.")
            raise Exception("Scaling only supportet for numbers.")

        try:
            logdata = self._logdata[datasetname]

            if scale != None and ( isinstance(scale, int) or isinstance(scale, float)):
                logdata = logdata * scale

            if casttype == "int":
                return int(logdata)
            else:
                return logdata
        except Exception:
            logging.warning(str(self._name) + " logvalue not found " + str(datasetname))
            return None
    
    def clearlog(self):
        self._logdata.clear()
        self._logdataCounter.clear()
        self._logdataSum.clear()
        self._logdataTimeStamp = None
        self._logdataStartTimeStamp = None

    def getinfo(self):
        output = str(self._name)
        if self._datasetdefinitions != None:
            for dataset in self._datasetdefinitions:
                try:
                    output += "\n" + str(dataset).rjust(30) + ": Live: " + str(self.getchannelvalue(dataset)).ljust(8) + " Log: " + str(self.getlogvalue(dataset)).ljust(8)
                except Exception as e:
                    logging.debug(str(self._name) + " Error getting deviceInfo. " + str(e))

        output += "\nHealthState: " + str(self.gethealthstate())
        return output

    def showcommunicationerrors(self):
        logging.info(str(self._name) + " - Communication Errors: " +  str(self.getcommunicationerrorscounter()))

    def showcommunicationerrorsrate(self):
        rate = self.getcommunicationerrorsrate()
        if rate != None:
            rate = round(rate*100)
        logging.info(str(self._name) + " - Communication error-rate: " +  str(rate) + "%, Errors: " +  str(self.getcommunicationerrorscounter()))

    def getchannelconfig(self, channel):
        try:
            config = self._channels[channel]
        except KeyError as e:
            logging.info("Channel not configurated. " + str(e))
            raise Exception("Channel not configurated: " + str(e))
        return config

    def getchannellist(self):
        result = []
        for channelId in self._channels:
            result.append(channelId)
        return result

    def getchannelvalue(self, channel, safemode=False, scale=None):
        try:
            if self._registers == None:
                logging.info("No channeldata available. Registers have not been read yet. Run read registers first. " + str(self._name) + ", " + str(channel))
                raise Exception("No register data available. Register not read?")

            if len(self._registers) == 0:
                logging.info("No channeldata available. Data is empty. " + str(self._name) + ", " + str(channel))
                raise Exception("No register data available.")

            if self._registerTimeStamp != None:
                difference = time.time() - self._registerTimeStamp
                if difference > self._datamaximumage:
                    logging.warning("Channel data to old. Device: " + str(self._name) + " Channel " + str(channel))
                    return None
            else:
                logging.error("Registers not read. Run readallregisters first.")
                raise Exception("registers not read.")

            config = self.getchannelconfig(channel)

            if config.mode != "r" and config.mode != "rw":
                logging.info("Cannot read from channel " + str(channel) + ". Mode is " + str(config.mode))
                raise Exception("Channel mode not readable.", channel, config.mode)

            registerValues = []
            for register in config.registers:
                try:
                    registerValues.append(self._registers[register])
                except Exception as e:
                    logging.debug("Register " + str(e) + " for channel " + str(channel) + " not found. Device: " + str(self._name))
                    raise Exception("Register not found: " + str(e))

            if config.channeltype == None:
                value = registerValues[0]
            elif config.channeltype == "NUMBER":
                try:
                    value = int(registerValues[0])
                except Exception as e:
                    value = float(registerValues[0])
                
            elif config.channeltype == "NTC":
                value = Dataprocessor.instance().adcNTC2Temp(registerValues[0])
            elif config.channeltype == "POTI":
                value = Dataprocessor.instance().adcPoti2Temp(registerValues[0])
            elif config.channeltype == "UINT16":
                value = Dataprocessor.instance().decode_16bit_uint(registerValues)
            elif config.channeltype == "UINT32":
                value = Dataprocessor.instance().decode_32bit_uint(registerValues)
            elif config.channeltype == "FLOAT32":
                value = Dataprocessor.instance().decode_32bit_float(registerValues)
            else:
                logging.warning("Unknown channeltype to read. Channeltype: " + str(config.channeltype))
                value = registerValues[0]

            value = self._specialProcessingRead(channel, value)

            if config.scale != 0 and ( isinstance(value, int) or isinstance(value, float) ):
                value = value * config.scale
            
            if scale != None and scale != 0 and ( isinstance(value, int) or isinstance(value, float) ) and ( isinstance(scale, int) or isinstance(scale, float) ):
                value = value * scale

            if isinstance(value, float):
                value = round(value, ROUNDINGDIGITS)

            return value
        except Exception as e:
            if safemode:
                return None
            else: 
                raise e

    def setchannelvalue(self, channel, value):
        if value == None:
            logging.info("Value for channel " + str(channel) + " cannot be None.")
            raise Exception("Value cannot be None")

        value = self._specialProcessingWrite(channel, value)
        config = self.getchannelconfig(channel)
        if config.mode != "w" and config.mode != "rw":
            logging.info("Cannot write to channel " + str(channel) + ". Mode is " + str(config.mode))
            raise Exception("Channel mode not writeable.", channel, config.mode)

        if config.scale != 0:
            value = value / config.scale

        if config.channeltype == None:
            registerValues = [value]
        elif config.channeltype == "NUMBER":
            registerValues = [int(value)]
        elif config.channeltype == "UINT16":
            registerValues = Dataprocessor.instance().encode_16bit_uint(value)
        elif config.channeltype == "UINT32":
            registerValues = Dataprocessor.instance().encode_32bit_uint(value)
        else:
            logging.warning("Unknown channeltype to set. Channeltype: " + str(config.channeltype))
            registerValues = [value]
        
        if len(config.registers) > 0:
            startregister = config.registers[0]
            if len(registerValues) > 1:
                self.writeregisters(startregister, registerValues)
            else:
                self.writeregister(startregister, registerValues[0])
        else:
            raise Exception("Invalid config: " + str(config))

        self.readallregisters()

    def getregisters(self):
        return self._registers

    # required for special processing in subclasses
    def _specialProcessingRead(self, channel, value):
        return value

    def _specialProcessingWrite(self, channel, value):
        return value
    
    # have to be implemented in subclasses
    def _connect(self):
        raise Exception(str(self._name) + ". Not implemented: _connect")

    def getcommunicationerrorsrate(self):
        return 0

    def getcommunicationerrorscounter(self):
        return 0

    def _readregister(self, registerId, registertype="holding"):
        raise Exception(str(self._name) + ". Not implemented: _readregister")
    
    def _readregisters(self, registerId, registersToRead, registertype="holding"):
        raise Exception(str(self._name) + ". Not implemented: _readregisters")

    def _writeregister(self, registerId, valueToWrite):
        raise Exception(str(self._name) + ". Not implemented: _writeregister")
    
    def _writeregisters(self, registerStartId, valuesToWrite):
        raise Exception(str(self._name) + ". Not implemented: _writeregisters")

    def getdata(self):
        raise Exception(str(self._name) + ". Not implemented: getdata")

    def getlogdata(self, time = None):
        raise Exception(str(self._name) + ". Not implemented: getlogdata")

# # Entry Point     
# if __name__ == "__main__":

#     from colr import color

#     from DcsConnection import DcsConnection

#     logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

#     #device connection tests
#     serial = "120100200505tes1"
#     serial2 = "120100200505tes2"
#     serial3 = "120100200505tes3"
#     cryptoKey = "41424142414241424142414241424142"
#     server = "my-pv.live"

#     device = GeneralDevice()
#     print(device)
#     data = device.getregisters()
#     print("Data: " + str(data))

#     device = GeneralDevice()
#     device.readallregisters()
#     data = device.getregisters()
#     print("Data: " + str(data))

#     device.start()
#     time.sleep(5)
#     device.stop()

#     #AUTO-Tests
#     #Constructor Tests
#     try:
#         device = GeneralDevice()
#         print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: creating valid device.', fore='red', style='bright'))

#     try:
#         setup = device.getsetup()
#         if(setup == None):
#             raise Exception("Setup is None")
#         print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

#     try:
#         data = device.getdata()
#         print(color('ERROR: getting device data.', fore='red', style='bright'))
#     except:
#         print(color('SUCCESS: getting device data.', fore='green', style='bright'))

#     try:
#         logdata = device.getlogdata()
#         print(color('ERROR: getting device logdata.', fore='red', style='bright'))
#     except:
#         print(color('SUCCESS: getting device logdata.', fore='green', style='bright'))

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
#         if(temp == "GeneralDevice"):
#             print(color('SUCCESS: getting device type.', fore='green', style='bright'))
#         else:
#             raise Exception("device type does not match.")
#     except:
#         print(color('ERROR: getting device type.', fore='red', style='bright'))
  
#     if(device != None and not device.setbuscommunicationwaittime(None)):
#         print(color('SUCCESS: setting modbus frequency (None).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: setting modbus frequency (None).', fore='red', style='bright'))

#     if(device != None and device.setbuscommunicationwaittime(0)):
#         print(color('SUCCESS: setting modbus frequency (0).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: setting modbus frequency (0).', fore='red', style='bright'))
    
#     if(device != None and device.setbuscommunicationwaittime(10)):
#         print(color('SUCCESS: setting modbus frequency (10).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: setting modbus frequency (10).', fore='red', style='bright'))

#     if(device != None and not device.setbuscommunicationwaittime(90000)):
#         print(color('SUCCESS: setting modbus frequency (90000).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: setting modbus frequency (90000).', fore='red', style='bright'))

#     if(device != None):
#         try:
#             register = device.readregister(1234)
#             print(color('ERROR: reading register. Alreday implemented', fore='red', style='bright'))
#         except Exception as e:
#             print(color('SUCCESS: reading register.', fore='green', style='bright'))

#     if(device != None):
#         try:
#             device.writeregister(123,33)
#             print(color('ERROR: writing Register.', fore='red', style='bright'))
#         except Exception as e:
#             print(color('SUCCESS: writing Register.', fore='green', style='bright'))

#     key = "ww2target"
#     targetValue = 30
#     if device != None:
#         try:
#             device.setsetupvalue(key, targetValue)
#             print(color('ERROR: Setting setup value with register key.', fore='red', style='bright'))
#         except Exception as e:
#             print(color('SUCCESS: Setting setup value with register key.', fore='green', style='bright'))

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


#     device = GeneralDevice()
#     connection = DcsConnection(serial, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     time.sleep(20)
#     device.stop()

#     # Channel tests
#     try:
#         device = GeneralDevice()
#         channels = device.getchannellist()
#         print(color('SUCCESS: getting channel list.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: getting channel list.', fore='red', style='bright'))

#     try:
#         device = GeneralDevice()
#         channelconfig = device.getchannelconfig("test")
#         print(color('ERROR: getting channel config.', fore='red', style='bright'))
#     except Exception as e:
#         if "Channel not configurated" in e.args[0] != None:
#             print(color('SUCCESS: getting channel config.', fore='green', style='bright'))
#         else:
#             print(color('ERROR: getting channel config. ' + str(e), fore='red', style='bright'))

#     try:
#         device = GeneralDevice()
#         channelconfig = device.getchannelvalue("test")
#         print(color('ERROR: getting channel value without reading registers before.', fore='red', style='bright'))
#     except Exception as e:
#         if "registers not read" in e.args[0] != None:
#             print(color('SUCCESS: getting channel value without reading registers before.', fore='green', style='bright'))
#         else:
#             print(color('ERROR: getting channel value without reading registers before. ' + str(e), fore='red', style='bright'))

#     try:
#         device = GeneralDevice()
#         device.readallregisters()
#         channelconfig = device.getchannelvalue("test")
#         print(color('ERROR: getting channel value.', fore='red', style='bright'))
#     except Exception as e:
#         if "Channel not configurated" in e.args[0] != None:
#             print(color('SUCCESS: getting channel value.', fore='green', style='bright'))
#         else:
#             print(color('ERROR: getting channel value. ' + str(e), fore='red', style='bright'))

#     try:
#         device = GeneralDevice()
#         channelconfig = device.setchannelvalue("test", 22)
#         print(color('ERROR: setting channel value.', fore='red', style='bright'))
#     except Exception as e:
#         if "Channel not configurated" in e.args[0] != None:
#             print(color('SUCCESS: setting channel value.', fore='green', style='bright'))
#         else:
#             print(color('ERROR: setting channel value. ' + str(e), fore='red', style='bright'))
 
#     #Modbus tests
#     device = GeneralDevice()
#     try:
#         device.readallregisters()
#         print(color('SUCCESS: reading registers.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: reading registers.', fore='red', style='bright'))

#     #register change 
#     device._registers[1022] = 33
#     device._registers[1023] = 1234
#     try:
#         device._syncsettings()
#         print(color('SUCCESS: syncing settings.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: syncing settings. ' + str(e), fore='red', style='bright'))
    
#     device.readallregisters()

#     if(device.getregistervalue(50) == None ):
#         print(color('SUCCESS: reading unknown register.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: reading unknown register.', fore='red', style='bright'))
    
#     register = device.getregistervalue(1003)
#     if(register == None):
#         print(color('SUCCESS: reading register that should be none.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: reading register that should be none.', fore='red', style='bright'))

#     if(device.getchannelvalue("power", True) == None ):
#         print(color('SUCCESS: getting dataset (power) before processing registers.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting dataset (power) before processing registers.', fore='red', style='bright'))

#     if(device.getlogvalue("power") == None ):
#         print(color('SUCCESS: getting logvalue (power) before processing registers.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power) before processing registers.', fore='red', style='bright'))

#     if(device.getlogvalue("test") == None ):
#         print(color('SUCCESS: getting logvalue (test) before processing registers.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (test) before processing registers.', fore='red', style='bright'))

#     device._processchannels()

#     if(device.getchannelvalue("power", True) == None ):
#         print(color('SUCCESS: getting dataset (power).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting dataset (power).', fore='red', style='bright'))

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

#     if( device.getlogvalue("power") == None ):
#         print(color('SUCCESS: getting logvalue (power).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power).', fore='red', style='bright'))

#     time.sleep(1)
#     device.readallregisters()
#     device._processchannels()
#     if( device.getlogvalue("power") == None ):
#         print(color('SUCCESS: getting logvalue (power) after wait.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power) after wait.', fore='red', style='bright'))

#     if( device.getlogvalue("abc") == None ):
#         print(color('SUCCESS: getting logvalue (abc) after wait.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (abc) after wait.', fore='red', style='bright'))

#     device.stop()
#     time.sleep(10)

#     device = GeneralDevice()
#     device._running = True
#     avgVal0 = device.getlogvalue("test")
#     sumVal0 = device.getlogvalue("power")
#     device._excecutebuscommunication()
#     avgVal1 = device.getlogvalue("test")
#     sumVal1 = device.getlogvalue("power")
#     device._excecutebuscommunication()
#     avgVal2 = device.getlogvalue("test")
#     sumVal2 = device.getlogvalue("power")
#     device._excecutebuscommunication()
#     avgVal3 = device.getlogvalue("test")
#     sumVal3 = device.getlogvalue("power")
#     device._excecutebuscommunication()
#     avgVal4 = device.getlogvalue("test")
#     sumVal4 = device.getlogvalue("power")
#     if( avgVal4 == avgVal1 and sumVal4 == sumVal2):
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

#     device = GeneralDevice()
#     device.setbuscommunicationwaittime(0)
#     device.start()
#     time.sleep(5)

#     if( device.getlogvalue("power") == None ):
#         print(color('SUCCESS: getting logvalue (power) after starting device with frequency 0.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power) after starting device with frequency 0.', fore='red', style='bright'))
    
#     if( device.getlogvalue("test") == None ):
#         print(color('SUCCESS: getting logvalue (test) after starting device with frequency = 0.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (test) after starting device with frequency = 0.', fore='red', style='bright'))

#     device.setbuscommunicationwaittime(1)
#     time.sleep(3)

#     value = device.getlogvalue("power")
#     if(value == None):
#         print(color('SUCCESS: getting logvalue (power) after starting device with frequency >0.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power) after starting device with frequency >0.', fore='red', style='bright'))

#     if( device.getlogvalue("test") == None ):
#         print(color('SUCCESS: getting logvalue (test) after starting device with frequency >0.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (test) after starting device with frequency >0.', fore='red', style='bright'))

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
#     device = GeneralDevice()
#     connection = DcsConnection(serial3, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     try:
#         while True:
#             print(color('[GeneralDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
#             print(device.getinfo())
#             device.showcommunicationerrors()
#             device.showcommunicationerrorsrate()
#             time.sleep(10)
#     except KeyboardInterrupt as e:
#         print("[DCS-Connection] Stopping Test...")
#         device.stop()
#     input("waiting...  PRESS ENTER")
