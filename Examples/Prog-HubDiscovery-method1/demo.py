#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from yocto_api import *

KnownHubs = []


def HubDiscovered(serial, url):
    global KnownHubs

    # The call-back can be called several times for the same hub
    # (the discovery technique is based on a periodic broadcast)
    # So we use a dictionnary to avoid duplicates
    if serial in KnownHubs:
        return

    print("hub found: " + serial + " (" + url + ")")
    # add the hub to the dictionnary so we won't have to
    # process is again.
    KnownHubs.append(serial)

    # connect to the hub
    msg = YRefParam()
    if YAPI.RegisterHub(url, msg) != YAPI.SUCCESS:
        print(' Ignore hub '+ serial + ' (' + msg.value +')')
        return

    #  find the hub module
    hub = YModule.FindModule(serial)

    # iterate on all functions on the module and find the ports
    fctCount = hub.functionCount()
    for i in range(fctCount):
        # retreive the hardware name of the ith function
        fctHwdName = hub.functionId(i)
        if fctHwdName[:7] == "hubPort":
            # The port logical name is always the serial#
            # of the connected device
            deviceid = hub.functionName(i)
            print("  " + fctHwdName + " : " + deviceid)


    # disconnect from the hub
    YAPI.UnregisterHub(url)


errmsg = YRefParam()
print("Waiting for hubs to signal themselves...")

# register the callback: HubDiscovered will be
# invoked each time a hub signals its presence
YAPI.RegisterHubDiscoveryCallback(HubDiscovered)

# wait for 30 seconds, doing nothing.
for j in range(30):
    YAPI.UpdateDeviceList(errmsg)
    YAPI.Sleep(1000, errmsg)
