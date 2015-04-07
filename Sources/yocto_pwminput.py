#*********************************************************************
#*
#* $Id: yocto_pwminput.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindPwmInput(), the high-level API for PwmInput functions
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


#--- (YPwmInput class start)
#noinspection PyProtectedMember
class YPwmInput(YSensor):
    """
    The Yoctopuce class YPwmInput allows you to read and configure Yoctopuce PWM
    sensors. It inherits from YSensor class the core functions to read measurements,
    register callback functions, access to the autonomous datalogger.
    This class adds the ability to configure the signal parameter used to transmit
    information: the duty cacle, the frequency or the pulse width.

    """
#--- (end of YPwmInput class start)
    #--- (YPwmInput return codes)
    #--- (end of YPwmInput return codes)
    #--- (YPwmInput dlldef)
    #--- (end of YPwmInput dlldef)
    #--- (YPwmInput definitions)
    DUTYCYCLE_INVALID = YAPI.INVALID_DOUBLE
    PULSEDURATION_INVALID = YAPI.INVALID_DOUBLE
    FREQUENCY_INVALID = YAPI.INVALID_DOUBLE
    PERIOD_INVALID = YAPI.INVALID_DOUBLE
    PULSECOUNTER_INVALID = YAPI.INVALID_LONG
    PULSETIMER_INVALID = YAPI.INVALID_LONG
    PWMREPORTMODE_PWM_DUTYCYCLE = 0
    PWMREPORTMODE_PWM_FREQUENCY = 1
    PWMREPORTMODE_PWM_PULSEDURATION = 2
    PWMREPORTMODE_PWM_EDGECOUNT = 3
    PWMREPORTMODE_INVALID = -1
    #--- (end of YPwmInput definitions)

    def __init__(self, func):
        super(YPwmInput, self).__init__(func)
        self._className = 'PwmInput'
        #--- (YPwmInput attributes)
        self._callback = None
        self._dutyCycle = YPwmInput.DUTYCYCLE_INVALID
        self._pulseDuration = YPwmInput.PULSEDURATION_INVALID
        self._frequency = YPwmInput.FREQUENCY_INVALID
        self._period = YPwmInput.PERIOD_INVALID
        self._pulseCounter = YPwmInput.PULSECOUNTER_INVALID
        self._pulseTimer = YPwmInput.PULSETIMER_INVALID
        self._pwmReportMode = YPwmInput.PWMREPORTMODE_INVALID
        #--- (end of YPwmInput attributes)

    #--- (YPwmInput implementation)
    def _parseAttr(self, member):
        if member.name == "dutyCycle":
            self._dutyCycle = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "pulseDuration":
            self._pulseDuration = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "frequency":
            self._frequency = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "period":
            self._period = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "pulseCounter":
            self._pulseCounter = member.ivalue
            return 1
        if member.name == "pulseTimer":
            self._pulseTimer = member.ivalue
            return 1
        if member.name == "pwmReportMode":
            self._pwmReportMode = member.ivalue
            return 1
        super(YPwmInput, self)._parseAttr(member)

    def get_dutyCycle(self):
        """
        Returns the PWM duty cycle, in per cents.

        @return a floating point number corresponding to the PWM duty cycle, in per cents

        On failure, throws an exception or returns YPwmInput.DUTYCYCLE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.DUTYCYCLE_INVALID
        return self._dutyCycle

    def get_pulseDuration(self):
        """
        Returns the PWM pulse length in milliseconds, as a floating point number.

        @return a floating point number corresponding to the PWM pulse length in milliseconds, as a
        floating point number

        On failure, throws an exception or returns YPwmInput.PULSEDURATION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.PULSEDURATION_INVALID
        return self._pulseDuration

    def get_frequency(self):
        """
        Returns the PWM frequency in Hz.

        @return a floating point number corresponding to the PWM frequency in Hz

        On failure, throws an exception or returns YPwmInput.FREQUENCY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.FREQUENCY_INVALID
        return self._frequency

    def get_period(self):
        """
        Returns the PWM period in milliseconds.

        @return a floating point number corresponding to the PWM period in milliseconds

        On failure, throws an exception or returns YPwmInput.PERIOD_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.PERIOD_INVALID
        return self._period

    def get_pulseCounter(self):
        """
        Returns the pulse counter value. Actually that
        counter is incremented twice per period. That counter is
        limited  to 1 billion

        @return an integer corresponding to the pulse counter value

        On failure, throws an exception or returns YPwmInput.PULSECOUNTER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.PULSECOUNTER_INVALID
        return self._pulseCounter

    def set_pulseCounter(self, newval):
        rest_val = str(newval)
        return self._setAttr("pulseCounter", rest_val)

    def get_pulseTimer(self):
        """
        Returns the timer of the pulses counter (ms)

        @return an integer corresponding to the timer of the pulses counter (ms)

        On failure, throws an exception or returns YPwmInput.PULSETIMER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.PULSETIMER_INVALID
        return self._pulseTimer

    def get_pwmReportMode(self):
        """
        Returns the parameter (frequency/duty cycle, pulse width, edges count) returned by the
        get_currentValue function and callbacks. Attention

        @return a value among YPwmInput.PWMREPORTMODE_PWM_DUTYCYCLE, YPwmInput.PWMREPORTMODE_PWM_FREQUENCY,
        YPwmInput.PWMREPORTMODE_PWM_PULSEDURATION and YPwmInput.PWMREPORTMODE_PWM_EDGECOUNT corresponding
        to the parameter (frequency/duty cycle, pulse width, edges count) returned by the get_currentValue
        function and callbacks

        On failure, throws an exception or returns YPwmInput.PWMREPORTMODE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmInput.PWMREPORTMODE_INVALID
        return self._pwmReportMode

    def set_pwmReportMode(self, newval):
        """
        Modifies the  parameter  type (frequency/duty cycle, pulse width, or edge count) returned by the
        get_currentValue function and callbacks.
        The edge count value is limited to the 6 lowest digits. For values greater than one million, use
        get_pulseCounter().

        @param newval : a value among YPwmInput.PWMREPORTMODE_PWM_DUTYCYCLE,
        YPwmInput.PWMREPORTMODE_PWM_FREQUENCY, YPwmInput.PWMREPORTMODE_PWM_PULSEDURATION and
        YPwmInput.PWMREPORTMODE_PWM_EDGECOUNT

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("pwmReportMode", rest_val)

    @staticmethod
    def FindPwmInput(func):
        """
        Retrieves a PWM input for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the PWM input is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPwmInput.isOnline() to test if the PWM input is
        indeed online at a given time. In case of ambiguity when looking for
        a PWM input by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the PWM input

        @return a YPwmInput object allowing you to drive the PWM input.
        """
        # obj
        obj = YFunction._FindFromCache("PwmInput", func)
        if obj is None:
            obj = YPwmInput(func)
            YFunction._AddToCache("PwmInput", func, obj)
        return obj

    def resetCounter(self):
        """
        Returns the pulse counter value as well as its timer.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_pulseCounter(0)

    def nextPwmInput(self):
        """
        Continues the enumeration of PWM inputs started using yFirstPwmInput().

        @return a pointer to a YPwmInput object, corresponding to
                a PWM input currently online, or a None pointer
                if there are no more PWM inputs to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YPwmInput.FindPwmInput(hwidRef.value)

#--- (end of YPwmInput implementation)

#--- (PwmInput functions)

    @staticmethod
    def FirstPwmInput():
        """
        Starts the enumeration of PWM inputs currently accessible.
        Use the method YPwmInput.nextPwmInput() to iterate on
        next PWM inputs.

        @return a pointer to a YPwmInput object, corresponding to
                the first PWM input currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("PwmInput", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YPwmInput.FindPwmInput(serialRef.value + "." + funcIdRef.value)

#--- (end of PwmInput functions)
