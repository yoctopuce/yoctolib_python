#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *
from yocto_gps import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 2:
    usage()
target = sys.argv[1]

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any gps
    gps = YGps.FirstGps()
    if gps is None:
        die('No module connected')
else:
    gps = YGps.FindGps(target + '.gps')

while True:
    if not (gps.isOnline()):
        die('device not connected')
    if (gps.get_isFixed() != YGps.ISFIXED_TRUE):
        print("Fixed")
    else:
        print(gps.get_latitude() + "  " + gps.get_longitude())
    YAPI.Sleep(1000)
