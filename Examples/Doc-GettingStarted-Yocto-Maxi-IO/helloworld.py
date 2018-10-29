# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Maxi-IO
#
#  You can find more information on our web site:
#   Yocto-Maxi-IO documentation:
#      https://www.yoctopuce.com/EN/products/yocto-maxi-io/doc.html
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
from yocto_digitalio import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any')
    print('Example:')
    print(scriptname + ' any')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 2:
    usage()
target = sys.argv[1].upper()

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # retreive any Relay then find its serial #
    io = YDigitalIO.FirstDigitalIO()
    if io is None:
        die('No module connected')
    m = io.get_module()
    target = m.get_serialNumber()

print('using ' + target)
io = YDigitalIO.FindDigitalIO(target + '.digitalIO')

if not (io.isOnline()):
    die('device not connected')

# lets configure the channels direction
# bits 0..3 as output
# bits 4..7 as input
io.set_portDirection(0x0F)
io.set_portPolarity(0)  # polarity set to regular
io.set_portOpenDrain(0)  # No open drain

print("Channels 0..3 are configured as outputs and channels 4..7")
print("are configured as inputs, you can connect some inputs to ")
print("ouputs and see what happens")

outputdata = 0
while io.isOnline():
    inputdata = io.get_portState()  # read port values
    line = ""  # display part state value as binary
    for i in range(0, 8):
        if (inputdata & (128 >> i)) > 0:
            line += '1'
        else:
            line += '0'
    print(" port value = " + line)
    outputdata = (outputdata + 1) % 16  # cycle ouput 0..15
    io.set_portState(outputdata)  # We could have used set_bitState as well
    YAPI.Sleep(1000, errmsg)

print("Module disconnected")
YAPI.FreeAPI()
