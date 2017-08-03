#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_cellular import *
from yocto_network import *
from yocto_wireless import *

errmsg = YRefParam()

# Setup the API to use local USB devices
if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + str(errmsg))


def getSubnetLen(subnet):
    split = subnet.split('.')
    subnet_int = (16777216 * int(split[0])) \
                 + (65536 * int(split[1])) \
                 + (256 * int(split[2])) \
                 + int(split[3])
    i = 0
    while (subnet_int & (1 << i)) == 0:
        i += 1
    return 32 - i


def configureNetwork(serial, useDHCP=True, ip="",
                     subnet="", gateway="", dns1="", dns2=""):
    print("Configure network function of " + serial)
    network = YNetwork.FindNetwork(serial + ".network")
    if not network.isOnline():
        print("Not a YoctoHub")
        return
    if useDHCP:
        print(" - Use DHCP")
        network.useDHCPauto()
    else:
        subnet_len = getSubnetLen(subnet)
        print(" - Use Static ip %s with subnet=%d  gateway=%s)" %
              (ip, subnet_len, gateway))
        network.useStaticIP(ip, subnet_len, gateway)
        network.set_primaryDNS(dns1)
        network.set_secondaryDNS(dns2)
    readiness = network.get_readiness()
    old_readiness = YNetwork.READINESS_INVALID
    while readiness != YNetwork.READINESS_LAN_OK and \
                    readiness != YNetwork.READINESS_WWW_OK:
        YAPI.Sleep(500)
        if old_readiness != readiness:
            if readiness == YNetwork.READINESS_DOWN:
                print(" - Network is down")
            if readiness == YNetwork.READINESS_EXISTS:
                print(" - Network exists")
            if readiness == YNetwork.READINESS_LINKED:
                print(" - Network is linked")
            if readiness == YNetwork.READINESS_LAN_OK:
                print(" - Network is LAN ready")
            if readiness == YNetwork.READINESS_WWW_OK:
                print(" - Network has Internet access")
            old_readiness = readiness
        readiness = network.get_readiness()
    print("Network interface is ready and can be accessed with the IP %s." %
          (network.get_ipAddress()))
    # do not forget to call saveToFlash() to make these settings persistent


def configureWireless(serial, ssid, passkey="", useDHCP=True, ip="", subnet="",
                      gateway="", dns1="", dns2=""):
    print("Configure Wireless for " + serial)
    wireless = YWireless.FindWireless(serial + ".wireless")
    network = YNetwork.FindNetwork(serial + ".network")
    if not wireless.isOnline() or not network.isOnline():
        print("Not a wireless YoctoHub")
        return
    if wireless.get_wlanState() == YWireless.WLANSTATE_INVALID:
        print("YoctoHub " + serial + " is too old. ")
        print("please the firmware to use this function")
        return

    # set wireless settings
    wireless.joinNetwork(ssid, passkey)
    # set IP settings
    if useDHCP:
        print(" - Use DHCP")
        network.useDHCPauto()
    else:
        subnet_len = getSubnetLen(subnet)
        print(" - Use Static ip %s with  subnet=%d and gateway =%s)" %
              (ip, subnet_len, gateway))
        network.useStaticIP(ip, subnet_len, gateway)
        network.set_primaryDNS(dns1)
        network.set_secondaryDNS(dns2)
    # ensure that the wireless settings are correct
    last_message = ""
    networkState = wireless.get_wlanState()
    while networkState != YWireless.WLANSTATE_CONNECTED and \
                    networkState != YWireless.WLANSTATE_REJECTED:
        message = wireless.get_message()
        if last_message != message:
            print(" - " + message)
            last_message = message
        YAPI.Sleep(500)
        networkState = wireless.get_wlanState()
    if networkState == YWireless.WLANSTATE_REJECTED:
        print("Unable to connect to %s network : %s" %
              (ssid, wireless.get_message()))
        return
    readiness = network.get_readiness()
    old_readiness = YNetwork.READINESS_INVALID
    while readiness != YNetwork.READINESS_LAN_OK and \
                    readiness != YNetwork.READINESS_WWW_OK:
        if old_readiness != readiness:
            if readiness == YNetwork.READINESS_DOWN:
                print(" - Network is down")
            if readiness == YNetwork.READINESS_EXISTS:
                print(" - Network exists")
            if readiness == YNetwork.READINESS_LINKED:
                print(" - Network is linked")
            if readiness == YNetwork.READINESS_LAN_OK:
                print(" - Network is LAN ready OK")
            if readiness == YNetwork.READINESS_WWW_OK:
                print(" - Network as WWW ready")
            old_readiness = readiness
        YAPI.Sleep(500)
        readiness = network.get_readiness()

    print("Wireless interface ready and can be accessed with the IP %s (link=%d%%)." %
          (network.get_ipAddress(), wireless.get_linkQuality()))
    # do not forget to call saveToFlash() to make these settings persistent


