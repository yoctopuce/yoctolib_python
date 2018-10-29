# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-0-10V-Tx
#
#  You can find more information on our web site:
#   Yocto-0-10V-Tx documentation:
#      https://www.yoctopuce.com/EN/products/yocto-0-10v-tx/doc.html
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
from yocto_voltageoutput import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + " <serial_number> <voltage>")
    print(scriptname + " <logical_name>  <voltage>")
    print(scriptname + " any  <voltage>    (use any discovered device)")
    print("     <voltage>: floating point number between 0.0 and 10.000")
    print('Example:')
    print(scriptname + ' any 7.5')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 4:
    usage()

target = sys.argv[1].upper()
voltage = float(sys.argv[2])

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # retreive any voltageOutput then find its serial
    vout = YVoltageOutput.FirstVoltageOutput()
    if vout is None:
        die('No module connected')
    m = vout.get_module()
    target = m.get_serialNumber()

print('using ' + target)
vout1 = YVoltageOutput.FindVoltageOutput(target + '.voltageOutput1')
vout2 = YVoltageOutput.FindVoltageOutput(target + '.voltageOutput2')

if not (vout1.isOnline()):
    die('device not connected')

# output 2 : smooth change
vout2.voltageMove(voltage, 3000)
# output 1 : immediate change
vout1.set_currentVoltage(voltage)
YAPI.FreeAPI()
