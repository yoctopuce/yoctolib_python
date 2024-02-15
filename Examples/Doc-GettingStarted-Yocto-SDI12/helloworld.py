# ********************************************************************
#
#  $Id: helloworld.py 58233 2023-12-04 10:57:58Z seb $
#
#  An example that shows how to use a  Yocto-SDI12
#
#  You can find more information on our web site:
#   Yocto-SDI12 documentation:
#      https://www.yoctopuce.com/EN/products/yocto-sdi12/doc.html
#   Python V2 API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_sdi12port import *


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
    sdi12Port = YSdi12Port.FirstSdi12Port()
    if sdi12Port is None:
        sys.exit('No module connected (check cable)')
else:
    sdi12Port = YSdi12Port.FirstSdi12Port(sys.argv[1] + ".sdi12port")
    if not sdi12Port.isOnline():
        sys.exit('Module not connected')

singleSensor = sdi12Port.discoverSingleSensor()
print("%-35s %s " % ("Sensor address :", singleSensor.get_sensorAddress()))
print("%-35s %s " % ("Sensor SDI-12 compatibility : " , singleSensor.get_sensorProtocol()))
print("%-35s %s " % ("Sensor company name : " , singleSensor.get_sensorVendor()))
print("%-35s %s " % ("Sensor model number : " , singleSensor.get_sensorModel()))
print("%-35s %s " % ("Sensor version : " , singleSensor.get_sensorVersion()))
print("%-35s %s " % ("Sensor serial number : " , singleSensor.get_sensorSerial()))

valSensor = sdi12Port.readSensor(singleSensor.get_sensorAddress(),"M",5000)
i = 0
while i < len(valSensor):
    if singleSensor.get_measureCount() > 1:
        print("{0} : {1:8.2f} {2:8s} ({3})".format(singleSensor.get_measureSymbol(i),
                valSensor[i], singleSensor.get_measureUnit(i),
                singleSensor.get_measureDescription(i)))
    else:
        print(valSensor[i])
    i += 1

YAPI.FreeAPI()
