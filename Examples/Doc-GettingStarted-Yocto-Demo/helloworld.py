#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_led import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname+' <serial_number>')
    print(scriptname+' <logical_name>')
    print(scriptname+' any  ')
    sys.exit()

def die(msg):
    sys.exit(msg+' (check USB cable)')

def setLedState(led,state):
    if led.isOnline():
        if state :
            led.set_power(YLed.POWER_ON)
        else:
            led.set_power(YLed.POWER_OFF)
    else:
       print('Module not connected (check identification and USB cable)')

errmsg=YRefParam()

#if len(sys.argv)<2 :  usage()

#target=sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

target="any"
if target=='any':
    # retreive any RGB led
    led = YLed.FirstLed()
    if led is None :
        die('No module connected')
else:
    led= YLed.FindLed(target + '.led')

if not(led.isOnline()):die('device not connected')

print('0: turn test led OFF')
print('1: turn test led ON')
print('x: exit')

try: input = raw_input  # python 2.x fix
except: pass

c= input("command:")

while c!='x':
    if c=='0' :  setLedState(led,False);
    elif c=='1' :setLedState(led,True);
    c= input("command:")