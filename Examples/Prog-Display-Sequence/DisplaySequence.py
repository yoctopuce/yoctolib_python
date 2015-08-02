#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import math
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from array import *

from yocto_api import *
from yocto_display import *


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
    # retreive any display
    disp = YDisplay.FirstDisplay()
    if disp is None :
        die('No module connected')
else:
    disp= YDisplay.FindDisplay(target + ".display")

if not disp.isOnline():
    die("Module not connected ")

disp.resetAll()

#retreive the display size

w=disp.get_displayWidth()
h=disp.get_displayHeight()

#reteive the first layer
l0 = disp.get_displayLayer(0)
count = 8
coord = array.array('b')
for i in range(1,2*count): coord.append(0)


# precompute the "leds" position
ledwidth =int (w / count)


for i in range (0,count):
    coord[i] = i *ledwidth
    coord[2*count-i-2] = coord[i]


framesCount =  2*count-2

# start recording
disp.newSequence()

# build one loop for recording
for i in range (0,framesCount):
    l0.selectColorPen(0)
    l0.drawBar(coord[(i+framesCount-1) % framesCount], h-1,coord[(i+framesCount-1) % framesCount]+ledwidth, h-4)
    l0.selectColorPen(0xffffff)
    l0.drawBar(coord[i], h-1, coord[i]+ledwidth, h-4)
    disp.pauseSequence(50)  # records a 50ms pause.

# self-call : causes an endless looop
disp.playSequence("K2000.seq")
# stop recording and save to device filesystem
disp.saveSequence("K2000.seq")

#play the sequence
disp.playSequence("K2000.seq")

print("This animation is running in background.")

