# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Volt
#
#  You can find more information on our web site:
#   Yocto-Volt documentation:
#      https://www.yoctopuce.com/EN/products/yocto-volt/doc.html
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
from yocto_voltage import *


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
    # retreive any voltage sensor
    sensor = YVoltage.FirstVoltage()
    if sensor is None:
        die('No module connected')
    m = sensor.get_module()
    target = m.get_serialNumber()

sensorDC = YVoltage.FindVoltage(target + '.voltage1')
sensorAC = YVoltage.FindVoltage(target + '.voltage2')

if not (sensorDC.isOnline()):
    die('device not connected')

while sensorDC.isOnline():
    print("Voltage : %3.2fV DC / %3.2fV AC (Ctrl-C to stop) " % \
          (sensorDC.get_currentValue(), sensorAC.get_currentValue()))
    YAPI.Sleep(1000)
YAPI.FreeAPI()
