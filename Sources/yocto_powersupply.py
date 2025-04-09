# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindPowerSupply(), the high-level API for PowerSupply functions
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


#--- (YPowerSupply class start)
#noinspection PyProtectedMember
class YPowerSupply(YFunction):
    """
    The YPowerSupply class allows you to drive a Yoctopuce power supply.
    It can be use to change the voltage and current limits, and to enable/disable
    the output.

    """
    #--- (end of YPowerSupply class start)
    #--- (YPowerSupply return codes)
    #--- (end of YPowerSupply return codes)
    #--- (YPowerSupply dlldef)
    #--- (end of YPowerSupply dlldef)
    #--- (YPowerSupply yapiwrapper)
    #--- (end of YPowerSupply yapiwrapper)
    #--- (YPowerSupply definitions)
    VOLTAGELIMIT_INVALID = YAPI.INVALID_DOUBLE
    CURRENTLIMIT_INVALID = YAPI.INVALID_DOUBLE
    MEASUREDVOLTAGE_INVALID = YAPI.INVALID_DOUBLE
    MEASUREDCURRENT_INVALID = YAPI.INVALID_DOUBLE
    INPUTVOLTAGE_INVALID = YAPI.INVALID_DOUBLE
    VOLTAGETRANSITION_INVALID = YAPI.INVALID_STRING
    VOLTAGELIMITATSTARTUP_INVALID = YAPI.INVALID_DOUBLE
    CURRENTLIMITATSTARTUP_INVALID = YAPI.INVALID_DOUBLE
    COMMAND_INVALID = YAPI.INVALID_STRING
    POWEROUTPUT_OFF = 0
    POWEROUTPUT_ON = 1
    POWEROUTPUT_INVALID = -1
    POWEROUTPUTATSTARTUP_OFF = 0
    POWEROUTPUTATSTARTUP_ON = 1
    POWEROUTPUTATSTARTUP_INVALID = -1
    #--- (end of YPowerSupply definitions)

    def __init__(self, func):
        super(YPowerSupply, self).__init__(func)
        self._className = 'PowerSupply'
        #--- (YPowerSupply attributes)
        self._callback = None
        self._voltageLimit = YPowerSupply.VOLTAGELIMIT_INVALID
        self._currentLimit = YPowerSupply.CURRENTLIMIT_INVALID
        self._powerOutput = YPowerSupply.POWEROUTPUT_INVALID
        self._measuredVoltage = YPowerSupply.MEASUREDVOLTAGE_INVALID
        self._measuredCurrent = YPowerSupply.MEASUREDCURRENT_INVALID
        self._inputVoltage = YPowerSupply.INPUTVOLTAGE_INVALID
        self._voltageTransition = YPowerSupply.VOLTAGETRANSITION_INVALID
        self._voltageLimitAtStartUp = YPowerSupply.VOLTAGELIMITATSTARTUP_INVALID
        self._currentLimitAtStartUp = YPowerSupply.CURRENTLIMITATSTARTUP_INVALID
        self._powerOutputAtStartUp = YPowerSupply.POWEROUTPUTATSTARTUP_INVALID
        self._command = YPowerSupply.COMMAND_INVALID
        #--- (end of YPowerSupply attributes)

    #--- (YPowerSupply implementation)
    def _parseAttr(self, json_val):
        if json_val.has("voltageLimit"):
            self._voltageLimit = round(json_val.getDouble("voltageLimit") / 65.536) / 1000.0
        if json_val.has("currentLimit"):
            self._currentLimit = round(json_val.getDouble("currentLimit") / 65.536) / 1000.0
        if json_val.has("powerOutput"):
            self._powerOutput = json_val.getInt("powerOutput") > 0
        if json_val.has("measuredVoltage"):
            self._measuredVoltage = round(json_val.getDouble("measuredVoltage") / 65.536) / 1000.0
        if json_val.has("measuredCurrent"):
            self._measuredCurrent = round(json_val.getDouble("measuredCurrent") / 65.536) / 1000.0
        if json_val.has("inputVoltage"):
            self._inputVoltage = round(json_val.getDouble("inputVoltage") / 65.536) / 1000.0
        if json_val.has("voltageTransition"):
            self._voltageTransition = json_val.getString("voltageTransition")
        if json_val.has("voltageLimitAtStartUp"):
            self._voltageLimitAtStartUp = round(json_val.getDouble("voltageLimitAtStartUp") / 65.536) / 1000.0
        if json_val.has("currentLimitAtStartUp"):
            self._currentLimitAtStartUp = round(json_val.getDouble("currentLimitAtStartUp") / 65.536) / 1000.0
        if json_val.has("powerOutputAtStartUp"):
            self._powerOutputAtStartUp = json_val.getInt("powerOutputAtStartUp") > 0
        if json_val.has("command"):
            self._command = json_val.getString("command")
        super(YPowerSupply, self)._parseAttr(json_val)

    def set_voltageLimit(self, newval):
        """
        Changes the voltage limit, in V.

        @param newval : a floating point number corresponding to the voltage limit, in V

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("voltageLimit", rest_val)

    def get_voltageLimit(self):
        """
        Returns the voltage limit, in V.

        @return a floating point number corresponding to the voltage limit, in V

        On failure, throws an exception or returns YPowerSupply.VOLTAGELIMIT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.VOLTAGELIMIT_INVALID
        res = self._voltageLimit
        return res

    def set_currentLimit(self, newval):
        """
        Changes the current limit, in mA.

        @param newval : a floating point number corresponding to the current limit, in mA

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("currentLimit", rest_val)

    def get_currentLimit(self):
        """
        Returns the current limit, in mA.

        @return a floating point number corresponding to the current limit, in mA

        On failure, throws an exception or returns YPowerSupply.CURRENTLIMIT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.CURRENTLIMIT_INVALID
        res = self._currentLimit
        return res

    def get_powerOutput(self):
        """
        Returns the power supply output switch state.

        @return either YPowerSupply.POWEROUTPUT_OFF or YPowerSupply.POWEROUTPUT_ON, according to the power
        supply output switch state

        On failure, throws an exception or returns YPowerSupply.POWEROUTPUT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.POWEROUTPUT_INVALID
        res = self._powerOutput
        return res

    def set_powerOutput(self, newval):
        """
        Changes the power supply output switch state.

        @param newval : either YPowerSupply.POWEROUTPUT_OFF or YPowerSupply.POWEROUTPUT_ON, according to
        the power supply output switch state

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("powerOutput", rest_val)

    def get_measuredVoltage(self):
        """
        Returns the measured output voltage, in V.

        @return a floating point number corresponding to the measured output voltage, in V

        On failure, throws an exception or returns YPowerSupply.MEASUREDVOLTAGE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.MEASUREDVOLTAGE_INVALID
        res = self._measuredVoltage
        return res

    def get_measuredCurrent(self):
        """
        Returns the measured output current, in mA.

        @return a floating point number corresponding to the measured output current, in mA

        On failure, throws an exception or returns YPowerSupply.MEASUREDCURRENT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.MEASUREDCURRENT_INVALID
        res = self._measuredCurrent
        return res

    def get_inputVoltage(self):
        """
        Returns the measured input voltage, in V.

        @return a floating point number corresponding to the measured input voltage, in V

        On failure, throws an exception or returns YPowerSupply.INPUTVOLTAGE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.INPUTVOLTAGE_INVALID
        res = self._inputVoltage
        return res

    def get_voltageTransition(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.VOLTAGETRANSITION_INVALID
        res = self._voltageTransition
        return res

    def set_voltageTransition(self, newval):
        rest_val = newval
        return self._setAttr("voltageTransition", rest_val)

    def set_voltageLimitAtStartUp(self, newval):
        """
        Changes the voltage set point at device start up. Remember to call the matching
        module saveToFlash() method, otherwise this call has no effect.

        @param newval : a floating point number corresponding to the voltage set point at device start up

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("voltageLimitAtStartUp", rest_val)

    def get_voltageLimitAtStartUp(self):
        """
        Returns the selected voltage limit at device startup, in V.

        @return a floating point number corresponding to the selected voltage limit at device startup, in V

        On failure, throws an exception or returns YPowerSupply.VOLTAGELIMITATSTARTUP_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.VOLTAGELIMITATSTARTUP_INVALID
        res = self._voltageLimitAtStartUp
        return res

    def set_currentLimitAtStartUp(self, newval):
        """
        Changes the current limit at device start up. Remember to call the matching
        module saveToFlash() method, otherwise this call has no effect.

        @param newval : a floating point number corresponding to the current limit at device start up

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("currentLimitAtStartUp", rest_val)

    def get_currentLimitAtStartUp(self):
        """
        Returns the selected current limit at device startup, in mA.

        @return a floating point number corresponding to the selected current limit at device startup, in mA

        On failure, throws an exception or returns YPowerSupply.CURRENTLIMITATSTARTUP_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.CURRENTLIMITATSTARTUP_INVALID
        res = self._currentLimitAtStartUp
        return res

    def get_powerOutputAtStartUp(self):
        """
        Returns the power supply output switch state.

        @return either YPowerSupply.POWEROUTPUTATSTARTUP_OFF or YPowerSupply.POWEROUTPUTATSTARTUP_ON,
        according to the power supply output switch state

        On failure, throws an exception or returns YPowerSupply.POWEROUTPUTATSTARTUP_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.POWEROUTPUTATSTARTUP_INVALID
        res = self._powerOutputAtStartUp
        return res

    def set_powerOutputAtStartUp(self, newval):
        """
        Changes the power supply output switch state at device start up. Remember to call the matching
        module saveToFlash() method, otherwise this call has no effect.

        @param newval : either YPowerSupply.POWEROUTPUTATSTARTUP_OFF or
        YPowerSupply.POWEROUTPUTATSTARTUP_ON, according to the power supply output switch state at device start up

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("powerOutputAtStartUp", rest_val)

    def get_command(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPowerSupply.COMMAND_INVALID
        res = self._command
        return res

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindPowerSupply(func):
        """
        Retrieves a regulated power supply for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the regulated power supply is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPowerSupply.isOnline() to test if the regulated power supply is
        indeed online at a given time. In case of ambiguity when looking for
        a regulated power supply by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the regulated power supply, for instance
                MyDevice.powerSupply.

        @return a YPowerSupply object allowing you to drive the regulated power supply.
        """
        # obj
        obj = YFunction._FindFromCache("PowerSupply", func)
        if obj is None:
            obj = YPowerSupply(func)
            YFunction._AddToCache("PowerSupply", func, obj)
        return obj

    def voltageMove(self, V_target, ms_duration):
        """
        Performs a smooth transition of output voltage. Any explicit voltage
        change cancels any ongoing transition process.

        @param V_target   : new output voltage value at the end of the transition
                (floating-point number, representing the end voltage in V)
        @param ms_duration : total duration of the transition, in milliseconds

        @return YAPI.SUCCESS when the call succeeds.
        """
        # newval
        if V_target < 0.0:
            V_target  = 0.0
        newval = "" + str(int(round(V_target*65536))) + ":" + str(int(ms_duration))

        return self.set_voltageTransition(newval)

    def nextPowerSupply(self):
        """
        Continues the enumeration of regulated power supplies started using yFirstPowerSupply().
        Caution: You can't make any assumption about the returned regulated power supplies order.
        If you want to find a specific a regulated power supply, use PowerSupply.findPowerSupply()
        and a hardwareID or a logical name.

        @return a pointer to a YPowerSupply object, corresponding to
                a regulated power supply currently online, or a None pointer
                if there are no more regulated power supplies to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YPowerSupply.FindPowerSupply(hwidRef.value)

#--- (end of YPowerSupply implementation)

#--- (YPowerSupply functions)

    @staticmethod
    def FirstPowerSupply():
        """
        Starts the enumeration of regulated power supplies currently accessible.
        Use the method YPowerSupply.nextPowerSupply() to iterate on
        next regulated power supplies.

        @return a pointer to a YPowerSupply object, corresponding to
                the first regulated power supply currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("PowerSupply", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YPowerSupply.FindPowerSupply(serialRef.value + "." + funcIdRef.value)

#--- (end of YPowerSupply functions)
