#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_display import *


def upgradeSerialList(allserials):
    errmsg = YRefParam()
    for serial in allserials:
        module = YModule.FindModule(serial)
        product = module.get_productName()
        serial = module.get_serialNumber()
        current = module.get_firmwareRelease()
        # check if a new firmare is available on yoctopuce.com
        newfirm = module.checkFirmware("www.yoctopuce.com", False)
        if (newfirm == ""):
            print(product + " " + serial + "(rev=" + current + ") is up to date")
        else:
            print(product + " " + serial + "(rev=" + current + ") need be updated with firmare : ")
            print("    " + newfirm)
            # execute the firmware upgrade
            update = module.updateFirmware(newfirm)
            status = update.startUpdate()
            while (100 > status >= 0):
                newstatus = update.get_progress()
                if (newstatus != status):
                    print(str(status) + "% " + update.get_progressMessage())
                YAPI.Sleep(500, errmsg)
                status = newstatus
            if (status < 0):
                print("    " + status + " Firmware Update failed: " + update.get_progressMessage())
                exit(1)
            else:
                if (module.isOnline()):
                    print(str(status) + "% Firmware Updated Successfully!")
                else:
                    print(str(status) + " Firmware Update failed: module " + serial + "is not online")
                    exit(1)

errmsg = YRefParam()
# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

i = 1
while i < len(sys.argv):
    print("Update module connected to hub " + sys.argv[i])
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

hubs = []
shield = []
devices = []
#fist step construct the list of all hub /shield and devices connected
module = YModule.FirstModule()
while module is not None:
    product = module.get_productName()
    serial = module.get_serialNumber()
    if (product == "YoctoHub-Ethernet" or product == "YoctoHub-Wireless" or product == "YoctoHub-Wireless-SR"):
        hubs.append(serial)
    elif product == "YoctoHub-Shield":
        shield.append(serial)
    elif product != "VirtualHub":
        devices.append(serial)
    module = module.nextModule()
# fist upgrades all Hubs...
upgradeSerialList(hubs)
# ... then all shield..
upgradeSerialList(shield)
# ... and finaly all devices
upgradeSerialList(devices)
print("All devices are now up to date")
YAPI.FreeAPI()
