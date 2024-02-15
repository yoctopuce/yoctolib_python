# ********************************************************************
#
#  $Id: helloworld.py 58233 2023-12-04 10:57:58Z seb $
#
#  An example that shows how to use a  Yocto-MaxiBuzzer
#
#  You can find more information on our web site:
#   Yocto-MaxiBuzzer documentation:
#      https://www.yoctopuce.com/EN/products/yocto-maxibuzzer/doc.html
#   Python V2 API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_buzzer import *
from yocto_colorled import *
from yocto_anbutton import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>  ')
    print(scriptname + ' <logical_name>   ')
    print(scriptname + ' any ')
    print('Example:')
    print(scriptname + ' any ')
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
    # retrieve any Buzzer
    buz = YBuzzer.FirstBuzzer()
    if buz is None:
        die('no device connected')
else:
    buz = YBuzzer.FindBuzzer(target)

if not (buz.isOnline()):
    die('device not connected')
serial = buz.get_module().get_serialNumber()
led = YColorLed.FindColorLed(serial + ".colorLed")
button1 = YAnButton.FindAnButton(serial + ".anButton1")
button2 = YAnButton.FindAnButton(serial + ".anButton2")
print("press any of the test buttons")
while button1.isOnline():
    b1 = button1.get_isPressed()
    b2 = button2.get_isPressed()
    if b1 or b2:
        if b1:
            volume = 60
            freq = 1500
            color = 0xff0000
        else:
            volume = 30
            color = 0x00ff00
            freq = 750
        led.resetBlinkSeq()
        led.addRgbMoveToBlinkSeq(color, 100)
        led.addRgbMoveToBlinkSeq(0, 100)
        led.startBlinkSeq()
        buz.set_volume(volume)
        for i in range(5):  # this can be done using sequence as well
            buz.set_frequency(freq)
            buz.freqMove(2 * freq, 250)
            YAPI.Sleep(250, errmsg)
        buz.set_frequency(0)
        led.stopBlinkSeq()
        led.set_rgbColor(0)
YAPI.FreeAPI()
