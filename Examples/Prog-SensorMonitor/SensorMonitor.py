#!/usr/bin/python
# -*- coding: utf-8 -*-
# add ../../Sources to the PYTHONPATH
import sys
import os

sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *

#
# Object handling the collection of sensor data
#
class SensorManager:
    DATEFORMAT = "%Y-%m-%d %H:%M:%S"

    # Constructor
    def __init__(self, sensor):
        self.sensor = sensor
        self.sensorName = sensor.get_friendlyName()
        self.lastStamp = 0
        self.dataFile = self.sensorName+'.csv'

    # Take care of a new online sensor
    def handleArrival(self):
        # register a callback for getting new measurements
        self.sensor.registerTimedReportCallback(self.sensorTimedReportCallback)
        # check the timestamp of the last measurement already known
        self.lastStamp = self.getLastTimestamp()
        # whether we need to recover any measurement from the datalogger
        print("Load missing data from %s :" % self.sensorName, end='     ')
        dataset = self.sensor.get_recordedData(self.lastStamp, 0)
        dataset.loadMore()
        progress = 0
        while progress < 100:
            progress = dataset.loadMore()
            print("\b\b\b\b%3d" % progress, end='%')
        details = dataset.get_measures()
        for measure in details:
            self.appendMeasureToFile(measure)
        print(' done')

    # Take care of a sensor disconnect
    def handleRemoval(self):
        # unregister the timed report callback
        self.sensor.registerTimedReportCallback(None)

    # timed report callback, invoked automatically for each new measurement
    def sensorTimedReportCallback(self, sensor, measure):
        # make sure we never go back in the past
        if measure.get_endTimeUTC() > self.lastStamp:
            self.appendMeasureToFile(measure)

    # retrieve the last timestamp available in the data file, if any
    # (aka SELECT max(timestamp))
    def getLastTimestamp(self):
        if not os.path.exists(self.dataFile):
            return 0
        with open(self.dataFile, 'rb') as myfile:
            if os.path.getsize(self.dataFile) > 500:
                myfile.seek(-500, 2)
            lastline = myfile.readlines()[-1].decode("utf-8")
        stamp = lastline.split(';')[0]
        local = datetime.datetime.strptime(stamp, SensorManager.DATEFORMAT)
        utc = local.astimezone()
        return utc.timestamp()

    # add a new measurement to the sensor data file
    # (aka INSERT INTO)
    def appendMeasureToFile(self, measure):
        self.lastStamp = measure.get_endTimeUTC()
        utc = measure.get_endTimeUTC_asDatetime()
        stamp = utc.strftime(SensorManager.DATEFORMAT)
        value = measure.get_averageValue()
        with open(self.dataFile, 'a') as file:
            file.write("%s;%.3f\n" % (stamp, value))

# Function invoked automatically each time a device gets online
def deviceArrival(module):
    serial = module.get_serialNumber()
    print('Device online : ' + serial)
    # If this device is unknown, enumerate sensors on the device
    sensorManagers = module.get_userData()
    if sensorManagers is None:
        sensorManagers = []
        sensor = YSensor.FirstSensor()
        while sensor:
            if sensor.get_module().get_serialNumber() == serial:
                # For each sensor, create a SensorManager
                # and add it to the list
                handler = SensorManager(sensor)
                sensorManagers.append(handler)
            sensor = sensor.nextSensor()
        module.set_userData(sensorManagers)
    # Notify the SensorManager about the arrival
    for handler in sensorManagers:
        handler.handleArrival()

# Function invoked automatically each time a device gets offline
def deviceRemoval(module):
    print('Device offline : ' + module.get_serialNumber())
    sensorManagers = module.get_userData()
    for handler in sensorManagers:
        handler.handleRemoval()

# Startup code
def main():
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    # (replace "usb" by the IP address of your YoctoHub and/or
    #  add additional calls to YAPI.RegisterHub if needed)
    if YAPI.PreregisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("Init error: " + errmsg.value)

    # Use Arrival/Removal callbacks to handle hot-plug
    YAPI.RegisterDeviceArrivalCallback(deviceArrival)
    YAPI.RegisterDeviceRemovalCallback(deviceRemoval)

    print('Hit Ctrl-C to Stop')
    while True:
        YAPI.UpdateDeviceList(errmsg)  # handle plug/unplug events
        YAPI.Sleep(500, errmsg)        # handle timed reports
        # display current time continuously
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print("\b\b\b\b\b\b\b\b\b"+now, end=' ')

if __name__ == '__main__':
    main()
