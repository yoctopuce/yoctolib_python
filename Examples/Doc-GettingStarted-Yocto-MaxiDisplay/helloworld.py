#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
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

errmsg=YRefParam()

if len(sys.argv)<2 :  usage()

target=sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)



if target=='any':
    # retreive any RGB led
    disp = YDisplay.FirstDisplay()
    if disp is None :
        die('No module connected')
else:
    disp= YDisplay.FindDisplay(target + ".display")

if not disp.isOnline():
    die("Module not connected ")

# display clean up
disp.resetAll()

# retreive the display size
w=disp.get_displayWidth()
h=disp.get_displayHeight()

# retreive the first layer
l0=disp.get_displayLayer(0)
l0.clear()

#display a text in the middle of the screen
l0.drawText(w / 2,h / 2, YDisplayLayer.ALIGN.CENTER, "Hello world!" )

# visualize each corner
l0.moveTo(0,5)
l0.lineTo(0,0)
l0.lineTo(5,0)
l0.moveTo(0,h-6)
l0.lineTo(0,h-1)
l0.lineTo(5,h-1)
l0.moveTo(w-1,h-6)
l0.lineTo(w-1,h-1)
l0.lineTo(w-6,h-1)
l0.moveTo(w-1,5)
l0.lineTo(w-1,0)
l0.lineTo(w-6,0)

# draw a circle in the top left corner of layer 1
l1=disp.get_displayLayer(1)
l1.clear()
l1.drawCircle(h / 8, h / 8, h / 8)

# and animate the layer
print("Use Ctrl-C to stop")
x=0
y=0
vx=1
vy=1
while True:
    x+=vx
    y+=vy
    if x<0 or x>w-(h / 4) :  vx=-vx
    if y<0 or y>h-(h / 4)  : vy=-vy
    l1.setLayerPosition(x,y,0)
    YAPI.Sleep(5,errmsg)
