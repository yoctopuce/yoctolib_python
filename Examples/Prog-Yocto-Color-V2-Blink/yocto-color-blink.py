#!/usr/bin/python
# -*- coding: utf-8 -*-
# add ../../Sources to the PYTHONPATH
import sys
import os

sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *
from yocto_colorledcluster import *


def main():
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

    leds = YColorLedCluster.FirstColorLedCluster()
    if leds is None:
        sys.exit("No Color Led cluster found (check USB cable)")

    leds.resetBlinkSeq(0)  # cleans the sequence 0
    leds.addRgbMoveToBlinkSeq(0, 0x400000, 0)    # move instantaneously to red 25%
    leds.addRgbMoveToBlinkSeq(0, 0x400000, 500)  # stay on the same color for 0.5sec
    leds.addRgbMoveToBlinkSeq(0, 0x000040, 0)    # move instantaneously to red 25%
    leds.addRgbMoveToBlinkSeq(0, 0x000040, 500)  # stay on the same color for 0.5sec
    leds.linkLedToBlinkSeq(0, 1, 0, 0)           # link led 0 to sequence 0
    leds.linkLedToBlinkSeqAtPowerOn(0, 1, 0, 0)  # led 0 will wutomatically be linked to sequence 0  at startup
    leds.set_blinkSeqStateAtPowerOn(0, 1)        # sequence 0  will automatically run at startup
    leds.saveBlinkSeq(0);                        # save the sequence on flash memory

    leds.resetBlinkSeq(1)  # cleans the sequence  1
    leds.addHslMoveToBlinkSeq(1, 0x00FF20, 2000)  # Circle over all hue values
    leds.addHslMoveToBlinkSeq(1, 0x55FF20, 2000)  # Sturation =100%
    leds.addHslMoveToBlinkSeq(1, 0xAAFF20, 2000)  # luminosiy = 12%
    leds.linkLedToBlinkSeq(1, 1, 1, 0)            # link led 1 to sequence 1
    leds.linkLedToBlinkSeqAtPowerOn(1, 1, 1, 0)   # led 1 will wutomatically be linked to sequence 1  at startup
    leds.set_blinkSeqStateAtPowerOn(1, 1)         #  sequence 1  will automatically run at startup
    leds.saveBlinkSeq(1)                          # save the sequence on flash  memory

    leds.saveLedsConfigAtPowerOn();               # All leds configuration

    leds.startBlinkSeq(0)                         # start sequence 0
    leds.startBlinkSeq(1)                         # start sequence 1

    print("The leds are now blinking autonomously");
    YAPI.FreeAPI()

if __name__ == '__main__':
    main()
