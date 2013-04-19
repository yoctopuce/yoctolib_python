#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_relay import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number> <channel> [ ON | OFF ]')
    print(scriptname + ' <logical_name> <channel>  [ ON | OFF ]')
    print(scriptname + ' any <channel> [ ON | OFF ]')
    print('Example:')
    print(scriptname + ' any 2 ON')
    sys.exit()

def die(msg):
    sys.exit(msg+' (check USB cable)')

if len(sys.argv)<3 :  usage()

target=sys.argv[1].upper()
channel=sys.argv[2]
state=sys.argv[3].upper()

# Setup the API to use local USB devices
errmsg=YRefParam()
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

if target=='ANY':
    # retreive any Relay then find its serial #
    relay = YRelay.FirstRelay()
    if relay is None : die('No module connected')
    m=relay.get_module()
    target = m.get_serialNumber()

print('using ' + target)
relay = YRelay.FindRelay(target + '.relay'+channel)

if not(relay.isOnline()):die('device not connected')

if relay.isOnline():
    if state == 'ON' :
        relay.set_output(YRelay.OUTPUT_ON)
    else:
        relay.set_output(YRelay.OUTPUT_OFF)
else:
    die('Module not connected')