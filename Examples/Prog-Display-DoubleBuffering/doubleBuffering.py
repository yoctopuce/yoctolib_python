#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import math
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))

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

# this is the recusive function to draw 1/3nd of the Von Koch flake
def recursiveLine(layer, x0, y0, x1, y1 ,   deep):
    if deep<=0:
        layer.moveTo(int(x0+0.5),int(y0+0.5))
        layer.lineTo(int(x1+0.5),int(y1+0.5))
    else:
        dx = (x1-x0) /3
        dy = (y1-y0) /3
        mx =  ((x0+x1) / 2) +  (0.87 *(y1-y0) / 3)
        my =  ((y0+y1) / 2) -  (0.87 *(x1-x0) / 3)
        recursiveLine(layer,x0,y0,x0+dx,y0+dy,deep-1)
        recursiveLine(layer,x0+dx,y0+dy,mx,my,deep-1)
        recursiveLine(layer,mx,my,x1-dx,y1-dy,deep-1)
        recursiveLine(layer,x1-dx,y1-dy,x1,y1,deep-1)

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

# display clean up
disp.resetAll()

l1=disp.get_displayLayer(1)
l2=disp.get_displayLayer(2)
l1.hide()    # L1 is hidden, l2 stays visible
centerX = disp.get_displayWidth() / 2
centerY = disp.get_displayHeight() / 2
radius  = disp.get_displayHeight() / 2
a=0

while True:
    # we draw in the hidden layer
    l1.clear()
    for  i in range(0,3):
        recursiveLine(l1,centerX + radius*math.cos(a+i*2.094),
              centerY + radius*math.sin(a+i*2.094) ,
              centerX + radius*math.cos(a+(i+1)*2.094),
              centerY + radius*math.sin(a+(i+1)*2.094), 2)
    # then we swap contents with the visible layer

    disp.swapLayerContent(1,2)
    # change the flake angle
    a+=0.1257

