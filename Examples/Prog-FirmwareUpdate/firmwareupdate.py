#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *


def upgradeSerialList(all_serials):
    for serial in all_serials:
        module = YModule.FindModule(serial)
        product = module.get_productName()
        serial = module.get_serialNumber()
        current = module.get_firmwareRelease()
        # check if a new firmware is available on yoctopuce.com
        new_firmware = module.checkFirmware("www.yoctopuce.com", True)
        if new_firmware == "":
            print(product + " " + serial + "(rev=" + current + ") is up to date")
        else:
            print(product + " " + serial + "(rev=" + current + ") need be updated with firmware : ")
            print("    " + new_firmware)
            # execute the firmware upgrade
            update = module.updateFirmware(new_firmware)
            status = update.startUpdate()
            while 100 > status >= 0:
                new_status = update.get_progress()
                if new_status != status:
                    print(str(new_status) + "% " + update.get_progressMessage())
                YAPI.Sleep(500, errmsg)
                status = new_status
            if status < 0:
                print("Firmware Update failed: " + update.get_progressMessage())
                exit(1)
            else:
                if module.isOnline():
                    print(str(status) + "% Firmware Updated Successfully!")
                else:
                    print(str(status) + " Firmware Update failed: module " + serial + "is not online")
                    exit(1)


errmsg = YRefParam()
# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

i = 1
for i in range(1, len(sys.argv)):
    print("Update module connected to hub " + sys.argv[i])
    # Setup the API to use local USB devices
    if YAPI.RegisterHub(sys.argv[i], errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

hubs = []
shield = []
devices = []
# fist step construct the list of all hub /shield and devices connected
module = YModule.FirstModule()
while module is not None:
    product = module.get_productName()
    serial = module.get_serialNumber()
    if product == "YoctoHub-Shield":
        shield.append(serial)
    elif product[0:8] == "YoctoHub":
        hubs.append(serial)
    elif product != "VirtualHub":
        devices.append(serial)
    module = module.nextModule()
# fist upgrades all Hubs...
upgradeSerialList(hubs)
# ... then all shield..
upgradeSerialList(shield)
# ... and finally all devices
upgradeSerialList(devices)
print("All devices are now up to date")
YAPI.FreeAPI()
