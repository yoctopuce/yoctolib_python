# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindAirQuality(), the high-level API for AirQuality functions
#
#  - - - - - - - - - License information: - - - - - - - - -
#
#  Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#
#  Yoctopuce Sarl (hereafter Licensor) grants to you a perpetual
#  non-exclusive license to use, modify, copy and integrate this
#  file into your software for the sole purpose of interfacing
#  with Yoctopuce products.
#
#  You may reproduce and distribute copies of this file in
#  source or object form, as long as the sole purpose of this
#  code is to interface with Yoctopuce products. You must retain
#  this notice in the distributed source file.
#
#  You should refer to Yoctopuce General Terms and Conditions
#  for additional information regarding your rights and
#  obligations.
#
#  THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#  WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING
#  WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#  EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#  INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA,
#  COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR
#  SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT
#  LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#  CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#  BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#  WARRANTY, OR OTHERWISE.
#
# *********************************************************************


__docformat__ = 'restructuredtext en'
from yocto_api import *


#--- (YAirQuality class start)
#noinspection PyProtectedMember
class YAirQuality(YSensor):
    """
    The YAirQuality class allows you to read and configure Yoctopuce air quality sensors.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YAirQuality class start)
    #--- (YAirQuality return codes)
    #--- (end of YAirQuality return codes)
    #--- (YAirQuality dlldef)
    #--- (end of YAirQuality dlldef)
    #--- (YAirQuality yapiwrapper)
    #--- (end of YAirQuality yapiwrapper)
    #--- (YAirQuality definitions)
    UBAINDEX_INVALID = YAPI.INVALID_DOUBLE
    RELATIVEINDEX_INVALID = YAPI.INVALID_DOUBLE
    AQIMODE_RELATIVE = 0
    AQIMODE_UBA = 1
    AQIMODE_INVALID = -1
    #--- (end of YAirQuality definitions)

    def __init__(self, func):
        super(YAirQuality, self).__init__(func)
        self._className = 'AirQuality'
        #--- (YAirQuality attributes)
        self._callback = None
        self._ubaIndex = YAirQuality.UBAINDEX_INVALID
        self._relativeIndex = YAirQuality.RELATIVEINDEX_INVALID
        self._aqiMode = YAirQuality.AQIMODE_INVALID
        #--- (end of YAirQuality attributes)

    #--- (YAirQuality implementation)
    def _parseAttr(self, json_val):
        if json_val.has("ubaIndex"):
            self._ubaIndex = round(json_val.getDouble("ubaIndex") / 65.536) / 1000.0
        if json_val.has("relativeIndex"):
            self._relativeIndex = round(json_val.getDouble("relativeIndex") / 65.536) / 1000.0
        if json_val.has("aqiMode"):
            self._aqiMode = json_val.getInt("aqiMode")
        super(YAirQuality, self)._parseAttr(json_val)

    def get_ubaIndex(self):
        """
        Returns the current air quality index, according to UBA (from 1 to 5).

        @return a floating point number corresponding to the current air quality index, according to UBA (from 1 to 5)

        On failure, throws an exception or returns YAirQuality.UBAINDEX_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YAirQuality.UBAINDEX_INVALID
        res = self._ubaIndex
        return res

    def get_relativeIndex(self):
        """
        Returns the relative air quality index, according to ScioSense (from 0 to 500).
        A value below 100 indicates better-than-average air quality compared to the past 24 hours,
        while a value above 100 indicates poorer-than-average air quality compared to the past 24 hours.

        @return a floating point number corresponding to the relative air quality index, according to
        ScioSense (from 0 to 500)

        On failure, throws an exception or returns YAirQuality.RELATIVEINDEX_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YAirQuality.RELATIVEINDEX_INVALID
        res = self._relativeIndex
        return res

    def get_aqiMode(self):
        """
        Returns the type of index reported by the get_currentValue function and callbacks (UBA index or relative index).

        @return either YAirQuality.AQIMODE_RELATIVE or YAirQuality.AQIMODE_UBA, according to the type of
        index reported by the get_currentValue function and callbacks (UBA index or relative index)

        On failure, throws an exception or returns YAirQuality.AQIMODE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YAirQuality.AQIMODE_INVALID
        res = self._aqiMode
        return res

    def set_aqiMode(self, newval):
        """
        Changes the the type of index reported by the get_currentValue function and callbacks (UBA index or
        relative index).
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : either YAirQuality.AQIMODE_RELATIVE or YAirQuality.AQIMODE_UBA, according to the
        the type of index reported by the get_currentValue function and callbacks (UBA index or relative index)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("aqiMode", rest_val)

    @staticmethod
    def FindAirQuality(func):
        """
        Retrieves a air quality sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the air quality sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YAirQuality.isOnline() to test if the air quality sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a air quality sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the air quality sensor, for instance
                MyDevice.airQuality.

        @return a YAirQuality object allowing you to drive the air quality sensor.
        """
        # obj
        obj = YFunction._FindFromCache("AirQuality", func)
        if obj is None:
            obj = YAirQuality(func)
            YFunction._AddToCache("AirQuality", func, obj)
        return obj

    def nextAirQuality(self):
        """
        Continues the enumeration of air quality sensors started using yFirstAirQuality().
        Caution: You can't make any assumption about the returned air quality sensors order.
        If you want to find a specific a air quality sensor, use AirQuality.findAirQuality()
        and a hardwareID or a logical name.

        @return a pointer to a YAirQuality object, corresponding to
                a air quality sensor currently online, or a None pointer
                if there are no more air quality sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YAirQuality.FindAirQuality(hwidRef.value)

#--- (end of YAirQuality implementation)

#--- (YAirQuality functions)

    @staticmethod
    def FirstAirQuality():
        """
        Starts the enumeration of air quality sensors currently accessible.
        Use the method YAirQuality.nextAirQuality() to iterate on
        next air quality sensors.

        @return a pointer to a YAirQuality object, corresponding to
                the first air quality sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("AirQuality", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YAirQuality.FindAirQuality(serialRef.value + "." + funcIdRef.value)

#--- (end of YAirQuality functions)
