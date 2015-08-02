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

def setcolor(led1,led2,color):
    if led1.isOnline():
        led1.set_rgbColor(color)  # immediate switch
        led2.rgbMove(color,1000)  # smooth transition
    else:
       print('Module not connected (check identification and USB cable)')

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
if led.isOnline():
    m = led.get_module()
    led1 = YColorLed.FindColorLed(m.get_serialNumber() + '.colorLed1')
    led2 = YColorLed.FindColorLed(m.get_serialNumber() + '.colorLed2')
else:
    die('device not connected')

print('r: set to red')
print('g: set to green')
print('b: set to blue')
print('x: exit')

try: input = raw_input  # python 2.x fix
except: pass

c= input("command:")

while c!='x':
    if c=='r' : setcolor(led1,led2,0xFF0000)
    elif c=='g' : setcolor(led1,led2,0x00FF00)
    elif c=='b' : setcolor(led1,led2,0x0000FF)
    c= input("command:")