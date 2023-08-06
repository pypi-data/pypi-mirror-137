#!/usr/bin/python

# from datetime import datetime, timedelta
import logging
import time
import json
import sys
import os
from datetime import datetime

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.ChannelConfig import ChannelConfig


SERIALLEN = 16

class MyDevice(ModbusRtuDevice):
    _serial = None

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

        # ModbusConnection.instance().setConfiguration(1, 8, 'N', 9600, 0.2, True, True)

        self._channels["day_counter"] = ChannelConfig([1000], "UINT16", 0, "r", datasettype="avg")
        self._channels["operation_mode"] = ChannelConfig([1001], "UINT16", 0, "r", datasettype="avg")
        self._channels["dc_breaker_state"] = ChannelConfig([1002], "UINT16", 0, "r", datasettype="sum")
       

    def _specialProcessingRead(self, channel, value):
        return value

    def _specialProcessingWrite(self, channel, value):
        return value
    
    def getdata(self):
        t = datetime.now()
        data = {
                "fwversion": self._firmwareversion,
				"power": t.second * 100,
                "temp1": t.minute,
                "check": 9544,
                "temp2": self.getchannelvalue("temp2", True),
				"loctime": time.strftime("%H:%M:%S")
                }            
        return data

    def getlogdata(self, time = None):
        logdata = {
            # "i_unknown": 123,
            "time": time,
            "i_power": self.getlogvalue("power", "int"),
            "i_boostpower": 750,
            "i_meterfeed": None,
            "i_metercons": 4,
            "i_temp1": self.getlogvalue("temp1", "int"),
            "i_m0l1": 6,
            "i_m0l2": 7,
            "i_m0l3": 8,
            "i_m1sum": 9,
            "i_m1l1": 10,
            "i_m1l2": 11,
            "i_m1l3": 12,
            "i_m2sum": 13,
            "i_m2l1": 14,
            "i_m2l2": 15,
            "i_m2l3": 16,
            "i_m2soc": 17,
            "i_m3sum": 18,
            "i_m3l1": 19,
            "i_m3l2": 20,
            "i_m3l3": 21,
            "i_m3soc": 22,
            "i_m4sum": 23,
            "i_m4l1": 24,
            "i_m4l2": 25,
            "i_m4l3": 26,
            "s_json" : "27",
            "i_temp2": self.getlogvalue("temp2", "int"),
            "i_power1": 29,
            "i_power2": 30,
            "i_power3": 31,
            "i_temp3": 32,
            "i_temp4": 33
            }
        return logdata

    def _supervise(self):
        pass

# # Entry Point     
# if __name__ == "__main__":

#     from colr import color
#     from DcsConnection import DcsConnection

#     logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

#     serial = "120100200505tes1"
#     cryptoKey = "41424142414241424142414241424142"
#     serial2 = "120100200505tes2"
#     cryptoKey2 = "41424142414241424142414241424142"
#     serial3 = "120100200505tes3"
#     cryptoKey3 = "41424142414241424142414241424142"
#     server = "my-pv.live"

#     try:
#         device = DeviceDcElwa("123456789", 1)
#         print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
#     except:
#         print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))
#         device = None
