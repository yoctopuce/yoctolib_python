#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_temperature import *

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
    # retreive any temperature sensor
    sensor = YTemperature.FirstTemperature()
    if sensor is None :
        die('No module connected')
else:
    sensor= YTemperature.FindTemperature(target + '.temperature1')

if not(sensor.isOnline()):die('device not connected')

# retreive module serial
serial=sensor.get_module().get_serialNumber()


# retreive both channels
channel1 = YTemperature.FindTemperature(serial + '.temperature1')
channel2 = YTemperature.FindTemperature(serial + '.temperature2')

while True:
    print("channel 1/2:  "+ "%2.1f / " % channel1.get_currentValue() + \
                            "%2.1f" % channel2.get_currentValue() + \
                            " deg C (Ctrl-C to stop)")
    YAPI.Sleep(1000)
