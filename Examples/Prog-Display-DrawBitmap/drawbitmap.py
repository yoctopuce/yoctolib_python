#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import math
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))

import array
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
# retreive the display size
w=disp.get_displayWidth()
h=disp.get_displayHeight()

# reteive the first layer
l0=disp.get_displayLayer(0)
bytesPerLines = int(w / 8)

data= array.array('B')
for i in range(0,h*bytesPerLines):
    data.append(0)


max_iteration = 50
centerX = 0.0
centerY = 0.0
targetX =  0.834555980181972
targetY  = 0.204552998862566
zoom    = 1.0
distance = 1.0

while  True:
    for i in range(0,len(data)):
        data[i]=0
    distance = distance *0.95
    centerX =  targetX * (1-distance)
    centerY =  targetY * (1-distance)
    max_iteration = int(0.5+max_iteration  + math.sqrt(zoom) )
    if (max_iteration>1500) :  max_iteration = 1500
    for j in range(0,h):
        for i in range (0,w):
            x0 = (((i - w/2.0) / (w/8))/zoom)-centerX
            y0 = (((j - h/2.0) / (w/8))/zoom)-centerY
            x = 0
            y = 0
            iteration = 0

            while  (x*x + y*y < 4) and (iteration < max_iteration ):
                xtemp = x*x - y*y + x0
                y = 2*x*y + y0
                x = xtemp
                iteration += 1

            if iteration>=max_iteration:
                data[j*bytesPerLines + (i >> 3)] |=  (128 >> (i & 7))


    l0.drawBitmap(0,0,w,data,0)
    zoom =zoom / 0.95

