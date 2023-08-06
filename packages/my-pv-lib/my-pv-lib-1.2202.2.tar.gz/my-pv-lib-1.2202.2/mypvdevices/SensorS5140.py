#!/usr/bin/python

import logging
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.DeviceConfigurable import DeviceConfigurable
from mypvdevices.ModbusConnection import ModbusConnection

class SensorS5140(ModbusRtuDevice, DeviceConfigurable):

    def __init__(self, unitId):
        super().__init__(unitId)

        self._buscommunicationWaitTime = 10
        self._datamaximumage = 10

        ModbusConnection.instance().setConfiguration(1, 8, 'N', 19200, 0.2, True, True)

# Entry Point     
if __name__ == "__main__":

    import time

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.DEBUG)

    device = SensorS5140(2)
    data = device.getRegisters()
    print("Data: " + str(data))

    device = SensorS5140(1)
    device.readRegisters()
    data = device.getRegisters()
    print("Data: " + str(data))

    device.configureChannel(1, [101], "test", 0)
    config = device.getChannelConfig(1)

    device.configureChannel(2, [102], "test", 0)
    device.configureChannel(3, [103], "test", 0)
    device.configureChannel(5, [100], "test", 0)

    # value1 = device.getChannelValue(1)
    # print("Channel 1: " + str(value1))
    # value2 = device.getChannelValue(2)
    # print("Channel 2: " + str(value2))
    # value3 = device.getChannelValue(3)
    # print("Channel 3: " + str(value3))
    
    # value5 = device.getChannelValue(5)
    # print("Channel 5: " + str(value5))

    # device.configureChannel(9, [100], "NTC", 0)
    # ntcvalue = device.getChannelValue(9)
    # print(ntcvalue)

    device.start()
    time.sleep(5)
    device.stop()
