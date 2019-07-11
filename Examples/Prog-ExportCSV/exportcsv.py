#!/usr/bin/python
# -*- coding: utf-8 -*-0
import sys
import os
import time

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *


def main():
    # Setup the API to use local USB devices
    errmsg = YRefParam()
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

    # Enumerate all connected sensors
    sensorList = []
    sensor = YSensor.FirstSensor()
    while sensor is not None:
        sensorList.append(sensor)
        sensor = sensor.nextSensor()
    if len(sensorList) == 0:
        sys.exit("No Yoctopuce sensor connected (check USB cable)")

    # Generate consolidated CSV output for all sensors
    data = YConsolidatedDataSet(0, 0, sensorList)
    record = []
    while data.nextRecord(record) < 100:
        line = datetime.datetime.fromtimestamp(record[0]).isoformat()
        for idx in range(1, len(record)):
            line += ";%.3f" % record[idx]
        print(line)
    YAPI.FreeAPI()


if __name__ == '__main__':
    main()
