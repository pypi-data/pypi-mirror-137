#!/usr/bin/python

# from datetime import datetime, timedelta
import logging
import time
import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.ModbusConnection import ModbusConnection
from mypvdevices.ChannelConfig import ChannelConfig
from mypvdevices.SetupMapping import SetupMapping

MODBUSWARNLEVEL = 0.5
REGISTERTIMEOUT = 30
SERIALLEN = 16

class DeviceDcElwa(ModbusRtuDevice):
    _serial = None
    _irerror = False
    _errorcode = 0

    def __init__(self, serial, unitId):
        super().__init__(unitId)

        if serial != None and len(serial) == SERIALLEN:
            self._serial = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)

        self._name = self._name + " " + str(self._serial)
        self._buscommunicationWaitTime = 10
        self._datamaximumage = 60

        ModbusConnection.instance().setConfiguration(1, 8, 'N', 9600, 0.2, True, True)

        self._channels["day_counter"] = ChannelConfig([1000], "NUMBER", 0, datasettype="avg")
        self._channels["operation_mode"] = ChannelConfig([1001], "NUMBER", 0, datasettype="avg")
        self._channels["dc_breaker_state"] = ChannelConfig([1002], "NUMBER", 0, datasettype="sum")
        self._channels["dc_relay_state"] = ChannelConfig([1003], "NUMBER", 0, datasettype="sum")
        self._channels["ac_relay_state"] = ChannelConfig([1004], "NUMBER", 0, datasettype="sum")
        self._channels["temp1"] = ChannelConfig([1005], "NUMBER", 0.1, datasettype="avg")     #ELWA Temperatur sensor
        self._channels["temp_day_min"] = ChannelConfig([1006], "NUMBER", 0.1, datasettype="avg")
        self._channels["temp_day_max"] = ChannelConfig([1007], "NUMBER", 0.1, datasettype="avg")
        self._channels["dc_temp_target"] = ChannelConfig([1008], "NUMBER", 0.1, "rw", datasettype="avg")
        self._channels["ac_temp_target"] = ChannelConfig([1009], "NUMBER", 0.1, "rw", datasettype="avg")
        self._channels["tempchip"] = ChannelConfig([1010], "NUMBER", 0, datasettype="avg")
        self._channels["iso_voltage"] = ChannelConfig([1011], "NUMBER", 0, datasettype="avg")
        self._channels["dc_voltage"] = ChannelConfig([1012], "NUMBER", 0, datasettype="avg")
        self._channels["dc_current"] = ChannelConfig([1013], "NUMBER", 0, datasettype="avg")
        self._channels["dc_power"] = ChannelConfig([1014], "NUMBER", 0, datasettype="sum")
        self._channels["dc_day_wh"] = ChannelConfig([1015], "NUMBER", 0, datasettype="avg")
        self._channels["dc_total_kwh"] = ChannelConfig([1016], "NUMBER", 0.001, datasettype="avg")
        self._channels["ac_day_wh"] = ChannelConfig([1017], "NUMBER", 0, datasettype="avg")
        self._channels["minutes_from_noon"] = ChannelConfig([1018], "NUMBER", 0, datasettype="avg")
        self._channels["minutes_since_dusk"] = ChannelConfig([1019], "NUMBER", 0, datasettype="avg")
        self._channels["ac_boost_mode"] = ChannelConfig([1020], "NUMBER", 0, "rw", datasettype="avg")
        self._channels["temp2"] = ChannelConfig([1021], "NUMBER", 0.1, datasettype="avg")     #IR-Interface temperature sensor
        self._channels["boost_temp_target"] = ChannelConfig([1022], "NUMBER", 0.1, "rw", datasettype="avg")     #ELWA Modbus Interface boost temperature
        self._channels["ww2offset_calibration"] = ChannelConfig([1023], "NUMBER", 0, "rw", datasettype="avg")     #Temp sensor offset calibration

        self._setup["device"] = SetupMapping(defaultvalue=self.getdevicetype())
        self._setup["fwversion"] = SetupMapping(defaultvalue=self._firmwareversion)
        self._setup["serialno"] = SetupMapping(defaultvalue=self._serial)
        self._setup["elno"] = SetupMapping(defaultvalue=self._unit)
        self._setup["ww2target"] = SetupMapping("boost_temp_target")
        self._setup["ww2offset"] = SetupMapping("ww2offset_calibration", forced=True, defaultvalue=1514)

    def getdevicetype(self):
        return "ELWA"

    def getdata(self):

        acRelayState = self.getchannelvalue("ac_relay_state", True)
        dcPower = self.getchannelvalue("dc_power", True)
        operationMode = self.getchannelvalue("operation_mode", True)
        acdaywh = self.getchannelvalue("ac_day_wh", True)

        if operationMode == 3 or operationMode == 5 or operationMode == 6 or operationMode == 7 or operationMode == 8 or operationMode == 9 or operationMode == 10 or operationMode == 11 or operationMode == 12 or operationMode == 13 or operationMode == 14 or operationMode == 15 or operationMode == 16 or operationMode == 20 or operationMode == 21 or operationMode == 135:
            acHeating = True
        else:
            acHeating = False

        if acRelayState != None:
            if acHeating == True and acRelayState == 1:
                boostpower = 750
            else:
                boostpower = 0
        else:
            boostpower = None

        if(boostpower != None):
            power = dcPower + boostpower
            meter = -boostpower
        else:
            power = dcPower
            meter = None

        if self._errorcode != 0:
            errorcode = self._errorcode
        else:
            errorcode = None

        errorrate = self.getcommunicationerrorsrate()
        modbusmodulestate = self.getmodbusmodulestate()

        data={
            "device": self.getdevicetype(),
            "fwversion": self._firmwareversion,
            "loctime": time.strftime("%H:%M:%S"),
            "dev_id": self._unit,
            "day_counter" : self.getchannelvalue("day_counter", True),
            "op_mode": operationMode,
            "dc_breaker": self.getchannelvalue("dc_breaker_state", True),
            "dc_relay": self.getchannelvalue("dc_relay_state", True),
            "ac_relay": acRelayState,
            "temp1": self.getchannelvalue("temp1", True, 10),
            "temp_day_min": self.getchannelvalue("temp_day_min", True, 10),
            "temp_day_max": self.getchannelvalue("temp_day_max", True, 10),
            "ww1target": self.getchannelvalue("dc_temp_target", True, 10),
            "ac_temp_target": self.getchannelvalue("ac_temp_target", True, 10),
            "tempchip": self.getchannelvalue("tempchip", True),
            "iso_voltage": self.getchannelvalue("iso_voltage", True),
            "dc_voltage": self.getchannelvalue("dc_voltage", True, 10),
            "dc_current": self.getchannelvalue("dc_current", True, 10),
            "power_elwa": power,
            "boostpower_elwa": boostpower,
            "dc_day_wh": self.getchannelvalue("dc_day_wh", True),
            "dc_total_kwh": self.getchannelvalue("dc_total_kwh", True),
            "ac_day_wh": self.getchannelvalue("ac_day_wh", True),
            "minutes_from_noon": self.getchannelvalue("minutes_from_noon", True),
            "minutes_since_dusk": self.getchannelvalue("minutes_since_dusk", True),
            "ac_boost_mode": self.getchannelvalue("ac_boost_mode", True),
            "m1sum": dcPower,
            "m0sum": meter,
            "temp2": self.getchannelvalue("temp2", True, 10),
            "ww2target": self.getchannelvalue("boost_temp_target", True),
            "ww2offset": self.getchannelvalue("ww2offset_calibration", True),
            "modbuserrorrate":  errorrate,
            "modbusmodulestate": modbusmodulestate,
            "errorcode_elwa": errorcode
        }       
        return data

    def getchannelvalue(self, datasetname, safemode=False, scale=None):
        if self._irerror == False or datasetname in ("temp2"):
            return super().getchannelvalue(datasetname, safemode, scale)
        else:
            return None

    def getlogdata(self, time = None):
        acRelayState = self.getlogvalue("ac_relay_state")
        acdaywh = self.getlogvalue("ac_day_wh")

        if acRelayState != None:
            boostpower = int(round(acRelayState*750))
        else:
            boostpower = None
        
        dcPower = self.getlogvalue("dc_power", "int")
        if dcPower != None:
            if(boostpower != None):
                power = int(dcPower + boostpower)
            else:
                power = dcPower
        else:
            power = None
        if(boostpower != None):
            metercons = -boostpower
        else:
            metercons = None

        pvprod = dcPower

        sLog={
            "logdataage": self.getlogdataage(),
            "healthstate": self.gethealthstate(),
            "errorcode": self._errorcode,
            "modbus_if_state": self.getmodbusmodulestate(),
			"modbus_error_rate": self.getcommunicationerrorsrate(),
			"day_counter" : self.getlogvalue("day_counter", "int"),
			"op_mode": self.getlogvalue("operation_mode", "int"),
			"dc_breaker": self.getlogvalue("dc_breaker_state", "int"),
			"dc_relay": self.getlogvalue("dc_relay_state", "int"),
			"ac_relay": self.getlogvalue("ac_relay_state", "int"),
			"temp": self.getlogvalue("temp1", "int", 10),
			"temp_day_min": self.getlogvalue("temp_day_min", "int", 10),
			"temp_day_max": self.getlogvalue("temp_day_max", "int", 10),
			"dc_temp_target": self.getlogvalue("dc_temp_target", "int", 10),
			"ac_temp_target": self.getlogvalue("ac_temp_target", "int", 10),
			"temp_internal": self.getlogvalue("tempchip", "int"),
			"iso_voltage": self.getlogvalue("iso_voltage", "int"),
			"dc_voltage": self.getlogvalue("dc_voltage", "int"),
			"dc_current": self.getlogvalue("dc_current", "int"),
			"dc_power": self.getlogvalue("dc_power", "int"),
			"dc_day_wh": self.getlogvalue("dc_day_wh", "int"),
			"dc_total_kwh": self.getlogvalue("dc_total_kwh", "int"),
			"ac_day_wh": self.getlogvalue("ac_day_wh", "int"),
			"minutes_from_noon": self.getlogvalue("minutes_from_noon", "int"),
			"minutes_since_dusk": self.getlogvalue("minutes_since_dusk", "int"),
			"ac_boost_mode": self.getlogvalue("ac_boost_mode", "int"),
			"temp2": self.getlogvalue("temp2", "int", 10),
			"ww2target": self.getlogvalue("boost_temp_target", "int"),
			"ww2offset": self.getlogvalue("ww2offset_calibration", "int"),
        }

        logData = {
            "time": time,
            "i_power": power,
            "i_boostpower": boostpower,
            "i_m1sum": pvprod,
            "i_metercons": metercons,
            "i_temp1": self.getlogvalue("temp1", "int", 10),
            "i_temp2": self.getlogvalue("temp2", "int", 10),
            "s_json" : json.dumps(sLog)
        }

        ModbusConnection.instance().resetcounters(self._unit)
        # self._logdata.clear()  #todo sicher?
        return logData

    def getlogvalue(self, datasetname, casttype=None, scale=None):
        if self._irerror == False or datasetname in ("temp2"):
            return super().getlogvalue(datasetname, casttype, scale)
        else:
            return None

    def __checkRegiterTimeStamp__(self):
        if self._registerLastSuccessfullReadTimeStamp != None and len(self._registers) > 0:
            difference = time.time() - self._registerLastSuccessfullReadTimeStamp
            if(difference > REGISTERTIMEOUT):
                return False    
        return True
    
    def _supervise(self):

        super()._supervise()
        
        value = super().getchannelvalue("temp1", True)
        if value != None and ( value > 1200 or value < 0 ):
            logging.warning(str(self._name) + " - Temp1 sensor error: " + str(value))
            temp1error = True
        else:
            temp1error = False

        value = super().getchannelvalue("temp2", True)
        if value != None and ( value > 1200 or value < 0 ):
            logging.warning(str(self._name) + " - Temp2 sensor error: " + str(value))
            temp2error = True
        else:
            temp2error = False

        value = super().getchannelvalue("operation_mode", True)
        if value != None and value > 100 :
            logging.warning(str(self._name) + " - Operation Mode " + str(value) + " detected.")
            opmodeError = True
        else:
            opmodeError = False

        if ModbusConnection.instance().checkmodbusconnection():
            modbusError = False
        else:
            logging.debug(str(self._name) + " - Modbus module not present.")
            ModbusConnection.instance().resetcounters(self._unit)
            modbusError = True

        modbusErrorRate = self.getcommunicationerrorsrate()
        
        if modbusError == False:
            if modbusErrorRate != None and modbusErrorRate >= 0.70:
                logging.warning(str(self._name) + " - Modbus communication to device not working.")
                modbusError = True
            else:                    
                modbusError = False

        registerisvalid = self.__checkRegiterTimeStamp__()
        if registerisvalid != True and modbusError == False:
            logging.warning(str(self._name) + " - Register values too old. Communication errors expected. Registers: " + str(self._registers) + " Timestamp: " + str(self._registerLastSuccessfullReadTimeStamp) + " Age: " + str(time.time() - self._registerLastSuccessfullReadTimeStamp))
            registerError = True
        else:
            registerError = False

        if registerError == False and modbusError == False and modbusErrorRate != None and modbusErrorRate > MODBUSWARNLEVEL and modbusErrorRate < 0.7:
            logging.warning(str(self._name) + " - Modbus error rate to hight " + str(modbusErrorRate) + ".")
            modbusWarning = True
        else:
            modbusWarning = False

        value = ModbusRtuDevice.getchannelvalue(self, "tempchip", True)
        if value == 0 and modbusError == False and registerError == False:
            logging.warning(str(self._name) + " - No IR Connection to Device.")
            irError = True
            self._irerror = True
        else:
            irError = False
            self._irerror = False

        healthState = 0

        #healthState warnings
        if temp2error == True or irError == True or opmodeError == True or modbusWarning == True:
            healthState = 1

        #healthState errors
        if temp1error == True or modbusError == True or registerError == True:
            healthState = 2

        self.__seterrorcode__(irerror=irError, modbuserror=modbusError, registererror=registerError, temp1error=temp1error, temp2error=temp2error, opmodeerror=opmodeError, modbuswarning=modbusWarning)

        if modbusErrorRate != None or healthState == 2:
            self._sethealthstate(healthState)

    def __seterrorcode__(self, modbuserror=0, irerror=0, registererror=0, temp1error=0, temp2error=0, opmodeerror=0, modbuswarning=0):
        if modbuswarning: 
            self.__setBit__(0)
        else:
            self.__resetBit__(0)

        if modbuserror:
            self.__setBit__(1)
        else:
            self.__resetBit__(1)

        if irerror:
            self.__setBit__(2)
        else:
            self.__resetBit__(2)

        if registererror:
            self.__setBit__(3)
        else:
            self.__resetBit__(3)

        if temp1error:
            self.__setBit__(4)
        else:
            self.__resetBit__(4)

        if temp2error:
            self.__setBit__(5)
        else:
            self.__resetBit__(5)

        if opmodeerror:
            self.__setBit__(6)
        else:
            self.__resetBit__(6)

    def __setBit__(self, offset):
        mask = 1 << offset
        self._errorcode = (self._errorcode | mask)

    def __resetBit__(self, offset):
        mask = ~(1 << offset)
        self._errorcode = (self._errorcode & mask)

