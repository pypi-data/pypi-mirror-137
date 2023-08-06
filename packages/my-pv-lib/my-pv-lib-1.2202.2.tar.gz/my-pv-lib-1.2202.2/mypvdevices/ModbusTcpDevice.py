#!/usr/bin/python

import logging
from socket import gaierror
from pymodbus.client.sync import ModbusTcpClient
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusDevice import ModbusDevice
from mypvdevices.DeviceDiscoverer import DeviceDiscoverer

RESOLVEHOSTERROR = 99
MODBUSRETRIES = 3

class ModbusTcpException(Exception):
    def __init__(self, msg, code):

        if code == None:
            msg="errorcode required"
            raise TypeError(msg)

        self.code = code
        self.message = msg
    def __str__(self):
        return repr(str(self.message) + ". Error-Code: " + str(self.code))

class ModbusTcpDevice(ModbusDevice):
    _modbusConnection = None
    _modbushosterror = False
    _modbusconnectionerrorcounter = 0
    _modbusconnectioncounter = 0
    _staticHost = None
    _identity = None
    _currentHost = None
    _port = None

    def __init__(self, identity, statichost, port, unitId = 1):
        super().__init__(unitId)

        if identity != None and isinstance(identity, str):
            self._identity = identity
        else:
            errmsg = "Instance not created. Identity is invalid. Identity=" + str(identity)
            logging.error(errmsg)
            raise ValueError(errmsg)

        if statichost != None and isinstance(statichost, str):
            self._staticHost = statichost
        else:
            if statichost != None:
                errmsg = "Instance not created. Host is invalid. Host=" + str(statichost)
                logging.error(errmsg)
                raise ValueError(errmsg)

        if isinstance(port, int):
            self._port = port
        else:
            errmsg = "Instance not created. Port is invalid. port=" + str(port)
            logging.error(errmsg)
            raise ValueError(errmsg)

        self._name = self._name + " " + str(self._identity)

    def _connect(self):        
        if self._staticHost:
            self._currentHost = self._staticHost
        else:
            try:
                ip = DeviceDiscoverer.instance().getipforserial(self._identity)
            except Exception as e:
                logging.warning("Discover error: " + str(e))
                ip = None
            if ip != None:
                self._currentHost = ip
            else:
                logging.warning("Cannot discover device: " + str(self._identity))
                # self._currentHost = None  #try to use old host

        try:
            if self._currentHost:
                self._modbusConnection = ModbusTcpClient(self._currentHost, self._port, timeout=0.3, auto_open=True, auto_close=True)
                self._modbushosterror = False
            else:
                logging.warning("Cannot connect. No host set.")
                raise Exception("No host set.")
        except ValueError as e:
                    print("Invald configuration for ModbusTcpClient: " + str(e))
                    raise(e)

    def _readregisters(self, startregisteraddress, registerstoread, registertype):
        if self._modbusConnection != None:
            logging.debug(str(self._name) + ": Reading " + str(registerstoread) + " " + str(registertype) + " registers starting with register "+ str(startregisteraddress))
            self._modbusconnectioncounter += 1
            for attempt in range(MODBUSRETRIES):
                try:
                    if registertype == "holding":
                        response = self._modbusConnection.read_holding_registers(startregisteraddress, registerstoread, unit=self._unit)
                    else:
                        response = self._modbusConnection.read_input_registers(startregisteraddress, registerstoread, unit=self._unit)
                    self._modbusConnection.close()

                    if response.isError():
                        raise Exception(str(response))
                    else:
                        self._modbushosterror = False
                        break

                except gaierror as e:
                    logging.warning(str(self._name) + " Cannot resolve host: " + str(self._modbusConnection.host()))
                    self._modbushosterror = True
                    self._increaseModbusErrorCounter()
                    raise ModbusTcpException("Cannot resolve host. " + str(self._modbusConnection.host()), RESOLVEHOSTERROR)
                
                except Exception as e:
                    logging.warning(str(self._name) + ". Modbus error: " + str(e))
                    self._increaseModbusErrorCounter()
                    raise e

            if response == None:
                errorcode = self._modbusConnection.last_error()

                if errorcode == 2:
                    raise ModbusTcpException("Host not reachable " + str(self._modbusConnection.host()), errorcode)
                elif errorcode == 4:
                    raise ModbusTcpException("Invalid Registers " + str(startregisteraddress) + " " + str(registerstoread), errorcode)
                else:
                    raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

            registers = dict()
            if response.registers:
                logging.debug("Device " + str(self._name) + ": Data: " + str(response.registers))
                for i in range(len(response.registers)):
                    registers[startregisteraddress + i] = response.registers[i]
            return registers

        else:
            logging.error(str(self._name) + ": no Modbus-Client ")
            raise Exception("No modbus-client.")

    def _readregister(self, registeraddress, registertype):
        if self._modbusConnection:
            logging.debug(str(self._name) + ": Reading " + str(registertype) + " register " + str(registeraddress))
            self._modbusconnectioncounter += 1
            for attempt in range(MODBUSRETRIES):
                try:
                    if registertype == "holding":
                        response = self._modbusConnection.read_holding_registers(registeraddress, 1, unit=self._unit)
                    else:
                        response = self._modbusConnection.read_input_registers(registeraddress, 1, unit=self._unit)
                    self._modbusConnection.close()

                    if response.isError():
                        raise Exception(str(response))
                    else:
                        self._modbushosterror = False
                        break

                except gaierror as e:
                    logging.warning(str(self._name) + " Cannot resolve host: " + str(self._modbusConnection.host()))
                    self._modbushosterror = True
                    self._increaseModbusErrorCounter()
                    raise ModbusTcpException("Cannot resolve host. " + str(self._modbusConnection.host()), RESOLVEHOSTERROR)
                
                except Exception as e:
                    logging.warning(str(self._name) + ". Modbus error: " + str(e))
                    self._increaseModbusErrorCounter()
                    raise e

            if response == None:
                errorcode = self._modbusConnection.last_error()

                if errorcode == 2:
                    raise ModbusTcpException("Host not reachable " + str(self._modbusConnection.host()), errorcode)
                elif errorcode == 4:
                    raise ModbusTcpException("Invalid Register " + str(registeraddress), errorcode)
                else:
                    raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

            register = None
            if response.registers:
                logging.debug("Device " + str(self._name) + ": Data: " + str(response.registers))
                register = response.registers[0]
            return register

        else:
            logging.error(str(self._name) + ": no Modbus-Client ")
            raise Exception("Register " + str(registeraddress) + " cannot be read. No modbus-client.")

    def _writeregister(self, registerId, valueToWrite):
        if self._modbusConnection:
            for attempt in range(MODBUSRETRIES):
                try:
                    self._modbusconnectioncounter += 1
                    response = self._modbusConnection.write_register(registerId, valueToWrite, unit=1)
                    self._modbusConnection.close()
                    if response.isError():
                        raise Exception(str(response))     
                    self._modbushosterror = False
                    break

                except gaierror as e:
                    logging.warning(str(self._name) + " Cannot resolve host: " + str(self._modbusConnection.host()))
                    self._modbushosterror = True
                    self._increaseModbusErrorCounter()
                    raise ModbusTcpException("Cannot resolve host. " + str(self._modbusConnection.host()), RESOLVEHOSTERROR)
                except Exception as e:
                    logging.warning(str(self._name) + " Modbus Write Error: " + str(e))
                    self._increaseModbusErrorCounter()
                    raise e

            if response == None:
                logging.warning(str(self._name) + " Cannot write register. Register " + str(registerId))
                self._increaseModbusErrorCounter()
                raise ModbusTcpException("Cannot write register " + str(registerId), 22)    #Todo errornr

    def _writeregisters(self, registerStartId, dataToWrite):
        if self._modbusConnection:
            for attempt in range(MODBUSRETRIES):
                try:
                    self._modbusconnectioncounter += 1
                    response = self._modbusConnection.write_registers(registerStartId, dataToWrite, unit=1)
                    self._modbusConnection.close()
                    if response.isError():
                        raise Exception(str(response))     
                    self._modbushosterror = False
                    break

                except gaierror as e:
                    logging.warning(str(self._name) + " Cannot resolve host: " + str(self._modbusConnection.host()))
                    self._modbushosterror = True
                    self._increaseModbusErrorCounter()
                    raise ModbusTcpException("Cannot resolve host. " + str(self._modbusConnection.host()), RESOLVEHOSTERROR)
                except Exception as e:
                    logging.warning(str(self._name) + " Modbus Write Error: " + str(e))
                    self._increaseModbusErrorCounter()
                    raise e

            if response == None:
                logging.warning(str(self._name) + " Cannot write register. Register " + str(registerStartId))
                self._increaseModbusErrorCounter()
                raise ModbusTcpException("Cannot write register " + str(registerStartId), 22)    #Todo errornr

    def _supervise(self):
        super()._supervise()
        if self._modbushosterror:
            try:
                self._connect()
            except Exception as e:
                logging.warning(str(self._name) + " Cannot rediscover device.")
                    
    def getcommunicationerrorscounter(self):
        return self._modbusconnectionerrorcounter

    def getcommunicationerrorsrate(self):
        with self._lock:
            errorRate = 0
            try:
                errorRate = round(self._modbusconnectionerrorcounter / self._modbusconnectioncounter, 2)
            except:
                logging.debug(str(self._name) + " Cannot calculate modbus tcp error rate.")
            return errorRate

    def resetcounters(self):
        with self._lock:
            try:
                self._modbusconnectionerrorcounter = 0
                self._modbusconnectioncounter = 0
            except Exception as e:
                logging.error(str(self._name) + " Error resetting modbus tcp connection counters. " + str(e))

    def _increaseModbusErrorCounter(self):
        self._modbusconnectionerrorcounter += self._modbusconnectionerrorcounter
        logging.debug(str(self._name) + " Communication error. Total errors: " + str(self._modbusconnectionerrorcounter))
        return self._modbusconnectionerrorcounter

