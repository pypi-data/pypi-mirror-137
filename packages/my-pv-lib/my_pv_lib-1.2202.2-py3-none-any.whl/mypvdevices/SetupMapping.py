#!/usr/bin/python

class SetupMapping:
    channelname = None
    forced = False
    value = None

    def __init__(self, channelname=None, forced = False, defaultvalue = None):

        if channelname != None:
            if isinstance(channelname, str):
                self.channelname = channelname
            else:
                raise TypeError("Channelname has to be None or str")

        if forced == None:
            raise TypeError("forced cannot be None")

        if isinstance(forced, bool):
            self.forced = forced
        else:
            raise TypeError("Channelname has to be bool")

        if defaultvalue != None:
            if isinstance(forced, str) or isinstance(forced, int) or isinstance(forced, float) or isinstance(forced, bool):
                self.value = defaultvalue
            else:
                raise TypeError("defaultvalue has to be str, int, float or bool")
