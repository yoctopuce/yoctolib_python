#*********************************************************************
#*
#* $Id: yocto_led.py 9921 2013-02-20 09:39:16Z seb $
#*
#* Implements yFindLed(), the high-level API for Led functions
#*
#* - - - - - - - - - License information: - - - - - - - - - 
#*
#* Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#*
#* 1) If you have obtained this file from www.yoctopuce.com,
#*    Yoctopuce Sarl licenses to you (hereafter Licensee) the
#*    right to use, modify, copy, and integrate this source file
#*    into your own solution for the sole purpose of interfacing
#*    a Yoctopuce product with Licensee's solution.
#*
#*    The use of this file and all relationship between Yoctopuce 
#*    and Licensee are governed by Yoctopuce General Terms and 
#*    Conditions.
#*
#*    THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#*    WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING 
#*    WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS 
#*    FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#*    EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#*    INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, 
#*    COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR 
#*    SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT 
#*    LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#*    CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#*    BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#*    WARRANTY, OR OTHERWISE.
#*
#* 2) If your intent is not to interface with Yoctopuce products,
#*    you are not entitled to use, read or create any derived
#*    material from this source file.
#*
#*********************************************************************/


__docformat__ = 'restructuredtext en'
from yocto_api import *
class YLed(YFunction):
    """
    Yoctopuce application programming interface
    allows you not only to drive the intensity of the led, but also to
    have it blink at various preset frequencies.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YLed definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    LUMINOSITY_INVALID              = YAPI.INVALID_LONG

    POWER_OFF                       = 0
    POWER_ON                        = 1
    POWER_INVALID                   = -1
    BLINKING_STILL                  = 0
    BLINKING_RELAX                  = 1
    BLINKING_AWARE                  = 2
    BLINKING_RUN                    = 3
    BLINKING_CALL                   = 4
    BLINKING_PANIC                  = 5
    BLINKING_INVALID                = -1


    _LedCache ={}

    #--- (end of YLed definitions)

    #--- (YLed implementation)

    def __init__(self,func):
        super(YLed,self).__init__("Led", func)
        #--- (YLed implementation)
        self._callback = None
        self._logicalName = YLed.LOGICALNAME_INVALID
        self._advertisedValue = YLed.ADVERTISEDVALUE_INVALID
        self._power = YLed.POWER_INVALID
        self._luminosity = YLed.LUMINOSITY_INVALID
        self._blinking = YLed.BLINKING_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "power":
                self._power = member.ivalue
            elif member.name == "luminosity":
                self._luminosity = member.ivalue
            elif member.name == "blinking":
                self._blinking = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the led.
        
        @return a string corresponding to the logical name of the led
        
        On failure, throws an exception or returns YLed.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YLed.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the led. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the led
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the led (no more than 6 characters).
        
        @return a string corresponding to the current value of the led (no more than 6 characters)
        
        On failure, throws an exception or returns YLed.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YLed.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_power(self):
        """
        Returns the current led state.
        
        @return either YLed.POWER_OFF or YLed.POWER_ON, according to the current led state
        
        On failure, throws an exception or returns YLed.POWER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YLed.POWER_INVALID
        return self._power

    def set_power(self, newval):
        """
        Changes the state of the led.
        
        @param newval : either YLed.POWER_OFF or YLed.POWER_ON, according to the state of the led
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("power", rest_val)


    def get_luminosity(self):
        """
        Returns the current led intensity (in per cent).
        
        @return an integer corresponding to the current led intensity (in per cent)
        
        On failure, throws an exception or returns YLed.LUMINOSITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
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
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
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

#--- (end of YLed implementation)

#--- (Led functions)

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
        if func in YLed._LedCache:
            return YLed._LedCache[func]
        res =YLed(func)
        YLed._LedCache[func] =  res
        return res

    @staticmethod 
    def  FirstLed():
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
        p = (ctypes.c_int*1)()
        err = YAPI.apiGetFunctionsByClass("Led", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YLed.FindLed(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _LedCleanup():
        pass

  #--- (end of Led functions)

