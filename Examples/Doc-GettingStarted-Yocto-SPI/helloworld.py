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
from yocto_spiport import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + " <serial_number>  <value>")
    print(scriptname + " <logical_name>   <value>")
    print(scriptname + " any  <value>   (use any discovered device)")
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 3:
    usage()
target = sys.argv[1].upper()
value = int(sys.argv[2])

# Setup the API to use local USB devices. You can
# use an IP address instead of 'usb' if the device
# is connected to a network.
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    spiPort = YSpiPort.FirstSpiPort()
    if spiPort is None:
        sys.exit('No module connected (check cable)')
else:
    spiPort = YSpiPort.FindSpiPort(sys.argv[1] + ".spiPort")
    if not spiPort.isOnline():
        sys.exit('Module not connected')

# sample code driving MAX7219 7-segment display driver
# such as SPI7SEGDISP8.56 from www.embedded-lab.com
spiPort.set_spiMode("250000,3,msb")
spiPort.set_ssPolarity(YSpiPort.SSPOLARITY_ACTIVE_LOW)
spiPort.set_protocol("Frame:5ms")
spiPort.reset()

# do not forget to onfigure the powerOutput of the Yocto - SPI
# (for SPI7SEGDISP8.56 powerOutput need to be set at 5v)
print("****************************")
print("* make sure voltage levels *")
print("* are properly configured  *")
print("****************************")

# initialize MAX7219
spiPort.writeHex('0c01')  # Exit from shutdown state
spiPort.writeHex('09ff')  # Enable BCD for all digits
spiPort.writeHex('0b07')  # Enable digits 0-7 (=8 in total)
spiPort.writeHex('0a0a')  # Set medium brightness
for i in range(1, 9):
    digit = value % 10
    spiPort.writeArray([i, digit])
    value = int(value / 10)

YAPI.FreeAPI()
