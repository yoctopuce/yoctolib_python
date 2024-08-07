# ********************************************************************
#
#  $Id: helloworld.py 58233 2023-12-04 10:57:58Z seb $
#
#  An example that shows how to use a  Yocto-PowerRelay
#
#  You can find more information on our web site:
#   Yocto-PowerRelay documentation:
#      https://www.yoctopuce.com/EN/products/yocto-powerrelay/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_relay import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>  [ A | B ]')
    print(scriptname + ' <logical_name>   [ A | B ]')
    print(scriptname + ' any [ A | B ]')
    print('Example:')
    print(scriptname + ' any B')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 2:
    usage()

target = sys.argv[1].upper()
state = sys.argv[2].upper()

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # retreive any Relay
    relay = YRelay.FirstRelay()
    if relay is None:
        die('no device connected')
else:
    relay = YRelay.FindRelay(target + ".relay1")

if not (relay.isOnline()):
    die('device not connected')

if state == 'A':
    relay.set_state(YRelay.STATE_A)
else:
    relay.set_state(YRelay.STATE_B)
YAPI.FreeAPI()
