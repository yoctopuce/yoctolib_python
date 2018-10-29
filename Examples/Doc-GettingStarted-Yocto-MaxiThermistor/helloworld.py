# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-MaxiThermistor
#
#  You can find more information on our web site:
#   Yocto-MaxiThermistor documentation:
#      https://www.yoctopuce.com/EN/products/yocto-maxithermistor/doc.html
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
    # retreive any temperature sensor
    sensor = YTemperature.FirstTemperature()
    if sensor is None:
        die('No module connected')
else:
    sensor = YTemperature.FindTemperature(target + '.temperature1')

if not (sensor.isOnline()):
    die('device not connected')

# retreive module serial
serial = sensor.get_module().get_serialNumber()

# retreive all 6 channels
channel1 = YTemperature.FindTemperature(serial + '.temperature1')
channel2 = YTemperature.FindTemperature(serial + '.temperature2')
channel3 = YTemperature.FindTemperature(serial + '.temperature3')
channel4 = YTemperature.FindTemperature(serial + '.temperature4')
channel5 = YTemperature.FindTemperature(serial + '.temperature5')
channel6 = YTemperature.FindTemperature(serial + '.temperature6')

while sensor.isOnline():
    print("| 1: " + "%2.1f " % channel1.get_currentValue() + \
          "| 2: " + "%2.1f " % channel2.get_currentValue() + \
          "| 3: " + "%2.1f " % channel3.get_currentValue() + \
          "| 4: " + "%2.1f " % channel4.get_currentValue() + \
          "| 5: " + "%2.1f " % channel5.get_currentValue() + \
          "| 6: " + "%2.1f " % channel6.get_currentValue() + \
          "| deg C |")
    YAPI.Sleep(1000)
YAPI.FreeAPI()
