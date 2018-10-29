# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-Motor-DC
#
#  You can find more information on our web site:
#   Yocto-Motor-DC documentation:
#      https://www.yoctopuce.com/EN/products/yocto-motor-dc/doc.html
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
from yocto_motor import *
from yocto_current import *
from yocto_voltage import *
from yocto_temperature import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number> power')
    print(scriptname + ' <logical_name>power')
    print(scriptname + ' any <channel> power')
    print('power is an integer between -100 and 100%')
    print('Example:')
    print(scriptname + ' any 75')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


# parse the command line


if len(sys.argv) < 3:
    usage()
target = sys.argv[1].upper()
power = int(sys.argv[2])

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # find any motor then retreive its serial #
    motor = YMotor.FirstMotor()
    if motor is None:
        die('No module connected')
    m = motor.get_module()
    target = m.get_serialNumber()
    print('using ' + target)

motor = YMotor.FindMotor(target + '.motor')
current = YCurrent.FindCurrent(target + '.current')
voltage = YVoltage.FindVoltage(target + '.voltage')
temperature = YTemperature.FindTemperature(target + '.temperature')

if motor.isOnline():
    # if the motor is in error state, reset it.
    if motor.get_motorStatus() >= YMotor.MOTORSTATUS_LOVOLT:  motor.resetStatus()
    motor.drivingForceMove(power, 2000)  # ramp up to power in 2 seconds
    while motor.isOnline():
        print("Status :  " + motor.get_advertisedValue() +
              " Current : " + "%2.1f" % (current.get_currentValue() / 1000) + "A  " + \
              "Voltage : " + "%2.1f" % (voltage.get_currentValue()) + "V  " + \
              "Temperature : " + "%2.1f" % (temperature.get_currentValue()) + "deg C")
        YAPI.Sleep(1000, errmsg)
else:
    die('device not connected')
YAPI.FreeAPI()
