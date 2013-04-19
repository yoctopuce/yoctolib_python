#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from yocto_api import *
from yocto_anbutton import *
from yocto_temperature import *
from yocto_lightsensor import *
from yocto_pressure import *
from yocto_humidity import *

def functionChange(fct,value):
    print("Change : "+str(fct)+" = "+str(value))


def deviceArrival(m):

    print('Device arrival          : ' + str(m))
    fctcount = m.functionCount()
    for  i in range(fctcount):
        fctName = m.functionId(i)
        fctFullName = m.get_serialNumber() + '.' + fctName

        # register call back for anbuttons
        if fctName.find('anButton')==0:
            bt = YAnButton.FindAnButton(fctFullName)
            if bt.isOnline():  bt.registerValueCallback(functionChange)
            print('Callback registered for : ' + fctFullName)

        # register call back for temperature
        if fctName.find('temperature')==0:
            t = YTemperature.FindTemperature(fctFullName)
            if t.isOnline() :  t.registerValueCallback(functionChange)
            print('Callback registered for : ' + fctFullName)

        # register call back for humidity
        if fctName.find('humidity')==0:
            h = YHumidity.FindHumidity(fctFullName)
            if h.isOnline() :  h.registerValueCallback(functionChange)
            print('Callback registered for : ' + fctFullName)

        # register call back for pressure
        if fctName.find('pressure')==0:
            h = YPressure.FindPressure(fctFullName)
            if h.isOnline() :  h.registerValueCallback(functionChange)
            print('Callback registered for : ' + fctFullName)

            # register call back for Light sesnor
        if fctName.find('lightSensor')==0:
            l = YLightSensor.FindLightSensor(fctFullName)
            if l.isOnline() :  l.registerValueCallback(functionChange)
            print('Callback registered for : ' + fctFullName)

        # and so on for other sensor type.....

def deviceRemoval(m):
    print('Device removal          : ' + m.get_serialNumber())


errmsg=YRefParam()

# No exception please
YAPI.DisableExceptions()

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

YAPI.RegisterDeviceArrivalCallback(deviceArrival)
YAPI.RegisterDeviceRemovalCallback(deviceRemoval)

print('Hit Ctrl-C to Stop ')

while True:
    YAPI.UpdateDeviceList(errmsg) # traps plug/unplug events
    YAPI.Sleep(500, errmsg)   # traps others events

