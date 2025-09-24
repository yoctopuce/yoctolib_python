# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindSpectralChannel(), the high-level API for SpectralChannel functions
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


#--- (YSpectralChannel class start)
#noinspection PyProtectedMember
class YSpectralChannel(YSensor):
    """
    The YSpectralChannel class allows you to read and configure Yoctopuce spectral analysis channels.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YSpectralChannel class start)
    #--- (YSpectralChannel return codes)
    #--- (end of YSpectralChannel return codes)
    #--- (YSpectralChannel dlldef)
    #--- (end of YSpectralChannel dlldef)
    #--- (YSpectralChannel yapiwrapper)
    #--- (end of YSpectralChannel yapiwrapper)
    #--- (YSpectralChannel definitions)
    RAWCOUNT_INVALID = YAPI.INVALID_INT
    CHANNELNAME_INVALID = YAPI.INVALID_STRING
    PEAKWAVELENGTH_INVALID = YAPI.INVALID_INT
    #--- (end of YSpectralChannel definitions)

    def __init__(self, func):
        super(YSpectralChannel, self).__init__(func)
        self._className = 'SpectralChannel'
        #--- (YSpectralChannel attributes)
        self._callback = None
        self._rawCount = YSpectralChannel.RAWCOUNT_INVALID
        self._channelName = YSpectralChannel.CHANNELNAME_INVALID
        self._peakWavelength = YSpectralChannel.PEAKWAVELENGTH_INVALID
        #--- (end of YSpectralChannel attributes)

    #--- (YSpectralChannel implementation)
    def _parseAttr(self, json_val):
        if json_val.has("rawCount"):
            self._rawCount = json_val.getInt("rawCount")
        if json_val.has("channelName"):
            self._channelName = json_val.getString("channelName")
        if json_val.has("peakWavelength"):
            self._peakWavelength = json_val.getInt("peakWavelength")
        super(YSpectralChannel, self)._parseAttr(json_val)

    def get_rawCount(self):
        """
        Retrieves the raw spectral intensity value as measured by the sensor, without any scaling or calibration.

        @return an integer

        On failure, throws an exception or returns YSpectralChannel.RAWCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralChannel.RAWCOUNT_INVALID
        res = self._rawCount
        return res

    def get_channelName(self):
        """
        Returns the target spectral band name.

        @return a string corresponding to the target spectral band name

        On failure, throws an exception or returns YSpectralChannel.CHANNELNAME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralChannel.CHANNELNAME_INVALID
        res = self._channelName
        return res

    def get_peakWavelength(self):
        """
        Returns the target spectral band peak wavelength, in nm.

        @return an integer corresponding to the target spectral band peak wavelength, in nm

        On failure, throws an exception or returns YSpectralChannel.PEAKWAVELENGTH_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralChannel.PEAKWAVELENGTH_INVALID
        res = self._peakWavelength
        return res

    @staticmethod
    def FindSpectralChannel(func):
        """
        Retrieves a spectral analysis channel for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the spectral analysis channel is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSpectralChannel.isOnline() to test if the spectral analysis channel is
        indeed online at a given time. In case of ambiguity when looking for
        a spectral analysis channel by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the spectral analysis channel, for instance
                MyDevice.spectralChannel1.

        @return a YSpectralChannel object allowing you to drive the spectral analysis channel.
        """
        # obj
        obj = YFunction._FindFromCache("SpectralChannel", func)
        if obj is None:
            obj = YSpectralChannel(func)
            YFunction._AddToCache("SpectralChannel", func, obj)
        return obj

    def nextSpectralChannel(self):
        """
        Continues the enumeration of spectral analysis channels started using yFirstSpectralChannel().
        Caution: You can't make any assumption about the returned spectral analysis channels order.
        If you want to find a specific a spectral analysis channel, use SpectralChannel.findSpectralChannel()
        and a hardwareID or a logical name.

        @return a pointer to a YSpectralChannel object, corresponding to
                a spectral analysis channel currently online, or a None pointer
                if there are no more spectral analysis channels to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YSpectralChannel.FindSpectralChannel(hwidRef.value)

#--- (end of YSpectralChannel implementation)

#--- (YSpectralChannel functions)

    @staticmethod
    def FirstSpectralChannel():
        """
        Starts the enumeration of spectral analysis channels currently accessible.
        Use the method YSpectralChannel.nextSpectralChannel() to iterate on
        next spectral analysis channels.

        @return a pointer to a YSpectralChannel object, corresponding to
                the first spectral analysis channel currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("SpectralChannel", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YSpectralChannel.FindSpectralChannel(serialRef.value + "." + funcIdRef.value)

#--- (end of YSpectralChannel functions)
