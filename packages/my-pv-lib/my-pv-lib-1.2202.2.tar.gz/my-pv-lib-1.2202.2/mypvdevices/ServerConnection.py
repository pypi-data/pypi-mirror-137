#!/usr/bin/python

import logging

class ServerConnection:
    
    def __init__(self):
        pass

    # def __del__(self):
    #     self._running = False

    def __str__(self):
        return self.__class__.__name__

    # def getServer(self):
    #     return self._serverAddress

    # def getsockethash(self):
    #     return self._socket.__hash__()

    # def addDevice(self, device):
    #     if(device != None):
    #         self._device = device
    #         return True
    #     else:
    #         return False

    # def isconnected(self):
    #     return self._connected

    def connect(self):
        raise Exception("not implemented connect")

    def disconnect(self):
        raise Exception("not implemented disconnect")

    def reconnect(self):
        raise Exception("not implemented reconnect")
    					
# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    # serial = "120100200505tes1"
    # serial2 = "120100200505tes2"
    # serial3 = "120100200505tes3"
    # cryptoKey = "41424142414241424142414241424142"
    # cryptoKeyInvalid = "ABABABABABABAB00ABABABABABABAB00"
    # server = "my-pv.live"

    