#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import math
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from array import *

from yocto_api import *
from yocto_files import *


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
    # retrieve any filesystem
    files = YFiles.FirstFiles()
    if files is None :
        die('No module connected')
else:
    files = YFiles.FindFiles(target + ".files")

if not files.isOnline():
    die("Module not connected ")

# create text files and upload them to the device
for i in range(1,5):
    contents = "This is file "+str(i)
    # convert the string to binary data
    binaryData = contents.encode("latin-1")
    # upload the file to the device
    files.upload("file"+str(i)+".txt", binaryData)

# list files found on the device
print("Files on device:")
filelist=files.get_list("*")

for i in range(len(filelist)):
    file = filelist[i]
    print('%-40s%08x    %d bytes' % (file.get_name(), file.get_crc()%0xffffffff, file.get_size()) )

# download a file
binaryData = files.download("file1.txt")

# and display
print("")
print("contents of file1.txt:")
print(binaryData.decode("latin-1"))
