#!/usr/bin/python

import logging
import threading
import time
from datetime import datetime
# import statistics
import sys
import os
import random

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.GeneralDevice import GeneralDevice
from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.ModbusTcpDevice import ModbusTcpDevice
from mypvdevices.ChannelConfig import ChannelConfig

class DummyDevice(ModbusTcpDevice):

    def __init__(self, identity, ip, port):
        super().__init__(identity, ip, port)

        self._channels["power"] = ChannelConfig([1001], "UINT16", 0, "rw")
        self._channels["temp1"] = ChannelConfig([1002], "UINT16", 0.1)


# Entry Point     
if __name__ == "__main__":

    # from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    serial = "1530693"

    device = DummyDevice(serial, None, 502)
    device.connect()
    # device.readregister(100)
    # device.readregister(200, "input")
    # device.readregisters(100, 4)
    # device.readregisters(100, 4, "input")
    device.readallregisters()
    registers = device.getregisters()
    print(registers)
    value = device.getregistervalue(100)
    print(value)
    # device.writeregister(100, 22)
    # device.writeregisters(100, [1,2]) # multiple registers and multiple values
    config = device.getchannelconfig("power")
    list = device.getchannellist()
    # power = device.getchannelvalue("power")
    device.setchannelvalue("power", 300)
