# -*- coding: utf-8 -*-
#*********************************************************************
#*
#* $Id: yocto_proximity.py 28742 2017-10-03 08:12:07Z seb $
#*
#* Implements yFindProximity(), the high-level API for Proximity functions
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


#--- (YProximity class start)
#noinspection PyProtectedMember
class YProximity(YSensor):
    """
    The Yoctopuce class YProximity allows you to use and configure Yoctopuce proximity
    sensors. It inherits from the YSensor class the core functions to read measurements,
    to register callback functions, to access the autonomous datalogger.
    This class adds the ability to easily perform a one-point linear calibration
    to compensate the effect of a glass or filter placed in front of the sensor.

    """
#--- (end of YProximity class start)
    #--- (YProximity return codes)
    #--- (end of YProximity return codes)
    #--- (YProximity dlldef)
    #--- (end of YProximity dlldef)
    #--- (YProximity definitions)
    SIGNALVALUE_INVALID = YAPI.INVALID_DOUBLE
    DETECTIONTHRESHOLD_INVALID = YAPI.INVALID_UINT
    LASTTIMEAPPROACHED_INVALID = YAPI.INVALID_LONG
    LASTTIMEREMOVED_INVALID = YAPI.INVALID_LONG
    PULSECOUNTER_INVALID = YAPI.INVALID_LONG
    PULSETIMER_INVALID = YAPI.INVALID_LONG
    ISPRESENT_FALSE = 0
    ISPRESENT_TRUE = 1
    ISPRESENT_INVALID = -1
    PROXIMITYREPORTMODE_NUMERIC = 0
    PROXIMITYREPORTMODE_PRESENCE = 1
    PROXIMITYREPORTMODE_PULSECOUNT = 2
    PROXIMITYREPORTMODE_INVALID = -1
    #--- (end of YProximity definitions)

    def __init__(self, func):
        super(YProximity, self).__init__(func)
        self._className = 'Proximity'
        #--- (YProximity attributes)
        self._callback = None
        self._signalValue = YProximity.SIGNALVALUE_INVALID
        self._detectionThreshold = YProximity.DETECTIONTHRESHOLD_INVALID
        self._isPresent = YProximity.ISPRESENT_INVALID
        self._lastTimeApproached = YProximity.LASTTIMEAPPROACHED_INVALID
        self._lastTimeRemoved = YProximity.LASTTIMEREMOVED_INVALID
        self._pulseCounter = YProximity.PULSECOUNTER_INVALID
        self._pulseTimer = YProximity.PULSETIMER_INVALID
        self._proximityReportMode = YProximity.PROXIMITYREPORTMODE_INVALID
        #--- (end of YProximity attributes)

    #--- (YProximity implementation)
    def _parseAttr(self, json_val):
        if json_val.has("signalValue"):
            self._signalValue = round(json_val.getDouble("signalValue") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("detectionThreshold"):
            self._detectionThreshold = json_val.getInt("detectionThreshold")
        if json_val.has("isPresent"):
            self._isPresent = (json_val.getInt("isPresent") > 0 if 1 else 0)
        if json_val.has("lastTimeApproached"):
            self._lastTimeApproached = json_val.getLong("lastTimeApproached")
        if json_val.has("lastTimeRemoved"):
            self._lastTimeRemoved = json_val.getLong("lastTimeRemoved")
        if json_val.has("pulseCounter"):
            self._pulseCounter = json_val.getLong("pulseCounter")
        if json_val.has("pulseTimer"):
            self._pulseTimer = json_val.getLong("pulseTimer")
        if json_val.has("proximityReportMode"):
            self._proximityReportMode = json_val.getInt("proximityReportMode")
        super(YProximity, self)._parseAttr(json_val)

    def get_signalValue(self):
        """
        Returns the current value of signal measured by the proximity sensor.

        @return a floating point number corresponding to the current value of signal measured by the proximity sensor

        On failure, throws an exception or returns YProximity.SIGNALVALUE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.SIGNALVALUE_INVALID
        res = round(self._signalValue * 1000) / 1000
        return res

    def get_detectionThreshold(self):
        """
        Returns the threshold used to determine the logical state of the proximity sensor, when considered
        as a binary input (on/off).

        @return an integer corresponding to the threshold used to determine the logical state of the
        proximity sensor, when considered
                as a binary input (on/off)

        On failure, throws an exception or returns YProximity.DETECTIONTHRESHOLD_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.DETECTIONTHRESHOLD_INVALID
        res = self._detectionThreshold
        return res

    def set_detectionThreshold(self, newval):
        """
        Changes the threshold used to determine the logical state of the proximity sensor, when considered
        as a binary input (on/off).

        @param newval : an integer corresponding to the threshold used to determine the logical state of
        the proximity sensor, when considered
                as a binary input (on/off)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("detectionThreshold", rest_val)

    def get_isPresent(self):
        """
        Returns true if the input (considered as binary) is active (detection value is smaller than the
        specified threshold), and false otherwise.

        @return either YProximity.ISPRESENT_FALSE or YProximity.ISPRESENT_TRUE, according to true if the
        input (considered as binary) is active (detection value is smaller than the specified threshold),
        and false otherwise

        On failure, throws an exception or returns YProximity.ISPRESENT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.ISPRESENT_INVALID
        res = self._isPresent
        return res

    def get_lastTimeApproached(self):
        """
        Returns the number of elapsed milliseconds between the module power on and the last observed
        detection (the input contact transitioned from absent to present).

        @return an integer corresponding to the number of elapsed milliseconds between the module power on
        and the last observed
                detection (the input contact transitioned from absent to present)

        On failure, throws an exception or returns YProximity.LASTTIMEAPPROACHED_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.LASTTIMEAPPROACHED_INVALID
        res = self._lastTimeApproached
        return res

    def get_lastTimeRemoved(self):
        """
        Returns the number of elapsed milliseconds between the module power on and the last observed
        detection (the input contact transitioned from present to absent).

        @return an integer corresponding to the number of elapsed milliseconds between the module power on
        and the last observed
                detection (the input contact transitioned from present to absent)

        On failure, throws an exception or returns YProximity.LASTTIMEREMOVED_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.LASTTIMEREMOVED_INVALID
        res = self._lastTimeRemoved
        return res

    def get_pulseCounter(self):
        """
        Returns the pulse counter value. The value is a 32 bit integer. In case
        of overflow (>=2^32), the counter will wrap. To reset the counter, just
        call the resetCounter() method.

        @return an integer corresponding to the pulse counter value

        On failure, throws an exception or returns YProximity.PULSECOUNTER_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.PULSECOUNTER_INVALID
        res = self._pulseCounter
        return res

    def set_pulseCounter(self, newval):
        rest_val = str(newval)
        return self._setAttr("pulseCounter", rest_val)

    def get_pulseTimer(self):
        """
        Returns the timer of the pulse counter (ms).

        @return an integer corresponding to the timer of the pulse counter (ms)

        On failure, throws an exception or returns YProximity.PULSETIMER_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.PULSETIMER_INVALID
        res = self._pulseTimer
        return res

    def get_proximityReportMode(self):
        """
        Returns the parameter (sensor value, presence or pulse count) returned by the get_currentValue
        function and callbacks.

        @return a value among YProximity.PROXIMITYREPORTMODE_NUMERIC,
        YProximity.PROXIMITYREPORTMODE_PRESENCE and YProximity.PROXIMITYREPORTMODE_PULSECOUNT corresponding
        to the parameter (sensor value, presence or pulse count) returned by the get_currentValue function and callbacks

        On failure, throws an exception or returns YProximity.PROXIMITYREPORTMODE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YProximity.PROXIMITYREPORTMODE_INVALID
        res = self._proximityReportMode
        return res

    def set_proximityReportMode(self, newval):
        """
        Changes the  parameter  type (sensor value, presence or pulse count) returned by the
        get_currentValue function and callbacks.
        The edge count value is limited to the 6 lowest digits. For values greater than one million, use
        get_pulseCounter().

        @param newval : a value among YProximity.PROXIMITYREPORTMODE_NUMERIC,
        YProximity.PROXIMITYREPORTMODE_PRESENCE and YProximity.PROXIMITYREPORTMODE_PULSECOUNT corresponding
        to the  parameter  type (sensor value, presence or pulse count) returned by the get_currentValue
        function and callbacks

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("proximityReportMode", rest_val)

    @staticmethod
    def FindProximity(func):
        """
        Retrieves a proximity sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the proximity sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YProximity.isOnline() to test if the proximity sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a proximity sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the proximity sensor

        @return a YProximity object allowing you to drive the proximity sensor.
        """
        # obj
        obj = YFunction._FindFromCache("Proximity", func)
        if obj is None:
            obj = YProximity(func)
            YFunction._AddToCache("Proximity", func, obj)
        return obj

    def resetCounter(self):
        """
        Resets the pulse counter value as well as its timer.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_pulseCounter(0)

    def nextProximity(self):
        """
        Continues the enumeration of proximity sensors started using yFirstProximity().

        @return a pointer to a YProximity object, corresponding to
                a proximity sensor currently online, or a None pointer
                if there are no more proximity sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YProximity.FindProximity(hwidRef.value)

#--- (end of YProximity implementation)

#--- (YProximity functions)

    @staticmethod
    def FirstProximity():
        """
        Starts the enumeration of proximity sensors currently accessible.
        Use the method YProximity.nextProximity() to iterate on
        next proximity sensors.

        @return a pointer to a YProximity object, corresponding to
                the first proximity sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Proximity", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YProximity.FindProximity(serialRef.value + "." + funcIdRef.value)

#--- (end of YProximity functions)
