#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *
from yocto_hubport import *


class YoctoShield(object):
    def __init__(self, serial):
        self._serial = serial
        self._subDevices = []

    def getSerial(self):
        return self._serial

    def addSubdevice(self, serial):
        for i in range(1, 5):
            p = YHubPort.FindHubPort("%s.hubPort%d" % (self._serial, i))
            if p.get_logicalName() == serial:
                self._subDevices.append(serial)
                return True
        return False

    def removeSubDevice(self, serial):
        if serial in self._subDevices:
            self._subDevices.remove(serial)

    def describe(self):
        print("  " + self._serial)
        for subdevice in self._subDevices:
            print("    " + subdevice)


class RootDevice(object):
    def __init__(self, serial, url):
        self._serial = serial
        self._url = url
        self._shields = []
        self._subDevices = []

    def getSerial(self):
        return self._serial

    def addSubDevice(self, serial):
        if serial[:7] == "YHUBSHL":
            self._shields.append(YoctoShield(serial))
        else:
            # Device to plug look if the device is plugged on a shield
            for shield in self._shields:
                if shield.addSubdevice(serial):
                    return
            self._subDevices.append(serial)

    def removeSubDevice(self, serial):
        if serial in self._subDevices:
            self._subDevices.remove(serial)
        for yoctoShield in reversed(list(self._shields)):
            if yoctoShield.getSerial() == serial:
                self._shields.remove(yoctoShield)
                break
            else:
                yoctoShield.removeSubDevice(serial)

    def describe(self):
        print(self._serial + " (" + self._url + ")")
        for subdevice in self._subDevices:
            print("  " + subdevice)
        for shield in self._shields:
            shield.describe()


__rootDevices = []


def getYoctoHub(serial):
    for rootDevice in __rootDevices:
        if rootDevice.getSerial() == serial:
            return rootDevice
    return None


def addRootDevice(serial, url):
    for rootDevice in __rootDevices:
        if rootDevice.getSerial() == serial:
            return rootDevice
    rootDevice = RootDevice(serial, url)
    __rootDevices.append(rootDevice)
    return rootDevice


def showNetwork():
    print("**** device inventory *****")
    for hub in __rootDevices:
        hub.describe()


def deviceArrival(module):
    serial = module.get_serialNumber()
    parentHub = module.get_parentHub()
    if parentHub == "":
        # root device
        url = module.get_url()
        addRootDevice(serial, url)
    else:
        hub = getYoctoHub(parentHub)
        if hub is not None:
            hub.addSubDevice(serial)


def deviceRemoval(module):
    serial = module.get_serialNumber()
    for rootDevice in reversed(list(__rootDevices)):
        rootDevice.removeSubDevice(serial)
        if rootDevice.getSerial() == serial:
            __rootDevices.remove(rootDevice)


# No exception please
YAPI.DisableExceptions()

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub error: " + str(errmsg))

if YAPI.RegisterHub("net", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub error: " + str(errmsg))

YAPI.RegisterDeviceArrivalCallback(deviceArrival)
YAPI.RegisterDeviceRemovalCallback(deviceRemoval)

print("Waiting for hubs to signal themselves...")
# wait for 5 seconds, doing nothing.
# noinspection InfiniteLoopStatement
while True:
    YAPI.UpdateDeviceList(errmsg)  # traps plug/unplug events
    YAPI.Sleep(1000, errmsg)  # traps others events
    showNetwork()
