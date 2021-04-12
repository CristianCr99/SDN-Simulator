
from scapy.layers.inet import *
from scapy.sendrecv import sniff, AsyncSniffer, send
import socket

from scapy.utils import wrpcap, wireshark

cache = []

p = Ether() / IP(src='192.168.1.2', dst='192.168.1.3') / TCP(sport=3000, dport=4000)

for i in range(0, 10):
    p = Ether() / IP(src='192.168.1.2', dst='192.168.1.3') / TCP(sport=3000, dport=4000)
    cache.append(p)

#p[TCP].dport = 30
#print(p[TCP].dport)

#t = AsyncSniffer()
#t.start()


#t.join()
#p.conversations()
#send(IP(dst="192.168.2.99")/ICMP())


#print(cache)

wireshark(cache, )
#wrpcap("./temp.cap", p)
#p.show()
# print(p.show(dump=True))