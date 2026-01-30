# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindSoundSpectrum(), the high-level API for SoundSpectrum functions
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


#--- (YSoundSpectrum class start)
#noinspection PyProtectedMember
class YSoundSpectrum(YFunction):
    """
    The YSoundSpectrum class allows you to read and configure Yoctopuce sound spectrum analyzers.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YSoundSpectrum class start)
    #--- (YSoundSpectrum return codes)
    #--- (end of YSoundSpectrum return codes)
    #--- (YSoundSpectrum dlldef)
    #--- (end of YSoundSpectrum dlldef)
    #--- (YSoundSpectrum yapiwrapper)
    #--- (end of YSoundSpectrum yapiwrapper)
    #--- (YSoundSpectrum definitions)
    INTEGRATIONTIME_INVALID = YAPI.INVALID_UINT
    SPECTRUMDATA_INVALID = YAPI.INVALID_STRING
    #--- (end of YSoundSpectrum definitions)

    def __init__(self, func):
        super(YSoundSpectrum, self).__init__(func)
        self._className = 'SoundSpectrum'
        #--- (YSoundSpectrum attributes)
        self._callback = None
        self._integrationTime = YSoundSpectrum.INTEGRATIONTIME_INVALID
        self._spectrumData = YSoundSpectrum.SPECTRUMDATA_INVALID
        #--- (end of YSoundSpectrum attributes)

    #--- (YSoundSpectrum implementation)
    def _parseAttr(self, json_val):
        if json_val.has("integrationTime"):
            self._integrationTime = json_val.getInt("integrationTime")
        if json_val.has("spectrumData"):
            self._spectrumData = json_val.getString("spectrumData")
        super(YSoundSpectrum, self)._parseAttr(json_val)

    def get_integrationTime(self):
        """
        Returns the integration time in milliseconds for calculating time
        weighted spectrum data.

        @return an integer corresponding to the integration time in milliseconds for calculating time
                weighted spectrum data

        On failure, throws an exception or returns YSoundSpectrum.INTEGRATIONTIME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSoundSpectrum.INTEGRATIONTIME_INVALID
        res = self._integrationTime
        return res

    def set_integrationTime(self, newval):
        """
        Changes the integration time in milliseconds for computing time weighted
        spectrum data. Be aware that on some devices, changing the integration
        time for time-weighted spectrum data may also affect the integration
        period for one or more sound pressure level measurements.
        Remember to call the saveToFlash() method of the
        module if the modification must be kept.

        @param newval : an integer corresponding to the integration time in milliseconds for computing time weighted
                spectrum data

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("integrationTime", rest_val)

    def get_spectrumData(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSoundSpectrum.SPECTRUMDATA_INVALID
        res = self._spectrumData
        return res

    @staticmethod
    def FindSoundSpectrum(func):
        """
        Retrieves a sound spectrum analyzer for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the sound spectrum analyzer is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSoundSpectrum.isOnline() to test if the sound spectrum analyzer is
        indeed online at a given time. In case of ambiguity when looking for
        a sound spectrum analyzer by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the sound spectrum analyzer, for instance
                MyDevice.soundSpectrum.

        @return a YSoundSpectrum object allowing you to drive the sound spectrum analyzer.
        """
        # obj
        obj = YFunction._FindFromCache("SoundSpectrum", func)
        if obj is None:
            obj = YSoundSpectrum(func)
            YFunction._AddToCache("SoundSpectrum", func, obj)
        return obj

    def nextSoundSpectrum(self):
        """
        comment from .yc definition
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YSoundSpectrum.FindSoundSpectrum(hwidRef.value)

#--- (end of YSoundSpectrum implementation)

#--- (YSoundSpectrum functions)

    @staticmethod
    def FirstSoundSpectrum():
        """
        comment from .yc definition
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
        err = YAPI.apiGetFunctionsByClass("SoundSpectrum", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YSoundSpectrum.FindSoundSpectrum(serialRef.value + "." + funcIdRef.value)

#--- (end of YSoundSpectrum functions)
