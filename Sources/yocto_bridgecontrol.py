# -*- coding: utf-8 -*-
#*********************************************************************
#*
#* $Id: yocto_bridgecontrol.py 27164 2017-04-13 09:57:00Z seb $
#*
#* Implements yFindBridgeControl(), the high-level API for BridgeControl functions
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


#--- (YBridgeControl class start)
#noinspection PyProtectedMember
class YBridgeControl(YFunction):
    """
    The Yoctopuce class YBridgeControl allows you to control bridge excitation parameters
    and measure parameters for a Wheatstone bridge sensor. To read the measurements, it
    is best to use the GenericSensor calss, which will compute the measured value
    in the optimal way.

    """
#--- (end of YBridgeControl class start)
    #--- (YBridgeControl return codes)
    #--- (end of YBridgeControl return codes)
    #--- (YBridgeControl dlldef)
    #--- (end of YBridgeControl dlldef)
    #--- (YBridgeControl definitions)
    BRIDGELATENCY_INVALID = YAPI.INVALID_UINT
    ADVALUE_INVALID = YAPI.INVALID_INT
    ADGAIN_INVALID = YAPI.INVALID_UINT
    EXCITATIONMODE_INTERNAL_AC = 0
    EXCITATIONMODE_INTERNAL_DC = 1
    EXCITATIONMODE_EXTERNAL_DC = 2
    EXCITATIONMODE_INVALID = -1
    #--- (end of YBridgeControl definitions)

    def __init__(self, func):
        super(YBridgeControl, self).__init__(func)
        self._className = 'BridgeControl'
        #--- (YBridgeControl attributes)
        self._callback = None
        self._excitationMode = YBridgeControl.EXCITATIONMODE_INVALID
        self._bridgeLatency = YBridgeControl.BRIDGELATENCY_INVALID
        self._adValue = YBridgeControl.ADVALUE_INVALID
        self._adGain = YBridgeControl.ADGAIN_INVALID
        #--- (end of YBridgeControl attributes)

    #--- (YBridgeControl implementation)
    def _parseAttr(self, json_val):
        if json_val.has("excitationMode"):
            self._excitationMode = json_val.getInt("excitationMode")
        if json_val.has("bridgeLatency"):
            self._bridgeLatency = json_val.getInt("bridgeLatency")
        if json_val.has("adValue"):
            self._adValue = json_val.getInt("adValue")
        if json_val.has("adGain"):
            self._adGain = json_val.getInt("adGain")
        super(YBridgeControl, self)._parseAttr(json_val)

    def get_excitationMode(self):
        """
        Returns the current Wheatstone bridge excitation method.

        @return a value among YBridgeControl.EXCITATIONMODE_INTERNAL_AC,
        YBridgeControl.EXCITATIONMODE_INTERNAL_DC and YBridgeControl.EXCITATIONMODE_EXTERNAL_DC
        corresponding to the current Wheatstone bridge excitation method

        On failure, throws an exception or returns YBridgeControl.EXCITATIONMODE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBridgeControl.EXCITATIONMODE_INVALID
        res = self._excitationMode
        return res

    def set_excitationMode(self, newval):
        """
        Changes the current Wheatstone bridge excitation method.

        @param newval : a value among YBridgeControl.EXCITATIONMODE_INTERNAL_AC,
        YBridgeControl.EXCITATIONMODE_INTERNAL_DC and YBridgeControl.EXCITATIONMODE_EXTERNAL_DC
        corresponding to the current Wheatstone bridge excitation method

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("excitationMode", rest_val)

    def get_bridgeLatency(self):
        """
        Returns the current Wheatstone bridge excitation method.

        @return an integer corresponding to the current Wheatstone bridge excitation method

        On failure, throws an exception or returns YBridgeControl.BRIDGELATENCY_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBridgeControl.BRIDGELATENCY_INVALID
        res = self._bridgeLatency
        return res

    def set_bridgeLatency(self, newval):
        """
        Changes the current Wheatstone bridge excitation method.

        @param newval : an integer corresponding to the current Wheatstone bridge excitation method

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("bridgeLatency", rest_val)

    def get_adValue(self):
        """
        Returns the raw value returned by the ratiometric A/D converter
        during last read.

        @return an integer corresponding to the raw value returned by the ratiometric A/D converter
                during last read

        On failure, throws an exception or returns YBridgeControl.ADVALUE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBridgeControl.ADVALUE_INVALID
        res = self._adValue
        return res

    def get_adGain(self):
        """
        Returns the current ratiometric A/D converter gain. The gain is automatically
        configured according to the signalRange set in the corresponding genericSensor.

        @return an integer corresponding to the current ratiometric A/D converter gain

        On failure, throws an exception or returns YBridgeControl.ADGAIN_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBridgeControl.ADGAIN_INVALID
        res = self._adGain
        return res

    @staticmethod
    def FindBridgeControl(func):
        """
        Retrieves a Wheatstone bridge controller for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the Wheatstone bridge controller is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YBridgeControl.isOnline() to test if the Wheatstone bridge controller is
        indeed online at a given time. In case of ambiguity when looking for
        a Wheatstone bridge controller by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the Wheatstone bridge controller

        @return a YBridgeControl object allowing you to drive the Wheatstone bridge controller.
        """
        # obj
        obj = YFunction._FindFromCache("BridgeControl", func)
        if obj is None:
            obj = YBridgeControl(func)
            YFunction._AddToCache("BridgeControl", func, obj)
        return obj

    def nextBridgeControl(self):
        """
        Continues the enumeration of Wheatstone bridge controllers started using yFirstBridgeControl().

        @return a pointer to a YBridgeControl object, corresponding to
                a Wheatstone bridge controller currently online, or a None pointer
                if there are no more Wheatstone bridge controllers to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YBridgeControl.FindBridgeControl(hwidRef.value)

#--- (end of YBridgeControl implementation)

#--- (BridgeControl functions)

    @staticmethod
    def FirstBridgeControl():
        """
        Starts the enumeration of Wheatstone bridge controllers currently accessible.
        Use the method YBridgeControl.nextBridgeControl() to iterate on
        next Wheatstone bridge controllers.

        @return a pointer to a YBridgeControl object, corresponding to
                the first Wheatstone bridge controller currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("BridgeControl", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YBridgeControl.FindBridgeControl(serialRef.value + "." + funcIdRef.value)

#--- (end of BridgeControl functions)
