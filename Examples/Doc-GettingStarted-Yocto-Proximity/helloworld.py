# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Proximity
#
#  You can find more information on our web site:
#   Yocto-Proximity documentation:
#      https://www.yoctopuce.com/EN/products/yocto-proximity/doc.html
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
from yocto_proximity import *
from yocto_lightsensor import *



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
    # retreive any Light sensor
    p = YProximity.FirstProximity()
    if p is None:
        die('No module connected')
    target = p.get_module().get_serialNumber()

else:
    p = YProximity.FindProximity(target + '.proximity1')


if not (p.isOnline()):
    die('device not connected')

al = YLightSensor.FindLightSensor(target+'.lightSensor1')
ir = YLightSensor.FindLightSensor(target+'.lightSensor2')


while p.isOnline():
    print("proximity :  " + str(int(p.get_currentValue())) )
    print("ambient :  " + str(int(al.get_currentValue())) )
    print("IR :  " + str(int(ir.get_currentValue())) )

    YAPI.Sleep(1000)
YAPI.FreeAPI()
