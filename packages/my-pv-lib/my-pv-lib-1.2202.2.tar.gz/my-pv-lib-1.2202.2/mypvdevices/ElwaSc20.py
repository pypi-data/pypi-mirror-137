#!/usr/bin/python

import logging
import sys
import os
import json
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.SerialDevice import SerialDevice
from mypvdevices.ChannelConfig import ChannelConfig
from mypvdevices.SetupMapping import SetupMapping

SERIALLEN = 16
ACTEMPMINIMUMVALUE = 5
ACTEMPMAXIMUMVALUE = 99

class ElwaSc20(SerialDevice):

    _serial = None
    _devicesubtype = "ELWA-USB"
    _deviceBoostpower = 750
    _oldacdaywh = None
    _oldacdaywhlog = None

    def __init__(self, serialnumber):

        if serialnumber != None and len(serialnumber) == SERIALLEN:
            self._serial = serialnumber
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serialnumber)
            logging.error(errmsg)
            raise ValueError(errmsg)

        super().__init__()

        self._name = self.__class__.__name__ + " " + str(self._serial)
        self._interfaceidentifiers = ["RS485", "FT230X"]
        self._baudrate = 9600
        self._bytesize = 8
        self._stopbits = 1
        self._parity = "N"
        self._timeout = 3
        self._seperator = '\\t'
        self._requestcommand = 'rs\r\n'.encode('utf-8')

        if self._serial[:6] == "120300":
            self._devicesubtype = "SC20"
            self._deviceBoostpower = 2000

        self._buscommunicationWaitTime = 5
        self._datamaximumage = 90

        self._channels["fw_version"] = ChannelConfig([0], None, 0, registertype="serial")
        self._channels["day_counter"] = ChannelConfig([1], "NUMBER", 0, registertype="serial")
        self._channels["operation_mode"] = ChannelConfig([2], "NUMBER", 0, registertype="serial")
        self._channels["dc_breaker_state"] = ChannelConfig([3], "NUMBER", 0, registertype="serial")
        self._channels["dc_relay_state"] = ChannelConfig([4], "NUMBER", 0, registertype="serial")
        self._channels["ac_relay_state"] = ChannelConfig([5], "NUMBER", 0, registertype="serial", datasettype="sum")
        self._channels["water_temp"] = ChannelConfig([6], "NUMBER", 0.1, registertype="serial",  datasettype="avg")
        self._channels["temp_day_min"] = ChannelConfig([7], "NUMBER", 0.1, registertype="serial")
        self._channels["temp_day_max"] = ChannelConfig([8], "NUMBER", 0.1, registertype="serial")
        self._channels["dc_temp_target"] = ChannelConfig([9], "NUMBER", 0.1, registertype="serial")
        self._channels["ac_temp_target"] = ChannelConfig([10], "NUMBER", 0.1, registertype="serial", mode="rw")
        self._channels["tempchip"] = ChannelConfig([11], "NUMBER", 0, registertype="serial")
        self._channels["iso_voltage"] = ChannelConfig([12], "NUMBER", 0, registertype="serial")
        self._channels["internal_mpp_value"] = ChannelConfig([13], "NUMBER", 0, registertype="serial")
        self._channels["dc_voltage"] = ChannelConfig([14], "NUMBER", 0, registertype="serial")
        self._channels["dc_current"] = ChannelConfig([15], "NUMBER", 0, registertype="serial")
        self._channels["dc_power"] = ChannelConfig([16], "NUMBER", 0, registertype="serial", datasettype="sum")
        self._channels["dc_day_wh"] = ChannelConfig([17], "NUMBER", 0, registertype="serial")
        self._channels["dc_total_kwh"] = ChannelConfig([18], "NUMBER", 0.001, registertype="serial")
        self._channels["ac_day_wh"] = ChannelConfig([19], "NUMBER", 0, registertype="serial", datasettype="avg")
        self._channels["internal_control_value_1"] = ChannelConfig([20], "NUMBER", 0, registertype="serial")
        self._channels["internal_control_value_2"] = ChannelConfig([21], "NUMBER", 0, registertype="serial")
        self._channels["internal_control_value_3"] = ChannelConfig([22], "NUMBER", 0, registertype="serial")
        self._channels["internal_clock"] = ChannelConfig([23], "NUMBER", 0, registertype="serial")
        self._channels["minutes_since_wakeup"] = ChannelConfig([24], "NUMBER", 0, registertype="serial")
        self._channels["ac_boost_mode"] = ChannelConfig([25], "NUMBER", 0, registertype="serial", mode="rw") # ac switch on time. 0: temperature controlled
        self._channels["is_master_device"] = ChannelConfig([26], "NUMBER", 0, registertype="serial")
        self._channels["serial"] = ChannelConfig([27], None, 0, registertype="serial", mode="rw")
        self._channels["pot_position"] = ChannelConfig([28], "NUMBER", 0, registertype="serial")
        self._channels["useacboost"] = ChannelConfig([30], "NUMBER", 0, registertype="serial", mode="rw", datasettype="avg")

        self._setup["fwversion"] = SetupMapping(defaultvalue=self._firmwareversion) #required to find write configuration in cloud
        self._setup["device"] = SetupMapping(defaultvalue=self._devicesubtype)
        self._setup["firmware"] = SetupMapping("fw_version")
        self._setup["libversion"] = SetupMapping(defaultvalue=self._firmwareversion)
        self._setup["serialno"] = SetupMapping(defaultvalue=self._serial)
        self._setup["ww1boost"] = SetupMapping("ac_temp_target")
        self._setup["booststarttime"] = SetupMapping("ac_boost_mode")     #time when we start to boost in minutes after 
        self._setup["useacboost"] = SetupMapping("useacboost")

    def _checkid(self, portname):
        try:
            self._commport.port = portname
            self._commport.open()
            connected_serial = self._readregister(27, "serial")
        except Exception as e:
            connected_serial = None

        self._commport.close()
        self._commport.port = None

        if connected_serial and connected_serial == self._serial:
            return True
        return False

    def _lookupcommand(self, registerId):
        if registerId == 10:
            return "sact"
        if registerId == 27:
            return "ssn"
        elif registerId == 25:
            return "acmode"
        else:
            raise Exception("invalid register id: " + str(registerId))

    def _readserialdata(self):
        data = super()._readserialdata()
        serial = list(data[27])
        acmode = serial[2]
        serial[2] = "0"
        serialfixed = "".join(serial)
        data[27] = serialfixed
        data.append(acmode)
        return data

    def _writeserialdata(self, registerId, data):
        if registerId == 30:
            # if not isinstance(data, bool):
            if data != 0 and data != 1:
                raise Exception("invalid value for register 30")
            registerId = 27
            serial = list(self._serial)
            serial[2] = str(data)
            data = "".join(serial)
        super()._writeserialdata(registerId, data)

    def getdata(self):
        acRelayState = self.getchannelvalue("ac_relay_state", True)
        dcPower = self.getchannelvalue("dc_power", True)
        operationMode = self.getchannelvalue("operation_mode", True)
        useacboost = self.getchannelvalue("useacboost", True)

        if operationMode == 3 or operationMode == 5 or operationMode == 6 or operationMode == 7 or operationMode == 8 or operationMode == 9 or operationMode == 10 or operationMode == 11 or operationMode == 12 or operationMode == 13 or operationMode == 14 or operationMode == 15 or operationMode == 16 or operationMode == 20 or operationMode == 21 or operationMode == 135:
            acHeating = True
        else:
            acHeating = False

        if acRelayState != None:
            if acHeating == True and acRelayState == 1 and useacboost == 1:
                boostpower = self._deviceBoostpower
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

        # if self._errorcode != 0:
        #     errorcode = self._errorcode
        # else:
        #     errorcode = None

        errorrate = self.getcommunicationerrorsrate()

        data={
            "fwversion": self._firmwareversion,
            "loctime": time.strftime("%H:%M:%S"),
            "day_counter" : self.getchannelvalue("day_counter", True),
            "op_mode": operationMode,
            "dc_breaker": self.getchannelvalue("dc_breaker_state", True),
            "dc_relay": self.getchannelvalue("dc_relay_state", True),
            "ac_boost": acRelayState,
            "temp1": self.getchannelvalue("water_temp", True, 10),
            "temp_day_min": self.getchannelvalue("temp_day_min", True, 10),
            "temp_day_max": self.getchannelvalue("temp_day_max", True, 10),
            "ww1target": self.getchannelvalue("dc_temp_target", True, 10),
            "ac_temp_target": self.getchannelvalue("ac_temp_target", True, 10),
            "tempchip": self.getchannelvalue("tempchip", True),
            "iso_voltage": self.getchannelvalue("iso_voltage", True),
            "dc_voltage": self.getchannelvalue("dc_voltage", True, 10),
            "dc_current": self.getchannelvalue("dc_current", True, 1000),
            "boostpower_sc20": boostpower,
            "dc_day_wh": self.getchannelvalue("dc_day_wh", True),
            "dc_total_kwh": self.getchannelvalue("dc_total_kwh", True),
            "ac_day_wh": self.getchannelvalue("ac_day_wh", True),
            # "ac_boost_mode": self.getchannelvalue("ac_boost_mode", True),
            "m1sum": dcPower,
            # "m0sum": meter,
            "buserrorrate":  errorrate
            # "errorcode_elwa": errorcode
        }
        if self._devicesubtype == "SC20":
            # data["power_sc20"] = power
            data["device"] =  "SC20"
        else:
            # data["power_elwa"] = power
            data["device"] =  "ELWA-USB"
        return data

    def getlogdata(self, time = None):
        acRelayState = self.getlogvalue("ac_relay_state")
        useacboost = self.getlogvalue("useacboost")

        if acRelayState != None and useacboost != None and useacboost >= 0.5:
            boostpower = int(round(acRelayState * self._deviceBoostpower))
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

        # sLog = {}

        logData = {
            "time": time,
            # "i_power": power,
            # "i_boostpower": boostpower,
            "i_m1sum": pvprod,
            # "i_metercons": metercons,
            "i_temp1": self.getlogvalue("water_temp", "int", 10)
            # "s_json" : json.dumps(sLog)
        }

        return logData

    def _checksumcheck(self, response_string, receivedchecksum):
        checksum = 0
        lasttab = response_string.rfind('\\t')
        payloadstring = response_string[2:lasttab+2]
        for c in payloadstring:
            if c == '\\':
                value = 9
                checksum += value
            elif c == 't':
                pass
            else:
                value = ord(c)
                checksum += value
        checksum = checksum % 256

        if receivedchecksum != checksum:
            raise Exception("Checksum missmatch.")

    def _supervise(self):
        super()._supervise()
        self._sethealthstate(0) # Todo

