# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindVirtualSensor(), the high-level API for VirtualSensor functions
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


#--- (YVirtualSensor class start)
#noinspection PyProtectedMember
class YVirtualSensor(YSensor):
    """
    The YVirtualSensor class allows you to use Yoctopuce virtual sensors.
    These sensors make it possible to show external data collected by the user
    as a Yoctopuce Sensor. This class inherits from YSensor class the core
    functions to read measurements, to register callback functions, and to access
    the autonomous datalogger. It adds the ability to change the sensor value as
    needed, or to mark current value as invalid.

    """
    #--- (end of YVirtualSensor class start)
    #--- (YVirtualSensor return codes)
    #--- (end of YVirtualSensor return codes)
    #--- (YVirtualSensor dlldef)
    #--- (end of YVirtualSensor dlldef)
    #--- (YVirtualSensor yapiwrapper)
    #--- (end of YVirtualSensor yapiwrapper)
    #--- (YVirtualSensor definitions)
    INVALIDVALUE_INVALID = YAPI.INVALID_DOUBLE
    #--- (end of YVirtualSensor definitions)

    def __init__(self, func):
        super(YVirtualSensor, self).__init__(func)
        self._className = 'VirtualSensor'
        #--- (YVirtualSensor attributes)
        self._callback = None
        self._invalidValue = YVirtualSensor.INVALIDVALUE_INVALID
        #--- (end of YVirtualSensor attributes)

    #--- (YVirtualSensor implementation)
    def _parseAttr(self, json_val):
        if json_val.has("invalidValue"):
            self._invalidValue = round(json_val.getDouble("invalidValue") / 65.536) / 1000.0
        super(YVirtualSensor, self)._parseAttr(json_val)

    def set_unit(self, newval):
        """
        Changes the measuring unit for the measured value.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : a string corresponding to the measuring unit for the measured value

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("unit", rest_val)

    def set_currentRawValue(self, newval):
        """
        Changes the current value of the sensor (raw value, before calibration).

        @param newval : a floating point number corresponding to the current value of the sensor (raw
        value, before calibration)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("currentRawValue", rest_val)

    def set_sensorState(self, newval):
        rest_val = str(newval)
        return self._setAttr("sensorState", rest_val)

    def set_invalidValue(self, newval):
        """
        Changes the invalid value of the sensor, returned if the sensor is read when in invalid state
        (for instance before having been set). Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : a floating point number corresponding to the invalid value of the sensor, returned
        if the sensor is read when in invalid state
                (for instance before having been set)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("invalidValue", rest_val)

    def get_invalidValue(self):
        """
        Returns the invalid value of the sensor, returned if the sensor is read when in invalid state
        (for instance before having been set).

        @return a floating point number corresponding to the invalid value of the sensor, returned if the
        sensor is read when in invalid state
                (for instance before having been set)

        On failure, throws an exception or returns YVirtualSensor.INVALIDVALUE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YVirtualSensor.INVALIDVALUE_INVALID
        res = self._invalidValue
        return res

    @staticmethod
    def FindVirtualSensor(func):
        """
        Retrieves a virtual sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the virtual sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YVirtualSensor.isOnline() to test if the virtual sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a virtual sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the virtual sensor, for instance
                MyDevice.virtualSensor1.

        @return a YVirtualSensor object allowing you to drive the virtual sensor.
        """
        # obj
        obj = YFunction._FindFromCache("VirtualSensor", func)
        if obj is None:
            obj = YVirtualSensor(func)
            YFunction._AddToCache("VirtualSensor", func, obj)
        return obj

    def set_sensorAsInvalid(self):
        """
        Changes the current sensor state to invalid (as if no value would have been ever set).

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_sensorState(1)

    def nextVirtualSensor(self):
        """
        Continues the enumeration of virtual sensors started using yFirstVirtualSensor().
        Caution: You can't make any assumption about the returned virtual sensors order.
        If you want to find a specific a virtual sensor, use VirtualSensor.findVirtualSensor()
        and a hardwareID or a logical name.

        @return a pointer to a YVirtualSensor object, corresponding to
                a virtual sensor currently online, or a None pointer
                if there are no more virtual sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YVirtualSensor.FindVirtualSensor(hwidRef.value)

#--- (end of YVirtualSensor implementation)

#--- (YVirtualSensor functions)

    @staticmethod
    def FirstVirtualSensor():
        """
        Starts the enumeration of virtual sensors currently accessible.
        Use the method YVirtualSensor.nextVirtualSensor() to iterate on
        next virtual sensors.

        @return a pointer to a YVirtualSensor object, corresponding to
                the first virtual sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("VirtualSensor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YVirtualSensor.FindVirtualSensor(serialRef.value + "." + funcIdRef.value)

#--- (end of YVirtualSensor functions)
