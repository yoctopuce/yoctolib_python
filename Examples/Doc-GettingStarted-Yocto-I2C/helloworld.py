# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-SPI
#
#  You can find more information on our web site:
#   Yocto-SPI documentation:
#      https://www.yoctopuce.com/EN/products/yocto-spi/doc.html
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
from yocto_i2cport import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + " <serial_number>  <value>")
    print(scriptname + " <logical_name>   <value>")
    print(scriptname + " any  <value>   (use any discovered device)")
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 2:
    usage()
target = sys.argv[1].upper()

# Setup the API to use local USB devices. You can
# use an IP address instead of 'usb' if the device
# is connected to a network.
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    i2cPort = YI2cPort.FirstI2cPort()
    if i2cPort is None:
        sys.exit('No module connected (check cable)')
else:
    i2cPort = YI2cPort.FindI2cPort(sys.argv[1] + ".i2cPort")
    if not i2cPort.isOnline():
        sys.exit('Module not connected')

# sample code reading MCP9804 temperature sensor
i2cPort.set_i2cMode("400kbps")
i2cPort.set_voltageLevel(YI2cPort.VOLTAGELEVEL_TTL3V)
i2cPort.reset()
# do not forget to configure the powerOutput and
# of the Yocto-I2C as well if used
print("****************************")
print("* make sure voltage levels *")
print("* are properly configured  *")
print("****************************")

toSend = [0x05]
received = i2cPort.i2cSendAndReceiveArray(0x1f, toSend, 2)
tempReg = (received[0] << 8) + received[1]
if tempReg & 0x1000:
    tempReg -= 0x2000   # perform sign extension
else:
    tempReg &= 0x0fff   # clear status bits
print("Ambiant temperature: " + str(tempReg / 16.0))

YAPI.FreeAPI()
