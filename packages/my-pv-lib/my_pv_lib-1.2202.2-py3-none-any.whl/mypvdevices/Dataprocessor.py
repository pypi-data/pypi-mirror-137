#!/usr/bin/python

import threading
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

class Dataprocessor:     #Singleton
    __instance__ = None
    __mutex__ = threading.Lock()

    @staticmethod
    def instance():
        """ Static access method. """
        if Dataprocessor.__instance__ == None:
            with Dataprocessor.__mutex__:
                Dataprocessor()
        return Dataprocessor.__instance__

    def __init__(self):
        """ Virtually private constructor. """
        if Dataprocessor.__instance__ != None:
            raise Exception("This class is a singleton! Instance already created")
        else:
            Dataprocessor.__instance__ = self

    def encode_16bit_uint(self, value):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_uint(value)
        payload = builder.to_registers()
        registers = builder.build()
        return registers

    def encode_32bit_uint(self, value):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_32bit_uint(value)
        payload = builder.to_registers()
        registers = builder.build()
        return registers

    def decode_16bit_uint(self, registers):
        decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.Big, wordorder=Endian.Big)
        decoded = decoder.decode_16bit_uint()
        return decoded

    def decode_32bit_uint(self, registers):
        decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.Big, wordorder=Endian.Big)
        decoded = decoder.decode_32bit_uint()
        return decoded
    
    def decode_32bit_float(self, registers):
        decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.Big, wordorder=Endian.Big)
        decoded = decoder.decode_32bit_float()
        return decoded

    def adcNTC2Temp(self, adc_value):     # requires a 12 bit ADC resolution on a voltage divider 10k/10k NTC delivers temp in 0.1degree res
        NTC_table=[1857, 1558, 1259, 1100, 992, 912, 848, 794, 
            749, 708, 673, 640, 611, 584, 558, 535, 512, 
            491, 471, 452, 434, 416, 399, 383, 367, 351, 
            336, 321, 306, 292, 278, 264, 250, 236, 223, 
            209, 196, 182, 169, 155, 142, 128, 115, 101, 
            86, 72, 57, 42, 27, 11, -5, -23, -40, -59, 
            -79, -101, -124, -149, -177, -208, -246, 
            -291, -352, -447, -542]
    
        p1 = NTC_table[ (adc_value >> 6)  ]
        p2 = NTC_table[ (adc_value >> 6)+1]
        t=round((p1 - ( (p1-p2) * (adc_value & 0x003F) ) / 64)/10,1)
        if t>120:
            return "short"
        if t<-44:
            return "open"
        return t

    def adcPoti2Temp(self, adc_value):    # für Raumgeber max=30degree min 10degree mitte 20degree Werte:voll 528, mitte: delivers temp in 0.1degree res
        t=round(adc_value*0.336+62.752)/10    #formel in Excel entwickelt y = 0,3356x + 62,752R² = 1
        if t>30:
            return "open"
        if t<10:
            return "short"
        return t  

# # Entry Point     
# if __name__ == "__main__":

#     from colr import color

#     logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

#     value = Dataprocessor.instance().adcPoti2Temp(100)
#     print(value)

#     value = Dataprocessor.instance().encode_16bit_uint(100)
#     print(value)
