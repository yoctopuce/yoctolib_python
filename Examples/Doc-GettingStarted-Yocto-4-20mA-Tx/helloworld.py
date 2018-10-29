# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-4-20mA-Tx
#
#  You can find more information on our web site:
#   Yocto-4-20mA-Tx documentation:
#      https://www.yoctopuce.com/EN/products/yocto-4-20ma-tx/doc.html
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
from yocto_currentloopoutput import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number> value')
    print(scriptname + ' <logical_name> value')
    print(scriptname + ' any value ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


errmsg = YRefParam()

if len(sys.argv) < 3:
    usage()

target = sys.argv[1]
value = float(sys.argv[2])

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any currentLoopOutput
    loop = YCurrentLoopOutput.FirstCurrentLoopOutput()
    if loop is None:
        die('No module connected')
else:
    loop = YCurrentLoopOutput.FindCurrentLoopOutput(target + '.currentLoopOutput')

# we need to retreive the second loop from the device
if not loop.isOnline(): die('device not connected')

loop.set_current(value)

loopPower = loop.get_loopPower()

if loopPower == YCurrentLoopOutput.LOOPPOWER_NOPWR:
    print("Current loop not powered")
elif loopPower == YCurrentLoopOutput.LOOPPOWER_NOPWR:
    print("Insufficient voltage on current loop")
else:
    sys.exit("current loop set to " + str(value) + " mA")
YAPI.FreeAPI()
