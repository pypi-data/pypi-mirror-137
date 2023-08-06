#!/usr/bin/python

class ChannelConfig:
    registers = None
    channeltype = None
    scale = 0
    mode = None
    registertype = None
    datasettype = None

    def __init__(self, registers, channeltype, scale, mode="r", registertype="holding", datasettype=None):

        if registers == None:
            raise TypeError("Registers cannot be None")

        if isinstance(registers, list):
            for register in registers:
                if not isinstance(register, int):
                    raise TypeError("Registers " + str(register) + " has to be int")
            self.registers = registers
        else:
            raise TypeError("Registers has to be list of int")

        if isinstance(scale, float) or isinstance(scale, int):
            self.scale = scale
        else:
            raise TypeError("Scale has to be float or int")

        if mode == "r" or mode == "w" or mode == "rw":
            self.mode = mode
        else:
            raise TypeError("Mode has to be 'r', 'w' or 'rw'")

        if registertype == "holding" or registertype == "input" or registertype == "serial":
            self.registertype = registertype
        else:
            raise TypeError("registertype has to be 'holding', 'input' or 'serial'")

        if datasettype == None or datasettype == "sum" or datasettype == "avg":
            self.datasettype = datasettype
        else:
            raise TypeError("datasettype has to be 'sum', 'avg' or None")

        self.channeltype = channeltype