def getAvailableWirelessNetwork(serial):
    print("Scan available wireless network from " + serial)
    wireless = YWireless.FindWireless(serial + ".wireless")
    if not wireless.isOnline():
        print("Not a wireless YoctoHub")
        return
    if wireless.get_wlanState() == YWireless.WLANSTATE_INVALID:
        print("YoctoHub " + serial + " is too old. ")
        print("please the firmware to use this function")
        return
    wireless.startWlanScan()
    networkState = wireless.get_wlanState()
    last_message = ""
    while networkState == YWireless.WLANSTATE_DOWN or \
                    networkState == YWireless.WLANSTATE_SCANNING:
        message = wireless.get_message()
        if last_message != message:
            print(" - %s" % message)
            last_message = message
        YAPI.Sleep(100)
        networkState = wireless.get_wlanState()
    wlans = wireless.get_detectedWlans()
    print("Detected networks:")
    for wl in wlans:
        assert isinstance(wl, YWlanRecord)
        print(" - ssid:%s channel:%d quality:%d security:%s" %
              (wl.get_ssid(), wl.get_channel(), wl.get_linkQuality(), wl.get_security()))


def configureCelluar(serial, pin_number="", operator="", apn_host="", apn_user="", apn_pass="",
                     data_mode=YCellular.ENABLEDATA_HOMENETWORK):
    print("Configure Cellular for " + serial)
    cellular = YCellular.FindCellular(serial + ".cellular")
    network = YNetwork.FindNetwork(serial + ".network")

    cellular.set_pin(pin_number)
    cellular.set_lockedOperator(operator)
    cellular.set_apn(apn_host)
    cellular.set_apnAuth(apn_user, apn_pass)
    cellular.set_enableData(data_mode)
    readiness = network.get_readiness()
    old_msg = ""
    while readiness != YNetwork.READINESS_WWW_OK:
        if readiness == YNetwork.READINESS_DOWN:
            msg = " - Network is down (%s)" % cellular.get_message()
        elif readiness == YNetwork.READINESS_EXISTS:
            msg = " - Network exists (%s)" % (cellular.get_message())
        elif readiness == YNetwork.READINESS_LINKED:
            msg = " - Network is linked (%s:%s)" % \
                  (cellular.get_cellOperator(), cellular.get_message())
        elif readiness == YNetwork.READINESS_LAN_OK:
            msg = " - Network is LAN ready (%s:%s)" % \
                  (cellular.get_cellOperator(), cellular.get_message())
        elif readiness == YNetwork.READINESS_WWW_OK:
            msg = " - Network has Internet access (%s:%s)" % \
                  (cellular.get_cellOperator(), cellular.get_message())
        if msg != old_msg:
            print(msg)
            old_msg = msg
        YAPI.Sleep(100)
        readiness = network.get_readiness()
    print("Network interface is ready and can be accessed with the IP %s." %
          (network.get_ipAddress()))


# do not forget to call saveToFlash() to make these settings persistent



m = YModule.FirstModule()
while m is not None:
    serial_number = m.get_serialNumber()
    print()
    print(serial_number + ' (' + m.get_productName() + ')')
    if m.hasFunction("wireless"):
        # getAvailableWirelessNetwork(serial_number)
        configureWireless(serial_number, "SWEETSHORTWPA")
    elif m.hasFunction("cellular"):
        configureCelluar(serial_number)
    elif m.hasFunction("network"):
        configureNetwork(serial_number)
    m.saveToFlash()
    m = m.nextModule()

YAPI.FreeAPI()
