# ********************************************************************
#
#  $Id: svn_id $
#
#  An example that show how to use a  Yocto-RFID-14443A
#
#  You can find more information on our web site:
#   Yocto-RFID-14443A documentation:
#      https://www.yoctopuce.com/EN/products/yocto-rfid-14443a/doc.html
#   Python V2 API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_rfidreader import *
from yocto_buzzer import *
from yocto_colorledcluster import *
from yocto_anbutton import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>  ')
    print(scriptname + ' <logical_name>   ')
    print(scriptname + ' any ')
    print('Example:')
    print(scriptname + ' any ')
    sys.exit()

def die(msg):
    sys.exit(msg + ' (check USB cable)')

if len(sys.argv) < 2:
    usage()

target = sys.argv[1].upper()

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # retrieve any Buzzer
    reader = YRfidReader.FirstRfidReader()
    if reader is None:
        die('no device connected')
else:
    reader =  YRfidReader.FirstRfidReader(target)

if not (reader.isOnline()):
    die('device not connected')
serial  = reader.get_module().get_serialNumber()
led     = YColorLedCluster.FindColorLedCluster(serial + ".colorLedCluster")
button1 = YAnButton.FindAnButton(serial + ".anButton1")
buzzer  = YBuzzer.FindBuzzer(serial + ".buzzer")

led.set_rgbColor(0,1,0x000000)
buzzer.set_volume(75)
print("Place a RFID tag near the Antenna")

tagList = []
while len(tagList)<=0:
    YAPI.Sleep(250)
    tagList = reader.get_tagIdList()

tagId      = tagList[0]
opStatus   = YRfidStatus()
options    = YRfidOptions()
taginfo    = reader.get_tagInfo(tagId,opStatus)
blocksize  = taginfo.get_tagBlockSize()
firstBlock = taginfo.get_tagFirstBlock()
print("Tag ID          = "+taginfo.get_tagId())
print("Tag Memory size = "+str(taginfo.get_tagMemorySize())+" bytes")
print("Tag Block  size = "+str(taginfo.get_tagBlockSize())+" bytes")

data = reader.tagReadHex(tagId, firstBlock, 3*blocksize, options, opStatus)
if (opStatus.get_errorCode()==YRfidStatus.SUCCESS):
    print ("First 3 blocks  = "+data)
    led.set_rgbColor(0,1,0x00FF00)
    buzzer.pulse(1000,100)
else:
    print("Cannot read tag contents ("+opStatus.get_errorMessage()+")")
    led.set_rgbColor(0, 1, 0xFF0000)

led.rgb_move(0, 1, 0x000000, 200)
YAPI.FreeAPI()
