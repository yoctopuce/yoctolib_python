#*********************************************************************
#*
#* $Id: yocto_datalogger.py 12326 2013-08-13 15:52:20Z mvuilleu $
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
from time import time
from math import ceil,floor


class YDataRun():
    """
    YDataRun Class: Sequence of measured data, stored by the data logger

    A run is a continuous interval of time during which a module was powered on.
    A data run provides easy access to all data collected during a given run,
    providing on-the-fly resampling at the desired reporting rate.
    """

    MINVALUE_INVALID     = -66666666.66666666
    AVERAGEVALUE_INVALID = -66666666.66666666
    MAXVALUE_INVALID     = -66666666.66666666

    def __init__(self,parent, run):
        self._dataLogger    = parent
        self._runNo         = run
        self._streams       = []
        self._browseInterval = 60
        self._startTimeUTC  = 0
        self._duration      = 0
        self._isLive        = False
        self._measureNames = None
        self._minValues = None
        self._avgValues= None
        self._maxValues= None

    # Internal: Append a stream to the run
    def addStream(self,stream):
        self._streams.append(stream)
        if not self._startTimeUTC:
            if stream.get_startTimeUTC() > 0:
                self._startTimeUTC = stream.get_startTimeUTC() - stream.get_startTime()

    # Internal: Compute the total duration of the run, once all streams have been added
    def finalize(self):
        last = self._streams[-1]
        self.duration = last.get_startTime() + last.get_rowCount() * last.get_dataSamplesInterval()
        self.isLive = (self._dataLogger.get_currentRunIndex() == self._runNo) and (self._dataLogger.get_recording() == YDataLogger.RECORDING_ON)
        if self.isLive and self.startTimeUTC == 0:
            self.startTimeUTC = time() - self.duration

        self._measureNames = self._dataLogger.get_measureNames()
        if len(self._streams) > 0:
            self.set_valueInterval(self._streams[0].get_dataSamplesInterval())
        else:
            self.set_valueInterval(60)

    # Internal: Update the run with any new data that may have appeared since the run was initially loaded
    def refresh(self):
        if self._isLive:
            last = self._streams[-1]
            last.loadStream()
            self._duration = last.get_startTime() + last.get_rowCount() * last.get_dataSamplesInterval()
            if time() > self._startTimeUTC + self._duration:
                # check if new streams have appeared in between
                newStreams = False
                streams = []
                self._dataLogger.get_dataStreams(streams)
                for stream in streams:
                    if stream.get_runIndex() == self._runNo and stream.get_startTime() > last.get_startTime():
                        self.addStream(stream)
                        newStreams = True
                if newStreams : self.finalize()
            self._isLive = (self._dataLogger.get_recording() == YDataLogger.RECORDING_ON)


    # Internal: Mark a measure as unavailable
    def invalidValue(self,pos):
        for  key in self._measureNames:
            self._minValues[key][pos] = YDataRun.MINVALUE_INVALID
            self._avgValues[key][pos] = YDataRun.AVERAGEVALUE_INVALID
            self._maxValues[key][pos] = YDataRun.MAXVALUE_INVALID

    # Internal: Compute the resampled measure values for a required position in run
    def computeValues(self,pos):
        #if there is no data stream, exit immediately
        if not len(self._streams):
            self.invalidValue(pos)
            return

        
        # search for the earliest stream with useful data for requested measure
        reqpos = pos
        timevalue = pos * self._browseInterval

        si = len(self._streams)-1
        stream = self._streams[si]
        while stream.get_startTime() > timevalue and si > 0:
            si-=1
            stream = self._streams[si]

        streamInterval = stream.get_dataSamplesInterval()
        thisAvail = int(floor(stream.get_startTime() / self._browseInterval))
        nextMissing = int(ceil((stream.get_startTime() + stream.get_rowCount() * streamInterval) / self._browseInterval))
        if nextMissing * self._browseInterval <= timevalue and si < len(self._streams)-1:
            # we went back one step to much
            prevMissing = nextMissing
            si+=1
            stream = self._streams[si]
            streamInterval = stream.get_dataSamplesInterval()
            thisAvail = int(floor(stream.get_startTime() / self._browseInterval))
            nextMissing = int(ceil((stream.get_startTime() + stream.get_rowCount() * streamInterval) / self._browseInterval))
        else:
            # nothing interesting before this stream
            if stream.get_startTime() > timevalue:
                prevMissing=0
            else:
                prevMissing = thisAvail-1

        if si+1 >= len(self._streams):
            nextAvail = pos+1
        else:
            nextStream = self._streams[si+1]
            nextAvail = int(floor(nextStream.get_startTime() / self._browseInterval))

        # Check if we are looking for a missing measure
        if  prevMissing <= pos <thisAvail :
            for pos in range( prevMissing  , thisAvail):
                self.invalidValue(pos)
            return

        if nextMissing <=  pos < nextAvail:
            for pos in range (nextMissing , nextAvail ):
                self.invalidValue(pos)
            return

        # make sure the requested cell is marked as invalid if we end up with no data in the stream
        self.invalidValue(reqpos)

        # process all useful rows from the stream containing requested position, until completely processed
        if prevMissing < thisAvail or prevMissing == 0:
            #stream is not a continuation, start with very beginning of stream
            row = 0
            pos = thisAvail
            startTime = stream.get_startTime()
        else:
            # stream is a continuation, start at next interval boundary
            pos = int(ceil(stream.get_startTime() / self._browseInterval))
            row = int(round((pos * self._browseInterval - stream.get_startTime()) / streamInterval))
            startTime = stream.get_startTime() + row * streamInterval

        stopAsap = False
        minCol = {}
        avgCol = {}
        maxCol = {}
        minVal = {}
        avgVal = {}
        maxVal = {}
        divisor = 0
        boundary = (pos+1) * self._browseInterval
        stopTime = int(ceil((stream.get_startTime() + stream.get_rowCount() * stream.get_dataSamplesInterval()) / self._browseInterval) * self._browseInterval)
        while startTime < stopTime:
            nextTime = startTime + streamInterval
            #print("startTime="+str(startTime)+" -- nextTime="+str(nextTime)+" -- stopTime="+str(stopTime)+" -- boundary="+str(boundary)+" -- row="+str(row)+" -- pos="+str(pos))
            if  not len(avgCol):
                streamsCols = stream.get_columnNames()
                for idx  in range(0,len(streamsCols)):
                    colname = streamsCols[idx]
                    if colname[-4:-3]  == "_":
                        name = colname[0:-4]
                        suffix = colname[-3:]
                        if suffix == 'min':
                            minCol[name] = idx
                        elif suffix == 'avg':
                            avgCol[name] = idx
                        elif suffix == 'max':
                            maxCol[name] = idx
                    else:
                        minCol[colname] = idx
                        avgCol[colname] = idx
                        maxCol[colname] = idx

            if not divisor:
                if boundary <= nextTime:
                    while boundary <= nextTime:
                        for key in self._measureNames:
                            self._minValues[key][pos] = stream.get_data(row, minCol[key])
                            self._avgValues[key][pos] = stream.get_data(row, avgCol[key])
                            self._maxValues[key][pos] = stream.get_data(row, maxCol[key])

                        pos+=1
                        boundary = (pos+1) * self._browseInterval
                else:
                    divisor = streamInterval
                    for key in self._measureNames:
                        minVal[key] = stream.get_data(row, minCol[key])
                        avgVal[key] = stream.get_data(row, avgCol[key]) * streamInterval
                        maxVal[key] = stream.get_data(row, maxCol[key])
            else:
                divisor += streamInterval
                for key in self._measureNames:
                    minVal[key] = min(minVal[key], stream.get_data(row, minCol[key]))
                    avgVal[key] += streamInterval * stream.get_data(row, avgCol[key])
                    maxVal[key] = max(maxVal[key], stream.get_data(row, maxCol[key]))

                if 2*abs(nextTime - boundary) <= streamInterval:
                    for key in self._measureNames:
                        self._minValues[key][pos] = minVal[key]
                        self._avgValues[key][pos] = avgVal[key] / divisor
                        self._maxValues[key][pos] = maxVal[key]

                    divisor = 0
                    pos+=1
                    boundary = (pos+1) * self._browseInterval
                    if stopAsap: break

            row+=1
            if row < stream.get_rowCount():
                #noinspection PyUnusedLocal
                startTime = nextTime
            else:
                si+=1
                if si >= len(self._streams): break
                stream = self._streams[si]
                startTime = stream.get_startTime()
                streamInterval = stream.get_dataSamplesInterval()
                row = 0
                avgCol = {}
                stopAsap = True


        if divisor > 0:
            # save partially computed value anyway
            for key in self._measureNames:
                self._minValues[key][pos] = minVal[key]
                self._avgValues[key][pos] = avgVal[key] / divisor
                self._maxValues[key][pos] = maxVal[key]


    def get_measureNames(self):
        """
        Returns the names of the measures recorded by the data logger.
        In most case, the measure names match the hardware identifier
        of the sensor that produced the data.
        
        @return a list of strings (the measure names)
        
        On failure, throws an exception or returns an empty array.
        """
        return self._measureNames

    def measureNames(self):
        return self._measureNames





    def get_startTimeUTC(self):
        """
        Returns the start time of the data stream, relative to the Jan 1, 1970.
        If the UTC time was not set in the datalogger at the time of the recording
        of this data stream, this method returns 0.
        
        This method does not cause any access to the device, as the value
        is preloaded in the object at instantiation time.
        
        @return an unsigned number corresponding to the number of seconds
                between the Jan 1, 1970 and the beginning of this data
                stream (i.e. Unix time representation of the absolute time).
        """
        return self.startTimeUTC

    def startTimeUTC(self):
        return self.startTimeUTC

    def get_duration(self):
        """
        Returns the duration (in seconds) of the data run.
        When the datalogger is actively recording and the specified run is the current
        run, calling this method reloads last sequence(s) from device to make sure
        it includes the latest recorded data.
        
        @return an unsigned number corresponding to the number of seconds
                between the beginning of the run (when the module was powered up)
                and the last recorded measure.
        """
        if self.isLive: self.refresh()
        return self._duration

    def duration(self):
        if self.isLive: self.refresh()
        return self._duration


    def get_valueInterval(self):
        """
        Returns the number of seconds covered by each value in this run.
        By default, the value interval is set to the coarsest data rate
        archived in the data logger flash for this run. The value interval
        can however be configured at will to a different rate when desired.
        
        @return an unsigned number corresponding to a number of seconds covered
                by each data sample in the Run.
        """
        return self._browseInterval

    def valueInterval(self):
        return self._browseInterval

    def set_valueInterval(self,valueInterval):
        """
        Changes the number of seconds covered by each value in this run.
        By default, the value interval is set to the coarsest data rate
        archived in the data logger flash for this run. The value interval
        can however be configured at will to a different rate when desired.
        
        @param valueInterval : an integer number of seconds.
        
        @return nothing
        """
   
        last = self._streams[-1]
        names = last.get_columnNames()
        self._minValues = {}
        self._avgValues = {}
        self._maxValues = {}
        for name in names :
            if name[-4:-3] == "_":
                name = name[0:-4]

            if not name in  self._minValues:
                self._minValues[name] = {}
                self._avgValues[name] = {}
                self._maxValues[name] = {}
        self._browseInterval = valueInterval

    def setValueInterval(self,valueInterval):
        return self.set_valueInterval(valueInterval)


    def get_valueCount(self):
        """
        Returns the number of values accessible in this run, given the selected data
        samples interval.
        When the datalogger is actively recording and the specified run is the current
        run, calling this method reloads last sequence(s) from device to make sure
        it includes the latest recorded data.
        
        @return an unsigned number corresponding to the run duration divided by the
                samples interval.
        """
        if self.isLive : self.refresh()
        return ceil(self.duration / self._browseInterval)

    def valueCount(self):
        if self.isLive : self.refresh()
        return ceil(self.duration / self._browseInterval)

    def get_minValue(self, measureName, pos):
        """
        Returns the minimal value of the measure observed at the specified time
        period.
        
        @param measureName : the name of the desired measure (one of the names
                returned by get_measureNames)
        @param pos : the position index, between 0 and the value returned by
                get_valueCount
        
        @return a floating point number (the minimal value)
        
        On failure, throws an exception or returns Y_MINVALUE_INVALID.
        """
        if not pos in self._minValues[measureName]: self.computeValues(pos)
        return self._minValues[measureName][pos]

    def  minValue(self, measureName, pos):
        if not pos in self._minValues[measureName]: self.computeValues(pos)
        return self._minValues[measureName][pos]


    def get_averageValue(self,measureName,pos):
        """
        Returns the average value of the measure observed at the specified time
        period.
        
        @param measureName : the name of the desired measure (one of the names
                returned by get_measureNames)
        @param pos : the position index, between 0 and the value returned by
                get_valueCount
        
        @return a floating point number (the average value)
        
        On failure, throws an exception or returns Y_AVERAGEVALUE_INVALID.
        """
        if not pos in self._avgValues[measureName]: self.computeValues(pos)
        return self._avgValues[measureName][pos]

    def averageValue(self,measureName, pos):
        if not pos in self._avgValues[measureName]: self.computeValues(pos)
        return self._avgValues[measureName][pos]


    def get_maxValue(self,measureName, pos):
        """
        Returns the maximal value of the measure observed at the specified time
        period.
        
        @param measureName : the name of the desired measure (one of the names
                returned by get_measureNames)
        @param pos : the position index, between 0 and the value returned by
                get_valueCount
        
        @return a floating point number (the maximal value)
        
        On failure, throws an exception or returns Y_MAXVALUE_INVALID.
        """
        if not pos in self._maxValues[measureName]: self.computeValues(pos)
        return self._maxValues[measureName]

    def maxValue(self,measureName, pos):
        if not pos in self._maxValues[measureName]: self.computeValues(pos)
        return self._maxValues[measureName]



