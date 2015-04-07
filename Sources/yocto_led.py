#*********************************************************************
#*
#* $Id: yocto_led.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindLed(), the high-level API for Led functions
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


#--- (YLed class start)
#noinspection PyProtectedMember
class YLed(YFunction):
    """
    Yoctopuce application programming interface
    allows you not only to drive the intensity of the led, but also to
    have it blink at various preset frequencies.

    """
#--- (end of YLed class start)
    #--- (YLed return codes)
    #--- (end of YLed return codes)
    #--- (YLed dlldef)
    #--- (end of YLed dlldef)
    #--- (YLed definitions)
    LUMINOSITY_INVALID = YAPI.INVALID_UINT
    POWER_OFF = 0
    POWER_ON = 1
    POWER_INVALID = -1
    BLINKING_STILL = 0
    BLINKING_RELAX = 1
    BLINKING_AWARE = 2
    BLINKING_RUN = 3
    BLINKING_CALL = 4
    BLINKING_PANIC = 5
    BLINKING_INVALID = -1
    #--- (end of YLed definitions)

    def __init__(self, func):
        super(YLed, self).__init__(func)
        self._className = 'Led'
        #--- (YLed attributes)
        self._callback = None
        self._power = YLed.POWER_INVALID
        self._luminosity = YLed.LUMINOSITY_INVALID
        self._blinking = YLed.BLINKING_INVALID
        #--- (end of YLed attributes)

    #--- (YLed implementation)
    def _parseAttr(self, member):
        if member.name == "power":
            self._power = member.ivalue
            return 1
        if member.name == "luminosity":
            self._luminosity = member.ivalue
            return 1
        if member.name == "blinking":
            self._blinking = member.ivalue
            return 1
        super(YLed, self)._parseAttr(member)

    def get_power(self):
        """
        Returns the current led state.

        @return either YLed.POWER_OFF or YLed.POWER_ON, according to the current led state

        On failure, throws an exception or returns YLed.POWER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YLed.POWER_INVALID
        return self._power

    def set_power(self, newval):
        """
        Changes the state of the led.

        @param newval : either YLed.POWER_OFF or YLed.POWER_ON, according to the state of the led

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("power", rest_val)

    def get_luminosity(self):
        """
        Returns the current led intensity (in per cent).

        @return an integer corresponding to the current led intensity (in per cent)

        On failure, throws an exception or returns YLed.LUMINOSITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YLed.LUMINOSITY_INVALID
        return self._luminosity

    def set_luminosity(self, newval):
        """
        Changes the current led intensity (in per cent).

        @param newval : an integer corresponding to the current led intensity (in per cent)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("luminosity", rest_val)

    def get_blinking(self):
        """
        Returns the current led signaling mode.

        @return a value among YLed.BLINKING_STILL, YLed.BLINKING_RELAX, YLed.BLINKING_AWARE,
        YLed.BLINKING_RUN, YLed.BLINKING_CALL and YLed.BLINKING_PANIC corresponding to the current led signaling mode

        On failure, throws an exception or returns YLed.BLINKING_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YLed.BLINKING_INVALID
        return self._blinking

    def set_blinking(self, newval):
        """
        Changes the current led signaling mode.

        @param newval : a value among YLed.BLINKING_STILL, YLed.BLINKING_RELAX, YLed.BLINKING_AWARE,
        YLed.BLINKING_RUN, YLed.BLINKING_CALL and YLed.BLINKING_PANIC corresponding to the current led signaling mode

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("blinking", rest_val)

    @staticmethod
    def FindLed(func):
        """
        Retrieves a led for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the led is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YLed.isOnline() to test if the led is
        indeed online at a given time. In case of ambiguity when looking for
        a led by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the led

        @return a YLed object allowing you to drive the led.
        """
        # obj
        obj = YFunction._FindFromCache("Led", func)
        if obj is None:
            obj = YLed(func)
            YFunction._AddToCache("Led", func, obj)
        return obj

    def nextLed(self):
        """
        Continues the enumeration of leds started using yFirstLed().

        @return a pointer to a YLed object, corresponding to
                a led currently online, or a None pointer
                if there are no more leds to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YLed.FindLed(hwidRef.value)

#--- (end of YLed implementation)

#--- (Led functions)

    @staticmethod
    def FirstLed():
        """
        Starts the enumeration of leds currently accessible.
        Use the method YLed.nextLed() to iterate on
        next leds.

        @return a pointer to a YLed object, corresponding to
                the first led currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Led", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YLed.FindLed(serialRef.value + "." + funcIdRef.value)

#--- (end of Led functions)
