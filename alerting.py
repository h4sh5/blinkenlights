#!/usr/bin/env python3

# make light blink and buzzer sound when new alert comes in suricata fast.log

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time
import sys

import tailer


impstart = time.time()

print('imports ready: %s seconds' % (time.time() - impstart))


def alarm(b):
    '''b is a gpiozero TonalBuzzer '''
    start = 60 #hz
    high = 80
    inc = 5
    gap = 0.05
    for f in range(start, high, inc):
        b.play(Tone(midi=f))
        time.sleep(gap) # then increase
    for f in range(high, start, -inc):
        b.play(Tone(midi=f))
        time.sleep(gap)
    b.stop()



# gpiozero uses BCM numbering, gpio 27 is pin 13 on rp3
b = TonalBuzzer(27)

fstart = time.time()

# roughly 2 seconds before reading til the end of file? adjustable 
followEndTime = 2 

log = open("/var/log/suricata/fast.log",'r')

for line in tailer.follow(log):
    # follow to the end of file, until delay between lines is sub second
    diff = time.time() - fstart
    if diff > followEndTime:
        print("new alert:", line)
        alarm(b)


exit(0) 
