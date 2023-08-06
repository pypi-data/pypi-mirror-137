#!/usr/bin/python

import logging
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.GeneralDevice import GeneralDevice

class ModbusDevice(GeneralDevice):

    _unit = None

    def __init__(self, unitId):
        super().__init__()

        if unitId != None and isinstance(unitId, int):
            self._unit = unitId
        else:
            errmsg = "Instance not created. UnitId is invalid. UnitId=" + str(unitId)
            logging.error(errmsg)
            raise TypeError(errmsg)

# # Entry Point     
# if __name__ == "__main__":

#     from colr import color
#     from DcsConnection import DcsConnection
#     import time

#     logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

#     #device connection tests
#     serial = "120100200505tes1"
#     serial2 = "120100200505tes2"
#     serial3 = "120100200505tes3"
#     cryptoKey = "41424142414241424142414241424142"
#     server = "my-pv.live"

#     device = ModbusDevice(1)
#     print(device)

#     #AUTO-Tests
#     #Constructor Tests
#     try:
#         device = ModbusDevice(1)
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
#         if(temp == "ModbusDevice"):
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
 
#     #Modbus tests
#     device = ModbusDevice(1)
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
#         if not device._setup["ww2target"] == 33:
#             raise Exception("ww2target missmatch")
#         if not device._setup["ww2offset"] == 1514:
#             raise Exception("ww2offset missmatch")
#         # if not device._registers[1023] == 1514:
#         #     raise Exception("register 1023 missmatch")
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

#     if( device.getlogvalue("test") == None ):
#         print(color('SUCCESS: getting logvalue (test).', fore='green', style='bright'))
#     else:
#         print(color('ERROR: getting logvalue (test).', fore='red', style='bright'))

#     time.sleep(1)
#     device.readallregisters()
#     device._processchannels()
#     if( device.getlogvalue("power") == None ):
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

#     device.stop()
#     time.sleep(10)

#     device = ModbusDevice(1)
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

#     device = ModbusDevice(1)
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
#     if(value == None ):
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
#     device = ModbusDevice(1)
#     connection = DcsConnection(serial3, cryptoKey, server, 50333)
#     device.addserverconnection(connection)
#     device.start()
#     try:
#         while True:
#             print(color('[ModbusDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
#             print(device.getinfo())
#             device.showcommunicationerrors()
#             device.showcommunicationerrorsrate()
#             time.sleep(10)
#     except KeyboardInterrupt as e:
#         print("[DCS-Connection] Stopping Test...")
#         device.stop()
#     input("waiting...  PRESS ENTER")
