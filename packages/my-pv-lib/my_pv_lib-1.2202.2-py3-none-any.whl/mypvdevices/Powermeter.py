#!/usr/bin/python

import logging

import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.GeneralDevice import GeneralDevice
from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.ModbusTcpDevice import ModbusTcpDevice
from mypvdevices.ChannelConfig import ChannelConfig

SERIALLEN = 7

class Powermeter(ModbusTcpDevice):

    _serial = None

    def __init__(self, serial, statichost):
        if serial != None and len(serial) == SERIALLEN:
            self._serial = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)

        super().__init__(serial, statichost, 502, 1)

        self._buscommunicationWaitTime = 1
        self._datamaximumage = 10
        self._channels["power"] = ChannelConfig([40499, 40500], "UINT32", 0)     #Power Value

    def _specialProcessingRead(self, channel, value):
        if channel == "power":
            p2 = (value^0xFFFFFFFF)               #xor
            p3 = p2-int(self._identity)  #substract serial number
            return p3
        else:
            return value

# Entry Point     
if __name__ == "__main__":

    import time

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

    device = Powermeter("1530638", None)

    device.connect()

    register = device.readregisters(40499, 2)

    device.readallregisters()
    data = device.getregisters()
    print("Data: " + str(data))

    registervalue = device.getregistervalue(40499)
    print("Registervalue" +  str(registervalue))

    power = device.getchannelvalue("power")
    print("Channel power: " + str(power))

    try:
        test = device.getchannelvalue("test")
        print("Channel test: " + str(test))
    except Exception as e:
        print(str(e))

    device.start()
    time.sleep(5)
    device.stop()

    power = device.getchannelvalue("power")
    print("Channel power: " + str(power))

    device.start()
    for i in range(10):
        time.sleep(2)
        power = device.getchannelvalue("power")
        print("Channel power: " + str(power))

    device.stop()

    print("\n\nNew Module")
    device2 = Powermeter("1525903", None)
    device2.start()
    for i in range(10):
        time.sleep(3)
        try:
            power = device2.getchannelvalue("power")
            print("Channel power: " + str(power))
        except Exception as e:
            print("Nothing read yet. " + str(e))
    device2.stop()

    print("\n\n2 Devices")
    device3 = Powermeter("1568049", None)
    device2.start()
    device3.start()
    for i in range(10):
        time.sleep(3)
        try:
            power2 = device2.getchannelvalue("power")
            print("Device 2 - Channel power: " + str(power2))
        except Exception as e:
            print("Device 2 - Nothing read yet. " + str(e))

        try:
            power3 = device3.getchannelvalue("power")
            print("Device 3 - Channel power: " + str(power3))
        except Exception as e:
            print("Device 3 - Nothing read yet. " + str(e))

    device2.stop()
    device3.stop()