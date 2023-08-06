#!/usr/bin/python

# from datetime import datetime, timedelta
import logging
import sys
import os
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusTcpDevice import ModbusTcpDevice
from mypvdevices.ChannelConfig import ChannelConfig

SERIALLEN = 16

class DeviceAcThor(ModbusTcpDevice):
    _serial = None

    def __init__(self, serial, statichost = None):
        if serial != None and len(serial) == SERIALLEN:
            self._serial = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)

        super().__init__(serial, statichost, 502, 1)

        self._name = self._name + " " + str(self._serial)
        self._buscommunicationWaitTime = 10
        self._datamaximumage = 60

        self._channels["power"] = ChannelConfig([1000], "UINT16", 0, "rw")
        self._channels["temp1"] = ChannelConfig([1001], "UINT16", 0.1)
        self._channels["WW1TempMax"] = ChannelConfig([1002], "UINT16", 0.1, "rw")
        self._channels["status"] = ChannelConfig([1003], "UINT16", 0)
        self._channels["WW1Min"] = ChannelConfig([1006], "UINT16", 0.1)
        self._channels["boostactive"] = ChannelConfig([1012], "UINT16", 0, "rw")
        self._channels["tempchip"] = ChannelConfig([1015], "UINT16", 0.1)
        self._channels["temp2"] = ChannelConfig([1030], "UINT16", 0.1)
        self._channels["temp3"] = ChannelConfig([1031], "UINT16", 0.1)
        self._channels["temp4"] = ChannelConfig([1032], "UINT16", 0.1)
        self._channels["temp5"] = ChannelConfig([1033], "UINT16", 0.1)
        self._channels["temp6"] = ChannelConfig([1034], "UINT16", 0.1)
        self._channels["temp7"] = ChannelConfig([1035], "UINT16", 0.1)
        self._channels["temp8"] = ChannelConfig([1036], "UINT16", 0.1)
        self._channels["Relay1Status"] = ChannelConfig([1058], "UINT16", 0)
        self._channels["loadstate"] = ChannelConfig([1059], "UINT16", 0.1)     #loadstate aller 3 Ausgänge
        self._channels["loadnominalpower"] = ChannelConfig([1060], "UINT16", 0)
        self._channels["power1"] = ChannelConfig([1074], "UINT16", 0)     #Power Ausgang 1
        self._channels["power2"] = ChannelConfig([1075], "UINT16", 0)     #Power Ausgang 2
        self._channels["power3"] = ChannelConfig([1076], "UINT16", 0)     #Power Ausgang 3
        self._channels["powerRelays"] = ChannelConfig([1080], "UINT16", 0, "rw")     #Power + relays

    # def _getregistermapping(self):
    #     datasets = {}
    #     datasets["power"] = self._createDataset(1000, "sum")
    #     datasets["temp1"] = self._createDataset(1001, "avg")
    #     datasets["ww1_temp_max"] = self._createDataset(1002, "avg")
    #     datasets["status"] = self._createDataset(1003, "avg")
    #     datasets["power_timeout"] = self._createDataset(1004, "avg")
    #     datasets["boost_mode"] = self._createDataset(1005, "avg")
    #     datasets["ww1_temp_min"] = self._createDataset(1006, "avg")
    #     datasets["boost_time_1_start"] = self._createDataset(1007, "avg")
    #     datasets["boost_time_1_stop"] = self._createDataset(1008, "avg")
    #     datasets["hour"] = self._createDataset(1009, "avg")
    #     datasets["minute"] = self._createDataset(1010, "avg")
    #     datasets["second"] = self._createDataset(1011, "avg")
    #     datasets["boost_activate"] = self._createDataset(1012, "avg")
    #     datasets["acthor_nummber"] = self._createDataset(1013, "avg")
    #     datasets["power_max"] = self._createDataset(1014, "sum")
    #     datasets["temp_chip"] = self._createDataset(1015, "avg")
    #     datasets["control_fw_version"] = self._createDataset(1016, "avg")
    #     datasets["ps_fw_version"] = self._createDataset(1017, "avg")
    #     datasets["acthor_serial_p1"] = self._createDataset(1018, "avg")
    #     datasets["acthor_serial_p2"] = self._createDataset(1019, "avg")
    #     datasets["acthor_serial_p3"] = self._createDataset(1020, "avg")
    #     datasets["acthor_serial_p4"] = self._createDataset(1021, "avg")
    #     datasets["acthor_serial_p5"] = self._createDataset(1022, "avg")
    #     datasets["acthor_serial_p6"] = self._createDataset(1023, "avg")
    #     datasets["acthor_serial_p7"] = self._createDataset(1024, "avg")
    #     datasets["acthor_serial_p8"] = self._createDataset(1025, "avg")
    #     datasets["boost_time_2_start"] = self._createDataset(1026, "avg")
    #     datasets["boost_time_2_stop"] = self._createDataset(1027, "avg")
    #     datasets["control_fw_subversion"] = self._createDataset(1028, "avg")
    #     datasets["control_fw_update_available"] = self._createDataset(1029, "avg")
    #     datasets["temp2"] = self._createDataset(1030, "avg")
    #     datasets["temp3"] = self._createDataset(1031, "avg")
    #     datasets["temp4"] = self._createDataset(1032, "avg")
    #     datasets["temp5"] = self._createDataset(1033, "avg")
    #     datasets["temp6"] = self._createDataset(1034, "avg")
    #     datasets["temp7"] = self._createDataset(1035, "avg")
    #     datasets["temp8"] = self._createDataset(1036, "avg")
    #     datasets["ww2_max"] = self._createDataset(1037, "avg")
    #     datasets["ww3_max"] = self._createDataset(1038, "avg")
    #     datasets["ww2_min"] = self._createDataset(1039, "avg")
    #     datasets["ww3_min"] = self._createDataset(1040, "avg")
    #     datasets["rh1_max"] = self._createDataset(1041, "avg")
    #     datasets["rh2_max"] = self._createDataset(1042, "avg")
    #     datasets["rh3_max"] = self._createDataset(1043, "avg")
    #     datasets["rh1_day_min"] = self._createDataset(1044, "avg")
    #     datasets["rh2_day_min"] = self._createDataset(1045, "avg")
    #     datasets["rh3_day_min"] = self._createDataset(1046, "avg")
    #     datasets["rh1_night_min"] = self._createDataset(1047, "avg")
    #     datasets["rh2_night_min"] = self._createDataset(1048, "avg")
    #     datasets["rh3_night_min"] = self._createDataset(1049, "avg")
    #     datasets["night_flag"] = self._createDataset(1050, "avg")
    #     datasets["utc_correction"] = self._createDataset(1051, "avg")
    #     datasets["dst_correction"] = self._createDataset(1052, "avg")
    #     datasets["legionella_interval"] = self._createDataset(1053, "avg")
    #     datasets["legionella_start"] = self._createDataset(1054, "avg")
    #     datasets["legionella_temp"] = self._createDataset(1055, "avg")
    #     datasets["legionella _mode"] = self._createDataset(1056, "avg")
    #     datasets["stratification_flag"] = self._createDataset(1057, "avg")
    #     datasets["relay1_state"] = self._createDataset(1058, "avg")
    #     datasets["load_state"] = self._createDataset(1059, "avg")
    #     datasets["load_nominal_power"] = self._createDataset(1060, "avg")
    #     datasets["u_l1"] = self._createDataset(1061, "avg")
    #     datasets["i_li"] = self._createDataset(1062, "avg")
    #     datasets["u_out"] = self._createDataset(1063, "avg")
    #     datasets["frequ"] = self._createDataset(1064, "avg")
    #     datasets["operation_mode"] = self._createDataset(1065, "avg")
    #     datasets["access_level"] = self._createDataset(1066, "avg")
    #     datasets["u_l2"] = self._createDataset(1067, "avg")
    #     datasets["i_l2"] = self._createDataset(1068, "avg")
    #     datasets["meter_power"] = self._createDataset(1069, "avg")
    #     datasets["control_type"] = self._createDataset(1070, "avg")
    #     datasets["power_max_abs"] = self._createDataset(1071, "avg")
    #     datasets["u_l3"] = self._createDataset(1072, "avg")
    #     datasets["i_l3"] = self._createDataset(1073, "avg")
    #     datasets["power_out_1"] = self._createDataset(1074, "avg")
    #     datasets["power_out_2"] = self._createDataset(1075, "avg")
    #     datasets["power_out_3"] = self._createDataset(1076, "avg")
    #     datasets["operation_state"] = self._createDataset(1077, "avg")
    #     datasets["power_high_word"] = self._createDataset(1078, "avg")
    #     datasets["power_low_word"] = self._createDataset(1079, "avg")
    #     datasets["power_plus_relays"] = self._createDataset(1080, "avg")
    #     return datasets

    def _createsetup(self):
        return {
            "device": self.getdevicetype(), \
            "fwversion": self._firmwareversion, \
            "serialno": self._serial, \
            "ww1_max": None, \
            "ww1_min": 100
            }

    def _getsettingsmap(self):
        settings = {
            "ww1_max": {
                "register": 1002,
                "forced": False
            },
        }
        return settings

    def getdata(self):

        data={
            "device": self.getdevicetype(),
            "fwversion": self._firmwareversion,
            "loctime": time.strftime("%H:%M:%S")
        }       
        return data

    def getlogdata(self, time = None):

        logdata={
            "time": time,
            "device": self.getdevicetype(),
            "fwversion": self._firmwareversion
        }       
        return logdata

    def _supervise(self):
        logging.debug("Supervision running... (Needs to be implemented)")    
    

