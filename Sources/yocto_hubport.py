# -*- coding: utf-8 -*-
#*********************************************************************
#*
#* $Id: yocto_hubport.py 28742 2017-10-03 08:12:07Z seb $
#*
#* Implements yFindHubPort(), the high-level API for HubPort functions
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


#--- (YHubPort class start)
#noinspection PyProtectedMember
class YHubPort(YFunction):
    """
    YHubPort objects provide control over the power supply for every
    YoctoHub port and provide information about the device connected to it.
    The logical name of a YHubPort is always automatically set to the
    unique serial number of the Yoctopuce device connected to it.

    """
#--- (end of YHubPort class start)
    #--- (YHubPort return codes)
    #--- (end of YHubPort return codes)
    #--- (YHubPort dlldef)
    #--- (end of YHubPort dlldef)
    #--- (YHubPort definitions)
    BAUDRATE_INVALID = YAPI.INVALID_UINT
    ENABLED_FALSE = 0
    ENABLED_TRUE = 1
    ENABLED_INVALID = -1
    PORTSTATE_OFF = 0
    PORTSTATE_OVRLD = 1
    PORTSTATE_ON = 2
    PORTSTATE_RUN = 3
    PORTSTATE_PROG = 4
    PORTSTATE_INVALID = -1
    #--- (end of YHubPort definitions)

    def __init__(self, func):
        super(YHubPort, self).__init__(func)
        self._className = 'HubPort'
        #--- (YHubPort attributes)
        self._callback = None
        self._enabled = YHubPort.ENABLED_INVALID
        self._portState = YHubPort.PORTSTATE_INVALID
        self._baudRate = YHubPort.BAUDRATE_INVALID
        #--- (end of YHubPort attributes)

    #--- (YHubPort implementation)
    def _parseAttr(self, json_val):
        if json_val.has("enabled"):
            self._enabled = (json_val.getInt("enabled") > 0 if 1 else 0)
        if json_val.has("portState"):
            self._portState = json_val.getInt("portState")
        if json_val.has("baudRate"):
            self._baudRate = json_val.getInt("baudRate")
        super(YHubPort, self)._parseAttr(json_val)

    def get_enabled(self):
        """
        Returns true if the Yocto-hub port is powered, false otherwise.

        @return either YHubPort.ENABLED_FALSE or YHubPort.ENABLED_TRUE, according to true if the Yocto-hub
        port is powered, false otherwise

        On failure, throws an exception or returns YHubPort.ENABLED_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YHubPort.ENABLED_INVALID
        res = self._enabled
        return res

    def set_enabled(self, newval):
        """
        Changes the activation of the Yocto-hub port. If the port is enabled, the
        connected module is powered. Otherwise, port power is shut down.

        @param newval : either YHubPort.ENABLED_FALSE or YHubPort.ENABLED_TRUE, according to the activation
        of the Yocto-hub port

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("enabled", rest_val)

    def get_portState(self):
        """
        Returns the current state of the Yocto-hub port.

        @return a value among YHubPort.PORTSTATE_OFF, YHubPort.PORTSTATE_OVRLD, YHubPort.PORTSTATE_ON,
        YHubPort.PORTSTATE_RUN and YHubPort.PORTSTATE_PROG corresponding to the current state of the Yocto-hub port

        On failure, throws an exception or returns YHubPort.PORTSTATE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YHubPort.PORTSTATE_INVALID
        res = self._portState
        return res

    def get_baudRate(self):
        """
        Returns the current baud rate used by this Yocto-hub port, in kbps.
        The default value is 1000 kbps, but a slower rate may be used if communication
        problems are encountered.

        @return an integer corresponding to the current baud rate used by this Yocto-hub port, in kbps

        On failure, throws an exception or returns YHubPort.BAUDRATE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YHubPort.BAUDRATE_INVALID
        res = self._baudRate
        return res

    @staticmethod
    def FindHubPort(func):
        """
        Retrieves a Yocto-hub port for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the Yocto-hub port is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YHubPort.isOnline() to test if the Yocto-hub port is
        indeed online at a given time. In case of ambiguity when looking for
        a Yocto-hub port by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the Yocto-hub port

        @return a YHubPort object allowing you to drive the Yocto-hub port.
        """
        # obj
        obj = YFunction._FindFromCache("HubPort", func)
        if obj is None:
            obj = YHubPort(func)
            YFunction._AddToCache("HubPort", func, obj)
        return obj

    def nextHubPort(self):
        """
        Continues the enumeration of Yocto-hub ports started using yFirstHubPort().

        @return a pointer to a YHubPort object, corresponding to
                a Yocto-hub port currently online, or a None pointer
                if there are no more Yocto-hub ports to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YHubPort.FindHubPort(hwidRef.value)

#--- (end of YHubPort implementation)

#--- (YHubPort functions)

    @staticmethod
    def FirstHubPort():
        """
        Starts the enumeration of Yocto-hub ports currently accessible.
        Use the method YHubPort.nextHubPort() to iterate on
        next Yocto-hub ports.

        @return a pointer to a YHubPort object, corresponding to
                the first Yocto-hub port currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("HubPort", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YHubPort.FindHubPort(serialRef.value + "." + funcIdRef.value)

#--- (end of YHubPort functions)
