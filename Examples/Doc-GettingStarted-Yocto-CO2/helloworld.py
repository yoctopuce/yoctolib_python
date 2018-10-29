# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-CO2
#
#  You can find more information on our web site:
#   Yocto-CO2 documentation:
#      https://www.yoctopuce.com/EN/products/yocto-co2/doc.html
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
from yocto_carbondioxide import *


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
    # retreive any carbonDioxide sensor
    sensor = YCarbonDioxide.FirstCarbonDioxide()
    if sensor is None:
        die('No module connected')
    print("Using: " + sensor.get_module().get_serialNumber())
else:
    sensor = YCarbonDioxide.FindCarbonDioxide(target + '.carbonDioxide')

if not (sensor.isOnline()):
    die('device not connected')

while sensor.isOnline():
    print("CO2 :  " + "%2.1f" % sensor.get_currentValue() + "ppm (Ctrl-C to stop)")
    YAPI.Sleep(1000)

YAPI.FreeAPI()
