# -*- coding: utf-8 -*-
#*********************************************************************
#*
#* $Id: yocto_compass.py 28742 2017-10-03 08:12:07Z seb $
#*
#* Implements yFindCompass(), the high-level API for Compass functions
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


#--- (YCompass class start)
#noinspection PyProtectedMember
class YCompass(YSensor):
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
#--- (end of YCompass class start)
    #--- (YCompass return codes)
    #--- (end of YCompass return codes)
    #--- (YCompass dlldef)
    #--- (end of YCompass dlldef)
    #--- (YCompass definitions)
    BANDWIDTH_INVALID = YAPI.INVALID_INT
    MAGNETICHEADING_INVALID = YAPI.INVALID_DOUBLE
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2
    AXIS_INVALID = -1
    #--- (end of YCompass definitions)

    def __init__(self, func):
        super(YCompass, self).__init__(func)
        self._className = 'Compass'
        #--- (YCompass attributes)
        self._callback = None
        self._bandwidth = YCompass.BANDWIDTH_INVALID
        self._axis = YCompass.AXIS_INVALID
        self._magneticHeading = YCompass.MAGNETICHEADING_INVALID
        #--- (end of YCompass attributes)

    #--- (YCompass implementation)
    def _parseAttr(self, json_val):
        if json_val.has("bandwidth"):
            self._bandwidth = json_val.getInt("bandwidth")
        if json_val.has("axis"):
            self._axis = json_val.getInt("axis")
        if json_val.has("magneticHeading"):
            self._magneticHeading = round(json_val.getDouble("magneticHeading") * 1000.0 / 65536.0) / 1000.0
        super(YCompass, self)._parseAttr(json_val)

    def get_bandwidth(self):
        """
        Returns the measure update frequency, measured in Hz (Yocto-3D-V2 only).

        @return an integer corresponding to the measure update frequency, measured in Hz (Yocto-3D-V2 only)

        On failure, throws an exception or returns YCompass.BANDWIDTH_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCompass.BANDWIDTH_INVALID
        res = self._bandwidth
        return res

    def set_bandwidth(self, newval):
        """
        Changes the measure update frequency, measured in Hz (Yocto-3D-V2 only). When the
        frequency is lower, the device performs averaging.

        @param newval : an integer corresponding to the measure update frequency, measured in Hz (Yocto-3D-V2 only)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("bandwidth", rest_val)

    def get_axis(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCompass.AXIS_INVALID
        res = self._axis
        return res

    def get_magneticHeading(self):
        """
        Returns the magnetic heading, regardless of the configured bearing.

        @return a floating point number corresponding to the magnetic heading, regardless of the configured bearing

        On failure, throws an exception or returns YCompass.MAGNETICHEADING_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCompass.MAGNETICHEADING_INVALID
        res = self._magneticHeading
        return res

    @staticmethod
    def FindCompass(func):
        """
        Retrieves a compass for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the compass is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCompass.isOnline() to test if the compass is
        indeed online at a given time. In case of ambiguity when looking for
        a compass by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the compass

        @return a YCompass object allowing you to drive the compass.
        """
        # obj
        obj = YFunction._FindFromCache("Compass", func)
        if obj is None:
            obj = YCompass(func)
            YFunction._AddToCache("Compass", func, obj)
        return obj

    def nextCompass(self):
        """
        Continues the enumeration of compasses started using yFirstCompass().

        @return a pointer to a YCompass object, corresponding to
                a compass currently online, or a None pointer
                if there are no more compasses to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YCompass.FindCompass(hwidRef.value)

#--- (end of YCompass implementation)

#--- (YCompass functions)

    @staticmethod
    def FirstCompass():
        """
        Starts the enumeration of compasses currently accessible.
        Use the method YCompass.nextCompass() to iterate on
        next compasses.

        @return a pointer to a YCompass object, corresponding to
                the first compass currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Compass", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YCompass.FindCompass(serialRef.value + "." + funcIdRef.value)

#--- (end of YCompass functions)
