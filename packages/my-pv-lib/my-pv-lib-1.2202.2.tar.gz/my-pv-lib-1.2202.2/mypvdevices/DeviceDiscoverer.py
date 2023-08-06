#!/usr/bin/python

import logging
from logging import debug, exception
import threading
import socket
import libscrc
from netifaces import interfaces, ifaddresses, AF_INET
from datetime import datetime

PORT = 16124
SOCKETTIMEOUT = 3
SEARCHCACHETIME = 5

class DeviceDiscovererException(Exception):
    def __init__(self, msg, code):

        if code == None:
            msg="errorcode required"
            raise TypeError(msg)

        self.code = code
        self.message = msg
    def __str__(self):
        return repr(str(self.message) + ". Error-Code: " + str(self.code))


class DeviceDiscoverer:     #Singleton
    _instance = None
    _mutex_ = threading.Lock()
    _powermeters = None
    _powermeterslastsearch = None
    _acthors = None
    _acthorslastsearch = None
    _acthors9s = None
    _acthors9slastsearch = None
    _elwas = None
    _elwaslastsearch = None

    @staticmethod
    def instance():
        """ Static access method. """
        if DeviceDiscoverer._instance == None:
            with DeviceDiscoverer._mutex_:
                DeviceDiscoverer()
        return DeviceDiscoverer._instance

    def __init__(self):
        """ Virtually private constructor. """
        if DeviceDiscoverer._instance != None:
            raise DeviceDiscovererException("[DeviceDiscoverer] This class is a singleton! Instance already created", 987)
        else:
            DeviceDiscoverer._instance = self
            self._powermeters = []
            self._acthors = []
            self._acthors9s = []
            self._elwas = []

    def _search(self, id, string, crc):
        logging.info("Searching for " + string + "...")
        try:
            id_encoded = bytes.fromhex(id)
            string_encoded = bytearray(string, "utf-8")
            crc_encoded = bytes.fromhex(crc)
        except Exception as e:
            logging.debug("Invalid parameters for command:" + str(e))
            raise TypeError()

        try:
            missing_string_ellements = 16 - len(string_encoded)
            string_full = string_encoded + b'\x00' * missing_string_ellements
            data = crc_encoded + id_encoded + string_full
            missing_data = 32 - len(data)
            data_full = data + B'\x00' * missing_data
        except Exception as e:
            logging.debug("Error preparing data:" + str(e))
            raise DeviceDiscovererException("Error preparing data:" + str(e), 1)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
            s.settimeout(SOCKETTIMEOUT)
            s.bind(("", PORT))
        except Exception as e:
            logging.debug("Error preparing socket:" + str(e))
            raise DeviceDiscovererException("Error preparing socket:" + str(e), 2)

        try:
            ips = self.get_ip4_broadcast_addresses()
            for element in ips:
                s.sendto(data_full, (element, PORT))
        except Exception as e:
            logging.debug("Error sending broadcast:" + str(e))
            s.close()
            raise DeviceDiscovererException("Error sending broadcast:" + str(e), 3)

        devices = []
        for i in range(20):
            logging.debug("Processing response %d", i)
            try:
                response = s.recvfrom(1024)
                logging.debug("Response: " + str(response))
                response_ip = response[1][0]
                response_data = response[0]
                if response_ip not in ips:
                    device = self.decoderesponse(response_data)
                    if device != None and device["identification"] == id:
                        devices.append(device)
            except socket.timeout:
                break
            except Exception as e:
                logging.debug("Error handling response: " + str(e))
        s.close()

        if len(devices) == 0:
            logging.info("No device found.")
        else:
            logging.info("Found " + str(len(devices)) + " devices.")
        return devices

    def get_ip4_broadcast_addresses(self):
        ip_list = []
        for interface in interfaces():
            try:
                links = ifaddresses(interface)[AF_INET]
            except Exception:
                links = []
                logging.debug("Interface " +  str(interface) + " is deactivated.")
            for link in links:
                ip = link['addr'].split('.')
                mask = link['netmask'].split('.')
                ip = [int(bin(int(octet)), 2) for octet in ip]
                mask = [int(bin(int(octet)), 2) for octet in mask]
                # subnet = [str(int(bin(ioctet & moctet), 2)) for ioctet, moctet in zip(ip, mask)]
                # host = [str(int(bin(ioctet & ~moctet), 2)) for ioctet, moctet in zip(ip, mask)]
                broadcast = [(ioctet | ~moctet) & 0xff for ioctet, moctet in zip(ip, mask)]
                broadcaststring = str(broadcast[0]) + "." + str(broadcast[1]) + "." + str(broadcast[2]) + "." + str(broadcast[3])
                ip_list.append(broadcaststring)
        return ip_list

    def _calccrc(self, data):
        crcdata = data[2:64]
        crc16 = libscrc.modbus(crcdata)
        return crc16

    def decoderesponse(self, data):
        if len(data) != 64:
            raise DeviceDiscovererException("Invalid data length", 5)
        crc_received_hex = data[0:2].hex()
        crc_received = int(crc_received_hex, 16)
        crc_calculated = self._calccrc(data) 
        if crc_received != crc_calculated:
            raise DeviceDiscovererException("CRC missmatch", 4)
        identification = data[2:4].hex()
        ip_address = str(data[4]) + "." + str(data[5]) + "." + str(data[6]) + "." + str(data[7])
        serialbytes = data[8:24]
        serial = serialbytes.decode('utf8').rstrip('\x00')
        fwversion = int.from_bytes(data[24:26], byteorder='big')
        elwa_nr = data[26]

        device = {
            "identification": identification,
            "ip_address": ip_address,
            "serial": serial,
            "fwversion": fwversion,
            "elwa_nr": elwa_nr
        }
        return device

    def searchacthor9s(self):
        if self._acthors9slastsearch != None:
            difference = datetime.now() - self._acthors9slastsearch
        else:
            difference = None
        if difference == None or difference.total_seconds() > SEARCHCACHETIME:
            self._acthors9s = self._search('4f4c', 'AC-THOR 9s', '84db')
            self._acthors9slastsearch = datetime.now()
        return self._acthors9s

    def searchacthor(self):
        if self._acthorslastsearch != None:
            difference = datetime.now() - self._acthorslastsearch
        else:
            difference = None
        if difference == None or difference.total_seconds() > SEARCHCACHETIME:
            self._acthors = self._search('4e84', 'AC-THOR', 'cb7a')
            self._acthorslastsearch = datetime.now()
        return self._acthors

    def searchpowermeter(self):
        if self._powermeterslastsearch != None:
            difference = datetime.now() - self._powermeterslastsearch
        else:
            difference = None
        if difference == None or difference.total_seconds() > SEARCHCACHETIME:
            self._powermeters = self._search('4e8e', "Power Meter", '401e')
            self._powermeterslastsearch = datetime.now()
        return self._powermeters
    
    def searchelwa(self):
        if self._elwaslastsearch != None:
            difference = datetime.now() - self._elwaslastsearch
        else:
            difference = None
        if difference == None or difference.total_seconds() > SEARCHCACHETIME:
            self._elwas = self._search('3efc', 'AC ELWA-E', '86d9')
            self._elwaslastsearch = datetime.now()
        return self._elwas

    def getipforserial(self, serial):
        logging.info("Getting IP-Address for serial " + str(serial))
        if serial == None:
            msg="serial required"
            logging.warning(msg)
            raise TypeError(msg)

        if not isinstance(serial, str):
            msg="serial hast to be a string"
            logging.warning(msg)
            raise TypeError(msg)

        with self._mutex_:
            device_type = serial[0:6]
            if device_type == "200300":
                devices = self.searchacthor9s()
            elif device_type == "200100":
                devices = self.searchacthor()
            elif device_type == "160124":
                devices = self.searchelwa()
            else:
                devices = self.searchpowermeter()

        try:
            for device in devices:
                if device["serial"] == serial:
                    logging.info("Found IP-Address: " + str(device["ip_address"]))
                    return device["ip_address"]
        except Exception as e:
            logging.error("Error searching for IP: " + str(e))
        logging.info("IP-Address not found.")
        return None

# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

    device = DeviceDiscoverer.instance().searchacthor()
    print(device)
    device9s = DeviceDiscoverer.instance().searchacthor9s()
    print(device9s)
    meters = DeviceDiscoverer.instance().searchpowermeter()
    print(meters)
    elwa = DeviceDiscoverer.instance().searchelwa()
    print(elwa)

    ip = DeviceDiscoverer.instance().getipforserial("120100200505tes1")
    ip = DeviceDiscoverer.instance().getipforserial("1601242002040015")
    ip = DeviceDiscoverer.instance().getipforserial("2003002007230020")
    ip = DeviceDiscoverer.instance().getipforserial("2001002006100016")
    ip = DeviceDiscoverer.instance().getipforserial("1530638")

    device = DeviceDiscoverer.instance().searchacthor()
    device = DeviceDiscoverer.instance().searchacthor()
    print(device)
    device9s = DeviceDiscoverer.instance().searchacthor9s()
    device9s = DeviceDiscoverer.instance().searchacthor9s()
    print(device9s)
    meters = DeviceDiscoverer.instance().searchpowermeter()
    meters = DeviceDiscoverer.instance().searchpowermeter()
    print(meters)
    elwa = DeviceDiscoverer.instance().searchelwa()
    elwa = DeviceDiscoverer.instance().searchelwa()
    print(elwa)

        