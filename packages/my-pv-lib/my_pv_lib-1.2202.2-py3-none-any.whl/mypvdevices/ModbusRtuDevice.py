#!/usr/bin/python

import logging
import time
from datetime import datetime
import sys
import os
import json

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusConnection import ModbusConnection
from mypvdevices.ModbusDevice import ModbusDevice

MODBUSRETRIES = 3

class ModbusRtuDevice(ModbusDevice):

    def __init__(self, unitId):
        super().__init__(unitId)

        self._name = self.__class__.__name__ + " " + str(self._unit)

    def _connect(self):
        logging.debug("Connect not required for ModbusRtu based devices.")
        pass
    
    def _readregister(self, registerId, registertype="holding"):
        try:
            for attempt in range(MODBUSRETRIES):
                if registertype == "holding":
                    registers = ModbusConnection.instance().readregisters(self._unit, registerId, 1)
                else:
                    registers = ModbusConnection.instance().readinputregisters(self._unit, registerId, 1)
                if registers != None:
                    return registers[registerId]
            raise Exception("Modbus communication failed.")
        except Exception as e:
            raise Exception("Register " + str(registertype) + ":" + str(registerId) + " cannot be read. " + str(e))

    def _readregisters(self, startregisteraddress, registerstoread, registertype="holding"):
        try:
            for attempt in range(MODBUSRETRIES):
                if registertype == "holding":
                    registers = ModbusConnection.instance().readregisters(self._unit, startregisteraddress, registerstoread)
                else:
                    registers = ModbusConnection.instance().readinputregisters(self._unit, startregisteraddress, registerstoread)
                if registers != None:
                    return registers
            raise Exception("Modbus communication failed.")
        except Exception as e:
            raise Exception("Registers " + str(registertype) + ":" + str(startregisteraddress) + ":" + str(registerstoread) + " cannot be read. " + str(e))

    def _writeregister(self, registerId, valueToWrite):
        logging.debug(str(self._name) + " writing register " + str(registerId) + " value: " + str(valueToWrite))
        if self._unit != None:
            ModbusConnection.instance().writeregister(self._unit, registerId, valueToWrite)
        else:
            print("Register " + str(registerId) + " changed to " + str(valueToWrite))

    def _writeregisters(self, registerStartId, valuesToWrite):
        logging.debug(str(self._name) + " writing registers starting at " + str(registerStartId) + " value: " + str(valuesToWrite))
        if self._unit != None:
            ModbusConnection.instance().writeregisters(self._unit, registerStartId, valuesToWrite)
        else:
            print("Register starting at" + str(registerStartId) + " changed to " + str(valuesToWrite))

    def getcommunicationerrorscounter(self):
        return ModbusConnection.instance().getModbusErrorCounter(self._unit)

    def getcommunicationerrorsrate(self):
        return ModbusConnection.instance().getModbusErrorRate(self._unit)

    def getmodbusmodulestate(self):
        return ModbusConnection.instance().getModbusModuleState()

# # Entry Point     
# if __name__ == "__main__":

#     from colr import color

#     from DcsConnection import DcsConnection

#     logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

#     #device connection tests
#     serial = "120100200505tes1"
#     cryptoKey = "41424142414241424142414241424142"
#     server = "my-pv.live"

#     device = ModbusRtuDevice(1)
#     device.readregister(1021)

#     #AUTO-Tests
#     #Constructor Tests
#     try:
#         device = ModbusRtuDevice(1)
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
#         logData = device.getlogdata()
#         print(color('ERROR: getting device logData.', fore='red', style='bright'))
#     except:
#         print(color('SUCCESS: getting device logData.', fore='green', style='bright'))

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
#         if(temp == "ModbusRtuDevice"):
#             print(color('SUCCESS: getting device type.', fore='green', style='bright'))
#         else:
#             raise Exception("device type does not match.")
#     except:
#         print(color('ERROR: getting device type.', fore='red', style='bright'))
 
#     #Modbus tests
#     device = ModbusRtuDevice(1)
#     try:
#         device.readallregisters()
#         print(color('SUCCESS: reading registers.', fore='green', style='bright'))
#     except Exception as e:
#         print(color('ERROR: reading registers. ' + str(e), fore='red', style='bright'))

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

#     power = device.getchannelvalue("power", True)
#     if(power == None):
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
#     device._registers[1013] = 700
#     device._processchannels()
#     power = device.getlogvalue("power")
#     if( power == None ):
#         print(color('SUCCESS: getting logvalue (power) after wait.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (power) after wait.', fore='red', style='bright'))

#     if( device.getlogvalue("test") == None ):
#         print(color('SUCCESS: getting logvalue (test) after wait.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (test) after wait.', fore='red', style='bright'))

#     if( device.getlogvalue("abc") == None ):
#         print(color('SUCCESS: getting logvalue (abc) after wait.', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (abc) after wait.', fore='red', style='bright'))

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

#     device = ModbusRtuDevice(1)
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

#     if(device != None):
#         try:
#             register = device.readregister(1021)
#             if register > 0 and register < 900: 
#                 print(color('SUCCESS: reading register.', fore='green', style='bright'))
#             else:
#                 print(color('ERROR: reading register. Value missmatch: ' + str(register), fore='red', style='bright'))
#         except Exception as e:
#             print(color('ERROR: reading register. Error: ' + str(e), fore='red', style='bright'))

#     if(device != None):
#         try:
#             registers = device.readregisters(1000, 22)
#             if registers[1021] !=  0 and registers[1001] == 0:
#                 print(color('SUCCESS: reading registers.', fore='green', style='bright'))
#             else:
#                 print(color('ERROR: reading registers. Value missmatch: ' + str(registers), fore='red', style='bright'))
#         except Exception as e:
#             print(color('ERROR: reading registers. Error: ' + str(e), fore='red', style='bright'))

#     #DCS communication tests
#     device = ModbusRtuDevice(1)
#     connection = DcsConnection(serial, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     try:
#         while True:
#             print(color('[ModbusRtuDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
#             print(device.getinfo())
#             device.showcommunicationerrors()
#             device.showcommunicationerrorsrate()
#             time.sleep(10)
#     except KeyboardInterrupt as e:
#         print("[DCS-Connection] Stopping Test...")
#         device.stop()
