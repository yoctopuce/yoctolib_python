# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Meteo
#
#  You can find more information on our web site:
#   Yocto-Meteo documentation:
#      https://www.yoctopuce.com/EN/products/yocto-meteo/doc.html
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
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *


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
    # retreive any humidity sensor
    sensor = YHumidity.FirstHumidity()
    if sensor is None:
        die('No module connected')
    m = sensor.get_module()
    target = m.get_serialNumber()

else:
    m = YModule.FindModule(target)

if not m.isOnline():
    die('device not connected')

humSensor = YHumidity.FindHumidity(target + '.humidity')
pressSensor = YPressure.FindPressure(target + '.pressure')
tempSensor = YTemperature.FindTemperature(target + '.temperature')

while m.isOnline():
    print('%2.1f' % tempSensor.get_currentValue() + "°C   " +
          "%4.0f" % pressSensor.get_currentValue() + "mb  " +
          "%4.0f" % humSensor.get_currentValue() + "% (Ctrl-c to stop)  ")
    YAPI.Sleep(1000)
YAPI.FreeAPI()