# Entry Point     
if __name__ == "__main__":

    from colr import color
    import time
    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    #device connection tests
    serialnr = "1203002111190000"
    cryptoKey = "0102030405060708090a0b0c0d0e0f00"
    dcsserial = "120100200505tes1"
    dcscryptokey = "41424142414241424142414241424142"
    server = "my-pv.live"

    device = ElwaSc20(serialnr)
    # device.readallregisters()
    # print(device)
    # useacboost = device.getchannelvalue("useacboost")
    
    # device.writeregister(30, 1)
    # device.readallregisters()
    # print(device)
    device.setsetupvalue("useacboost", 1)
    # device.readallregisters()
    # print(device)
    # device.setsetupvalue("useacboost", 0)
    # device.readallregisters()
    # print(device)
    # print()

    # device.writeregister(10, 532)
    # device.writeregister(27, "1203002111190000")
    # device.writeregister(25, 200)
    # device.readallregisters()
    # print(device)

    # device.readallregisters()
    # print(device)
    # print(device.readregister(27, registertype='serial'))
    # print(device.readregisters(27, 2, registertype='serial'))
    # print(device)
    # try:
    #     device.writeregister(10, 532)
    # except Exception as e:
    #     print(e)
    # device.readallregisters()
    # print(device)

    # device.setsetupvalue("ww1boost", 50)
    # device.readallregisters()
    # print(device)

    # try:
    #     device.writeregister(25, 200)
    # except Exception as e:
    #     print(e)
    # device.readallregisters()
    # print(device)

    # try:
    #     device.writeregister(27, "1203002111190000")
    # except Exception as e:
    #     print(e)
    # device.readallregisters()
    # print(device)

    # print()

    # device.setsetupvalue("booststarttime", 205)
    # device.readallregisters()
    # print(device)
    # print()

    # device2 = ElwaSc20("1201061912110002")
    # device.readallregisters()
    # device2.readallregisters()
    # print(device)
    # print(device2)
    # print()
    # device = ElwaSc20(serialnr)
    # device._connect()
    # device._connect()
    # device.readallregisters()
    # print(device)

    # device = ElwaSc20(serialnr)
    # device.readallregisters()
    # print(device)

    # device = ElwaSc20(serialnr)
    # setup = device.getsetup()
    # print(setup)
    # device.setsetupvalue("ww1boost", 43)
    # setup = device.getsetup()
    # print(setup)
    # device.setsetupvalue("test", 55)
    # setup = device.getsetup()
    # print(setup)

    # device = ElwaSc20(serialnr)
    # device.readallregisters()
    # device._syncsettings()
    # device._syncsettings()
    # print(device.getsetup())
    
    # register = device.readregisters(0, 30, "serial")
    # print(register)
    
    # device.writeregister(10, 50)

    # device.readallregisters()
    # print(device)

    # print("serial: " + str(device.getchannelvalue("serial")))
    # print("water_temp: " + str(device.getchannelvalue("water_temp")))

    # print("ac_temp_setting: " + str(device.getchannelvalue("ac_temp_target")))
    # device.setchannelvalue("ac_temp_setting", 45)
    # print("ac_temp_setting: " + str(device.getchannelvalue("ac_temp_target")))

    # counter = device.getcommunicationerrorscounter()
    # rate = device.getcommunicationerrorsrate()
    # device.resetcounters()

    # try:
    #     register = device.readregister(27, "serial")
    # except:
    #     pass
    # counter = device.getcommunicationerrorscounter()
    # rate = device.getcommunicationerrorsrate()

    # register = device.readregisters(1, 20, "serial")
    # counter = device.getcommunicationerrorscounter()
    # rate = device.getcommunicationerrorsrate()

    # register = device.readregister(27, "serial")
    # print(register)

    # register = device.readregister(27, "serial")
    # print(register)

    # try:
    #     register = device.readregister(500, "serial")
    #     print(register)
    # except Exception as e:
    #     print("should raise an exception because of invalid id: " + str(e))

    # registers = device.readregisters(5, 20, "serial")
    # print(registers)

    # try:
    #     registers = device.readregisters(1, 100, "serial")
    #     print(register)
    # except Exception as e:
    #     print("should raise an exception because of invalid id: " + str(e))

    # device.readallregisters()

    # print(device)

    # #AUTO-Tests
    # try:
    #     device = ElwaSc20("test")
    #     print(color('ERROR: creating invalid device.', fore='red', style='bright'))
    # except:
    #     print(color('SUCCESS: creating invalid device.', fore='green', style='bright'))

    # try:
    #     device = ElwaSc20("test")
    #     print(color('ERROR: creating invalid device - none.', fore='red', style='bright'))
    # except:
    #     print(color('SUCCESS: creating invalid device - none.', fore='green', style='bright'))

    # try:
    #     device = ElwaSc20(serialnr)
    #     print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
    # except:
    #     print(color('ERROR: creating valid device.', fore='red', style='bright'))

    # try:
    #     device._connect()
    #     print(color('SUCCESS: connecting device.', fore='green', style='bright'))
    # except Exception as e:
    #     print(color('ERROR: connecting device.', fore='red', style='bright'))

    # try:
    #     device.readallregisters()
    #     print(color('SUCCESS: reading registers.', fore='green', style='bright'))
    # except:
    #     print(color('ERROR: reading registers.', fore='red', style='bright'))

    # try:
    #     setup = device.getsetup()
    #     if(setup == None):
    #         raise Exception("Setup is None")
    #     print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
    # except Exception as e:
    #     print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

    # try:
    #     data = device.getdata()
    #     if(data == None):
    #         raise Exception("Data is None")
    #     print(color('SUCCESS: getting device data.', fore='green', style='bright'))
    # except Exception as e:
    #     print(color('ERROR: getting device data.', fore='red', style='bright'))

    # try:
    #     logdata = device.getlogdata()
    #     if(logdata == None):
    #         raise Exception("logdata is None")
    #     print(color('SUCCESS: getting device logdata.', fore='green', style='bright'))
    # except:
    #     print(color('ERROR: getting device logdata.', fore='red', style='bright'))

    # try:
    #     device.stop()
    #     print(color('SUCCESS: stopping device before start.', fore='green', style='bright'))
    # except:
    #     print(color('ERROR: stopping device before start.', fore='red', style='bright'))

    # try:
    #     temp = device.getstate()
    #     if(temp == False):
    #         print(color('SUCCESS: getting device state (before start).', fore='green', style='bright'))
    #     else:
    #         raise Exception("device state is not stopped.")
    # except:
    #     print(color('ERROR: getting device state (before start).', fore='red', style='bright'))

    # try:
    #     temp = device.getdevicetype()
    #     if(temp == "ElwaSc20"):
    #         print(color('SUCCESS: getting device type.', fore='green', style='bright'))
    #     else:
    #         raise Exception("device type does not match.")
    # except:
    #     print(color('ERROR: getting device type.', fore='red', style='bright'))

    # try:
    #     device.readallregisters()
    #     print(color('SUCCESS: reading registers.', fore='green', style='bright'))
    # except:
    #     print(color('ERROR: reading registers.', fore='red', style='bright'))

    #DCS communication tests
    device = ElwaSc20(serialnr)
    # device = ElwaSc20("1201061912110002")
    connection = DcsConnection(dcsserial, dcscryptokey, server, 50333)
    device.addserverconnection(connection)
    device.start()
    try:
        while True:
            print(color('[SerialDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            print(device)
            print(device.getinfo())
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            logdata = device.getlogdata()
            print(logdata)
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
    input("waiting...  PRESS ENTER")