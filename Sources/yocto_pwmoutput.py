#*********************************************************************
#*
#* $Id: yocto_pwmoutput.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindPwmOutput(), the high-level API for PwmOutput functions
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


#--- (YPwmOutput class start)
#noinspection PyProtectedMember
class YPwmOutput(YFunction):
    """
    The Yoctopuce application programming interface allows you to configure, start, and stop the PWM.

    """
#--- (end of YPwmOutput class start)
    #--- (YPwmOutput return codes)
    #--- (end of YPwmOutput return codes)
    #--- (YPwmOutput dlldef)
    #--- (end of YPwmOutput dlldef)
    #--- (YPwmOutput definitions)
    FREQUENCY_INVALID = YAPI.INVALID_DOUBLE
    PERIOD_INVALID = YAPI.INVALID_DOUBLE
    DUTYCYCLE_INVALID = YAPI.INVALID_DOUBLE
    PULSEDURATION_INVALID = YAPI.INVALID_DOUBLE
    PWMTRANSITION_INVALID = YAPI.INVALID_STRING
    DUTYCYCLEATPOWERON_INVALID = YAPI.INVALID_DOUBLE
    ENABLED_FALSE = 0
    ENABLED_TRUE = 1
    ENABLED_INVALID = -1
    ENABLEDATPOWERON_FALSE = 0
    ENABLEDATPOWERON_TRUE = 1
    ENABLEDATPOWERON_INVALID = -1
    #--- (end of YPwmOutput definitions)

    def __init__(self, func):
        super(YPwmOutput, self).__init__(func)
        self._className = 'PwmOutput'
        #--- (YPwmOutput attributes)
        self._callback = None
        self._enabled = YPwmOutput.ENABLED_INVALID
        self._frequency = YPwmOutput.FREQUENCY_INVALID
        self._period = YPwmOutput.PERIOD_INVALID
        self._dutyCycle = YPwmOutput.DUTYCYCLE_INVALID
        self._pulseDuration = YPwmOutput.PULSEDURATION_INVALID
        self._pwmTransition = YPwmOutput.PWMTRANSITION_INVALID
        self._enabledAtPowerOn = YPwmOutput.ENABLEDATPOWERON_INVALID
        self._dutyCycleAtPowerOn = YPwmOutput.DUTYCYCLEATPOWERON_INVALID
        #--- (end of YPwmOutput attributes)

    #--- (YPwmOutput implementation)
    def _parseAttr(self, member):
        if member.name == "enabled":
            self._enabled = member.ivalue
            return 1
        if member.name == "frequency":
            self._frequency = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "period":
            self._period = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "dutyCycle":
            self._dutyCycle = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "pulseDuration":
            self._pulseDuration = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "pwmTransition":
            self._pwmTransition = member.svalue
            return 1
        if member.name == "enabledAtPowerOn":
            self._enabledAtPowerOn = member.ivalue
            return 1
        if member.name == "dutyCycleAtPowerOn":
            self._dutyCycleAtPowerOn = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        super(YPwmOutput, self)._parseAttr(member)

    def get_enabled(self):
        """
        Returns the state of the PWMs.

        @return either YPwmOutput.ENABLED_FALSE or YPwmOutput.ENABLED_TRUE, according to the state of the PWMs

        On failure, throws an exception or returns YPwmOutput.ENABLED_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.ENABLED_INVALID
        return self._enabled

    def set_enabled(self, newval):
        """
        Stops or starts the PWM.

        @param newval : either YPwmOutput.ENABLED_FALSE or YPwmOutput.ENABLED_TRUE

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("enabled", rest_val)

    def set_frequency(self, newval):
        """
        Changes the PWM frequency. The duty cycle is kept unchanged thanks to an
        automatic pulse width change.

        @param newval : a floating point number corresponding to the PWM frequency

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("frequency", rest_val)

    def get_frequency(self):
        """
        Returns the PWM frequency in Hz.

        @return a floating point number corresponding to the PWM frequency in Hz

        On failure, throws an exception or returns YPwmOutput.FREQUENCY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.FREQUENCY_INVALID
        return self._frequency

    def set_period(self, newval):
        """
        Changes the PWM period in milliseconds.

        @param newval : a floating point number corresponding to the PWM period in milliseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("period", rest_val)

    def get_period(self):
        """
        Returns the PWM period in milliseconds.

        @return a floating point number corresponding to the PWM period in milliseconds

        On failure, throws an exception or returns YPwmOutput.PERIOD_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.PERIOD_INVALID
        return self._period

    def set_dutyCycle(self, newval):
        """
        Changes the PWM duty cycle, in per cents.

        @param newval : a floating point number corresponding to the PWM duty cycle, in per cents

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("dutyCycle", rest_val)

    def get_dutyCycle(self):
        """
        Returns the PWM duty cycle, in per cents.

        @return a floating point number corresponding to the PWM duty cycle, in per cents

        On failure, throws an exception or returns YPwmOutput.DUTYCYCLE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.DUTYCYCLE_INVALID
        return self._dutyCycle

    def set_pulseDuration(self, newval):
        """
        Changes the PWM pulse length, in milliseconds. A pulse length cannot be longer than period,
        otherwise it is truncated.

        @param newval : a floating point number corresponding to the PWM pulse length, in milliseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("pulseDuration", rest_val)

    def get_pulseDuration(self):
        """
        Returns the PWM pulse length in milliseconds, as a floating point number.

        @return a floating point number corresponding to the PWM pulse length in milliseconds, as a
        floating point number

        On failure, throws an exception or returns YPwmOutput.PULSEDURATION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.PULSEDURATION_INVALID
        return self._pulseDuration

    def get_pwmTransition(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.PWMTRANSITION_INVALID
        return self._pwmTransition

    def set_pwmTransition(self, newval):
        rest_val = newval
        return self._setAttr("pwmTransition", rest_val)

    def get_enabledAtPowerOn(self):
        """
        Returns the state of the PWM at device power on.

        @return either YPwmOutput.ENABLEDATPOWERON_FALSE or YPwmOutput.ENABLEDATPOWERON_TRUE, according to
        the state of the PWM at device power on

        On failure, throws an exception or returns YPwmOutput.ENABLEDATPOWERON_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.ENABLEDATPOWERON_INVALID
        return self._enabledAtPowerOn

    def set_enabledAtPowerOn(self, newval):
        """
        Changes the state of the PWM at device power on. Remember to call the matching module saveToFlash()
        method, otherwise this call will have no effect.

        @param newval : either YPwmOutput.ENABLEDATPOWERON_FALSE or YPwmOutput.ENABLEDATPOWERON_TRUE,
        according to the state of the PWM at device power on

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("enabledAtPowerOn", rest_val)

    def set_dutyCycleAtPowerOn(self, newval):
        """
        Changes the PWM duty cycle at device power on. Remember to call the matching
        module saveToFlash() method, otherwise this call will have no effect.

        @param newval : a floating point number corresponding to the PWM duty cycle at device power on

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("dutyCycleAtPowerOn", rest_val)

    def get_dutyCycleAtPowerOn(self):
        """
        Returns the PWMs duty cycle at device power on as a floating point number between 0 and 100

        @return a floating point number corresponding to the PWMs duty cycle at device power on as a
        floating point number between 0 and 100

        On failure, throws an exception or returns YPwmOutput.DUTYCYCLEATPOWERON_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPwmOutput.DUTYCYCLEATPOWERON_INVALID
        return self._dutyCycleAtPowerOn

    @staticmethod
    def FindPwmOutput(func):
        """
        Retrieves a PWM for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the PWM is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPwmOutput.isOnline() to test if the PWM is
        indeed online at a given time. In case of ambiguity when looking for
        a PWM by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the PWM

        @return a YPwmOutput object allowing you to drive the PWM.
        """
        # obj
        obj = YFunction._FindFromCache("PwmOutput", func)
        if obj is None:
            obj = YPwmOutput(func)
            YFunction._AddToCache("PwmOutput", func, obj)
        return obj

    def pulseDurationMove(self, ms_target, ms_duration):
        """
        Performs a smooth transistion of the pulse duration toward a given value. Any period,
        frequency, duty cycle or pulse width change will cancel any ongoing transition process.

        @param ms_target   : new pulse duration at the end of the transition
                (floating-point number, representing the pulse duration in milliseconds)
        @param ms_duration : total duration of the transition, in milliseconds

        @return YAPI.SUCCESS when the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # newval
        if ms_target < 0.0:
            ms_target = 0.0
        newval = "" + str(int(round(ms_target*65536))) + "ms:" + str(int(ms_duration))
        return self.set_pwmTransition(newval)

    def dutyCycleMove(self, target, ms_duration):
        """
        Performs a smooth change of the pulse duration toward a given value.

        @param target      : new duty cycle at the end of the transition
                (floating-point number, between 0 and 1)
        @param ms_duration : total duration of the transition, in milliseconds

        @return YAPI.SUCCESS when the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # newval
        if target < 0.0:
            target = 0.0
        if target > 100.0:
            target = 100.0
        newval = "" + str(int(round(target*65536))) + ":" + str(int(ms_duration))
        return self.set_pwmTransition(newval)

    def nextPwmOutput(self):
        """
        Continues the enumeration of PWMs started using yFirstPwmOutput().

        @return a pointer to a YPwmOutput object, corresponding to
                a PWM currently online, or a None pointer
                if there are no more PWMs to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YPwmOutput.FindPwmOutput(hwidRef.value)

#--- (end of YPwmOutput implementation)

#--- (PwmOutput functions)

    @staticmethod
    def FirstPwmOutput():
        """
        Starts the enumeration of PWMs currently accessible.
        Use the method YPwmOutput.nextPwmOutput() to iterate on
        next PWMs.

        @return a pointer to a YPwmOutput object, corresponding to
                the first PWM currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("PwmOutput", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YPwmOutput.FindPwmOutput(serialRef.value + "." + funcIdRef.value)

#--- (end of PwmOutput functions)
