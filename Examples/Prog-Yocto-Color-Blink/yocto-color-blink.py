#!/usr/bin/python
# -*- coding: utf-8 -*-
# add ../../Sources to the PYTHONPATH
import sys
import os

sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *
from yocto_colorled import *


def main():
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

    led = YColorLed.FirstColorLed()
    if led is None:
        sys.exit("No led connected (check USB cable)")

    led.resetBlinkSeq()  # cleans the sequence
    led.addRgbMoveToBlinkSeq(0x00FF00, 500)  # move to green in 500 ms
    led.addRgbMoveToBlinkSeq(0x000000, 0)  # switch to black instantaneously
    led.addRgbMoveToBlinkSeq(0x000000, 250)  # stays black for 250ms
    led.addRgbMoveToBlinkSeq(0x0000FF, 0)  # switch to blue instantaneously
    led.addRgbMoveToBlinkSeq(0x0000FF, 100)  # stays blue for 100ms
    led.addRgbMoveToBlinkSeq(0x000000, 0)  # switch to black instantaneously
    led.addRgbMoveToBlinkSeq(0x000000, 250)  # stays black for 250ms
    led.addRgbMoveToBlinkSeq(0xFF0000, 0)  # switch to red instantaneously
    led.addRgbMoveToBlinkSeq(0xFF0000, 100)  # stays red for 100ms
    led.addRgbMoveToBlinkSeq(0x000000, 0)  # switch to black instantaneously
    led.addRgbMoveToBlinkSeq(0x000000, 1000)  # stays black for 1s
    led.startBlinkSeq()  # starts sequence
    print("The led is now blinking autonomously")
    YAPI.FreeAPI()

if __name__ == '__main__':
    main()
