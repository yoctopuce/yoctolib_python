# ********************************************************************
#
#  $Id: helloworld.py 58233 2023-12-04 10:57:58Z seb $
#
#  An example that shows how to use a  Yocto-Serial
#
#  You can find more information on our web site:
#   Yocto-Serial documentation:
#      https://www.yoctopuce.com/EN/products/yocto-serial/doc.html
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
from yocto_serialport import *

# Setup the API to use local USB devices. You can
# use an IP address instead of 'usb' if the device
# is connected to a network.

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if len(sys.argv) > 1:
    serialPort = YSerialPort.FindSerialPort(sys.argv[1] + ".serialPort")
    if not serialPort.isOnline():
        sys.exit('Module not connected')
else:
    serialPort = YSerialPort.FirstSerialPort()
    if serialPort is None:
        sys.exit('No module connected (check cable)')

    serialPort.set_serialMode("9600,8N1")
    serialPort.set_protocol("Line")
    serialPort.reset()

    print("****************************")
    print("* make sure voltage levels *")
    print("* are properly configured  *")
    print("****************************")

while True:
    print("Type line to send, or Ctrl-C to exit:")
    line = input(": ")  # use raw_input in python 2.x
    if line == "":
        break
    serialPort.writeLine(line)
    YAPI.Sleep(500)
    line = serialPort.readLine()
    if line != "":
        print("Received: " + line)
YAPI.FreeAPI()
