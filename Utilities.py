from scapy.layers.inet import *


class Utilities:

    def mac_address_check(self, mac_address):
        try:
            if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
                return True
            return False
        except:
            return False

    def ip_address_check(self, ip_address):
        try:
            if len(ip_address.split('.')) == 4:
                for i in ip_address.split('.'):
                    if not int(i) >= 0:
                        return False
                return True
            return False
        except:
            return False

    def port_check(self, port):
        try:
            port_number = int(port)
            if 1 <= port_number <= 65535:
                return True
            return False
        except:
            return False

    def is_number_positive(self, number):
        try:
            number = int(number)
            if number > 0:
                return True
            return False
        except:
            return False


