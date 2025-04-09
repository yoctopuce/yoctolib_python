# ********************************************************************
#
#  $Id: helloworld.py 65359 2025-03-26 11:48:58Z tiago $
#
#  An example that shows how to use a  Yocto-Spectral
#
#  You can find more information on our web site:
#   Yocto-Spectral documentation:
#      https://www.yoctopuce.com/EN/products/yocto-spectral/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_colorsensor import *
from yocto_api import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + " <serial_number>  <value>")
    print(scriptname + " <logical_name>   <value>")
    print(scriptname + " any  <value>   (use any discovered device)")
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 2:
    usage()
target = sys.argv[1].upper()

# Setup the API to use local USB devices. You can
# use an IP address instead of 'usb' if the device
# is connected to a network.
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    colorSensor = YColorSensor.FirstColorSensor()
    if colorSensor is None:
        sys.exit('No module connected (check cable)')
else:
    colorSensor = YColorSensor.FindColorSensor(sys.argv[1] + ".colorSensor")
    if not colorSensor.isOnline():
        sys.exit('Module not connected')
while(colorSensor.isOnline()):
    colorSensor.set_workingMode(0)
    colorSensor.set_estimationModel(0)

    print("Near color : " + colorSensor.get_nearSimpleColor())
    print("RGB Hex : " + str(hex(colorSensor.get_estimatedRGB())))
    print("--------------------------------------------")
    YAPI.Sleep(5000, errmsg)
YAPI.FreeAPI()
