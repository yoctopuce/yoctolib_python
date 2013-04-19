#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_datalogger import *
from datetime import *

errmsg=YRefParam()
# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

logger = YDataLogger.FirstDataLogger()
if logger is None:
    sys.stderr.write("No module with data logger found\n")
    sys.stderr.write("(Device not connected or firmware too old)\n")
    sys.exit()

sys.stdout.write("Using DataLogger of " + logger.get_module().get_serialNumber()+"\n")

dataStreams = YRefParam()
if logger.get_dataStreams(dataStreams) != YAPI.SUCCESS:
    sys.stderr.write("get_dataStreams failed \n")
    sys.exit()
sys.stdout.write(str(len(dataStreams.value)) + " stream(s) of data.\n");

for i in range(len(dataStreams.value)):
    s = dataStreams.value[i]
    sys.stdout.write("Data stream " + str(i) + ":\n")
    sys.stdout.write("- Run #" + str(s.get_runIndex())+ "\n")
    sys.stdout.write("  time = " + datetime.fromtimestamp(s.get_startTime()).strftime('%Y-%m-%d %H:%M:%S'))
    if  s.get_startTimeUTC() > 0:
        sys.stdout.write("  UTC  = " + datetime.fromtimestamp(s.get_startTimeUTC()).strftime('%Y-%m-%d %H:%M:%S')+"\n")
    else:
        sys.stdout.write("\n")

    nrows = s.get_rowCount()
    if nrows > 0:
        sys.stdout.write("- " + str(nrows) + " samples, taken every ");
        sys.stdout.write(str(s.get_dataSamplesInterval()) + " [s]\n");
        names = s.get_columnNames()
        for name in  names:
            sys.stdout.write(name + "  ");
        sys.stdout.write("\n");
        table = s.get_dataRows();
        for row in table:
            for c in row:
                sys.stdout.write(str(c) + "   ");
            sys.stdout.write("\n");
sys.stdout.write("Done. Have a nice day :)\n")



