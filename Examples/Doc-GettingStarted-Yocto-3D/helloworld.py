# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-3D
#
#  You can find more information on our web site:
#   Yocto-3D documentation:
#      https://www.yoctopuce.com/EN/products/yocto-3d/doc.html
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
from yocto_tilt import *
from yocto_compass import *
from yocto_gyro import *
from yocto_accelerometer import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


errmsg = YRefParam()

if len(sys.argv) < 2:
    usage()

target = sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any tilt sensor
    anytilt = YTilt.FirstTilt()
    if anytilt is None:
        die('No module connected (check USB cable)')
    m = anytilt.get_module()
    target = m.get_serialNumber()
else:
    anytilt = YTilt.FindTilt(target + ".tilt1")
    if not (anytilt.isOnline()):
        die('Module not connected (check identification and USB cable)')

serial = anytilt.get_module().get_serialNumber()
tilt1 = YTilt.FindTilt(serial + ".tilt1")
tilt2 = YTilt.FindTilt(serial + ".tilt2")
compass = YCompass.FindCompass(serial + ".compass")
accelerometer = YAccelerometer.FindAccelerometer(serial + ".accelerometer")
gyro = YGyro.FindGyro(serial + ".gyro")

count = 0

if not (tilt1.isOnline()):
    die("Module not connected (check identification and USB cable)")

while tilt1.isOnline():

    if count % 10 == 0:
        print("tilt1   tilt2   compass acc     gyro")

    print("%-7.1f " % tilt1.get_currentValue() + \
          "%-7.1f " % tilt2.get_currentValue() + \
          "%-7.1f " % compass.get_currentValue() + \
          "%-7.1f " % accelerometer.get_currentValue() + \
          "%-7.1f" % gyro.get_currentValue())
    count += 1
    YAPI.Sleep(250, errmsg)
YAPI.FreeAPI()
