#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_weighscale import *

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
    # retreive any genericSensor sensor
    sensor = YWeighScale.FirstWeighScale()
    if sensor is None:
        die('No module connected')
else:
    sensor = YGenericSensor.FindWeighScale(target + '.WeighScale')

if not (sensor.isOnline()): die('device not connected')

# On startup, enable excitation and tare weigh scale
print("Resetting tare weight...");
sensor.set_excitation(YWeighScale.EXCITATION_AC);
YAPI.Sleep(3000);
sensor.tare();

while sensor.isOnline():
    print("Weight:  %f %s" % (sensor.get_currentValue(), sensor.get_unit()))
    print("  (Ctrl-C to stop)")
    YAPI.Sleep(1000)
YAPI.FreeAPI()
