#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *
from yocto_serialport import *

# Setup the API to use local USB devices. You can
# use an IP address instead of 'usb' if the device
# is connected to a network.

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if len(sys.argv) > 1:
    serialPort = YSerialPort.FindSerialPort(sys.argv[1])
else:
    serialPort = YSerialPort.FirstSerialPort()
    if serialPort is None:
        sys.exit('No module connected (check cable)')

print("Please enter the MODBUS slave address (1...255)")
slave = 0
while (slave < 1) or (slave > 255):
    slave = int(input("slave: "))  # use raw_input in python 2.x

reg = 0
while (reg < 1) or (reg >= 50000) or (reg % 10000) == 0:
    print("Please select a Coil No (>=1), Input Bit No (>=10001),")
    print("Input Register No (>=30001) or Holding Register No (>=40001)")
    reg = int(input("No: "))  # use raw_input in python 2.x

while True:
    if reg >= 40001:
        val = serialPort.modbusReadRegisters(slave, reg - 40001, 1)[0]
    elif reg >= 30001:
        val = serialPort.modbusReadInputRegisters(slave, reg - 30001, 1)[0]
    elif reg >= 10001:
        val = serialPort.modbusReadInputBits(slave, reg - 10001, 1)[0]
    else:
        val = serialPort.modbusReadBits(slave, reg - 1, 1)[0]

    print("Current value: " + str(val))
    print("Press ENTER to read again, Q to quit")
    if (reg % 40000) < 10000:
        print(" or enter a new value")

    cmd = input(": ")  # use raw_input in python 2.x
    if (cmd == "q") or (cmd == "Q"): sys.exit()

    if cmd != "" and ((reg % 40000) < 10000):
        val = int(cmd)
        if reg >= 40001:
            serialPort.modbusWriteRegister(slave, reg - 40001, val)
        else:
            serialPort.modbusWriteBit(slave, reg - 1, val)
