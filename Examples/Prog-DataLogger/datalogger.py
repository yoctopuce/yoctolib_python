#!/usr/bin/python
# -*- coding: utf-8 -*-
# add ../../Sources to the PYTHONPATH
import sys
import os
import time

sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *


def dumpSensor(sensor):
    fmt = "%d %b %Y %H:%M:%S,%f"
    print("Using DataLogger of " + sensor.get_friendlyName())
    dataset = sensor.get_recordedData(0, 0)
    print("loading summary... ")
    dataset.loadMore()
    summary = dataset.get_summary()
    print("from %s to %s : min=%.3f%s avg=%.3f%s  max=%.3f%s" % (
        summary.get_startTimeUTC_asDatetime().strftime(fmt),
        summary.get_endTimeUTC_asDatetime().strftime(fmt),
        summary.get_minValue(), sensor.get_unit(),
        summary.get_averageValue(), sensor.get_unit(),
        summary.get_maxValue(), sensor.get_unit()))
    print("loading details :   0%")
    progress = 0
    while progress < 100:
        progress = dataset.loadMore()
        # print("\b\b\b\b%3d%%" % progress)
    details = dataset.get_measures()
    for measure in details:
        print("from %s to %s : min=%.3f%s avg=%.3f%s  max=%.3f%s" % (
            measure.get_startTimeUTC_asDatetime().strftime(fmt),
            measure.get_endTimeUTC_asDatetime().strftime(fmt),
            measure.get_minValue(), sensor.get_unit(),
            measure.get_averageValue(), sensor.get_unit(),
            measure.get_maxValue(), sensor.get_unit()))


def main():
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

    if len(sys.argv) == 1 or sys.argv[1] == 'any':
        sensor = YSensor.FirstSensor()
        if sensor is None:
            sys.exit("No module connected (check USB cable)")
    else:
        sensor = YSensor.FindSensor(sys.argv[0])
        if not sensor.isOnline():
            sys.exit("Sensor " + sensor.get_hardwareId() + " is not connected (check USB cable)")
    dumpSensor(sensor)
    YAPI.FreeAPI()


if __name__ == '__main__':
    main()
