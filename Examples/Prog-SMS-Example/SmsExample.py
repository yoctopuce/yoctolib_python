#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import math

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from array import *
from yocto_api import *
from yocto_messagebox import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')

# callback that will be invoked when a new message is received
def smsCallback(msgBox, sms):
    print('New message dated %s:' % sms.get_timestamp())
    print('  from %s' % sms.get_sender())
    print('  "%s"' % sms.get_textData())
    sms.deleteFromSIM()


errmsg = YRefParam()

if len(sys.argv) < 2:
    usage()

target = sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error: " + errmsg.value)

if target == 'any':
    # retrieve any filesystem
    mbox = YMessageBox.FirstMessageBox()
    if mbox is None:
        die('No module connected')
else:
    mbox = YMessageBox.FindMessageBox(target + ".messageBox")

if not mbox.isOnline():
    die("Module not connected ")

# list messages found on the device
print("Messages found on the SIM Card:")
messages = mbox.get_messages()
if len(messages) == 0:
    print("  No messages found")
for sms in messages:
    print('- dated %s:' % sms.get_timestamp())
    print('  from %s' % sms.get_sender())
    print('  "%s"' % sms.get_textData())

# register a callback to receive any new message
mbox.registerSmsCallback(smsCallback)

# offer to send a new message
print("To test sending SMS, provide message recipient.")
print("To skip sending, leave empty and press Enter.")
number = input("Recipient number (+xxxxxxxxxx): ")
if number:
    # if that call fails, make sure that your SIM operator
    # allows you to send SMS given your current contract
    mbox.sendTextMessage(number, "Hello from YoctoHub-GSM !")

while True:
    print("Waiting to receive SMS, press Ctrl-C to quit.")
    YAPI.Sleep(5000)

YAPI.FreeAPI()
