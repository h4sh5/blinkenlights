#!/usr/bin/env python3

# make lights blink with different network packet traffic types

import RPi.GPIO as gpio
import time
import sys

impstart = time.time()



# scapy 
from scapy.all import *

# threads
import _thread

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
    time.sleep(0.3)
    gpio.output(pin, gpio.LOW)


# handler
def thread_handler(packet):
    if packet.haslayer(TCP):
        #import code
        #code.interact(local=locals())
        payload = bytes(packet[TCP].payload)
        #if b"HTTP" in  payload:
        if b'HTTP' in payload or packet[TCP].sport == 80 or \
               packet[TCP].dport == 80:
            print("---------- HTTP ------------")
            print(payload)
            toggle_pin(httpGreen)
        
        if packet[TCP].sport == 443 or packet[TCP].dport == 443:
            print("---------- 443 ------------")
            #toggle_pin(tlsYellow)
            toggle_pin(tlsYellow)
    
    
    elif packet.haslayer(DNS):
        
        print("------------ DNS detected -----------")
        toggle_pin(dnsBlue)
        print(packet[DNS])
    elif packet.haslayer(UDP):
        print("---------- some UDP ----------")
        print(packet[UDP])
        toggle_pin(udpRed)
 
        

def process_packet(packet):
    _thread.start_new_thread(thread_handler, (packet,))

dev = 'eth0'
if len(sys.argv) >= 2:
    dev = sys.argv[1]

print("starting capture on", dev)
# start sniffing packet
sniff(filter="", prn=process_packet, iface=dev, store=False)



exit(0) 


# -------- example code ---------

while 1:
    gpio.output(red, gpio.HIGH)
    time.sleep(1)
    print("blink")
    gpio.output(red, gpio.LOW)
    time.sleep(1)


