# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindThreshold(), the high-level API for Threshold functions
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


#--- (YThreshold class start)
#noinspection PyProtectedMember
class YThreshold(YFunction):
    """
    The Threshold class allows you define a threshold on a Yoctopuce sensor
    to trigger a predefined action, on specific devices where this is implemented.

    """
    #--- (end of YThreshold class start)
    #--- (YThreshold return codes)
    #--- (end of YThreshold return codes)
    #--- (YThreshold dlldef)
    #--- (end of YThreshold dlldef)
    #--- (YThreshold yapiwrapper)
    #--- (end of YThreshold yapiwrapper)
    #--- (YThreshold definitions)
    TARGETSENSOR_INVALID = YAPI.INVALID_STRING
    ALERTLEVEL_INVALID = YAPI.INVALID_DOUBLE
    SAFELEVEL_INVALID = YAPI.INVALID_DOUBLE
    THRESHOLDSTATE_SAFE = 0
    THRESHOLDSTATE_ALERT = 1
    THRESHOLDSTATE_INVALID = -1
    #--- (end of YThreshold definitions)

    def __init__(self, func):
        super(YThreshold, self).__init__(func)
        self._className = 'Threshold'
        #--- (YThreshold attributes)
        self._callback = None
        self._thresholdState = YThreshold.THRESHOLDSTATE_INVALID
        self._targetSensor = YThreshold.TARGETSENSOR_INVALID
        self._alertLevel = YThreshold.ALERTLEVEL_INVALID
        self._safeLevel = YThreshold.SAFELEVEL_INVALID
        #--- (end of YThreshold attributes)

    #--- (YThreshold implementation)
    def _parseAttr(self, json_val):
        if json_val.has("thresholdState"):
            self._thresholdState = json_val.getInt("thresholdState")
        if json_val.has("targetSensor"):
            self._targetSensor = json_val.getString("targetSensor")
        if json_val.has("alertLevel"):
            self._alertLevel = round(json_val.getDouble("alertLevel") / 65.536) / 1000.0
        if json_val.has("safeLevel"):
            self._safeLevel = round(json_val.getDouble("safeLevel") / 65.536) / 1000.0
        super(YThreshold, self)._parseAttr(json_val)

    def get_thresholdState(self):
        """
        Returns current state of the threshold function.

        @return either YThreshold.THRESHOLDSTATE_SAFE or YThreshold.THRESHOLDSTATE_ALERT, according to
        current state of the threshold function

        On failure, throws an exception or returns YThreshold.THRESHOLDSTATE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.THRESHOLDSTATE_INVALID
        res = self._thresholdState
        return res

    def get_targetSensor(self):
        """
        Returns the name of the sensor monitored by the threshold function.

        @return a string corresponding to the name of the sensor monitored by the threshold function

        On failure, throws an exception or returns YThreshold.TARGETSENSOR_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.TARGETSENSOR_INVALID
        res = self._targetSensor
        return res

    def set_alertLevel(self, newval):
        """
        Changes the sensor alert level triggering the threshold function.
        Remember to call the matching module saveToFlash()
        method if you want to preserve the setting after reboot.

        @param newval : a floating point number corresponding to the sensor alert level triggering the
        threshold function

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("alertLevel", rest_val)

    def get_alertLevel(self):
        """
        Returns the sensor alert level, triggering the threshold function.

        @return a floating point number corresponding to the sensor alert level, triggering the threshold function

        On failure, throws an exception or returns YThreshold.ALERTLEVEL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.ALERTLEVEL_INVALID
        res = self._alertLevel
        return res

    def set_safeLevel(self, newval):
        """
        Changes the sensor acceptable level for disabling the threshold function.
        Remember to call the matching module saveToFlash()
        method if you want to preserve the setting after reboot.

        @param newval : a floating point number corresponding to the sensor acceptable level for disabling
        the threshold function

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("safeLevel", rest_val)

    def get_safeLevel(self):
        """
        Returns the sensor acceptable level for disabling the threshold function.

        @return a floating point number corresponding to the sensor acceptable level for disabling the
        threshold function

        On failure, throws an exception or returns YThreshold.SAFELEVEL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.SAFELEVEL_INVALID
        res = self._safeLevel
        return res

    @staticmethod
    def FindThreshold(func):
        """
        Retrieves a threshold function for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the threshold function is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YThreshold.isOnline() to test if the threshold function is
        indeed online at a given time. In case of ambiguity when looking for
        a threshold function by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the threshold function, for instance
                MyDevice.threshold1.

        @return a YThreshold object allowing you to drive the threshold function.
        """
        # obj
        obj = YFunction._FindFromCache("Threshold", func)
        if obj is None:
            obj = YThreshold(func)
            YFunction._AddToCache("Threshold", func, obj)
        return obj

    def nextThreshold(self):
        """
        Continues the enumeration of threshold functions started using yFirstThreshold().
        Caution: You can't make any assumption about the returned threshold functions order.
        If you want to find a specific a threshold function, use Threshold.findThreshold()
        and a hardwareID or a logical name.

        @return a pointer to a YThreshold object, corresponding to
                a threshold function currently online, or a None pointer
                if there are no more threshold functions to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YThreshold.FindThreshold(hwidRef.value)

#--- (end of YThreshold implementation)

#--- (YThreshold functions)

    @staticmethod
    def FirstThreshold():
        """
        Starts the enumeration of threshold functions currently accessible.
        Use the method YThreshold.nextThreshold() to iterate on
        next threshold functions.

        @return a pointer to a YThreshold object, corresponding to
                the first threshold function currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Threshold", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YThreshold.FindThreshold(serialRef.value + "." + funcIdRef.value)

#--- (end of YThreshold functions)