# Entry Point     
if __name__ == "__main__":

    from colr import color

    # SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    # sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    # from mypvdevices.DcsConnection import DcsConnection
    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    serial = "120100200505tes1"
    cryptoKey = "41424142414241424142414241424142"
    serial2 = "120100200505tes2"
    cryptoKey2 = "41424142414241424142414241424142"
    serial3 = "120100200505tes3"
    cryptoKey3 = "41424142414241424142414241424142"
    server = "my-pv.live"

    try:
        device = DeviceDcElwa("123456789", 1)
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))
        device = None

    try:
        device = DeviceDcElwa(None, 1)
        print(color('ERROR: serial is None.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial is None.', fore='green', style='bright'))

    try:
        device = DeviceDcElwa(serial, 1)
        register = device.readregister(1021)
        register2 = device.readregister(1005)
        if not register > 0 and not register2 != None:
            raise Exception("invalid values")
        print(color('SUCCESS: reading some registers.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: reading some registers.', fore='red', style='bright'))

    # try to read from valid device
    device = DeviceDcElwa(serial, 1)
    try:
        device.readallregisters()
        if(len(device._registers) == 24):
            print(color('SUCCESS: reading registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid length")
    except Exception as e:
        print(color('ERROR: reading registers. ' + str(e), fore='red', style='bright'))

    try:
        if device._syncsettings():
            print(color('SUCCESS: syncing settings.', fore='green', style='bright'))
        else:
            raise Exception("settings sync failed")
    except Exception as e:
        print(color('ERROR: syncing settings. ' + str(e), fore='red', style='bright'))

    try:
        device._processchannels()
        value = device.getchannelvalue("dc_power", True)
        if( value != None ):
            print(color('SUCCESS: processing registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers. ' + str(e), fore='red', style='bright'))

    try:
        value = device.getchannelvalue("seppi", True)
        if( value == None ):
            print(color('SUCCESS: getting value of unkown registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: getting value of unkown registers. ' + str(e), fore='red', style='bright'))

    time.sleep(2)
    device._processchannels()
    time.sleep(2)

    device.readallregisters()
    try:
        device._processchannels()
        value = device.getlogvalue("dc_power")
        if( value != None ):
            print(color('SUCCESS: processing registers again.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers again. ' + str(e), fore='red', style='bright'))

    
    data = device.getdata()
    if(data != None and data != {}):
        print(color('SUCCESS: getting getdata.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting getdata.', fore='red', style='bright'))

    logData = device.getlogdata()
    if(logData != None and logData != {}):
        print(color('SUCCESS: getting getLogData.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting getLogData.', fore='red', style='bright'))

    key = "ww2target"
    targetValue = 55
    try:
        device.setsetupvalue(key, targetValue)
        print(color('SUCCESS: sending setup value to device.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending setup value to device.', fore='red', style='bright'))

    setup = device.getsetup()
    if(setup[key] == targetValue):
        print(color('SUCCESS: Setting setup value.', fore='green', style='bright'))
    else:
        print(color('ERROR: Setting setup value.', fore='red', style='bright'))

    if(device != None):
        try:
            register = device.readregister(1021)
            if register > 0 and register < 900: 
                print(color('SUCCESS: reading register.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading register. Value missmatch: ' + str(register), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading register. Error: ' + str(e), fore='red', style='bright'))

    if(device != None):
        try:
            registers = device.readregisters(1020, 2)
            if registers[1021] !=  0:
                print(color('SUCCESS: reading registers.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading registers. Value missmatch: ' + str(registers), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading registers. Error: ' + str(e), fore='red', style='bright'))
    try:
        device._supervise()
        print(color('SUCCESS: supervising.', fore='green', style='bright'))
    except Exception as e:
            print(color('ERROR: supervising. Error: ' + str(e), fore='red', style='bright'))

    input("Press ENTER to start running tests")
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceDcElwa(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addserverconnection(connection)
    device.start()

    try:
        time.sleep(10)
        while True:
            print(color('[DeviceDcElwa] test active. Press CTRL+C to stop', fore='blue', style='bright'))
            print(device)
            print(device.getinfo())
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DeviceDcElwa] Stopping Test...")
        device.stop()

    input("Press ENTER to start communication tests")

    #DCS communication tests
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceDcElwa(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addserverconnection(connection)

    device2 = DeviceDcElwa(serial2, 2)
    connection2 = DcsConnection(serial2, cryptoKey2, server, 50333)
    device2.addserverconnection(connection2)

    device3 = DeviceDcElwa(serial3, 7)
    connection3 = DcsConnection(serial3, cryptoKey3, server, 50333)
    device3.addserverconnection(connection3)

    device.start()
    device2.start()
    device3.start()
    try:
        while True:
            print(color('[DeviceDcElwa] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            # print(device.getinfo())
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            device2.showcommunicationerrors()
            device2.showcommunicationerrorsrate()
            device3.showcommunicationerrors()
            device3.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
        device2.stop()
        device3.stop()
    input("waiting...")
