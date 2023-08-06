#!/usr/bin/python

import logging
# from datetime import datetime
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.ChannelConfig import ChannelConfig
from mypvdevices.ModbusConnection import ModbusConnection

class EastronMeter(ModbusRtuDevice):

    def __init__(self, unitId):
        super().__init__(unitId)

        self._registerStartAddress = 52
        self._registersToRead = 2
        self._readSleepTime = 3
        self._registertype = "input"

        ModbusConnection.instance().setConfiguration(1, 8, 'N', 19200, 0.2, True, True)

        self._channels["power"] = ChannelConfig([52, 53], "FLOAT32", 0)
        # self._channels["total_energy"] = ChannelConfig([342, 343], "FLOAT32", 0)

# Entry Point     
if __name__ == "__main__":

    import time

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

    device = EastronMeter(1)
    device.readallregisters()
    data = device.getregisters()
    print("Data: " + str(data))

    value1 = device.getchannelvalue("power")
    print("Channel 1: " + str(value1))
    # value2 = device.getchannelvalue("total_energy")
    # print("Channel 2: " + str(value2))

    device.start()
    time.sleep(5)
    device.stop()

    value1 = device.getchannelvalue("power")
    print("Channel 1: " + str(value1))
    # value2 = device.getchannelvalue("total_energy")
    # print("Channel 2: " + str(value2))
