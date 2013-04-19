#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_anbutton import *

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
    # retreive any button 
    channel = YAnButton.FirstAnButton()
    if channel is None :
        die('No module connected')
else:
    channel= YAnButton.FindAnButton(target + '.anButton1')

if not(channel.isOnline()):
    die('device not connected')
else:
    m = channel.get_module()
    channel1 =YAnButton.FindAnButton(m.get_serialNumber() + '.anButton1')
    channel5 =YAnButton.FindAnButton(m.get_serialNumber() + '.anButton2')

done = False
while not done:
    line=""
    if channel1.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        line="Button 1 pressed     "
    else:
        line="Button 1 not pressed "
    line +=' - analog value: '+str(channel1.get_calibratedValue())
    print(line)

    if channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        line="Button 5 pressed     "
    else:
        line="Button 5 not pressed "
    line +=' - analog value: '+str(channel5.get_calibratedValue())
    print(line)

    print('(press both buttons simultaneously to exit)')
    done = (channel1.get_isPressed() == YAnButton.ISPRESSED_TRUE) and \
    (channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE)
    YAPI.Sleep(1000)

