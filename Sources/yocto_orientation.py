# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindOrientation(), the high-level API for Orientation functions
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


#--- (YOrientation class start)
#noinspection PyProtectedMember
class YOrientation(YSensor):
    """
    The YOrientation class allows you to read and configure Yoctopuce orientation sensors.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YOrientation class start)
    #--- (YOrientation return codes)
    #--- (end of YOrientation return codes)
    #--- (YOrientation dlldef)
    #--- (end of YOrientation dlldef)
    #--- (YOrientation yapiwrapper)
    #--- (end of YOrientation yapiwrapper)
    #--- (YOrientation definitions)
    COMMAND_INVALID = YAPI.INVALID_STRING
    ZEROOFFSET_INVALID = YAPI.INVALID_DOUBLE
    COUNTERCLOCKWISE_FALSE = 0
    COUNTERCLOCKWISE_TRUE = 1
    COUNTERCLOCKWISE_INVALID = -1
    #--- (end of YOrientation definitions)

    def __init__(self, func):
        super(YOrientation, self).__init__(func)
        self._className = 'Orientation'
        #--- (YOrientation attributes)
        self._callback = None
        self._counterClockwise = YOrientation.COUNTERCLOCKWISE_INVALID
        self._command = YOrientation.COMMAND_INVALID
        self._zeroOffset = YOrientation.ZEROOFFSET_INVALID
        #--- (end of YOrientation attributes)

    #--- (YOrientation implementation)
    def _parseAttr(self, json_val):
        if json_val.has("counterClockwise"):
            self._counterClockwise = json_val.getInt("counterClockwise") > 0
        if json_val.has("command"):
            self._command = json_val.getString("command")
        if json_val.has("zeroOffset"):
            self._zeroOffset = round(json_val.getDouble("zeroOffset") / 65.536) / 1000.0
        super(YOrientation, self)._parseAttr(json_val)

    def get_counterClockwise(self):
        """
        Returns a value indicating whether the sensor is operating in a counterclockwise direction.

        @return either YOrientation.COUNTERCLOCKWISE_FALSE or YOrientation.COUNTERCLOCKWISE_TRUE, according
        to a value indicating whether the sensor is operating in a counterclockwise direction

        On failure, throws an exception or returns YOrientation.COUNTERCLOCKWISE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YOrientation.COUNTERCLOCKWISE_INVALID
        res = self._counterClockwise
        return res

    def set_counterClockwise(self, newval):
        """
        Defines the operating direction of the sensor.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : either YOrientation.COUNTERCLOCKWISE_FALSE or YOrientation.COUNTERCLOCKWISE_TRUE

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("counterClockwise", rest_val)

    def get_command(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YOrientation.COMMAND_INVALID
        res = self._command
        return res

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    def set_zeroOffset(self, newval):
        """
        Sets an offset between the orientation reported by the sensor and the actual orientation. This
        can typically be used  to compensate for mechanical offset. This offset can also be set
        automatically using the zero() method.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : a floating point number

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("zeroOffset", rest_val)

    def get_zeroOffset(self):
        """
        Returns the Offset between the orientation reported by the sensor and the actual orientation.

        @return a floating point number corresponding to the Offset between the orientation reported by the
        sensor and the actual orientation

        On failure, throws an exception or returns YOrientation.ZEROOFFSET_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YOrientation.ZEROOFFSET_INVALID
        res = self._zeroOffset
        return res

    @staticmethod
    def FindOrientation(func):
        """
        Retrieves an orientation sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the orientation sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YOrientation.isOnline() to test if the orientation sensor is
        indeed online at a given time. In case of ambiguity when looking for
        an orientation sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the orientation sensor, for instance
                MyDevice.orientation.

        @return a YOrientation object allowing you to drive the orientation sensor.
        """
        # obj
        obj = YFunction._FindFromCache("Orientation", func)
        if obj is None:
            obj = YOrientation(func)
            YFunction._AddToCache("Orientation", func, obj)
        return obj

    def sendCommand(self, command):
        return self.set_command(command)

    def zero(self):
        """
        Reset the sensor's zero to current position by automatically setting a new offset.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("Z")

    def set_calibration(self, offsetValues):
        """
        Modifies the calibration of the MA600A sensor using an array of 32
        values representing the offset in degrees between the true values and
        those measured regularly every 11.25 degrees starting from zero. The calibration
        is applied immediately and is stored permanently in the MA600A sensor.
        Before calculating the offset values, remember to clear any previous
        calibration using the clearCalibration function and set
        the zero offset  to 0. After a calibration change, the sensor will stop
        measurements for about one second.
        Do not confuse this function with the generic calibrateFromPoints function,
        which works at the YSensor level and is not necessarily well suited to
        a sensor returning circular values.

        @param offsetValues : array of 32 floating point values in the [-11.25..+11.25] range

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # res
        # npt
        # idx
        # corr
        npt = len(offsetValues)
        if npt != 32:
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid calibration parameters (32 expected)")
            return YAPI.INVALID_ARGUMENT
        res = "C"
        idx = 0
        while idx < npt:
            corr = int(round(offsetValues[idx] * 128 / 11.25))
            if (corr < -128) or (corr > 127):
                self._throw(YAPI.INVALID_ARGUMENT, "Calibration parameter exceeds permitted range (+/-11.25)")
                return YAPI.INVALID_ARGUMENT
            if corr < 0:
                corr = corr + 256
            res = "" + res + "" + ("%02x" % corr)
            idx = idx + 1
        return self.sendCommand(res)

    def get_Calibration(self, offsetValues):
        """
        Retrieves offset correction data points previously entered using the method
        set_calibration.

        @param offsetValues : array of 32 floating point numbers, that will be filled by the
                function with the offset values for the correction points.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return 0

    def clearCalibration(self):
        """
        Cancels any calibration set with set_calibration. This function
        is equivalent to calling set_calibration with only zeros.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("-")

    def nextOrientation(self):
        """
        Continues the enumeration of orientation sensors started using yFirstOrientation().
        Caution: You can't make any assumption about the returned orientation sensors order.
        If you want to find a specific an orientation sensor, use Orientation.findOrientation()
        and a hardwareID or a logical name.

        @return a pointer to a YOrientation object, corresponding to
                an orientation sensor currently online, or a None pointer
                if there are no more orientation sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YOrientation.FindOrientation(hwidRef.value)

#--- (end of YOrientation implementation)

#--- (YOrientation functions)

    @staticmethod
    def FirstOrientation():
        """
        Starts the enumeration of orientation sensors currently accessible.
        Use the method YOrientation.nextOrientation() to iterate on
        next orientation sensors.

        @return a pointer to a YOrientation object, corresponding to
                the first orientation sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Orientation", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YOrientation.FindOrientation(serialRef.value + "." + funcIdRef.value)

#--- (end of YOrientation functions)
