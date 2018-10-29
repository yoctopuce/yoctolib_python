# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-WatchdogDC
#
#  You can find more information on our web site:
#   Yocto-WatchdogDC documentation:
#      https://www.yoctopuce.com/EN/products/yocto-watchdogdc/doc.html
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
from yocto_watchdog import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>  [ on | off | reset]')
    print(scriptname + ' <logical_name>   [ on | off | reset]')
    print(scriptname + ' any [ on | off | reset]')
    print('Example:')
    print(scriptname + ' any on')
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
    # retreive any Watchdog
    watchdog = YWatchdog.FirstWatchdog()
    if watchdog is None: die('no device connected')
else:
    watchdog = YWatchdog.FindWatchdog(target)

if not (watchdog.isOnline()):
    die('device not connected')

if state == 'RESET':
    watchdog.resetWatchdog()
elif state == 'ON':
    watchdog.set_running(YWatchdog.RUNNING_ON)
else:
    watchdog.set_running(YWatchdog.RUNNING_OFF)
YAPI.FreeAPI()