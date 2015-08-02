#*********************************************************************
#*
#* $Id: yocto_magnetometer.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindMagnetometer(), the high-level API for Magnetometer functions
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


#--- (YMagnetometer class start)
#noinspection PyProtectedMember
class YMagnetometer(YSensor):
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
#--- (end of YMagnetometer class start)
    #--- (YMagnetometer return codes)
    #--- (end of YMagnetometer return codes)
    #--- (YMagnetometer dlldef)
    #--- (end of YMagnetometer dlldef)
    #--- (YMagnetometer definitions)
    XVALUE_INVALID = YAPI.INVALID_DOUBLE
    YVALUE_INVALID = YAPI.INVALID_DOUBLE
    ZVALUE_INVALID = YAPI.INVALID_DOUBLE
    #--- (end of YMagnetometer definitions)

    def __init__(self, func):
        super(YMagnetometer, self).__init__(func)
        self._className = 'Magnetometer'
        #--- (YMagnetometer attributes)
        self._callback = None
        self._xValue = YMagnetometer.XVALUE_INVALID
        self._yValue = YMagnetometer.YVALUE_INVALID
        self._zValue = YMagnetometer.ZVALUE_INVALID
        #--- (end of YMagnetometer attributes)

    #--- (YMagnetometer implementation)
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
        super(YMagnetometer, self)._parseAttr(member)

    def get_xValue(self):
        """
        Returns the X component of the magnetic field, as a floating point number.

        @return a floating point number corresponding to the X component of the magnetic field, as a
        floating point number

        On failure, throws an exception or returns YMagnetometer.XVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMagnetometer.XVALUE_INVALID
        return self._xValue

    def get_yValue(self):
        """
        Returns the Y component of the magnetic field, as a floating point number.

        @return a floating point number corresponding to the Y component of the magnetic field, as a
        floating point number

        On failure, throws an exception or returns YMagnetometer.YVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMagnetometer.YVALUE_INVALID
        return self._yValue

    def get_zValue(self):
        """
        Returns the Z component of the magnetic field, as a floating point number.

        @return a floating point number corresponding to the Z component of the magnetic field, as a
        floating point number

        On failure, throws an exception or returns YMagnetometer.ZVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMagnetometer.ZVALUE_INVALID
        return self._zValue

    @staticmethod
    def FindMagnetometer(func):
        """
        Retrieves a magnetometer for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the magnetometer is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YMagnetometer.isOnline() to test if the magnetometer is
        indeed online at a given time. In case of ambiguity when looking for
        a magnetometer by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the magnetometer

        @return a YMagnetometer object allowing you to drive the magnetometer.
        """
        # obj
        obj = YFunction._FindFromCache("Magnetometer", func)
        if obj is None:
            obj = YMagnetometer(func)
            YFunction._AddToCache("Magnetometer", func, obj)
        return obj

    def nextMagnetometer(self):
        """
        Continues the enumeration of magnetometers started using yFirstMagnetometer().

        @return a pointer to a YMagnetometer object, corresponding to
                a magnetometer currently online, or a None pointer
                if there are no more magnetometers to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YMagnetometer.FindMagnetometer(hwidRef.value)

#--- (end of YMagnetometer implementation)

#--- (Magnetometer functions)

    @staticmethod
    def FirstMagnetometer():
        """
        Starts the enumeration of magnetometers currently accessible.
        Use the method YMagnetometer.nextMagnetometer() to iterate on
        next magnetometers.

        @return a pointer to a YMagnetometer object, corresponding to
                the first magnetometer currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Magnetometer", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YMagnetometer.FindMagnetometer(serialRef.value + "." + funcIdRef.value)

#--- (end of Magnetometer functions)
