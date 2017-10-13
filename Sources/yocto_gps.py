# -*- coding: utf-8 -*-
#*********************************************************************
#*
#* $Id: yocto_gps.py 28742 2017-10-03 08:12:07Z seb $
#*
#* Implements yFindGps(), the high-level API for Gps functions
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


#--- (YGps class start)
#noinspection PyProtectedMember
class YGps(YFunction):
    """
    The Gps function allows you to extract positionning
    data from the GPS device. This class can provides
    complete positionning information: However, if you
    whish to define callbacks on position changes, you
    should use the YLatitude et YLongitude classes.

    """
#--- (end of YGps class start)
    #--- (YGps return codes)
    #--- (end of YGps return codes)
    #--- (YGps dlldef)
    #--- (end of YGps dlldef)
    #--- (YGps definitions)
    SATCOUNT_INVALID = YAPI.INVALID_LONG
    LATITUDE_INVALID = YAPI.INVALID_STRING
    LONGITUDE_INVALID = YAPI.INVALID_STRING
    DILUTION_INVALID = YAPI.INVALID_DOUBLE
    ALTITUDE_INVALID = YAPI.INVALID_DOUBLE
    GROUNDSPEED_INVALID = YAPI.INVALID_DOUBLE
    DIRECTION_INVALID = YAPI.INVALID_DOUBLE
    UNIXTIME_INVALID = YAPI.INVALID_LONG
    DATETIME_INVALID = YAPI.INVALID_STRING
    UTCOFFSET_INVALID = YAPI.INVALID_INT
    COMMAND_INVALID = YAPI.INVALID_STRING
    ISFIXED_FALSE = 0
    ISFIXED_TRUE = 1
    ISFIXED_INVALID = -1
    COORDSYSTEM_GPS_DMS = 0
    COORDSYSTEM_GPS_DM = 1
    COORDSYSTEM_GPS_D = 2
    COORDSYSTEM_INVALID = -1
    #--- (end of YGps definitions)

    def __init__(self, func):
        super(YGps, self).__init__(func)
        self._className = 'Gps'
        #--- (YGps attributes)
        self._callback = None
        self._isFixed = YGps.ISFIXED_INVALID
        self._satCount = YGps.SATCOUNT_INVALID
        self._coordSystem = YGps.COORDSYSTEM_INVALID
        self._latitude = YGps.LATITUDE_INVALID
        self._longitude = YGps.LONGITUDE_INVALID
        self._dilution = YGps.DILUTION_INVALID
        self._altitude = YGps.ALTITUDE_INVALID
        self._groundSpeed = YGps.GROUNDSPEED_INVALID
        self._direction = YGps.DIRECTION_INVALID
        self._unixTime = YGps.UNIXTIME_INVALID
        self._dateTime = YGps.DATETIME_INVALID
        self._utcOffset = YGps.UTCOFFSET_INVALID
        self._command = YGps.COMMAND_INVALID
        #--- (end of YGps attributes)

    #--- (YGps implementation)
    def _parseAttr(self, json_val):
        if json_val.has("isFixed"):
            self._isFixed = (json_val.getInt("isFixed") > 0 if 1 else 0)
        if json_val.has("satCount"):
            self._satCount = json_val.getLong("satCount")
        if json_val.has("coordSystem"):
            self._coordSystem = json_val.getInt("coordSystem")
        if json_val.has("latitude"):
            self._latitude = json_val.getString("latitude")
        if json_val.has("longitude"):
            self._longitude = json_val.getString("longitude")
        if json_val.has("dilution"):
            self._dilution = round(json_val.getDouble("dilution") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("altitude"):
            self._altitude = round(json_val.getDouble("altitude") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("groundSpeed"):
            self._groundSpeed = round(json_val.getDouble("groundSpeed") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("direction"):
            self._direction = round(json_val.getDouble("direction") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("unixTime"):
            self._unixTime = json_val.getLong("unixTime")
        if json_val.has("dateTime"):
            self._dateTime = json_val.getString("dateTime")
        if json_val.has("utcOffset"):
            self._utcOffset = json_val.getInt("utcOffset")
        if json_val.has("command"):
            self._command = json_val.getString("command")
        super(YGps, self)._parseAttr(json_val)

    def get_isFixed(self):
        """
        Returns TRUE if the receiver has found enough satellites to work.

        @return either YGps.ISFIXED_FALSE or YGps.ISFIXED_TRUE, according to TRUE if the receiver has found
        enough satellites to work

        On failure, throws an exception or returns YGps.ISFIXED_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.ISFIXED_INVALID
        res = self._isFixed
        return res

    def get_satCount(self):
        """
        Returns the count of visible satellites.

        @return an integer corresponding to the count of visible satellites

        On failure, throws an exception or returns YGps.SATCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.SATCOUNT_INVALID
        res = self._satCount
        return res

    def get_coordSystem(self):
        """
        Returns the representation system used for positioning data.

        @return a value among YGps.COORDSYSTEM_GPS_DMS, YGps.COORDSYSTEM_GPS_DM and YGps.COORDSYSTEM_GPS_D
        corresponding to the representation system used for positioning data

        On failure, throws an exception or returns YGps.COORDSYSTEM_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.COORDSYSTEM_INVALID
        res = self._coordSystem
        return res

    def set_coordSystem(self, newval):
        """
        Changes the representation system used for positioning data.

        @param newval : a value among YGps.COORDSYSTEM_GPS_DMS, YGps.COORDSYSTEM_GPS_DM and
        YGps.COORDSYSTEM_GPS_D corresponding to the representation system used for positioning data

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("coordSystem", rest_val)

    def get_latitude(self):
        """
        Returns the current latitude.

        @return a string corresponding to the current latitude

        On failure, throws an exception or returns YGps.LATITUDE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.LATITUDE_INVALID
        res = self._latitude
        return res

    def get_longitude(self):
        """
        Returns the current longitude.

        @return a string corresponding to the current longitude

        On failure, throws an exception or returns YGps.LONGITUDE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.LONGITUDE_INVALID
        res = self._longitude
        return res

    def get_dilution(self):
        """
        Returns the current horizontal dilution of precision,
        the smaller that number is, the better .

        @return a floating point number corresponding to the current horizontal dilution of precision,
                the smaller that number is, the better

        On failure, throws an exception or returns YGps.DILUTION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.DILUTION_INVALID
        res = self._dilution
        return res

    def get_altitude(self):
        """
        Returns the current altitude. Beware:  GPS technology
        is very inaccurate regarding altitude.

        @return a floating point number corresponding to the current altitude

        On failure, throws an exception or returns YGps.ALTITUDE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.ALTITUDE_INVALID
        res = self._altitude
        return res

    def get_groundSpeed(self):
        """
        Returns the current ground speed in Km/h.

        @return a floating point number corresponding to the current ground speed in Km/h

        On failure, throws an exception or returns YGps.GROUNDSPEED_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.GROUNDSPEED_INVALID
        res = self._groundSpeed
        return res

    def get_direction(self):
        """
        Returns the current move bearing in degrees, zero
        is the true (geographic) north.

        @return a floating point number corresponding to the current move bearing in degrees, zero
                is the true (geographic) north

        On failure, throws an exception or returns YGps.DIRECTION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.DIRECTION_INVALID
        res = self._direction
        return res

    def get_unixTime(self):
        """
        Returns the current time in Unix format (number of
        seconds elapsed since Jan 1st, 1970).

        @return an integer corresponding to the current time in Unix format (number of
                seconds elapsed since Jan 1st, 1970)

        On failure, throws an exception or returns YGps.UNIXTIME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.UNIXTIME_INVALID
        res = self._unixTime
        return res

    def get_dateTime(self):
        """
        Returns the current time in the form "YYYY/MM/DD hh:mm:ss".

        @return a string corresponding to the current time in the form "YYYY/MM/DD hh:mm:ss"

        On failure, throws an exception or returns YGps.DATETIME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.DATETIME_INVALID
        res = self._dateTime
        return res

    def get_utcOffset(self):
        """
        Returns the number of seconds between current time and UTC time (time zone).

        @return an integer corresponding to the number of seconds between current time and UTC time (time zone)

        On failure, throws an exception or returns YGps.UTCOFFSET_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.UTCOFFSET_INVALID
        res = self._utcOffset
        return res

    def set_utcOffset(self, newval):
        """
        Changes the number of seconds between current time and UTC time (time zone).
        The timezone is automatically rounded to the nearest multiple of 15 minutes.
        If current UTC time is known, the current time is automatically be updated according to the selected time zone.

        @param newval : an integer corresponding to the number of seconds between current time and UTC time (time zone)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("utcOffset", rest_val)

    def get_command(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGps.COMMAND_INVALID
        res = self._command
        return res

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindGps(func):
        """
        Retrieves a GPS for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the GPS is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YGps.isOnline() to test if the GPS is
        indeed online at a given time. In case of ambiguity when looking for
        a GPS by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the GPS

        @return a YGps object allowing you to drive the GPS.
        """
        # obj
        obj = YFunction._FindFromCache("Gps", func)
        if obj is None:
            obj = YGps(func)
            YFunction._AddToCache("Gps", func, obj)
        return obj

    def nextGps(self):
        """
        Continues the enumeration of GPS started using yFirstGps().

        @return a pointer to a YGps object, corresponding to
                a GPS currently online, or a None pointer
                if there are no more GPS to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YGps.FindGps(hwidRef.value)

#--- (end of YGps implementation)

#--- (YGps functions)

    @staticmethod
    def FirstGps():
        """
        Starts the enumeration of GPS currently accessible.
        Use the method YGps.nextGps() to iterate on
        next GPS.

        @return a pointer to a YGps object, corresponding to
                the first GPS currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Gps", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YGps.FindGps(serialRef.value + "." + funcIdRef.value)

#--- (end of YGps functions)
