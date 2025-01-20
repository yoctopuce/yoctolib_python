# ********************************************************************
#
#  $Id: helloworld.py 58233 2023-12-04 10:57:58Z seb $
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

from yocto_spectralsensor import *
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
    spectralSensor = YSpectralSensor.FirstSpectralSensor()
    if spectralSensor is None:
        sys.exit('No module connected (check cable)')
else:
    i2cPort = YSpectralSensor.FindSpectralSensor(sys.argv[1] + ".spectralSensor")
    if not i2cPort.isOnline():
        sys.exit('Module not connected')

# sample code reading MCP9804 temperature sensor
spectralSensor.set_gain(6)
spectralSensor.set_integrationTime(150)
spectralSensor.set_ledCurrent(6)

print("Near color : " + spectralSensor.get_nearSimpleColor())
print("Color HEX : " + str(hex(spectralSensor.get_estimatedRGB())))
YAPI.FreeAPI()
