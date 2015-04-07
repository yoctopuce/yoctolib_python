#*********************************************************************
#*
#* $Id: yocto_accelerometer.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindAccelerometer(), the high-level API for Accelerometer functions
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


#--- (YAccelerometer class start)
#noinspection PyProtectedMember
class YAccelerometer(YSensor):
    """
    The YSensor class is the parent class for all Yoctopuce sensors. It can be
    used to read the current value and unit of any sensor, read the min/max
    value, configure autonomous recording frequency and access recorded data.
    It also provide a function to register a callback invoked each time the
    observed value changes, or at a predefined interval. Using this class rather
    than a specific subclass makes it possible to create generic applications
    that work with any Yoctopuce sensor, even those that do not yet exist.
    Note: The YAnButton class is the only analog input which does not inherit
    from YSensor.

    """
#--- (end of YAccelerometer class start)
    #--- (YAccelerometer return codes)
    #--- (end of YAccelerometer return codes)
    #--- (YAccelerometer dlldef)
    #--- (end of YAccelerometer dlldef)
    #--- (YAccelerometer definitions)
    XVALUE_INVALID = YAPI.INVALID_DOUBLE
    YVALUE_INVALID = YAPI.INVALID_DOUBLE
    ZVALUE_INVALID = YAPI.INVALID_DOUBLE
    GRAVITYCANCELLATION_OFF = 0
    GRAVITYCANCELLATION_ON = 1
    GRAVITYCANCELLATION_INVALID = -1
    #--- (end of YAccelerometer definitions)

    def __init__(self, func):
        super(YAccelerometer, self).__init__(func)
        self._className = 'Accelerometer'
        #--- (YAccelerometer attributes)
        self._callback = None
        self._xValue = YAccelerometer.XVALUE_INVALID
        self._yValue = YAccelerometer.YVALUE_INVALID
        self._zValue = YAccelerometer.ZVALUE_INVALID
        self._gravityCancellation = YAccelerometer.GRAVITYCANCELLATION_INVALID
        #--- (end of YAccelerometer attributes)

    #--- (YAccelerometer implementation)
    def _parseAttr(self, member):
        if member.name == "xValue":
            self._xValue = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "yValue":
            self._yValue = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "zValue":
            self._zValue = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "gravityCancellation":
            self._gravityCancellation = member.ivalue
            return 1
        super(YAccelerometer, self)._parseAttr(member)

    def get_xValue(self):
        """
        Returns the X component of the acceleration, as a floating point number.

        @return a floating point number corresponding to the X component of the acceleration, as a floating point number

        On failure, throws an exception or returns YAccelerometer.XVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAccelerometer.XVALUE_INVALID
        return self._xValue

    def get_yValue(self):
        """
        Returns the Y component of the acceleration, as a floating point number.

        @return a floating point number corresponding to the Y component of the acceleration, as a floating point number

        On failure, throws an exception or returns YAccelerometer.YVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAccelerometer.YVALUE_INVALID
        return self._yValue

    def get_zValue(self):
        """
        Returns the Z component of the acceleration, as a floating point number.

        @return a floating point number corresponding to the Z component of the acceleration, as a floating point number

        On failure, throws an exception or returns YAccelerometer.ZVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAccelerometer.ZVALUE_INVALID
        return self._zValue

    def get_gravityCancellation(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAccelerometer.GRAVITYCANCELLATION_INVALID
        return self._gravityCancellation

    def set_gravityCancellation(self, newval):
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("gravityCancellation", rest_val)

    @staticmethod
    def FindAccelerometer(func):
        """
        Retrieves an accelerometer for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the accelerometer is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YAccelerometer.isOnline() to test if the accelerometer is
        indeed online at a given time. In case of ambiguity when looking for
        an accelerometer by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the accelerometer

        @return a YAccelerometer object allowing you to drive the accelerometer.
        """
        # obj
        obj = YFunction._FindFromCache("Accelerometer", func)
        if obj is None:
            obj = YAccelerometer(func)
            YFunction._AddToCache("Accelerometer", func, obj)
        return obj

    def nextAccelerometer(self):
        """
        Continues the enumeration of accelerometers started using yFirstAccelerometer().

        @return a pointer to a YAccelerometer object, corresponding to
                an accelerometer currently online, or a None pointer
                if there are no more accelerometers to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YAccelerometer.FindAccelerometer(hwidRef.value)

#--- (end of YAccelerometer implementation)

#--- (Accelerometer functions)

    @staticmethod
    def FirstAccelerometer():
        """
        Starts the enumeration of accelerometers currently accessible.
        Use the method YAccelerometer.nextAccelerometer() to iterate on
        next accelerometers.

        @return a pointer to a YAccelerometer object, corresponding to
                the first accelerometer currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Accelerometer", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YAccelerometer.FindAccelerometer(serialRef.value + "." + funcIdRef.value)

#--- (end of Accelerometer functions)
