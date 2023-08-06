#!/usr/bin/python

import logging
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.GeneralDevice import GeneralDevice
from mypvdevices.ChannelConfig import ChannelConfig

class DeviceConfigurable(GeneralDevice):

    def configureChannel(self, channel, registerNumbers, type, scale, mode = "r"):
        '''Configures a channel
        :param channel: Channel name
        :type channel: int, str
        :raises: :class:`TypeError`: Invalid type of param'''

        if channel == None:
            raise TypeError("Channel cannot be None")

        if not isinstance(channel, int) and not isinstance(channel, str):
            raise TypeError("Channel has to be int or string")

        self._channels[channel] = ChannelConfig(registerNumbers, type, scale, mode)

# Entry Point     
if __name__ == "__main__":

    import time

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.DEBUG)

    device = DeviceConfigurable()
    device.readRegisters()
    data = device.getRegisters()
    print("Data: " + str(data))

    device.configureChannel(1, [100], "test", 0)
    device.configureChannel(2, [101], "test", 0)
    device.configureChannel("power", [101], "test", 0, "rw")
    device.configureChannel("power2", [101, 102], "UINT32", 0, "rw")

    print(device)
    list = device.getChannelList()

    value1 = device.getChannelValue(1)
    print("Channel 1: " + str(value1))
    value2 = device.getChannelValue(2)
    print("Channel 2: " + str(value2))

    device.setChannelValue("power2", 10)
    device.setChannelValue("power", 10)

    device.start()
    time.sleep(5)
    device.stop()

    device = DeviceConfigurable()
    print(device)
    data = device.getRegisters()
    print("Data: " + str(data))

    device = DeviceConfigurable()
    device.readRegisters()
    registerValue = device.getRegisterValue(100)
    data = device.getRegisters()
    print("Data: " + str(data))

    device.configureChannel(1, [101], "NTC", 0)
    config = device.getChannelConfig(1)

    device.configureChannel(2, [102], "POTI", 0)
    device.configureChannel(3, [103], "temperature", 0)

    device.configureChannel("power", [101], "test", 0)
    config = device.getChannelConfig("power")

    value1 = device.getChannelValue(1)
    print("Channel 1: " + str(value1))
    value2 = device.getChannelValue(2)
    print("Channel 2: " + str(value2))
    value3 = device.getChannelValue(3)
    print("Channel 3: " + str(value3))

    power = device.getChannelValue("power")
    print("Channel power: " + str(power))

    device.configureChannel(9, [100], "NTC", 0)
    ntcvalue = device.getChannelValue(9)
    print(ntcvalue)

    device.start()
    time.sleep(10)
    device.stop()

    print(device)

    device.start()
    time.sleep(10)
    device.start()
    time.sleep(10)
    device.stop()
    time.sleep(10)
    device.stop()
    time.sleep(4)

