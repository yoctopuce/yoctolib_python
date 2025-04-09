# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindPower(), the high-level API for Power functions
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


#--- (YPower class start)
#noinspection PyProtectedMember
class YPower(YSensor):
    """
    The YPower class allows you to read and configure Yoctopuce electrical power sensors.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.
    This class adds the ability to access the energy counter and the power factor.

    """
    #--- (end of YPower class start)
    #--- (YPower return codes)
    #--- (end of YPower return codes)
    #--- (YPower dlldef)
    #--- (end of YPower dlldef)
    #--- (YPower yapiwrapper)
    #--- (end of YPower yapiwrapper)
    #--- (YPower definitions)
    POWERFACTOR_INVALID = YAPI.INVALID_DOUBLE
    COSPHI_INVALID = YAPI.INVALID_DOUBLE
    METER_INVALID = YAPI.INVALID_DOUBLE
    DELIVEREDENERGYMETER_INVALID = YAPI.INVALID_DOUBLE
    RECEIVEDENERGYMETER_INVALID = YAPI.INVALID_DOUBLE
    METERTIMER_INVALID = YAPI.INVALID_UINT
    #--- (end of YPower definitions)

    def __init__(self, func):
        super(YPower, self).__init__(func)
        self._className = 'Power'
        #--- (YPower attributes)
        self._callback = None
        self._powerFactor = YPower.POWERFACTOR_INVALID
        self._cosPhi = YPower.COSPHI_INVALID
        self._meter = YPower.METER_INVALID
        self._deliveredEnergyMeter = YPower.DELIVEREDENERGYMETER_INVALID
        self._receivedEnergyMeter = YPower.RECEIVEDENERGYMETER_INVALID
        self._meterTimer = YPower.METERTIMER_INVALID
        #--- (end of YPower attributes)

    #--- (YPower implementation)
    def _parseAttr(self, json_val):
        if json_val.has("powerFactor"):
            self._powerFactor = round(json_val.getDouble("powerFactor") / 65.536) / 1000.0
        if json_val.has("cosPhi"):
            self._cosPhi = round(json_val.getDouble("cosPhi") / 65.536) / 1000.0
        if json_val.has("meter"):
            self._meter = round(json_val.getDouble("meter") / 65.536) / 1000.0
        if json_val.has("deliveredEnergyMeter"):
            self._deliveredEnergyMeter = round(json_val.getDouble("deliveredEnergyMeter") / 65.536) / 1000.0
        if json_val.has("receivedEnergyMeter"):
            self._receivedEnergyMeter = round(json_val.getDouble("receivedEnergyMeter") / 65.536) / 1000.0
        if json_val.has("meterTimer"):
            self._meterTimer = json_val.getInt("meterTimer")
        super(YPower, self)._parseAttr(json_val)

    def get_powerFactor(self):
        """
        Returns the power factor (PF), i.e. ratio between the active power consumed (in W)
        and the apparent power provided (VA).

        @return a floating point number corresponding to the power factor (PF), i.e

        On failure, throws an exception or returns YPower.POWERFACTOR_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPower.POWERFACTOR_INVALID
        res = self._powerFactor
        if res == YPower.POWERFACTOR_INVALID:
            res = self._cosPhi
        res = round(res * 1000) / 1000
        return res

    def get_cosPhi(self):
        """
        Returns the Displacement Power factor (DPF), i.e. cosine of the phase shift between
        the voltage and current fundamentals.
        On the Yocto-Watt (V1), the value returned by this method correponds to the
        power factor as this device is cannot estimate the true DPF.

        @return a floating point number corresponding to the Displacement Power factor (DPF), i.e

        On failure, throws an exception or returns YPower.COSPHI_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPower.COSPHI_INVALID
        res = self._cosPhi
        return res

    def set_meter(self, newval):
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("meter", rest_val)

    def get_meter(self):
        """
        Returns the energy counter, maintained by the wattmeter by integrating the
        power consumption over time. This is the sum of forward and backwad energy transfers,
        if you are insterested in only one direction, use  get_receivedEnergyMeter() or
        get_deliveredEnergyMeter(). Note that this counter is reset at each start of the device.

        @return a floating point number corresponding to the energy counter, maintained by the wattmeter by
        integrating the
                power consumption over time

        On failure, throws an exception or returns YPower.METER_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPower.METER_INVALID
        res = self._meter
        return res

    def get_deliveredEnergyMeter(self):
        """
        Returns the energy counter, maintained by the wattmeter by integrating the power consumption over time,
        but only when positive. Note that this counter is reset at each start of the device.

        @return a floating point number corresponding to the energy counter, maintained by the wattmeter by
        integrating the power consumption over time,
                but only when positive

        On failure, throws an exception or returns YPower.DELIVEREDENERGYMETER_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPower.DELIVEREDENERGYMETER_INVALID
        res = self._deliveredEnergyMeter
        return res

    def get_receivedEnergyMeter(self):
        """
        Returns the energy counter, maintained by the wattmeter by integrating the power consumption over time,
        but only when negative. Note that this counter is reset at each start of the device.

        @return a floating point number corresponding to the energy counter, maintained by the wattmeter by
        integrating the power consumption over time,
                but only when negative

        On failure, throws an exception or returns YPower.RECEIVEDENERGYMETER_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPower.RECEIVEDENERGYMETER_INVALID
        res = self._receivedEnergyMeter
        return res

    def get_meterTimer(self):
        """
        Returns the elapsed time since last energy counter reset, in seconds.

        @return an integer corresponding to the elapsed time since last energy counter reset, in seconds

        On failure, throws an exception or returns YPower.METERTIMER_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YPower.METERTIMER_INVALID
        res = self._meterTimer
        return res

    @staticmethod
    def FindPower(func):
        """
        Retrieves a electrical power sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the electrical power sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPower.isOnline() to test if the electrical power sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a electrical power sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the electrical power sensor, for instance
                YWATTMK1.power.

        @return a YPower object allowing you to drive the electrical power sensor.
        """
        # obj
        obj = YFunction._FindFromCache("Power", func)
        if obj is None:
            obj = YPower(func)
            YFunction._AddToCache("Power", func, obj)
        return obj

    def reset(self):
        """
        Resets the energy counters.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_meter(0)

    def nextPower(self):
        """
        Continues the enumeration of electrical power sensors started using yFirstPower().
        Caution: You can't make any assumption about the returned electrical power sensors order.
        If you want to find a specific a electrical power sensor, use Power.findPower()
        and a hardwareID or a logical name.

        @return a pointer to a YPower object, corresponding to
                a electrical power sensor currently online, or a None pointer
                if there are no more electrical power sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YPower.FindPower(hwidRef.value)

#--- (end of YPower implementation)

#--- (YPower functions)

    @staticmethod
    def FirstPower():
        """
        Starts the enumeration of electrical power sensors currently accessible.
        Use the method YPower.nextPower() to iterate on
        next electrical power sensors.

        @return a pointer to a YPower object, corresponding to
                the first electrical power sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Power", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YPower.FindPower(serialRef.value + "." + funcIdRef.value)

#--- (end of YPower functions)