class YDataLogger(YFunction):
    """
    Yoctopuce sensors include a non-volatile memory capable of storing ongoing measured
    data automatically, without requiring a permanent connection to a computer.
    The Yoctopuce application programming interface includes fonctions to control
    the functioning of this internal data logger.
    Since the sensors do not include a battery, they don't have an absolute time
    reference. Therefore, measures are simply indexed by the absolute run number
    and time relative to the start of the run. Every new power up starts a new run.
    It is however possible to setup an absolute UTC time by software at a given time,
    so that the data logger keeps track of it until next time it is powered off.
    """

    Y_DATA_INVALID = YAPI.INVALID_DOUBLE

    #--- (generated code: YDataLogger definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    OLDESTRUNINDEX_INVALID          = YAPI.INVALID_LONG
    CURRENTRUNINDEX_INVALID         = YAPI.INVALID_LONG
    SAMPLINGINTERVAL_INVALID        = YAPI.INVALID_LONG
    TIMEUTC_INVALID                 = YAPI.INVALID_LONG

    RECORDING_OFF                   = 0
    RECORDING_ON                    = 1
    RECORDING_INVALID               = -1
    AUTOSTART_OFF                   = 0
    AUTOSTART_ON                    = 1
    AUTOSTART_INVALID               = -1
    CLEARHISTORY_FALSE              = 0
    CLEARHISTORY_TRUE               = 1
    CLEARHISTORY_INVALID            = -1


    _DataLoggerCache ={}

    #--- (end of generated code: YDataLogger definitions)

    def __init__(self,func):
        super(YDataLogger,self).__init__("DataLogger", func)
        self._dataRuns = None
        self._liveRun = 0

        #--- (generated code: YDataLogger implementation)

    def __init__(self,func):
        super(YDataLogger,self).__init__("DataLogger", func)
        self._callback = None
        self._logicalName = YDataLogger.LOGICALNAME_INVALID
        self._advertisedValue = YDataLogger.ADVERTISEDVALUE_INVALID
        self._oldestRunIndex = YDataLogger.OLDESTRUNINDEX_INVALID
        self._currentRunIndex = YDataLogger.CURRENTRUNINDEX_INVALID
        self._samplingInterval = YDataLogger.SAMPLINGINTERVAL_INVALID
        self._timeUTC = YDataLogger.TIMEUTC_INVALID
        self._recording = YDataLogger.RECORDING_INVALID
        self._autoStart = YDataLogger.AUTOSTART_INVALID
        self._clearHistory = YDataLogger.CLEARHISTORY_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "oldestRunIndex":
                self._oldestRunIndex = member.ivalue
            elif member.name == "currentRunIndex":
                self._currentRunIndex = member.ivalue
            elif member.name == "samplingInterval":
                self._samplingInterval = member.ivalue
            elif member.name == "timeUTC":
                self._timeUTC = member.ivalue
            elif member.name == "recording":
                self._recording = member.ivalue
            elif member.name == "autoStart":
                self._autoStart = member.ivalue
            elif member.name == "clearHistory":
                self._clearHistory = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the data logger.
        
        @return a string corresponding to the logical name of the data logger
        
        On failure, throws an exception or returns YDataLogger.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDataLogger.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the data logger. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the data logger
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the data logger (no more than 6 characters).
        
        @return a string corresponding to the current value of the data logger (no more than 6 characters)
        
        On failure, throws an exception or returns YDataLogger.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDataLogger.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_oldestRunIndex(self):
        """
        Returns the index of the oldest run for which the non-volatile memory still holds recorded data.
        
        @return an integer corresponding to the index of the oldest run for which the non-volatile memory
        still holds recorded data
        
        On failure, throws an exception or returns YDataLogger.OLDESTRUNINDEX_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDataLogger.OLDESTRUNINDEX_INVALID
        return self._oldestRunIndex

    def get_currentRunIndex(self):
        """
        Returns the current run number, corresponding to the number of times the module was
        powered on with the dataLogger enabled at some point.
        
        @return an integer corresponding to the current run number, corresponding to the number of times the module was
                powered on with the dataLogger enabled at some point
        
        On failure, throws an exception or returns YDataLogger.CURRENTRUNINDEX_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDataLogger.CURRENTRUNINDEX_INVALID
        return self._currentRunIndex

    def get_samplingInterval(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDataLogger.SAMPLINGINTERVAL_INVALID
        return self._samplingInterval

    def set_samplingInterval(self, newval):
        rest_val = str(newval)
        return self._setAttr("samplingInterval", rest_val)


    def get_timeUTC(self):
        """
        Returns the Unix timestamp for current UTC time, if known.
        
        @return an integer corresponding to the Unix timestamp for current UTC time, if known
        
        On failure, throws an exception or returns YDataLogger.TIMEUTC_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
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
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
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
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("recording", rest_val)


    def get_autoStart(self):
        """
        Returns the default activation state of the data logger on power up.
        
        @return either YDataLogger.AUTOSTART_OFF or YDataLogger.AUTOSTART_ON, according to the default
        activation state of the data logger on power up
        
        On failure, throws an exception or returns YDataLogger.AUTOSTART_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
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
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("autoStart", rest_val)


    def get_clearHistory(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDataLogger.CLEARHISTORY_INVALID
        return self._clearHistory

    def set_clearHistory(self, newval):
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("clearHistory", rest_val)


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

    def registerValueCallback(self, callback):
        """
        Registers the callback function that is invoked on every change of advertised value.
        The callback is invoked only during the execution of ySleep or yHandleEvents.
        This provides control over the time when the callback is triggered. For good responsiveness, remember to call
        one of these two functions periodically. To unregister a callback, pass a None pointer as argument.
        
        @param callback : the callback function to call, or a None pointer. The callback function should take two
                arguments: the function object of which the value has changed, and the character string describing
                the new advertised value.
        @noreturn
        """
        if callback is not None:
            self._registerFuncCallback(self)
        else:
            self._unregisterFuncCallback(self)
        self._callback = callback

    def set_callback(self, callback):
        self.registerValueCallback(callback)

    def setCallback(self, callback):
        self.registerValueCallback(callback)


    def advertiseValue(self,value):
        if self._callback is not None:
            self._callback(self, value)

#--- (end of generated code: YDataLogger implementation)

    _dataLoggerURL = ""

    def getData(self,runIdx,timeIdx,jsondataRef):
        devRef = YRefParam()
        errmsgRef = YRefParam()
        bufferRef = YRefParam()

        if self._dataLoggerURL == "": self._dataLoggerURL = "/logger.json";

        # Resolve our reference to our device, load REST API
        res = self._getDevice(devRef,  errmsgRef)
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

            res = devRef.value.HTTPRequest("GET " + self._dataLoggerURL + " HTTP/1.1\n\r\n\r", bufferRef,  errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res

        try:
            jsondataRef.value = YAPI.TJsonParser(bufferRef.value)
        except YAPI.JsonError as e:
            if not errmsgRef is None : errmsgRef.value = "unexpected JSON structure: " + e.msg
            return YAPI.IO_ERROR

        if jsondataRef.value.httpcode == 404 and self._dataLoggerURL != "/dataLogger.json":
            # retry using backward-compatible datalogger URL
            self._dataLoggerURL = "/dataLogger.json"
            return self.getData(runIdx, timeIdx, jsondataRef)

        return YAPI.SUCCESS


    def get_measureNames(self):
        """
        Returns the names of the measures recorded by the data logger.
        In most case, the measure names match the hardware identifier
        of the sensor that produced the data.
        
        @return a list of strings (the measure names)
        
        On failure, throws an exception or returns an empty array.
        """
        return self._measureNames

    def  measureNames(self):
        return self.measureNames


    #Internal function to preload the list of all runs, for high-level functions
    def loadRuns(self):

        self._measureNames = []
        self._dataRuns = {}
        self._liveRun = self.get_currentRunIndex()

        # preload stream list
        streamsRef = YRefParam()
        res = self.get_dataStreams(streamsRef)
        if res != YAPI.SUCCESS: return res
        lastStream = None

        # sort streams into runs
        for stream in streamsRef.value:
            lastStream = stream
            runIdx = stream.get_runIndex()
            if not runIdx in self._dataRuns:
                self._dataRuns[runIdx] = YDataRun(self, runIdx)
            self._dataRuns[runIdx].addStream(stream)

        #finalize computation of data in each run
        names = lastStream.get_columnNames()
        self._measureNames = []
        for name in names :
            if name[-4:-3] != "_":
                self._measureNames.append(name)
            else:
                if name[-4:] == '_min':
                    self._measureNames.append(name[-4:])
        for run in self._dataRuns:
            self._dataRuns[run].finalize()
        return YAPI.SUCCESS

    def get_dataRun(self,runIdx):
        """
        Returns a data run object holding all measured data for a given
        period during which the module was turned on (a run). This object can then
        be used to retrieve measures (min, average and max) at a desired data rate.
        
        @param runIdx : the index of the desired run
        
        @return an YDataRun object
        
        On failure, throws an exception or returns None.
        """
        if self._dataRuns is None or runIdx > self._liveRun: self.loadRuns()
        if self._dataRuns is None: return None
        if not runIdx in self._dataRuns: return None
        return self._dataRuns[runIdx]

    def getDataRun(self,runIdx):
        if self._dataRuns is not None or runIdx > self._liveRun: self.loadRuns()
        if not runIdx in self._dataRuns: return None
        return self._dataRuns[runIdx]


    def forgetAllDataStreams(self):
        """
        Clears the data logger memory and discards all recorded data streams.
        This method also resets the current run index to zero.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_clearHistory(YDataLogger.CLEARHISTORY_TRUE)

    def get_dataStreams(self, v):
        """
        Builds a list of all data streams hold by the data logger.
        The caller must pass by reference an empty array to hold YDataStream
        objects, and the function fills it with objects describing available
        data sequences.
        
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
        for i in range(len(root.items)):
            el = root.items[i]
            v.value.append(YDataStream(self, el.items[0].ivalue, el.items[1].ivalue, el.items[2].ivalue, el.items[3].ivalue))


        return YAPI.SUCCESS

    def throw_friend(self,errType, errMsg):
        self._throw(errType, errMsg)

    #--- (generated code: DataLogger functions)

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
        if func in YDataLogger._DataLoggerCache:
            return YDataLogger._DataLoggerCache[func]
        res =YDataLogger(func)
        YDataLogger._DataLoggerCache[func] =  res
        return res

    @staticmethod 
    def  FirstDataLogger():
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
        p = (ctypes.c_int*1)()
        err = YAPI.apiGetFunctionsByClass("DataLogger", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YDataLogger.FindDataLogger(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _DataLoggerCleanup():
        pass

  #--- (end of generated code: DataLogger functions)

class YDataStream:

    def __init__(self, parent,  run,  stamp,  utc,  itv):
        self.dataLogger = parent
        self.runNo = run
        self.timeStamp = stamp
        self.utcStamp = utc
        self.interval = itv
        self.nRows = 0
        self.nCols = 0
        self.columnNames = []
        self.values = None

    def __del__(self):
        self.columnNames = None
        self.values = None

    def get_runIndex(self):
        """
        Returns the run index of the data stream. A run can be made of
        multiple datastreams, for different time intervals.
        
        This method does not cause any access to the device, as the value
        is preloaded in the object at instantiation time.
        
        @return an unsigned number corresponding to the run index.
        """
        return  self.runNo

    def get_startTime(self):
        """
        Returns the start time of the data stream, relative to the beginning
        of the run. If you need an absolute time, use get_startTimeUTC().
        
        This method does not cause any access to the device, as the value
        is preloaded in the object at instantiation time.
        
        @return an unsigned number corresponding to the number of seconds
                between the start of the run and the beginning of this data
                stream.
        """
        return  self.timeStamp

    def get_startTimeUTC(self):
        """
        Returns the start time of the data stream, relative to the Jan 1, 1970.
        If the UTC time was not set in the datalogger at the time of the recording
        of this data stream, this method returns 0.
        
        This method does not cause any access to the device, as the value
        is preloaded in the object at instantiation time.
        
        @return an unsigned number corresponding to the number of seconds
                between the Jan 1, 1970 and the beginning of this data
                stream (i.e. Unix time representation of the absolute time).
        """
        return  self.utcStamp

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
        return  self.interval

    def get_rowCount(self):
        """
        Returns the number of data rows present in this stream.
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @return an unsigned number corresponding to the number of rows.
        
        On failure, throws an exception or returns zero.
        """
        if not self.nRows: self.loadStream()
        return self.nRows

    def get_columnCount(self):
        """
        Returns the number of data columns present in this stream.
        The meaning of the values present in each column can be obtained
        using the method get_columnNames().
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @return an unsigned number corresponding to the number of rows.
        
        On failure, throws an exception or returns zero.
        """
        if not self.nCols: self.loadStream()
        return self.nCols

    def get_columnNames(self):
        """
        Returns the title (or meaning) of each data column present in this stream.
        In most case, the title of the data column is the hardware identifier
        of the sensor that produced the data. For archived streams created by
        summarizing a high-resolution data stream, there can be a suffix appended
        to the sensor identifier, such as _min for the minimum value, _avg for the
        average value and _max for the maximal value.
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @return a list containing as many strings as there are columns in the
                data stream.
        
        On failure, throws an exception or returns an empty array.
        """
        #noinspection PyTypeChecker
        if not(len(self.columnNames)): self.loadStream()
        return self.columnNames

    def get_dataRows(self):
        """
        Returns the whole data set contained in the stream, as a bidimensional
        table of numbers.
        The meaning of the values present in each column can be obtained
        using the method get_columnNames().
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @return a list containing as many elements as there are rows in the
                data stream. Each row itself is a list of floating-point
                numbers.
        
        On failure, throws an exception or returns an empty array.
        """
        if self.values is None: self.loadStream()
        return self.values

    def get_data(self, row, col):
        """
        Returns a single measure from the data stream, specified by its
        row and column index.
        The meaning of the values present in each column can be obtained
        using the method get_columnNames().
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @param row : row index
        @param col : column index
        
        @return a floating-point number
        
        On failure, throws an exception or returns Y_DATA_INVALID.
        """
        if self.values is None: self.loadStream()

        if row >= self.nRows or row < 0:
            return YDataLogger.Y_DATA_INVALID

        if col >= self.nCols or col < 0:
            return YDataLogger.Y_DATA_INVALID

        return self.values[row][col]

    def loadStream(self):
        jsonRef = YRefParam()
        coldiv  = []
        coltype = []
        udat    = []
        colscl  = []
        colofs  = []
        caltyp  = []
        calhdl  = []
        calpar  = []
        calraw  = []
        calref  = []
        c = 0
        x = 0
        y = 0
        res = self.dataLogger.getData(self.runNo, self.timeStamp, jsonRef)
        if res != YAPI.SUCCESS:
            return res
        self.nRows = 0
        self.nCols = 0
        del self.columnNames[:]
        self.values = [[]]
        root = jsonRef.value.GetRootNode()
        for i in range(len(root.members)):
            el = root.members[i]
            name = el.name
            if name == "time":
                self.timeStamp = el.ivalue
            elif name == "UTC":
                self.utcStamp = el.ivalue
            elif name == "interval":
                self.interval = el.ivalue
            elif name == "nRows":
                self.nRows = el.ivalue
            elif name == "keys":
                if not self.nCols:
                    self.nCols = len(el.items)
                for j in range(self.nCols):
                    self.columnNames.append(el.items[j].svalue)
            elif name == "div":
                if not self.nCols:
                    self.nCols = len(el.items)
                for j in range(self.nCols):
                    coldiv.append(el.items[j].ivalue)
            elif name == "type":
                if not self.nCols:
                    self.nCols = len(el.items)
                for j in range(self.nCols):
                    coltype.append(el.items[j].ivalue)
            elif name == "scal":
                if not self.nCols:
                    self.nCols = len(el.items)
                for j in range(self.nCols):
                    colscl.append(el.items[j].ivalue / 65536.0)
                    if coltype[j]:
                        colofs.append(-32767)
                    else:
                        colofs.append(0)
            elif name ==  "cal":
                if not self.nCols:
                    self.nCols = len(el.items)
                for j in range(self.nCols):
                    calibration_str=el.items[j].svalue
                    cur_calpar = []
                    cur_calraw = []
                    cur_calref = []
                    calibType = YAPI._decodeCalibrationPoints(calibration_str
                                                        ,cur_calpar
                                                        ,cur_calraw
                                                        ,cur_calref
                                                        ,colscl[j]
                                                        ,colofs[j])
                    calhdl.append( YAPI._getCalibrationHandler(calibType))
                    caltyp.append( calibType )
                    calpar.append( cur_calpar )
                    calraw.append( cur_calraw )
                    calref.append( cur_calref )
            elif name == "data":
                if len(colscl) <= 0:
                    for j in range(self.nCols):
                        colscl.append(1.0 / coldiv[j])
                        if coltype[j]:
                            colofs[j] = -32767
                        else:
                            colofs[j] = 0

                del udat[:]
                if el.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRING:
                    sdat = el.svalue
                    p=0
                    while  p<len(sdat):
                        c = sdat[p]
                        p+=1
                        if c >= 'a':
                            srcpos = int(len(udat) - 1 - (ord(c) - ord('a')))
                            if srcpos < 0:
                                self.dataLogger.throw_friend(YAPI.IO_ERROR, "Unexpected JSON reply format")
                                return YAPI.IO_ERROR
                            val = udat[srcpos]
                        else:
                            if p + 2 > len(sdat):
                                self.dataLogger.throw_friend(YAPI.IO_ERROR, "Unexpected JSON reply format")
                                return YAPI.IO_ERROR

                            val = (ord(c) - ord('0'))
                            c = sdat[p]
                            p+=1
                            val += (ord(c) - ord('0')) << 5
                            c = sdat[p]
                            p+=1
                            if c == 'z': c = "\\"
                            val += (ord(c) - ord('0')) << 10
                        udat.append(val)
                else:
                    count = len(el.items)
                    for j in range(count):
                        tmp = int(el.items[j].ivalue)
                        udat.append(tmp)
                #noinspection PyUnusedLocal,PyUnusedLocal
                self.values = [[0 for j in range(self.nCols)] for i in range(self.nRows)]

                for uval in udat:
                    if coltype[x] <2 :
                        value = (uval +colofs[x]) * colscl[x]
                    else :
                        value = YAPI._decimalToDouble(uval-32767)
                    if  caltyp[x]>0 and calhdl[x] is not None:
                        handler = calhdl[x]
                        # use post-calibration function
                        if caltyp[x] <= 10 :
                            # linear calibration using unscaled value
                            value = handler((uval + colofs[x]) / coldiv[x], caltyp[x], calpar[x], calraw[x], calref[x])
                        elif caltyp[c] > 20:
                            # custom calibration function: floating-point value is uncalibrated in the datalogger
                            value = handler.yCalibrationHandler(value, caltyp[x], calpar[x], calraw[x], calref[x])
                    self.values[y][x] = value
                    x+=1
                    if x == self.nCols :
                        x = 0
                        y += 1
        return YAPI.SUCCESS
