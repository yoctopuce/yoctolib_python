#*********************************************************************
#*
#* $Id: yocto_relay.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindRelay(), the high-level API for Relay functions
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
class YRelay(YFunction):
    """
    The Yoctopuce application programming interface allows you to switch the relay state.
    This change is not persistent: the relay will automatically return to its idle position
    whenever power is lost or if the module is restarted.
    The library can also generate automatically short pulses of determined duration.
    On devices with two output for each relay (double throw), the two outputs are named A and B,
    with output A corresponding to the idle position (at power off) and the output B corresponding to the
    active state. If you prefer the alternate default state, simply switch your cables on the board.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YRelay definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    PULSETIMER_INVALID              = YAPI.INVALID_LONG
    DELAYEDPULSETIMER_INVALID       = None
    COUNTDOWN_INVALID               = YAPI.INVALID_LONG

    STATE_A                         = 0
    STATE_B                         = 1
    STATE_INVALID                   = -1
    OUTPUT_OFF                      = 0
    OUTPUT_ON                       = 1
    OUTPUT_INVALID                  = -1


    _RelayCache ={}

    #--- (end of YRelay definitions)

    #--- (YRelay implementation)

    def __init__(self,func):
        super(YRelay,self).__init__("Relay", func)
        self._callback = None
        self._logicalName = YRelay.LOGICALNAME_INVALID
        self._advertisedValue = YRelay.ADVERTISEDVALUE_INVALID
        self._state = YRelay.STATE_INVALID
        self._output = YRelay.OUTPUT_INVALID
        self._pulseTimer = YRelay.PULSETIMER_INVALID
        self._delayedPulseTimer = YRelay.DELAYEDPULSETIMER_INVALID
        self._countdown = YRelay.COUNTDOWN_INVALID

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
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the relay.
        
        @return a string corresponding to the logical name of the relay
        
        On failure, throws an exception or returns YRelay.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRelay.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the relay. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the relay
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the relay (no more than 6 characters).
        
        @return a string corresponding to the current value of the relay (no more than 6 characters)
        
        On failure, throws an exception or returns YRelay.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRelay.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_state(self):
        """
        Returns the state of the relays (A for the idle position, B for the active position).
        
        @return either YRelay.STATE_A or YRelay.STATE_B, according to the state of the relays (A for the
        idle position, B for the active position)
        
        On failure, throws an exception or returns YRelay.STATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRelay.STATE_INVALID
        return self._state

    def set_state(self, newval):
        """
        Changes the state of the relays (A for the idle position, B for the active position).
        
        @param newval : either YRelay.STATE_A or YRelay.STATE_B, according to the state of the relays (A
        for the idle position, B for the active position)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("state", rest_val)


    def get_output(self):
        """
        Returns the output state of the relays, when used as a simple switch (single throw).
        
        @return either YRelay.OUTPUT_OFF or YRelay.OUTPUT_ON, according to the output state of the relays,
        when used as a simple switch (single throw)
        
        On failure, throws an exception or returns YRelay.OUTPUT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRelay.OUTPUT_INVALID
        return self._output

    def set_output(self, newval):
        """
        Changes the output state of the relays, when used as a simple switch (single throw).
        
        @param newval : either YRelay.OUTPUT_OFF or YRelay.OUTPUT_ON, according to the output state of the
        relays, when used as a simple switch (single throw)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("output", rest_val)


    def get_pulseTimer(self):
        """
        Returns the number of milliseconds remaining before the relays is returned to idle position
        (state A), during a measured pulse generation. When there is no ongoing pulse, returns zero.
        
        @return an integer corresponding to the number of milliseconds remaining before the relays is
        returned to idle position
                (state A), during a measured pulse generation
        
        On failure, throws an exception or returns YRelay.PULSETIMER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRelay.PULSETIMER_INVALID
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
                return YRelay.DELAYEDPULSETIMER_INVALID
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
        
        On failure, throws an exception or returns YRelay.COUNTDOWN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YRelay.COUNTDOWN_INVALID
        return self._countdown

    def nextRelay(self):
        """
        Continues the enumeration of relays started using yFirstRelay().
        
        @return a pointer to a YRelay object, corresponding to
                a relay currently online, or a None pointer
                if there are no more relays to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YRelay.FindRelay(hwidRef.value)

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

#--- (end of YRelay implementation)

#--- (Relay functions)

    @staticmethod 
    def FindRelay(func):
        """
        Retrieves a relay for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the relay is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRelay.isOnline() to test if the relay is
        indeed online at a given time. In case of ambiguity when looking for
        a relay by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the relay
        
        @return a YRelay object allowing you to drive the relay.
        """
        if func in YRelay._RelayCache:
            return YRelay._RelayCache[func]
        res =YRelay(func)
        YRelay._RelayCache[func] =  res
        return res

    @staticmethod 
    def  FirstRelay():
        """
        Starts the enumeration of relays currently accessible.
        Use the method YRelay.nextRelay() to iterate on
        next relays.
        
        @return a pointer to a YRelay object, corresponding to
                the first relay currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Relay", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YRelay.FindRelay(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _RelayCleanup():
        pass

  #--- (end of Relay functions)

