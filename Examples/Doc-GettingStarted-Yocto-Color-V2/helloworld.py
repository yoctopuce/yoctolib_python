# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Color-V2
#
#  You can find more information on our web site:
#   Yocto-Color-V2 documentation:
#      https://www.yoctopuce.com/EN/products/yocto-color-v2/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))


from yocto_api import *
from yocto_colorledcluster import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


def setcolor(led_cluster, nb_leds, color):
    if led_cluster.isOnline():
        # immediate transition for fist half of leds
        led_cluster.set_rgbColor(0, nb_leds / 2, color)
        # immediate transition for second half of leds
        led_cluster.rgb_move(nb_leds / 2, nb_leds / 2, color, 2000)
    else:
        print('Module not connected (check identification and USB cable)')


errmsg = YRefParam()

if len(sys.argv) < 2:
    usage()

target = sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any RGB led
    led_cluster = YColorLedCluster.FirstColorLedCluster()
    if led_cluster is None:
        die('No module connected')
else:
    led_cluster = YColorLedCluster.FindColorLedCluster(target + '.colorLedCluster')

if not led_cluster.isOnline():
    die('device not connected')

nb_leds = 2
led_cluster.set_activeLedCount(nb_leds)
led_cluster.set_ledType(YColorLedCluster.LEDTYPE_RGB)

print('r: set to red')
print('g: set to green')
print('b: set to blue')
print('x: exit')

try:
    input = raw_input  # python 2.x fix
except:
    pass

c = input("command:")

while c != 'x':
    if c == 'r':
        setcolor(led_cluster, nb_leds, 0xFF0000)
    elif c == 'g':
        setcolor(led_cluster, nb_leds, 0x00FF00)
    elif c == 'b':
        setcolor(led_cluster, nb_leds, 0x0000FF)
    c = input("command:")
YAPI.FreeAPI()
