#*********************************************************************
#*
#* $Id: yocto_wakeupmonitor.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindWakeUpMonitor(), the high-level API for WakeUpMonitor functions
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
class YWakeUpMonitor(YFunction):
    #--- (globals)


    #--- (end of globals)

    #--- (YWakeUpMonitor definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    POWERDURATION_INVALID           = YAPI.INVALID_LONG
    SLEEPCOUNTDOWN_INVALID          = YAPI.INVALID_LONG
    NEXTWAKEUP_INVALID              = YAPI.INVALID_LONG
    RTCTIME_INVALID                 = YAPI.INVALID_LONG
    ENDOFTIME_INVALID               = YAPI.INVALID_LONG

    WAKEUPREASON_USBPOWER           = 0
    WAKEUPREASON_EXTPOWER           = 1
    WAKEUPREASON_ENDOFSLEEP         = 2
    WAKEUPREASON_EXTSIG1            = 3
    WAKEUPREASON_EXTSIG2            = 4
    WAKEUPREASON_EXTSIG3            = 5
    WAKEUPREASON_EXTSIG4            = 6
    WAKEUPREASON_SCHEDULE1          = 7
    WAKEUPREASON_SCHEDULE2          = 8
    WAKEUPREASON_SCHEDULE3          = 9
    WAKEUPREASON_SCHEDULE4          = 10
    WAKEUPREASON_SCHEDULE5          = 11
    WAKEUPREASON_SCHEDULE6          = 12
    WAKEUPREASON_INVALID            = -1
    WAKEUPSTATE_SLEEPING            = 0
    WAKEUPSTATE_AWAKE               = 1
    WAKEUPSTATE_INVALID             = -1


    _WakeUpMonitorCache ={}

    #--- (end of YWakeUpMonitor definitions)

    #--- (YWakeUpMonitor implementation)

    def __init__(self,func):
        super(YWakeUpMonitor,self).__init__("WakeUpMonitor", func)
        self._callback = None
        self._logicalName = YWakeUpMonitor.LOGICALNAME_INVALID
        self._advertisedValue = YWakeUpMonitor.ADVERTISEDVALUE_INVALID
        self._powerDuration = YWakeUpMonitor.POWERDURATION_INVALID
        self._sleepCountdown = YWakeUpMonitor.SLEEPCOUNTDOWN_INVALID
        self._nextWakeUp = YWakeUpMonitor.NEXTWAKEUP_INVALID
        self._wakeUpReason = YWakeUpMonitor.WAKEUPREASON_INVALID
        self._wakeUpState = YWakeUpMonitor.WAKEUPSTATE_INVALID
        self._rtcTime = YWakeUpMonitor.RTCTIME_INVALID
        self._endOfTime = 2145960000

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "powerDuration":
                self._powerDuration = member.ivalue
            elif member.name == "sleepCountdown":
                self._sleepCountdown = member.ivalue
            elif member.name == "nextWakeUp":
                self._nextWakeUp = member.ivalue
            elif member.name == "wakeUpReason":
                self._wakeUpReason = member.ivalue
            elif member.name == "wakeUpState":
                self._wakeUpState = member.ivalue
            elif member.name == "rtcTime":
                self._rtcTime = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the monitor.
        
        @return a string corresponding to the logical name of the monitor
        
        On failure, throws an exception or returns YWakeUpMonitor.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the monitor. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the monitor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the monitor (no more than 6 characters).
        
        @return a string corresponding to the current value of the monitor (no more than 6 characters)
        
        On failure, throws an exception or returns YWakeUpMonitor.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_powerDuration(self):
        """
        Returns the maximal wake up time (seconds) before going to sleep automatically.
        
        @return an integer corresponding to the maximal wake up time (seconds) before going to sleep automatically
        
        On failure, throws an exception or returns YWakeUpMonitor.POWERDURATION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.POWERDURATION_INVALID
        return self._powerDuration

    def set_powerDuration(self, newval):
        """
        Changes the maximal wake up time (seconds) before going to sleep automatically.
        
        @param newval : an integer corresponding to the maximal wake up time (seconds) before going to
        sleep automatically
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("powerDuration", rest_val)


    def get_sleepCountdown(self):
        """
        Returns the delay before next sleep.
        
        @return an integer corresponding to the delay before next sleep
        
        On failure, throws an exception or returns YWakeUpMonitor.SLEEPCOUNTDOWN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.SLEEPCOUNTDOWN_INVALID
        return self._sleepCountdown

    def set_sleepCountdown(self, newval):
        """
        Changes the delay before next sleep.
        
        @param newval : an integer corresponding to the delay before next sleep
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("sleepCountdown", rest_val)


    def get_nextWakeUp(self):
        """
        Returns the next scheduled wake-up date/time (UNIX format)
        
        @return an integer corresponding to the next scheduled wake-up date/time (UNIX format)
        
        On failure, throws an exception or returns YWakeUpMonitor.NEXTWAKEUP_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.NEXTWAKEUP_INVALID
        return self._nextWakeUp

    def set_nextWakeUp(self, newval):
        """
        Changes the days of the week where a wake up must take place.
        
        @param newval : an integer corresponding to the days of the week where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("nextWakeUp", rest_val)


    def get_wakeUpReason(self):
        """
        Return the last wake up reason.
        
        @return a value among YWakeUpMonitor.WAKEUPREASON_USBPOWER, YWakeUpMonitor.WAKEUPREASON_EXTPOWER,
        YWakeUpMonitor.WAKEUPREASON_ENDOFSLEEP, YWakeUpMonitor.WAKEUPREASON_EXTSIG1,
        YWakeUpMonitor.WAKEUPREASON_EXTSIG2, YWakeUpMonitor.WAKEUPREASON_EXTSIG3,
        YWakeUpMonitor.WAKEUPREASON_EXTSIG4, YWakeUpMonitor.WAKEUPREASON_SCHEDULE1,
        YWakeUpMonitor.WAKEUPREASON_SCHEDULE2, YWakeUpMonitor.WAKEUPREASON_SCHEDULE3,
        YWakeUpMonitor.WAKEUPREASON_SCHEDULE4, YWakeUpMonitor.WAKEUPREASON_SCHEDULE5 and
        YWakeUpMonitor.WAKEUPREASON_SCHEDULE6
        
        On failure, throws an exception or returns YWakeUpMonitor.WAKEUPREASON_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.WAKEUPREASON_INVALID
        return self._wakeUpReason

    def get_wakeUpState(self):
        """
        Returns  the current state of the monitor
        
        @return either YWakeUpMonitor.WAKEUPSTATE_SLEEPING or YWakeUpMonitor.WAKEUPSTATE_AWAKE, according
        to  the current state of the monitor
        
        On failure, throws an exception or returns YWakeUpMonitor.WAKEUPSTATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.WAKEUPSTATE_INVALID
        return self._wakeUpState

    def set_wakeUpState(self, newval):
        rest_val = str(newval)
        return self._setAttr("wakeUpState", rest_val)


    def get_rtcTime(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpMonitor.RTCTIME_INVALID
        return self._rtcTime
    def wakeUp(self ):
        """
        Forces a wakeup.
        """
        # //fixme use real enum value instead of hardcoded int
        return self.set_wakeUpState(YWakeUpMonitor.WAKEUPSTATE_AWAKE)
        

    def sleep(self, secBeforeSleep):
        """
        Go to sleep until the next wakeup condition is met,  the
        RTC time must have been set before calling this function.
        
        @param secBeforeSleep : number of seconds before going into sleep mode,
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        currTime = self.get_rtcTime()
        if not (currTime != 0) : self._throw( YAPI.RTC_NOT_READY,  "RTC time not set")
        self.set_nextWakeUp(self._endOfTime)
        self.set_sleepCountdown(secBeforeSleep)
        return YAPI.SUCCESS

    def sleepFor(self, secUntilWakeUp, secBeforeSleep):
        """
        Go to sleep for a specific time or until the next wakeup condition is met, the
        RTC time must have been set before calling this function. The count down before sleep
        can be canceled with resetSleepCountDown.
        
        @param secUntilWakeUp : sleep duration, in secondes
        @param secBeforeSleep : number of seconds before going into sleep mode
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        currTime = self.get_rtcTime()
        if not (currTime != 0) : self._throw( YAPI.RTC_NOT_READY,  "RTC time not set")
        self.set_nextWakeUp(currTime+secUntilWakeUp)
        self.set_sleepCountdown(secBeforeSleep)
        return YAPI.SUCCESS

    def sleepUntil(self, wakeUpTime, secBeforeSleep):
        """
        Go to sleep until a specific date is reached or until the next wakeup condition is met, the
        RTC time must have been set before calling this function. The count down before sleep
        can be canceled with resetSleepCountDown.
        
        @param wakeUpTime : wake-up datetime (UNIX format)
        @param secBeforeSleep : number of seconds before going into sleep mode
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        currTime = self.get_rtcTime()
        if not (currTime != 0) : self._throw( YAPI.RTC_NOT_READY,  "RTC time not set")
        self.set_nextWakeUp(wakeUpTime)
        self.set_sleepCountdown(secBeforeSleep)
        return YAPI.SUCCESS

    def resetSleepCountDown(self ):
        """
        Reset the sleep countdown.
        
        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        self.set_sleepCountdown(0)
        self.set_nextWakeUp(0)
        return YAPI.SUCCESS


    def nextWakeUpMonitor(self):
        """
        Continues the enumeration of monitors started using yFirstWakeUpMonitor().
        
        @return a pointer to a YWakeUpMonitor object, corresponding to
                a monitor currently online, or a None pointer
                if there are no more monitors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YWakeUpMonitor.FindWakeUpMonitor(hwidRef.value)

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

#--- (end of YWakeUpMonitor implementation)

#--- (WakeUpMonitor functions)

    @staticmethod 
    def FindWakeUpMonitor(func):
        """
        Retrieves a monitor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the monitor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWakeUpMonitor.isOnline() to test if the monitor is
        indeed online at a given time. In case of ambiguity when looking for
        a monitor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the monitor
        
        @return a YWakeUpMonitor object allowing you to drive the monitor.
        """
        if func in YWakeUpMonitor._WakeUpMonitorCache:
            return YWakeUpMonitor._WakeUpMonitorCache[func]
        res =YWakeUpMonitor(func)
        YWakeUpMonitor._WakeUpMonitorCache[func] =  res
        return res

    @staticmethod 
    def  FirstWakeUpMonitor():
        """
        Starts the enumeration of monitors currently accessible.
        Use the method YWakeUpMonitor.nextWakeUpMonitor() to iterate on
        next monitors.
        
        @return a pointer to a YWakeUpMonitor object, corresponding to
                the first monitor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("WakeUpMonitor", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YWakeUpMonitor.FindWakeUpMonitor(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _WakeUpMonitorCleanup():
        pass

  #--- (end of WakeUpMonitor functions)

