# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Amp
#
#  You can find more information on our web site:
#   Yocto-Amp documentation:
#      https://www.yoctopuce.com/EN/products/yocto-amp/doc.html
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
from yocto_current import *


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
    # retreive any voltage sensor (can be AC or DC)
    sensor = YCurrent.FirstCurrent()
    if sensor is None:
        die('No module connected')
else:
    sensor = YCurrent.FindCurrent(target + '.current1')

# we need to retreive both DC and AC voltage from the device.
if not sensor.isOnline():
    die('Module not connected')

m = sensor.get_module()
sensorDC = YCurrent.FindCurrent(m.get_serialNumber() + '.current1')
sensorAC = YCurrent.FindCurrent(m.get_serialNumber() + '.current2')

while sensor.isOnline():
    print('DC: ' + str(sensorDC.get_currentValue()) + ' mA ' + \
          'AC: ' + str(sensorAC.get_currentValue()) + ' mA ')
    print('  (press Ctrl-C to exit)')
    YAPI.Sleep(1000, errmsg)
YAPI.FreeAPI()
