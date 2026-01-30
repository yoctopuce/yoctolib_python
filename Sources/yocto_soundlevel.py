# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindSoundLevel(), the high-level API for SoundLevel functions
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


#--- (YSoundLevel class start)
#noinspection PyProtectedMember
class YSoundLevel(YSensor):
    """
    The YSoundLevel class allows you to read and configure Yoctopuce sound pressure level meters.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YSoundLevel class start)
    #--- (YSoundLevel return codes)
    #--- (end of YSoundLevel return codes)
    #--- (YSoundLevel dlldef)
    #--- (end of YSoundLevel dlldef)
    #--- (YSoundLevel yapiwrapper)
    #--- (end of YSoundLevel yapiwrapper)
    #--- (YSoundLevel definitions)
    LABEL_INVALID = YAPI.INVALID_STRING
    INTEGRATIONTIME_INVALID = YAPI.INVALID_UINT
    #--- (end of YSoundLevel definitions)

    def __init__(self, func):
        super(YSoundLevel, self).__init__(func)
        self._className = 'SoundLevel'
        #--- (YSoundLevel attributes)
        self._callback = None
        self._label = YSoundLevel.LABEL_INVALID
        self._integrationTime = YSoundLevel.INTEGRATIONTIME_INVALID
        #--- (end of YSoundLevel attributes)

    #--- (YSoundLevel implementation)
    def _parseAttr(self, json_val):
        if json_val.has("label"):
            self._label = json_val.getString("label")
        if json_val.has("integrationTime"):
            self._integrationTime = json_val.getInt("integrationTime")
        super(YSoundLevel, self)._parseAttr(json_val)

    def set_unit(self, newval):
        """
        Changes the measuring unit for the sound pressure level (dBA, dBC or dBZ).
        That unit will directly determine frequency weighting to be used to compute
        the measured value. Remember to call the saveToFlash() method of the
        module if the modification must be kept.

        @param newval : a string corresponding to the measuring unit for the sound pressure level (dBA, dBC or dBZ)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("unit", rest_val)

    def get_label(self):
        """
        Returns the label for the sound pressure level measurement, as per
        IEC standard 61672-1:2013.

        @return a string corresponding to the label for the sound pressure level measurement, as per
                IEC standard 61672-1:2013

        On failure, throws an exception or returns YSoundLevel.LABEL_INVALID.
        """
        # res
        if self._cacheExpiration == datetime.datetime.fromtimestamp(86400):
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSoundLevel.LABEL_INVALID
        res = self._label
        return res

    def get_integrationTime(self):
        """
        Returns the integration time in milliseconds for measuring the sound pressure level.

        @return an integer corresponding to the integration time in milliseconds for measuring the sound pressure level

        On failure, throws an exception or returns YSoundLevel.INTEGRATIONTIME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSoundLevel.INTEGRATIONTIME_INVALID
        res = self._integrationTime
        return res

    @staticmethod
    def FindSoundLevel(func):
        """
        Retrieves a sound pressure level meter for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the sound pressure level meter is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSoundLevel.isOnline() to test if the sound pressure level meter is
        indeed online at a given time. In case of ambiguity when looking for
        a sound pressure level meter by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the sound pressure level meter, for instance
                MyDevice.soundLevel1.

        @return a YSoundLevel object allowing you to drive the sound pressure level meter.
        """
        # obj
        obj = YFunction._FindFromCache("SoundLevel", func)
        if obj is None:
            obj = YSoundLevel(func)
            YFunction._AddToCache("SoundLevel", func, obj)
        return obj

    def nextSoundLevel(self):
        """
        Continues the enumeration of sound pressure level meters started using yFirstSoundLevel().
        Caution: You can't make any assumption about the returned sound pressure level meters order.
        If you want to find a specific a sound pressure level meter, use SoundLevel.findSoundLevel()
        and a hardwareID or a logical name.

        @return a pointer to a YSoundLevel object, corresponding to
                a sound pressure level meter currently online, or a None pointer
                if there are no more sound pressure level meters to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YSoundLevel.FindSoundLevel(hwidRef.value)

#--- (end of YSoundLevel implementation)

#--- (YSoundLevel functions)

    @staticmethod
    def FirstSoundLevel():
        """
        Starts the enumeration of sound pressure level meters currently accessible.
        Use the method YSoundLevel.nextSoundLevel() to iterate on
        next sound pressure level meters.

        @return a pointer to a YSoundLevel object, corresponding to
                the first sound pressure level meter currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("SoundLevel", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YSoundLevel.FindSoundLevel(serialRef.value + "." + funcIdRef.value)

#--- (end of YSoundLevel functions)
