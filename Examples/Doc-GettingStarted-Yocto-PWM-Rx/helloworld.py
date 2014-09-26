#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_pwminput import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname+' <serial_number>')
    print(scriptname+' <logical_name>')
    print(scriptname+' any  ')
    sys.exit()

def die(msg):
    sys.exit(msg+' (check USB cable)')

errmsg=YRefParam()

if len(sys.argv)<2 :  usage()

target=sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

if target=='any':
    # retreive any pwm input channel
    anypwm = YPwmInput.FirstPwmInput()
    if anypwm is None :
        die('No module connected')
    m = anypwm.get_module()
    target = m.get_serialNumber()


pwm1= YPwmInput.FindPwmInput(target + '.pwmInput1')
pwm2= YPwmInput.FindPwmInput(target + '.pwmInput2')


if not(pwm1.isOnline()):die('device not connected')

while pwm1.isOnline():
    print("PWM1 : %.1fHz  %.1f%% %d   " %\
          (pwm1.get_frequency(), pwm1.get_dutyCycle(),pwm1.get_pulseCounter()))
    print("PWM2 : %.1fHz  %.1f%% %d   " %\
          (pwm2.get_frequency(), pwm2.get_dutyCycle(),pwm2.get_pulseCounter()))
    YAPI.Sleep(1000)
