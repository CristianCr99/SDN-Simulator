import re
import scapy
from scapy.layers.inet import *
from scapy.sendrecv import sniff, AsyncSniffer, send
import socket
import tkinter as tk
from scapy.utils import wrpcap, wireshark, rdpcap
from IPy import IP

class Utilities():

    def mac_address_check(self, mac_address):
        try:
            if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
                return True
            return False
        except:
            return False

    def ip_address_check(self, ip_address):
        try:
            IP(ip_address)
            if len(ip_address.split('.')) == 4:
                return True
            return False
        except:
            return False

    def port_check(self, port):
        try:
            port_number = int(port)
            if port_number >= 1 and port_number <= 65535:
                return True
            return False
        except:
            return False




utilities = Utilities()


print(utilities.mac_address_check("00-11-22-33-44-66"))
print(utilities.mac_address_check("1 2 3 4 5 6 7 8 9 a b c"))
print(utilities.mac_address_check("This is not a mac"))
print(utilities.mac_address_check("AA:BB:CC:a:EE:FF"))
print(utilities.mac_address_check("AA:BB:CC:DD:EE:FF"))

print('\n')


print(utilities.ip_address_check("255.255.-1.255"))
print(utilities.ip_address_check("255.255.255"))
print(utilities.ip_address_check("255.255.255.255"))
print(utilities.ip_address_check("0.255.255.255"))

print('\n')

print(utilities.port_check("0"))
print(utilities.port_check("-100"))
print(utilities.port_check("65536"))
print(utilities.port_check("255.255.255"))
print(utilities.port_check("20000"))