# Entry Point     
if __name__ == "__main__":

    from colr import color

    # from mypvdevices.DeviceAcThor import DeviceAcThor
    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.DEBUG)

    serial = "2001002006100016"
    serial_fake = "2001005006100000"
    correctip = "192.168.92.29"

    #device connection tests
    dcsserial = "120100200505tes1"
    cryptoKey = "41424142414241424142414241424142"
    server = "my-pv.live"

    # try to read from valid device
    device = DeviceAcThor(serial, correctip)
    try:
        device.readallregisters()
        if(len(device._registers) == 81):
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
        value = device.getchannelvalue("power")
        if( value != None ):
            print(color('SUCCESS: processing registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers. ' + str(e), fore='red', style='bright'))

    try:
        value = device.getchannelvalue("seppi")
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
        value = device.getlogvalue("power")
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

    key = "ww1_max"
    targetValue = 50
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
            register = device.readregister(1015)
            if register > 0 and register < 900: 
                print(color('SUCCESS: reading register.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading register. Value missmatch: ' + str(register), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading register. Error: ' + str(e), fore='red', style='bright'))

    if(device != None):
        try:
            registers = device.readregisters(1000, 10)
            if registers[1001] !=  0 and registers[1006] != 0:
                print(color('SUCCESS: reading registers.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading registers. Value missmatch: ' + str(registers), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading registers. Error: ' + str(e), fore='red', style='bright'))


    # input("Press ENTER to start running tests")
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceAcThor(serial)
    connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
    device.addserverconnection(connection)
    device.start()

    try:
        while True:
            print(color('[DeviceAcThor] test active. Press CTRL+C to stop', fore='blue', style='bright'))
            print(device.getinfo())
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            device._supervise()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DeviceAcThor] Stopping Test...")
        device.stop()

    input("Press ENTER to start communication tests")

    #DCS communication tests
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceAcThor(serial, correctip)
    connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
    device.addserverconnection(connection)

    # device2 = DeviceAcThor(serial2, 2)
    # connection2 = DcsConnection(serial2, cryptoKey2, server, 50333)
    # device2.addserverconnection(connection2)

    # device3 = DeviceAcThor(serial3, 7)
    # connection3 = DcsConnection(serial3, cryptoKey3, server, 50333)
    # device3.addserverconnection(connection3)

    device.start()
    # device2.start()
    # device3.start()
    try:
        while True:
            print(color('[DeviceAcThor] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            # print(device.getinfo())
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            # device2.showcommunicationerrors()
            # device2.showcommunicationerrorsrate()
            # device3.showcommunicationerrors()
            # device3.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
        # device2.stop()
        # device3.stop()
    input("waiting...")