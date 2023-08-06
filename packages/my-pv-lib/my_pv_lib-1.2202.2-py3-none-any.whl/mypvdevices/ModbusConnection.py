#!/usr/bin/python

import threading
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import logging
import time
from colr import color

BUSRECOVERYTIME = 0.5

class ModbusConnection:     #Singleton
    __instance__ = None
    __connectionErrorCounter__ = None
    __connectionCounter__ = None
    __modbusConnection__ = None
    __modbusClient__ = None
    __mutex__ = threading.Lock()
    __modbusModuleState = None
    __modbus_stopbits = 1
    __modbusbytesize = 8
    __modbusparity = 'N'
    __modbusbaudrate = 9600
    __modbustimeout = 0.2
    __modbusretryonempty = True
    __modbusretryoninvalid = True

    @staticmethod
    def instance():
        """ Static access method. """
        if ModbusConnection.__instance__ == None:
            with ModbusConnection.__mutex__:
                ModbusConnection()
        return ModbusConnection.__instance__

    def __init__(self):
        """ Virtually private constructor. """
        if ModbusConnection.__instance__ != None:
            raise Exception("[ModbusConnection] This class is a singleton! Instance already created")
        else:
            ModbusConnection.__instance__ = self

        self.__connectionErrorCounter__ = dict()
        self.__connectionCounter__ = dict()
        self.__modbusClient__ = ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = self.__modbus_stopbits, bytesize = self.__modbusbytesize, parity = self.__modbusparity, baudrate= self.__modbusbaudrate, timeout=self.__modbustimeout, retry_on_empty=self.__modbusretryonempty, retry_on_invalid=self.__modbusretryoninvalid)

    def __increaseModbusErrorCounter__(self, unitId):
        try:
            self.__connectionErrorCounter__[unitId] = self.__connectionErrorCounter__[unitId] + 1
        except:
            self.__connectionErrorCounter__[unitId] = 1
        
        logging.debug("[ModbusConnection] Node " + str(unitId) + ": Communication error. Total errors: " + str(self.__connectionErrorCounter__[unitId]))
        counter = self.__connectionErrorCounter__[unitId]
        return counter

    def setConfiguration(self, stopbits, bytesize, parity, baudrate, timeout, retry_on_empty, retry_on_invalid):
        self.__modbus_stopbits = stopbits
        self.__modbusbytesize = bytesize
        self.__modbusparity = parity
        self.__modbusbaudrate = baudrate
        self.__modbustimeout = timeout
        self.__modbusretryonempty = retry_on_empty
        self.__modbusretryoninvalid = retry_on_invalid

        with self.__mutex__:
            self.__modbusClient__.close()
            self.__modbusClient__ = ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = self.__modbus_stopbits, bytesize = self.__modbusbytesize, parity = self.__modbusparity, baudrate= self.__modbusbaudrate, timeout=self.__modbustimeout, retry_on_empty=self.__modbusretryonempty, retry_on_invalid=self.__modbusretryoninvalid)

    def getModbusErrorCounter(self, unitId):
        try:
            return self.__connectionErrorCounter__[unitId]
        except:
            self.__connectionErrorCounter__[unitId] = 0
            return 0

    def getModbusErrorRate(self, node):
        try:
            self.__connectionErrorCounter__[node]
            self.__connectionCounter__[node]
        except:
            return 0

        try:
            if self.__connectionCounter__[node] == 0:
                return 0
            return round(self.__connectionErrorCounter__[node] / self.__connectionCounter__[node], 2)
        except Exception as e:
            logging.warning("[ModbusConnection] Node " + str(node) + ": Cannot calculate error rate.")
            return None

    def getModbusModuleState(self):
        return self.__modbusModuleState

    def resetcounters(self, unitId):
        with self.__mutex__:
            try:
                self.__connectionErrorCounter__[unitId] = 0
                self.__connectionCounter__[unitId] = 0
            except Exception as e:
                logging.error("[ModbusConnection] Node " + str(node) + ": Error resetting counters. " + str(e))

    def __connectSocket__(self):
        if self.__modbusClient__.socket == None:
            logging.debug("[ModbusConnection] Modbus not connected. Connecting...")
            try:
                self.__modbusConnection__ = self.__modbusClient__.connect()
                if(self.__modbusConnection__ != True):
                    logging.error("[ModbusConnection] Cannot connect modbus. Check modbus module.")
                    raise Exception("Module Error")
            except Exception as e:
                logging.error("[ModbusConnection] Unknown modbus connection error: " + str(e))
                raise(e)
        return self.__modbusConnection__

    def checkmodbusconnection(self):
        return self.__modbusConnection__

    def writeregister(self, node, registerId, value):
        result = None
        with self.__mutex__:
            logging.debug("[ModbusConnection] Node " + str(node) + ": writing register " + str(registerId) +" with value "+ str(value))
            try:
                self.__connectionCounter__[node] += 1
            except:
                self.__connectionCounter__[node] = 1
            if self.__modbusClient__ != None:
                try:
                    socket = self.__connectSocket__()
                except Exception as e:
                    logging.warning("[ModbusConnection] Modbus socket error: " + str(e))
                    self.__increaseModbusErrorCounter__(node)
                    raise e
                #     socket = None
                if(socket):
                    try:
                        result = self.__modbusClient__.write_register(registerId, value, unit = node)
                        if result.isError():
                            raise Exception(str(result))
                    except Exception as e:
                        logging.warning("[ModbusConnection] Modbus Write Error: " + str(e))
                        self.__increaseModbusErrorCounter__(node)
                        result = None
                else:
                    logging.warning("[ModbusConnection] Cannot write to node " + str(node) + ".")
        return result

    def writeregisters(self, node, registerStartId, values):
        result = None
        with self.__mutex__:
            logging.debug("[ModbusConnection] Node " + str(node) + ": writing registers starting at" + str(registerStartId) +" with value "+ str(values))
            try:
                self.__connectionCounter__[node] += 1
            except:
                self.__connectionCounter__[node] = 1
            if self.__modbusClient__ != None:
                try:
                    socket = self.__connectSocket__()
                except Exception as e:
                    logging.warning("[ModbusConnection] Modbus socket error: " + str(e))
                    self.__increaseModbusErrorCounter__(node)
                    raise e
                #     socket = None
                if(socket):
                    try:
                        result = self.__modbusClient__.write_registers(registerStartId, values, unit = node)
                        if result.isError():
                            raise Exception(str(result))
                    except Exception as e:
                        logging.warning("[ModbusConnection] Modbus Write Error: " + str(e))
                        self.__increaseModbusErrorCounter__(node)
                        result = None
                else:
                    logging.warning("[ModbusConnection] Cannot write to node " + str(node) + ".")
        return result

    def readregisters(self, node, startAddress = 1000, registersToRead = 1):
        return self._readregisters(node, startAddress, registersToRead, "holding")

    def _readregisters(self, node, startAddress, registersToRead, type="holding"):
        with self.__mutex__:
            logging.debug("[ModbusConnection] Node " + str(node) + ": Reading " + str(registersToRead) + " " + str(type) + "-registers starting with register "+ str(startAddress))
            try:
                self.__connectionCounter__[node] += 1
            except:
                self.__connectionCounter__[node] = 1
            
            if self.__modbusClient__ != None:
                try:
                    socket = self.__connectSocket__()
                except Exception as e:
                    logging.warning("[ModbusConnection] Modbus socket error: " + str(e))
                    socket = None
                if(socket):
                    self.__modbusModuleState = "CONNECTED"
                    registers = dict()
                    try:
                        if type == "input":
                            modbus_response = self.__modbusClient__.read_input_registers(startAddress, registersToRead, unit=node)
                        else:
                            modbus_response = self.__modbusClient__.read_holding_registers(startAddress, registersToRead, unit=node)
                        if modbus_response.isError():
                            raise Exception(str(modbus_response))

                        logging.debug("[ModbusConnection] Node " + str(node) + ": Data: " + str(modbus_response.registers))
                        for i in range(len(modbus_response.registers)):
                            registers[startAddress + i] = modbus_response.registers[i]

                        return registers

                    except Exception as e:
                        logging.debug("[ModbusConnection] Modbus read error at node " + str(node) + ": " + str(e))
                        self.__increaseModbusErrorCounter__(node)
                        time.sleep(BUSRECOVERYTIME)
                else:
                    logging.debug("[ModbusConnection] Cannot read from node " + str(node) + ". Modbus-Socket not connected. Module Error?")
                    self.__modbusModuleState = "ERROR"
            return None

    def readinputregisters(self, node, startAddress = 1000, registersToRead = 1):
        return self._readregisters(node, startAddress, registersToRead, "input")


# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    unitToTest = 1

    # trying to use modbus module
    try:
        socket = ModbusConnection.instance().__connectSocket__()
    except:
        socket = None
    if(socket == True):
        print(color('SUCCESS: Using modbus module.', fore='green', style='bright'))
    else:
        print(color('ERROR: Using modbus module.', fore='red', style='bright'))
        input("PRESS ENTER TO CONTINUE TESTING")

    # testing module state
    internalTempRegisterNumber = 1021
    register = ModbusConnection.instance().readregisters(unitToTest, internalTempRegisterNumber, 1)
    state =  ModbusConnection.instance().getModbusModuleState()
    if(state == "CONNECTED"):
        print(color('SUCCESS: Modbus module state check.', fore='green', style='bright'))
    else:
        print(color('ERROR: Modbus module state check.', fore='red', style='bright'))

    # trying to read temperature from modbus module internal sensor
    internalTempRegisterNumber = 1021
    register = ModbusConnection.instance().readregisters(unitToTest, internalTempRegisterNumber, 1)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register != None and register != {} and errors == 0 and errorrate == 0):
        print(color('SUCCESS: Valid register read of interface temperature.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid register read of interface temperature failed.', fore='red', style='bright'))

    try:
        if register == None:
            raise(Exception("Empty Register."))
        if(register[internalTempRegisterNumber] < 999 and register[internalTempRegisterNumber] > 0):
            print(color('SUCCESS: Read temperature value in valid range. Temperature: ' + str(register[internalTempRegisterNumber]/10), fore='green', style='bright'))
        else:
            print(color('ERROR: Read temperature value in valid range. OUT OF RANGE: ' + str(register[internalTempRegisterNumber]/10), fore='red', style='bright'))
    except Exception as e:
            print(color('ERROR: Read temperature value in valid range. No data found. ' + str(e), fore='red', style='bright'))

    # reading multiple registers
    ModbusConnection.instance().resetcounters(unitToTest)
    register = ModbusConnection.instance().readregisters(unitToTest, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register != None and register != {} and errors == 0 and errorrate == 0):
        print(color('SUCCESS: Valid multiple register read.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid multiple register read.', fore='red', style='bright'))

    # reading multiple registers again
    ModbusConnection.instance().resetcounters(unitToTest)
    register = ModbusConnection.instance().readregisters(unitToTest, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register != None and register != {} and errors == 0 and errorrate == 0):
        print(color('SUCCESS: Valid multiple register read twice.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid multiple register read twice.', fore='red', style='bright'))

    # reading an invalid node id
    register = ModbusConnection.instance().readregisters(99, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(99)
    if(register == None and errors == 1):
        print(color('SUCCESS: Invalid node read.', fore='green', style='bright'))
    else:
        print(color('ERROR: Invalid node read.', fore='red', style='bright'))

    # reading from broadcast address
    register = ModbusConnection.instance().readregisters(0, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(0)
    if(register == None and errors == 1):
        print(color('ERROR: Node 0 (Broadcast) read.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Node 0 (Broadcast) read.', fore='green', style='bright'))

    # reading of multiple invalid registers
    ModbusConnection.instance().resetcounters(unitToTest)
    register = ModbusConnection.instance().readregisters(unitToTest, 4130, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register == None and errors == 1 and errorrate == 1):
        print(color('SUCCESS: Multiple invalid register read.', fore='green', style='bright'))
    else:
        print(color('ERROR: Multiple invalid register read.', fore='red', style='bright'))

    # reading multiple registers multiple times
    ModbusConnection.instance().resetcounters(unitToTest)
    temp = 0
    for i in range(0, 50):
        register = ModbusConnection.instance().readregisters(unitToTest, 1000, 24)
        errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
        errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
        temp = ModbusConnection.instance().__connectionCounter__[unitToTest]
        time.sleep(0.3)
    if(register != None and register != {} and errors == 0 and errorrate == 0 and temp == 50):
        print(color('SUCCESS: Valid multiple register read multiple times.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid multiple register read multiple times.', fore='red', style='bright'))

    # trying to change configuration
    internalTempRegisterNumber = 1021
    ModbusConnection.instance().setConfiguration(1, 8, 'N', 19200, 0.2, True, True)     #change to invalid baudrate
    registerInvalid = ModbusConnection.instance().readregisters(unitToTest, internalTempRegisterNumber, 1)
    ModbusConnection.instance().setConfiguration(1, 8, 'N', 9600, 0.2, True, True)  #chnage to valid baudrate
    registerValid = ModbusConnection.instance().readregisters(unitToTest, internalTempRegisterNumber, 1)

    if(registerValid != None and registerValid != {} and registerInvalid == None):
        print(color('SUCCESS: Configuration change test.', fore='green', style='bright'))
    else:
        print(color('ERROR: Configuration change test.', fore='red', style='bright'))

    # writing to vaild node
    ModbusConnection.instance().resetcounters(unitToTest)
    register = 1023
    value = 1514
    try:
        result = ModbusConnection.instance().writeregister(unitToTest, register, value)
        errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
        errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
        if(result != None and result.value == value and errors == 0 and errorrate == 0):
            print(color('SUCCESS: write register to vaild node.', fore='green', style='bright'))
        else:
            print(color('ERROR: write register to vaild node. Invalid value', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: write register to vaild node. ' + str(e), fore='red', style='bright'))

    # writing to invaild node
    node = 99
    register = 1023
    value = 1514
    ModbusConnection.instance().resetcounters(node)
    try:
        result = ModbusConnection.instance().writeregister(node, register, value)
        errors = ModbusConnection.instance().getModbusErrorCounter(node)
        errorrate =  ModbusConnection.instance().getModbusErrorRate(node)
        if(result == None and errors == 1 and errorrate == 1):
            print(color('SUCCESS: write register to invaild node.', fore='green', style='bright'))
        else:
            print(color('ERROR: write register to invaild node.', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: write register to invaild node. ' + str(e), fore='red', style='bright'))