#!/usr/bin/python

import logging
import threading
import time
from datetime import datetime
# import statistics
from colr import color
import sys
import os
import random

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from GeneralDevice import GeneralDevice
from ModbusRtuDevice import ModbusRtuDevice
from ModbusTcpDevice import ModbusTcpDevice
from ChannelConfig import ChannelConfig

class DummyDevice(ModbusRtuDevice):

    def __init__(self, serial):
        super().__init__(1)

        self._channels["power"] = ChannelConfig([1001], "UINT16", 0, "rw", datasettype="avg")
        self._channels["temp1"] = ChannelConfig([1002], "UINT16", 0.1, datasettype="sum")

    def _createsetup(self):
        return {
            "device": self.getdevicetype(), \
            "fwversion": self._firmwareversion, \
            "elno": self._unit, \
            "ww2target": None, \
            "ww2offset": 1514
            }

    def _readregister(self, registerId, registertype):
        return 23

    def _readregisters(self, startregisteraddress, registerstoread, registertype):
        result = dict()
        result[startregisteraddress] = 567
        return result

    def _writeregister(self, registerId, valueToWrite):
        logging.debug(str(self._name) + " writing register " + str(registerId) + " value: " + str(valueToWrite))
        self._registers[registerId] = valueToWrite

    def _writeregisters(self, registerStartId, dataToWrite):
        logging.debug(str(self._name) + " writing register " + str(registerStartId) + " value: " + str(dataToWrite))
        self._registers[registerStartId] = dataToWrite[0]


# Entry Point     
if __name__ == "__main__":

    # from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    serial = "120100200505tes1"

    device = DummyDevice(serial)

    device.readallregisters()
    device._processchannels()

    register = device.readregister(100)
    registers = device.readregister(200, "input")
    device.readregisters(100, 4)
    device.readregisters(100, 4, "input")
    device.readallregisters()
    registers = device.getregisters()
    print(registers)
    value = device.getregistervalue(100)
    print(value)
    value = device.getregistervalue(1001)
    print(value)
    device.writeregister(100, 22)
    device.writeregisters(100, [1,2]) # multiple registers and multiple values
    config = device.getchannelconfig("power")
    list = device.getchannellist()
    power = device.getchannelvalue("power")
    device.setchannelvalue("power", 300)
