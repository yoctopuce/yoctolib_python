#*********************************************************************
#*
#* $Id: yocto_datalogger.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindDataLogger(), the high-level API for DataLogger
#*
#* - - - - - - - - - License information: - - - - - - - - - 
#*
#*  Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#*
#*  Yoctopuce Sarl (hereafter Licensor) grants to you a perpetual
#*  non-exclusive license to use, modify, copy and integrate this
#*  file into your software for the sole purpose of interfacing 
#*  with Yoctopuce products. 
#*
#*  You may reproduce and distribute copies of this file in 
#*  source or object form, as long as the sole purpose of this
#*  code is to interface with Yoctopuce products. You must retain 
#*  this notice in the distributed source file.
#*
#*  You should refer to Yoctopuce General Terms and Conditions
#*  for additional information regarding your rights and 
#*  obligations.
#*
#*  THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#*  WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING 
#*  WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS 
#*  FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#*  EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#*  INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, 
#*  COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR 
#*  SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT 
#*  LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#*  CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#*  BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#*  WARRANTY, OR OTHERWISE.
#*
#*********************************************************************/

__docformat__ = 'restructuredtext en'
from yocto_api import *


#--- (generated code: YDataLogger class start)
#noinspection PyProtectedMember
class YDataLogger(YFunction):
    """
    Yoctopuce sensors include a non-volatile memory capable of storing ongoing measured
    data automatically, without requiring a permanent connection to a computer.
    The DataLogger function controls the global parameters of the internal data
    logger.

    """
