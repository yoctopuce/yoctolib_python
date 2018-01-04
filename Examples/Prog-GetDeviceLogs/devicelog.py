#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from yocto_api import *


def logfun(m, s):
    print(m.get_serialNumber() + ' : ' + s)


def deviceArrival(m):
    serial = m.get_serialNumber()
    print('Device arrival : ' + serial)
    m.registerLogCallback(logfun)


def deviceRemoval(m):
    print('Device removal : ' + m.get_serialNumber())


errmsg = YRefParam()

# No exception please
YAPI.DisableExceptions()

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

YAPI.RegisterDeviceArrivalCallback(deviceArrival)
YAPI.RegisterDeviceRemovalCallback(deviceRemoval)

print('Hit Ctrl-C to Stop ')
while True:
    YAPI.UpdateDeviceList(errmsg)  # traps plug/unplug events
    YAPI.Sleep(500, errmsg)  # traps others events
