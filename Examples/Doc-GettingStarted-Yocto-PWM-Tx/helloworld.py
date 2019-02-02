# ********************************************************************
#
#  $Id: helloworld.py 34161 2019-01-28 14:41:40Z mvuilleu $
#
#  An example that show how to use a  Yocto-PWM-Tx
#
#  You can find more information on our web site:
#   Yocto-PWM-Tx documentation:
#      https://www.yoctopuce.com/EN/products/yocto-pwm-tx/doc.html
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
from yocto_pwmoutput import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + " <serial_number>  <frequency> <duty_cycle>")
    print(scriptname + " <logical_name> <frequency> <duty_cycle>")
    print(scriptname + " any  <frequency> <duty_cycle>   (use any discovered device)")
    print("     <frequency>: integer between 1Hz and 1000000Hz")
    print("     <duty_cycle>: floating point number between 0.0 and 100.0")
    print('Example:')
    print(scriptname + ' any 1000 22.5')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 4:
    usage()

target = sys.argv[1].upper()
frequency = int(sys.argv[2])
duty_cycle = float(sys.argv[3])

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # retreive any pwmoutput then find its serial #
    pwmoutput = YPwmOutput.FirstPwmOutput()
    if pwmoutput is None:
        die('No module connected')
    m = pwmoutput.get_module()
    target = m.get_serialNumber()

print('using ' + target)
pwmoutput1 = YPwmOutput.FindPwmOutput(target + '.pwmOutput1')
pwmoutput2 = YPwmOutput.FindPwmOutput(target + '.pwmOutput2')

if not (pwmoutput1.isOnline()):
    die('device not connected')

# output 2 : smooth change
pwmoutput2.set_frequency(frequency)
pwmoutput2.set_enabled(YPwmOutput.ENABLED_TRUE)
pwmoutput2.dutyCycleMove(duty_cycle, 3000)
# output 1 : immediate change
pwmoutput1.set_frequency(frequency)
pwmoutput1.set_enabled(YPwmOutput.ENABLED_TRUE)
pwmoutput1.set_dutyCycle(duty_cycle)
YAPI.FreeAPI()
