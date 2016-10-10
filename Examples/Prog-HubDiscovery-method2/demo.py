#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from yocto_api import *


# hub discovery, method 2 :  this example
# will register any and all hubs found.

# called each time a new device (networked or not) is detected
def arrivalCallback(dev):
    # iterate on all functions on the module and find the ports
    isAHub = False
    fctCount = dev.functionCount()
    for i in range(fctCount):
        # retreive the hardware name of the ith function
        fctHwdName = dev.functionId(i)
        if fctHwdName[:7] == "hubPort":
            # the device contains a  hubPortx function, so it's a hub
            if not isAHub:
                print("hub found : " + dev.get_friendlyName())
                isAHub = True
            # The port logical name is always the serial#
            # of the connected device
            deviceid = dev.functionName(i)
            print(" " + fctHwdName + " : " + deviceid)


errmsg = YRefParam()

print("Waiting for hubs to signal themselves...")

# configure the API to contact any networked device
if YAPI.RegisterHub("net", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

# each time a new device is connected/discovered
# arrivalCallback will be called.
YAPI.RegisterDeviceArrivalCallback(arrivalCallback)

# wait for 30 seconds, doing nothing.
for j in range(30):
    YAPI.UpdateDeviceList(errmsg)
    YAPI.Sleep(1000, errmsg)
