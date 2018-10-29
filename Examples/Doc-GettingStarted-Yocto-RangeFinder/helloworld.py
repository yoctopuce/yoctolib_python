# ********************************************************************
#
#  $Id: helloworld.py 32628 2018-10-10 13:37:59Z seb $
#
#  An example that show how to use a  Yocto-RangeFinder
#
#  You can find more information on our web site:
#   Yocto-RangeFinder documentation:
#      https://www.yoctopuce.com/EN/products/yocto-rangefinder/doc.html
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
from yocto_rangefinder import *
from yocto_lightsensor import *
from yocto_temperature import *

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
    # retrieve any Range finder
    rf = YRangeFinder.FirstRangeFinder()
    if rf is None:
        die('No module connected')
    target = rf.get_module().get_serialNumber()
else:
    rf = YRangeFinder.FindRangeFinder(target + '.rangeFinder1')

if not (rf.isOnline()):
    die('device not connected')

ir  = YLightSensor.FindLightSensor(target+'.lightSensor1')
tmp = YTemperature.FindTemperature(target+'.temperature1')

while rf.isOnline():
    print("Distance    :  " + str(int(rf.get_currentValue())) )
    print("Ambiant IR  :  " + str(int(ir.get_currentValue())) )
    print("Temperature :  " + str(int(tmp.get_currentValue())) )
    YAPI.Sleep(1000)

YAPI.FreeAPI()