# # Entry Point     
# if __name__ == "__main__":

#     from colr import color
#     import time

#     from DcsConnection import DcsConnection

#     logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

#     # serial = "1601242002040015"
#     serial = "2001002006100016"
#     serial_fake = "2001005006100000"
#     correctip = "192.168.92.29"

#     #device connection tests
#     dcsserial = "120100200505tes1"
#     cryptoKey = "41424142414241424142414241424142"
#     server = "my-pv.live"

#     #Constructor Tests
#     try:
#         device = ModbusTcpDevice(serial, None, 502)
#         print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
#     except:
#         print(color('ERROR: creating valid device.', fore='red', style='bright'))

#     try:
#         setup = device.getsetup()
#         if setup == {}:
#             print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
#         else:
#             raise Exception("Setup not valid")
#     except Exception as e:
#         print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

#     try:
#         data = device.getdata()
#         print(color('ERROR: getting device data.', fore='red', style='bright'))
#     except:
#         print(color('SUCCESS: getting device data.', fore='green', style='bright'))

#     try:
#         logData = device.getlogdata()
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
#         if(temp == "ModbusTcpDevice"):
#             print(color('SUCCESS: getting device type.', fore='green', style='bright'))
#         else:
#             raise Exception("device type does not match.")
#     except:
#         print(color('ERROR: getting device type.', fore='red', style='bright'))

#     device = ModbusTcpDevice(serial, None, 502)
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

#     time.sleep(3)
#     device.stop()

#     #DCS communication tests
#     device = ModbusTcpDevice(serial, None, 502)
#     connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     try:
#         while True:
#             print(color('[ModbusTcpDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
#             print(device.getinfo())
#             device.showcommunicationerrors()
#             device.showcommunicationerrorsrate()
#             time.sleep(10)
#     except KeyboardInterrupt as e:
#         print("[DCS-Connection] Stopping Test...")
#         device.stop()
