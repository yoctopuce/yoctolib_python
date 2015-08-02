#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_servo import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number> <channel> position')
    print(scriptname + ' <logical_name> <channel> position')
    print(scriptname + ' any <channel> position')
    print('Example:')
    print(scriptname + ' any 2 500')
    sys.exit()

def die(msg):
    sys.exit(msg+' (check USB cable)')

if len(sys.argv)<3 :  usage()

target=sys.argv[1].upper()
channel=sys.argv[2]
position=int(sys.argv[3])

# Setup the API to use local USB devices
errmsg=YRefParam()
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

if target=='ANY':
    # retreive any servo then find its serial #
    servo = YServo.FirstServo()
    if servo is None : die('No module connected')
    m=servo.get_module()
    target = m.get_serialNumber()

print('using ' + target)
servo = YServo.FindServo(target + '.servo'+channel)

if not(servo.isOnline()):die('device not connected')

servo.move(position,1000)

