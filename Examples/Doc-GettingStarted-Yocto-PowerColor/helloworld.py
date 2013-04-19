#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_colorled import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname+' <serial_number>')
    print(scriptname+' <logical_name>')
    print(scriptname+' any  ')
    sys.exit()

def die(msg):
    sys.exit(msg+' (check USB cable)')

errmsg=YRefParam()

if len(sys.argv)<2 :  usage()

target=sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)


if target=='any':
    # retreive any RGB led
    led = YColorLed.FirstColorLed()
    if led is None :
        die('No module connected')
else:
    led= YColorLed.FindColorLed(target + '.colorLed1')

#  we need to retreive the second led from the device
if  not led.isOnline(): die('device not connected')

print('r: set to red')
print('g: set to green')
print('b: set to blue')
print('x: exit')

try: input = raw_input  # python 2.x fix
except: pass

c= input("command:")

while c!='x':
    if c=='r' : led.set_rgbColor(0xFF0000)
    elif c=='g' : led.set_rgbColor(0x00FF00)
    elif c=='b' : led.set_rgbColor(0x0000FF)
    c= input("command:")