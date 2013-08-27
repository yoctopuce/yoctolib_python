#*********************************************************************
#*
#* $Id: yocto_realtimeclock.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindRealTimeClock(), the high-level API for RealTimeClock functions
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
class YRealTimeClock(YFunction):
    """
    The RealTimeClock function maintains and provides current date and time, even accross power cut
    lasting several days. It is the base for automated wake-up functions provided by the WakeUpScheduler.
    The current time may represent a local time as well as an UTC time, but no automatic time change
    will occur to account for daylight saving time.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YRealTimeClock definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    UNIXTIME_INVALID                = YAPI.INVALID_LONG
    DATETIME_INVALID                = YAPI.INVALID_STRING
    UTCOFFSET_INVALID               = YAPI.INVALID_LONG

    TIMESET_FALSE                   = 0
    TIMESET_TRUE                    = 1
    TIMESET_INVALID                 = -1


    _RealTimeClockCache ={}

    #--- (end of YRealTimeClock definitions)

    #--- (YRealTimeClock implementation)

    def __init__(self,func):
        super(YRealTimeClock,self).__init__("RealTimeClock", func)
        self._callback = None
        self._logicalName = YRealTimeClock.LOGICALNAME_INVALID
        self._advertisedValue = YRealTimeClock.ADVERTISEDVALUE_INVALID
        self._unixTime = YRealTimeClock.UNIXTIME_INVALID
        self._dateTime = YRealTimeClock.DATETIME_INVALID
        self._utcOffset = YRealTimeClock.UTCOFFSET_INVALID
        self._timeSet = YRealTimeClock.TIMESET_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "unixTime":
                self._unixTime = member.ivalue
            elif member.name == "dateTime":
                self._dateTime = member.svalue
            elif member.name == "utcOffset":
                self._utcOffset = member.ivalue
            elif member.name == "timeSet":
                self._timeSet = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the clock.
        
        @return a string corresponding to the logical name of the clock
        
        On failure, throws an exception or returns YRealTimeClock.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRealTimeClock.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the clock. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the clock
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the clock (no more than 6 characters).
        
        @return a string corresponding to the current value of the clock (no more than 6 characters)
        
        On failure, throws an exception or returns YRealTimeClock.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRealTimeClock.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_unixTime(self):
        """
        Returns the current time in Unix format (number of elapsed seconds since Jan 1st, 1970).
        
        @return an integer corresponding to the current time in Unix format (number of elapsed seconds
        since Jan 1st, 1970)
        
        On failure, throws an exception or returns YRealTimeClock.UNIXTIME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRealTimeClock.UNIXTIME_INVALID
        return self._unixTime

    def set_unixTime(self, newval):
        """
        Changes the current time. Time is specifid in Unix format (number of elapsed seconds since Jan 1st, 1970).
        If current UTC time is known, utcOffset will be automatically adjusted for the new specified time.
        
        @param newval : an integer corresponding to the current time
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("unixTime", rest_val)


    def get_dateTime(self):
        """
        Returns the current time in the form "YYYY/MM/DD hh:mm:ss"
        
        @return a string corresponding to the current time in the form "YYYY/MM/DD hh:mm:ss"
        
        On failure, throws an exception or returns YRealTimeClock.DATETIME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRealTimeClock.DATETIME_INVALID
        return self._dateTime

    def get_utcOffset(self):
        """
        Returns the number of seconds between current time and UTC time (time zone).
        
        @return an integer corresponding to the number of seconds between current time and UTC time (time zone)
        
        On failure, throws an exception or returns YRealTimeClock.UTCOFFSET_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRealTimeClock.UTCOFFSET_INVALID
        return self._utcOffset

    def set_utcOffset(self, newval):
        """
        Changes the number of seconds between current time and UTC time (time zone).
        The timezone is automatically rounded to the nearest multiple of 15 minutes.
        If current UTC time is known, the current time will automatically be updated according to the
        selected time zone.
        
        @param newval : an integer corresponding to the number of seconds between current time and UTC time (time zone)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("utcOffset", rest_val)


    def get_timeSet(self):
        """
        Returns true if the clock has been set, and false otherwise.
        
        @return either YRealTimeClock.TIMESET_FALSE or YRealTimeClock.TIMESET_TRUE, according to true if
        the clock has been set, and false otherwise
        
        On failure, throws an exception or returns YRealTimeClock.TIMESET_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRealTimeClock.TIMESET_INVALID
        return self._timeSet

    def nextRealTimeClock(self):
        """
        Continues the enumeration of clocks started using yFirstRealTimeClock().
        
        @return a pointer to a YRealTimeClock object, corresponding to
                a clock currently online, or a None pointer
                if there are no more clocks to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YRealTimeClock.FindRealTimeClock(hwidRef.value)

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

#--- (end of YRealTimeClock implementation)

#--- (RealTimeClock functions)

    @staticmethod 
    def FindRealTimeClock(func):
        """
        Retrieves a clock for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the clock is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRealTimeClock.isOnline() to test if the clock is
        indeed online at a given time. In case of ambiguity when looking for
        a clock by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the clock
        
        @return a YRealTimeClock object allowing you to drive the clock.
        """
        if func in YRealTimeClock._RealTimeClockCache:
            return YRealTimeClock._RealTimeClockCache[func]
        res =YRealTimeClock(func)
        YRealTimeClock._RealTimeClockCache[func] =  res
        return res

    @staticmethod 
    def  FirstRealTimeClock():
        """
        Starts the enumeration of clocks currently accessible.
        Use the method YRealTimeClock.nextRealTimeClock() to iterate on
        next clocks.
        
        @return a pointer to a YRealTimeClock object, corresponding to
                the first clock currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("RealTimeClock", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YRealTimeClock.FindRealTimeClock(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _RealTimeClockCleanup():
        pass

  #--- (end of RealTimeClock functions)

