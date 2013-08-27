#*********************************************************************
#*
#* $Id: yocto_watchdog.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindWatchdog(), the high-level API for Watchdog functions
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
class YWatchdog(YFunction):
    """
    The watchog function works like a relay and can cause a brief power cut
    to an appliance after a preset delay to force this appliance to
    reset. The Watchdog must be called from time to time to reset the
    timer and prevent the appliance reset.
    The watchdog can be driven direcly with <i>pulse</i> and <i>delayedpulse</i> methods to switch
    off an appliance for a given duration.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YWatchdog definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    PULSETIMER_INVALID              = YAPI.INVALID_LONG
    DELAYEDPULSETIMER_INVALID       = None
    COUNTDOWN_INVALID               = YAPI.INVALID_LONG
    TRIGGERDELAY_INVALID            = YAPI.INVALID_LONG
    TRIGGERDURATION_INVALID         = YAPI.INVALID_LONG

    STATE_A                         = 0
    STATE_B                         = 1
    STATE_INVALID                   = -1
    OUTPUT_OFF                      = 0
    OUTPUT_ON                       = 1
    OUTPUT_INVALID                  = -1
    AUTOSTART_OFF                   = 0
    AUTOSTART_ON                    = 1
    AUTOSTART_INVALID               = -1
    RUNNING_OFF                     = 0
    RUNNING_ON                      = 1
    RUNNING_INVALID                 = -1


    _WatchdogCache ={}

    #--- (end of YWatchdog definitions)

    #--- (YWatchdog implementation)

    def __init__(self,func):
        super(YWatchdog,self).__init__("Watchdog", func)
        self._callback = None
        self._logicalName = YWatchdog.LOGICALNAME_INVALID
        self._advertisedValue = YWatchdog.ADVERTISEDVALUE_INVALID
        self._state = YWatchdog.STATE_INVALID
        self._output = YWatchdog.OUTPUT_INVALID
        self._pulseTimer = YWatchdog.PULSETIMER_INVALID
        self._delayedPulseTimer = YWatchdog.DELAYEDPULSETIMER_INVALID
        self._countdown = YWatchdog.COUNTDOWN_INVALID
        self._autoStart = YWatchdog.AUTOSTART_INVALID
        self._running = YWatchdog.RUNNING_INVALID
        self._triggerDelay = YWatchdog.TRIGGERDELAY_INVALID
        self._triggerDuration = YWatchdog.TRIGGERDURATION_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "state":
                self._state = member.ivalue
            elif member.name == "output":
                self._output = member.ivalue
            elif member.name == "pulseTimer":
                self._pulseTimer = member.ivalue
            elif member.name == "delayedPulseTimer":
                if member.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: self._delayedPulseTimer = -1
                self._delayedPulseTimer = {"moving":None,"target":None,"ms":None }
                for submemb in member.members:
                    if submemb.name == "moving":
                        self._delayedPulseTimer["moving"]  = submemb.ivalue
                    elif submemb.name == "target": 
                        self._delayedPulseTimer["target"] = submemb.ivalue
                    elif submemb.name == "ms": 
                        self._delayedPulseTimer["ms"] = submemb.ivalue
            elif member.name == "countdown":
                self._countdown = member.ivalue
            elif member.name == "autoStart":
                self._autoStart = member.ivalue
            elif member.name == "running":
                self._running = member.ivalue
            elif member.name == "triggerDelay":
                self._triggerDelay = member.ivalue
            elif member.name == "triggerDuration":
                self._triggerDuration = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the watchdog.
        
        @return a string corresponding to the logical name of the watchdog
        
        On failure, throws an exception or returns YWatchdog.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the watchdog. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the watchdog
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the watchdog (no more than 6 characters).
        
        @return a string corresponding to the current value of the watchdog (no more than 6 characters)
        
        On failure, throws an exception or returns YWatchdog.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_state(self):
        """
        Returns the state of the watchdog (A for the idle position, B for the active position).
        
        @return either YWatchdog.STATE_A or YWatchdog.STATE_B, according to the state of the watchdog (A
        for the idle position, B for the active position)
        
        On failure, throws an exception or returns YWatchdog.STATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.STATE_INVALID
        return self._state

    def set_state(self, newval):
        """
        Changes the state of the watchdog (A for the idle position, B for the active position).
        
        @param newval : either YWatchdog.STATE_A or YWatchdog.STATE_B, according to the state of the
        watchdog (A for the idle position, B for the active position)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("state", rest_val)


    def get_output(self):
        """
        Returns the output state of the watchdog, when used as a simple switch (single throw).
        
        @return either YWatchdog.OUTPUT_OFF or YWatchdog.OUTPUT_ON, according to the output state of the
        watchdog, when used as a simple switch (single throw)
        
        On failure, throws an exception or returns YWatchdog.OUTPUT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.OUTPUT_INVALID
        return self._output

    def set_output(self, newval):
        """
        Changes the output state of the watchdog, when used as a simple switch (single throw).
        
        @param newval : either YWatchdog.OUTPUT_OFF or YWatchdog.OUTPUT_ON, according to the output state
        of the watchdog, when used as a simple switch (single throw)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("output", rest_val)


    def get_pulseTimer(self):
        """
        Returns the number of milliseconds remaining before the watchdog is returned to idle position
        (state A), during a measured pulse generation. When there is no ongoing pulse, returns zero.
        
        @return an integer corresponding to the number of milliseconds remaining before the watchdog is
        returned to idle position
                (state A), during a measured pulse generation
        
        On failure, throws an exception or returns YWatchdog.PULSETIMER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.PULSETIMER_INVALID
        return self._pulseTimer

    def set_pulseTimer(self, newval):
        rest_val = str(newval)
        return self._setAttr("pulseTimer", rest_val)


    def pulse(self , ms_duration):
        """
        Sets the relay to output B (active) for a specified duration, then brings it
        automatically back to output A (idle state).
        
        @param ms_duration : pulse duration, in millisecondes
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(ms_duration)
        return self._setAttr("pulseTimer", rest_val)

    def get_delayedPulseTimer(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.DELAYEDPULSETIMER_INVALID
        return self._delayedPulseTimer

    def set_delayedPulseTimer(self, newval):
        rest_val = str(newval.target)+":"+str(newval.ms)
        return self._setAttr("delayedPulseTimer", rest_val)


    def delayedPulse(self , ms_delay,ms_duration):
        """
        Schedules a pulse.
        
        @param ms_delay : waiting time before the pulse, in millisecondes
        @param ms_duration : pulse duration, in millisecondes
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(ms_delay)+":"+str(ms_duration)
        return self._setAttr("delayedPulseTimer", rest_val)

    def get_countdown(self):
        """
        Returns the number of milliseconds remaining before a pulse (delayedPulse() call)
        When there is no scheduled pulse, returns zero.
        
        @return an integer corresponding to the number of milliseconds remaining before a pulse (delayedPulse() call)
                When there is no scheduled pulse, returns zero
        
        On failure, throws an exception or returns YWatchdog.COUNTDOWN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.COUNTDOWN_INVALID
        return self._countdown

    def get_autoStart(self):
        """
        Returns the watchdog runing state at module power up.
        
        @return either YWatchdog.AUTOSTART_OFF or YWatchdog.AUTOSTART_ON, according to the watchdog runing
        state at module power up
        
        On failure, throws an exception or returns YWatchdog.AUTOSTART_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.AUTOSTART_INVALID
        return self._autoStart

    def set_autoStart(self, newval):
        """
        Changes the watchdog runningsttae at module power up. Remember to call the
        saveToFlash() method and then to reboot the module to apply this setting.
        
        @param newval : either YWatchdog.AUTOSTART_OFF or YWatchdog.AUTOSTART_ON, according to the watchdog
        runningsttae at module power up
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("autoStart", rest_val)


    def get_running(self):
        """
        Returns the watchdog running state.
        
        @return either YWatchdog.RUNNING_OFF or YWatchdog.RUNNING_ON, according to the watchdog running state
        
        On failure, throws an exception or returns YWatchdog.RUNNING_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.RUNNING_INVALID
        return self._running

    def set_running(self, newval):
        """
        Changes the running state of the watchdog.
        
        @param newval : either YWatchdog.RUNNING_OFF or YWatchdog.RUNNING_ON, according to the running
        state of the watchdog
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("running", rest_val)


    def resetWatchdog(self):
        """
        Resets the watchdog. When the watchdog is running, this function
        must be called on a regular basis to prevent the watchog to
        trigger
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1"
        return self._setAttr("running", rest_val)

    def get_triggerDelay(self):
        """
        Returns  the waiting duration before a reset is automatically triggered by the watchdog, in milliseconds.
        
        @return an integer corresponding to  the waiting duration before a reset is automatically triggered
        by the watchdog, in milliseconds
        
        On failure, throws an exception or returns YWatchdog.TRIGGERDELAY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.TRIGGERDELAY_INVALID
        return self._triggerDelay

    def set_triggerDelay(self, newval):
        """
        Changes the waiting delay before a reset is triggered by the watchdog, in milliseconds.
        
        @param newval : an integer corresponding to the waiting delay before a reset is triggered by the
        watchdog, in milliseconds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("triggerDelay", rest_val)


    def get_triggerDuration(self):
        """
        Returns the duration of resets caused by the watchdog, in milliseconds.
        
        @return an integer corresponding to the duration of resets caused by the watchdog, in milliseconds
        
        On failure, throws an exception or returns YWatchdog.TRIGGERDURATION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWatchdog.TRIGGERDURATION_INVALID
        return self._triggerDuration

    def set_triggerDuration(self, newval):
        """
        Changes the duration of resets caused by the watchdog, in milliseconds.
        
        @param newval : an integer corresponding to the duration of resets caused by the watchdog, in milliseconds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("triggerDuration", rest_val)


    def nextWatchdog(self):
        """
        Continues the enumeration of watchdog started using yFirstWatchdog().
        
        @return a pointer to a YWatchdog object, corresponding to
                a watchdog currently online, or a None pointer
                if there are no more watchdog to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YWatchdog.FindWatchdog(hwidRef.value)

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

#--- (end of YWatchdog implementation)

#--- (Watchdog functions)

    @staticmethod 
    def FindWatchdog(func):
        """
        Retrieves a watchdog for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the watchdog is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWatchdog.isOnline() to test if the watchdog is
        indeed online at a given time. In case of ambiguity when looking for
        a watchdog by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the watchdog
        
        @return a YWatchdog object allowing you to drive the watchdog.
        """
        if func in YWatchdog._WatchdogCache:
            return YWatchdog._WatchdogCache[func]
        res =YWatchdog(func)
        YWatchdog._WatchdogCache[func] =  res
        return res

    @staticmethod 
    def  FirstWatchdog():
        """
        Starts the enumeration of watchdog currently accessible.
        Use the method YWatchdog.nextWatchdog() to iterate on
        next watchdog.
        
        @return a pointer to a YWatchdog object, corresponding to
                the first watchdog currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Watchdog", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YWatchdog.FindWatchdog(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _WatchdogCleanup():
        pass

  #--- (end of Watchdog functions)

