# ********************************************************************
#
#  $Id: helloworld.py 55641 2023-07-26 09:43:42Z seb $
#
#  An example that show how to use a  Yocto-MaxiKnob
#
#  You can find more information on our web site:
#   Yocto-MaxiKnob documentation:
#      https://www.yoctopuce.com/EN/products/yocto-maxiknob/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
# !/usr/bin/python


from yocto_buzzer import *
from yocto_colorledcluster import *
from yocto_quadraturedecoder import *
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


def notefreq(note):
    return 220.0 * math.exp(note * math.log(2) / 12)

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
leds = YColorLedCluster.FindColorLedCluster(serial + ".colorLedCluster")
button = YAnButton.FindAnButton(serial + ".anButton1")
qd = YQuadratureDecoder.FindQuadratureDecoder(serial + ".quadratureDecoder1")

if (not button.isOnline()) or (not qd.isOnline()):
    sys.exit("Make sure the Yocto-MaxiKnob is configured with at least one AnButton and One Quadrature decoder.")

lastPos = qd.get_currentValue()
buz.set_volume(100)
qd.set_edgesPerCycle(2)

print("press button 1, or turn the encoder")
while button.isOnline():
    if button.get_isPressed() and lastPos != 0:
        lastPos = 0
        qd.set_currentValue(0)
        buz.playNotes("'E32 C8")
        leds.set_rgbColor(0, 1, 0x000000)
    else:
        p = math.floor(qd.get_currentValue())
        if lastPos != p:
            lastPos = p
            buz.pulse(notefreq(p), 250)
            leds.set_hslColor(0, 1, 0x00FF7f | (p % 255) << 16)

YAPI.FreeAPI()
