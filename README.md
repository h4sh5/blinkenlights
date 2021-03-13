# Blinkenlights

Made with a RPi3B+, on python3
Stare at your network traffic (literally)

color codes are in the code, but feel free to change them! They are just connected to different color LEDs.

requirments (on raspbian):
```
sudo apt install python3-scapy
sudo apt install python3-rpi.gpio
```

## usage

set eth0 to promiscuous mode:
```sh
sudo ifconfig eth0 promisc
```

run the script:
```
chmod +x blinkenlights.py

# default w/ eth0
sudo ./blinkenlights.py 
# or, with another iface
sudo ./blinkenlights.py wlan0
```

Here it is in action on a RPi3B+:

![Blinking lights](blinks.gif)




