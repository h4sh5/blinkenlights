#!/usr/bin/env python3

# make lights blink with different network packet traffic types

import RPi.GPIO as gpio
import time

impstart = time.time()

# scapy 
from scapy.all import *

print('imports ready: %s seconds' % (time.time() - impstart))


udpRed = 3
tlsYellow = 5
httpGreen = 7
dnsBlue = 11

# BOARD means plain pin numbers
gpio.setmode(gpio.BOARD)

outputs = [udpRed, tlsYellow, httpGreen, dnsBlue]

for p in outputs:
    gpio.setup(p, gpio.OUT)
    gpio.output(p, gpio.LOW)


def toggle_pin(pin):
    gpio.output(pin, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(pin, gpio.LOW)


# handler
def process_packet(packet):
    if packet.haslayer(TCP):
        #import code
        #code.interact(local=locals())
        payload = bytes(packet[TCP].payload)
        #if b"HTTP" in  payload:
        if payload.haslayer(HTTP):
            print("---------- HTTP ------------")
            print(payload)
            toggle_pin(httpGreen)
        
        if packet[TCP].sport == 443 or packet[TCP].dport == 443:
            print("---------- 443 ------------")
            toggle_pin(tlsYellow)
    
    
    elif packet.haslayer(UDP):
        
        if packet[UDP].haslayer(DNS):
            print("------------ DNS detected -----------")
            toggle_pin(dnsBlue)
            print(packet[DNS])
        else:
            print("---------- some UDP ----------")
            print(packet[UDP])
            toggle_pin(udpRed)
 
        


# start sniffing packet
sniff(filter="tcp or udp", prn=process_packet, iface="eth0", store=False)



exit(0) 


# -------- example code ---------

while 1:
    gpio.output(red, gpio.HIGH)
    time.sleep(1)
    print("blink")
    gpio.output(red, gpio.LOW)
    time.sleep(1)