#--- (end of generated code: YDataLogger class start)

    Y_DATA_INVALID = YAPI.INVALID_DOUBLE

    #--- (generated code: YDataLogger definitions)
    CURRENTRUNINDEX_INVALID = YAPI.INVALID_UINT
    TIMEUTC_INVALID = YAPI.INVALID_LONG
    RECORDING_OFF = 0
    RECORDING_ON = 1
    RECORDING_INVALID = -1
    AUTOSTART_OFF = 0
    AUTOSTART_ON = 1
    AUTOSTART_INVALID = -1
    BEACONDRIVEN_OFF = 0
    BEACONDRIVEN_ON = 1
    BEACONDRIVEN_INVALID = -1
    CLEARHISTORY_FALSE = 0
    CLEARHISTORY_TRUE = 1
    CLEARHISTORY_INVALID = -1
    #--- (end of generated code: YDataLogger definitions)

    def __init__(self, func):
        super(YDataLogger, self).__init__(func)
        self._className = "DataLogger"
        #--- (generated code: YDataLogger attributes)
        self._callback = None
        self._currentRunIndex = YDataLogger.CURRENTRUNINDEX_INVALID
        self._timeUTC = YDataLogger.TIMEUTC_INVALID
        self._recording = YDataLogger.RECORDING_INVALID
        self._autoStart = YDataLogger.AUTOSTART_INVALID
        self._beaconDriven = YDataLogger.BEACONDRIVEN_INVALID
        self._clearHistory = YDataLogger.CLEARHISTORY_INVALID
        #--- (end of generated code: YDataLogger attributes)
        self._dataLoggerURL = ""

    #--- (generated code: YDataLogger implementation)
    def _parseAttr(self, member):
        if member.name == "currentRunIndex":
            self._currentRunIndex = member.ivalue
            return 1
        if member.name == "timeUTC":
            self._timeUTC = member.ivalue
            return 1
        if member.name == "recording":
            self._recording = member.ivalue
            return 1
        if member.name == "autoStart":
            self._autoStart = member.ivalue
            return 1
        if member.name == "beaconDriven":
            self._beaconDriven = member.ivalue
            return 1
        if member.name == "clearHistory":
            self._clearHistory = member.ivalue
            return 1
        super(YDataLogger, self)._parseAttr(member)

    def get_currentRunIndex(self):
        """
        Returns the current run number, corresponding to the number of times the module was
        powered on with the dataLogger enabled at some point.

        @return an integer corresponding to the current run number, corresponding to the number of times the module was
                powered on with the dataLogger enabled at some point

        On failure, throws an exception or returns YDataLogger.CURRENTRUNINDEX_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YDataLogger.CURRENTRUNINDEX_INVALID
        return self._currentRunIndex

    def get_timeUTC(self):
        """
        Returns the Unix timestamp for current UTC time, if known.

        @return an integer corresponding to the Unix timestamp for current UTC time, if known

        On failure, throws an exception or returns YDataLogger.TIMEUTC_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YDataLogger.TIMEUTC_INVALID
        return self._timeUTC

    def set_timeUTC(self, newval):
        """
        Changes the current UTC time reference used for recorded data.

        @param newval : an integer corresponding to the current UTC time reference used for recorded data

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("timeUTC", rest_val)

    def get_recording(self):
        """
        Returns the current activation state of the data logger.

        @return either YDataLogger.RECORDING_OFF or YDataLogger.RECORDING_ON, according to the current
        activation state of the data logger

        On failure, throws an exception or returns YDataLogger.RECORDING_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YDataLogger.RECORDING_INVALID
        return self._recording

    def set_recording(self, newval):
        """
        Changes the activation state of the data logger to start/stop recording data.

        @param newval : either YDataLogger.RECORDING_OFF or YDataLogger.RECORDING_ON, according to the
        activation state of the data logger to start/stop recording data

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("recording", rest_val)

    def get_autoStart(self):
        """
        Returns the default activation state of the data logger on power up.

        @return either YDataLogger.AUTOSTART_OFF or YDataLogger.AUTOSTART_ON, according to the default
        activation state of the data logger on power up

        On failure, throws an exception or returns YDataLogger.AUTOSTART_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YDataLogger.AUTOSTART_INVALID
        return self._autoStart

    def set_autoStart(self, newval):
        """
        Changes the default activation state of the data logger on power up.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : either YDataLogger.AUTOSTART_OFF or YDataLogger.AUTOSTART_ON, according to the
        default activation state of the data logger on power up

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("autoStart", rest_val)

    def get_beaconDriven(self):
        """
        Return true if the data logger is synchronised with the localization beacon.

        @return either YDataLogger.BEACONDRIVEN_OFF or YDataLogger.BEACONDRIVEN_ON

        On failure, throws an exception or returns YDataLogger.BEACONDRIVEN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YDataLogger.BEACONDRIVEN_INVALID
        return self._beaconDriven

    def set_beaconDriven(self, newval):
        """
        Changes the type of synchronisation of the data logger.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : either YDataLogger.BEACONDRIVEN_OFF or YDataLogger.BEACONDRIVEN_ON, according to
        the type of synchronisation of the data logger

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("beaconDriven", rest_val)

    def get_clearHistory(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YDataLogger.CLEARHISTORY_INVALID
        return self._clearHistory

    def set_clearHistory(self, newval):
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("clearHistory", rest_val)

    @staticmethod
    def FindDataLogger(func):
        """
        Retrieves a data logger for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the data logger is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YDataLogger.isOnline() to test if the data logger is
        indeed online at a given time. In case of ambiguity when looking for
        a data logger by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the data logger

        @return a YDataLogger object allowing you to drive the data logger.
        """
        # obj
        obj = YFunction._FindFromCache("DataLogger", func)
        if obj is None:
            obj = YDataLogger(func)
            YFunction._AddToCache("DataLogger", func, obj)
        return obj

    def forgetAllDataStreams(self):
        """
        Clears the data logger memory and discards all recorded data streams.
        This method also resets the current run index to zero.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_clearHistory(YDataLogger.CLEARHISTORY_TRUE)

    def get_dataSets(self):
        """
        Returns a list of YDataSet objects that can be used to retrieve
        all measures stored by the data logger.

        This function only works if the device uses a recent firmware,
        as YDataSet objects are not supported by firmwares older than
        version 13000.

        @return a list of YDataSet object.

        On failure, throws an exception or returns an empty list.
        """
        return self.parse_dataSets(self._download("logger.json"))

    def parse_dataSets(self, json):
        dslist = []
        res = []
        # // may throw an exception
        dslist = self._json_get_array(json)
        del res[:]
        for y in dslist:
            res.append(YDataSet(self, y))
        return res

    def nextDataLogger(self):
        """
        Continues the enumeration of data loggers started using yFirstDataLogger().

        @return a pointer to a YDataLogger object, corresponding to
                a data logger currently online, or a None pointer
                if there are no more data loggers to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YDataLogger.FindDataLogger(hwidRef.value)

#--- (end of generated code: YDataLogger implementation)

    def getData(self, runIdx, timeIdx, jsondataRef):
        devRef = YRefParam()
        errmsgRef = YRefParam()
        bufferRef = YRefParam()
        if self._dataLoggerURL == "":
            self._dataLoggerURL = "/logger.json"

        # Resolve our reference to our device, load REST API
        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res
        if timeIdx > 0:
            query = "GET " + self._dataLoggerURL + "?run=" + str(runIdx) + "&time=" + str(timeIdx) + " HTTP/1.1\r\n\r\n"
        else:
            query = "GET " + self._dataLoggerURL + " HTTP/1.1\r\n\r\n"
        res = devRef.value.HTTPRequest(query, bufferRef, errmsgRef)
        if YAPI.YISERR(res):
            res = YAPI.UpdateDeviceList(errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res
            res = devRef.value.HTTPRequest("GET " + self._dataLoggerURL + " HTTP/1.1\n\r\n\r", bufferRef, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res
        try:
            jsondataRef.value = YAPI.TJsonParser(bufferRef.value)
        except YAPI.JsonError as e:
            if not errmsgRef is None:
                errmsgRef.value = "unexpected JSON structure: " + e.msg
            return YAPI.IO_ERROR
        if jsondataRef.value.httpcode == 404 and self._dataLoggerURL != "/dataLogger.json":
            # retry using backward-compatible datalogger URL
            self._dataLoggerURL = "/dataLogger.json"
            return self.getData(runIdx, timeIdx, jsondataRef)

        return YAPI.SUCCESS

    def get_dataStreams(self, v):
        """
        Builds a list of all data streams hold by the data logger (legacy method).
        The caller must pass by reference an empty array to hold YDataStream
        objects, and the function fills it with objects describing available
        data sequences.

        This is the old way to retrieve data from the DataLogger.
        For new applications, you should rather use get_dataSets()
        method, or call directly get_recordedData() on the
        sensor object.

        @param v : an array of YDataStream objects to be filled in

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        jRef = YRefParam()
        v.value = []
        res = self.getData(0, 0, jRef)
        if res != YAPI.SUCCESS:
            return res

        root = jRef.value.GetRootNode()
        if len(root.items) == 0:
            return YAPI.SUCCESS
        if root.items[0].recordtype == YAPI.TJSONRECORDTYPE.JSON_ARRAY:
            for i in range(len(root.items)):
                # old datalogger format: [runIdx, timerel, utc, interval]
                el = root.items[i]
                v.value.append(
                    YOldDataStream(self, el.items[0].ivalue,
                                   el.items[1].ivalue, el.items[2].ivalue, el.items[3].ivalue))
        elif root.items[0].recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
            # new datalogger format: {"id":"...","unit":"...","streams":["...",...]}
            json_buffer = jRef.value.convertToString(root, False)
            sets = self.parse_dataSets(YString2Byte(json_buffer))
            for curset in sets:
                ds = curset.get_privateDataStreams()
                for si in ds:
                    # return a user-owned copy
                    v.value.append(si)
        return YAPI.SUCCESS

    #--- (generated code: DataLogger functions)

    @staticmethod
    def FirstDataLogger():
        """
        Starts the enumeration of data loggers currently accessible.
        Use the method YDataLogger.nextDataLogger() to iterate on
        next data loggers.

        @return a pointer to a YDataLogger object, corresponding to
                the first data logger currently online, or a None pointer
                if there are none.
        """
        devRef = YRefParam()
        neededsizeRef = YRefParam()
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        errmsgRef = YRefParam()
        size = YAPI.C_INTSIZE
        #noinspection PyTypeChecker,PyCallingNonCallable
        p = (ctypes.c_int * 1)()
        err = YAPI.apiGetFunctionsByClass("DataLogger", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YDataLogger.FindDataLogger(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: DataLogger functions)


class YOldDataStream(YDataStream):

    def __init__(self, parent, run, stamp, utc, itv):
        super(YOldDataStream, self).__init__(parent)
        self._dataLogger = parent
        self._runNo = run
        self._timeStamp = stamp
        self._utcStamp = utc
        self._interval = itv
        self._samplesPerHour = 3600 / self._interval
        self._isClosed = 1
        self._minVal = self.DATA_INVALID
        self._avgVal = self.DATA_INVALID
        self._maxVal = self.DATA_INVALID

    def get_startTime(self):
        """
        Returns the relative start time of the data stream, measured in seconds.
        For recent firmwares, the value is relative to the present time,
        which means the value is always negative.
        If the device uses a firmware older than version 13000, value is
        relative to the start of the time the device was powered on, and
        is always positive.
        If you need an absolute UTC timestamp, use get_startTimeUTC().
        
        @return an unsigned number corresponding to the number of seconds
                between the start of the run and the beginning of this data
                stream.
        """
        return self._timeStamp

    def get_dataSamplesInterval(self):
        """
        Returns the number of seconds elapsed between  two consecutive
        rows of this data stream. By default, the data logger records one row
        per second, but there might be alternative streams at lower resolution
        created by summarizing the original stream for archiving purposes.
        
        This method does not cause any access to the device, as the value
        is preloaded in the object at instantiation time.
        
        @return an unsigned number corresponding to a number of seconds.
        """
        return self._interval

    def loadStream(self):
        jsonRef = YRefParam()
        coldiv = []
        coltype = []
        udat = []
        colscl = []
        colofs = []
        c = 0
        x = 0
        y = 0
        res = self._dataLogger.getData(self._runNo, self._timeStamp, jsonRef)
        if res != YAPI.SUCCESS:
            return res
        self._nRows = 0
        self._nCols = 0
        del self._columnNames[:]
        self._values = [[]]
        root = jsonRef.value.GetRootNode()
        for i in range(len(root.members)):
            el = root.members[i]
            name = el.name
            if name == "time":
                self._timeStamp = el.ivalue
            elif name == "UTC":
                self._utcStamp = el.ivalue
            elif name == "interval":
                self._interval = el.ivalue
            elif name == "nRows":
                self._nRows = el.ivalue
            elif name == "keys":
                if not self._nCols:
                    self._nCols = len(el.items)
                for j in range(self._nCols):
                    self._columnNames.append(el.items[j].svalue)
            elif name == "div":
                if not self._nCols:
                    self._nCols = len(el.items)
                for j in range(self._nCols):
                    coldiv.append(el.items[j].ivalue)
            elif name == "type":
                if not self._nCols:
                    self._nCols = len(el.items)
                for j in range(self._nCols):
                    coltype.append(el.items[j].ivalue)
            elif name == "scal":
                if not self._nCols:
                    self._nCols = len(el.items)
                for j in range(self._nCols):
                    colscl.append(el.items[j].ivalue / 65536.0)
                    if coltype[j]:
                        colofs.append(-32767)
                    else:
                        colofs.append(0)
            elif name == "data":
                if len(colscl) <= 0:
                    for j in range(self._nCols):
                        colscl.append(1.0 / coldiv[j])
                        if coltype[j]:
                            colofs[j] = -32767
                        else:
                            colofs[j] = 0

                del udat[:]
                if el.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRING:
                    sdat = el.svalue
                    p = 0
                    while p < len(sdat):
                        c = sdat[p]
                        p += 1
                        if c >= 'a':
                            srcpos = int(len(udat) - 1 - (ord(c) - ord('a')))
                            if srcpos < 0:
                                #noinspection PyProtectedMember
                                self._dataLogger._throw(YAPI.IO_ERROR, "Unexpected JSON reply format")
                                return YAPI.IO_ERROR
                            val = udat[srcpos]
                        else:
                            if p + 2 > len(sdat):
                                #noinspection PyProtectedMember
                                self._dataLogger._throw(YAPI.IO_ERROR, "Unexpected JSON reply format")
                                return YAPI.IO_ERROR

                            val = (ord(c) - ord('0'))
                            c = sdat[p]
                            p += 1
                            val += (ord(c) - ord('0')) << 5
                            c = sdat[p]
                            p += 1
                            if c == 'z':
                                c = "\\"
                            val += (ord(c) - ord('0')) << 10
                        udat.append(val)
                else:
                    count = len(el.items)
                    for j in range(count):
                        tmp = int(el.items[j].ivalue)
                        udat.append(tmp)
                self._values = [[0] * self._nCols] * self._nRows
                for uval in udat:
                    if coltype[x] < 2:
                        value = (uval + colofs[x]) * colscl[x]
                    else:
                        #noinspection PyProtectedMember
                        value = YAPI._decimalToDouble(uval - 32767)
                    self._values[y][x] = value
                    x += 1
                    if x == self._nCols:
                        x = 0
                        y += 1
        return YAPI.SUCCESS
