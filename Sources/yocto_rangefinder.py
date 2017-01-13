#*********************************************************************
#*
#* $Id: yocto_rangefinder.py 26329 2017-01-11 14:04:39Z mvuilleu $
#*
#* Implements yFindRangeFinder(), the high-level API for RangeFinder functions
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


#--- (YRangeFinder class start)
#noinspection PyProtectedMember
class YRangeFinder(YSensor):
    """
    The Yoctopuce class YRangeFinder allows you to use and configure Yoctopuce range finders
    sensors. It inherits from YSensor class the core functions to read measurements,
    register callback functions, access to the autonomous datalogger.
    This class adds the ability to easily perform a one-point linear calibration
    to compensate the effect of a glass or filter placed in front of the sensor.

    """
#--- (end of YRangeFinder class start)
    #--- (YRangeFinder return codes)
    #--- (end of YRangeFinder return codes)
    #--- (YRangeFinder dlldef)
    #--- (end of YRangeFinder dlldef)
    #--- (YRangeFinder definitions)
    COMMAND_INVALID = YAPI.INVALID_STRING
    RANGEFINDERMODE_DEFAULT = 0
    RANGEFINDERMODE_LONG_RANGE = 1
    RANGEFINDERMODE_HIGH_ACCURACY = 2
    RANGEFINDERMODE_HIGH_SPEED = 3
    RANGEFINDERMODE_INVALID = -1
    #--- (end of YRangeFinder definitions)

    def __init__(self, func):
        super(YRangeFinder, self).__init__(func)
        self._className = 'RangeFinder'
        #--- (YRangeFinder attributes)
        self._callback = None
        self._rangeFinderMode = YRangeFinder.RANGEFINDERMODE_INVALID
        self._command = YRangeFinder.COMMAND_INVALID
        #--- (end of YRangeFinder attributes)

    #--- (YRangeFinder implementation)
    def _parseAttr(self, member):
        if member.name == "rangeFinderMode":
            self._rangeFinderMode = member.ivalue
            return 1
        if member.name == "command":
            self._command = member.svalue
            return 1
        super(YRangeFinder, self)._parseAttr(member)

    def set_unit(self, newval):
        """
        Changes the measuring unit for the measured temperature. That unit is a string.
        String value can be " or mm. Any other value will be ignored.
        Remember to call the saveToFlash() method of the module if the modification must be kept.
        WARNING: if a specific calibration is defined for the rangeFinder function, a
        unit system change will probably break it.

        @param newval : a string corresponding to the measuring unit for the measured temperature

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("unit", rest_val)

    def get_rangeFinderMode(self):
        """
        Returns the rangefinder running mode. The rangefinder running mode
        allows to put priority on precision, speed or maximum range.

        @return a value among YRangeFinder.RANGEFINDERMODE_DEFAULT, YRangeFinder.RANGEFINDERMODE_LONG_RANGE,
        YRangeFinder.RANGEFINDERMODE_HIGH_ACCURACY and YRangeFinder.RANGEFINDERMODE_HIGH_SPEED
        corresponding to the rangefinder running mode

        On failure, throws an exception or returns YRangeFinder.RANGEFINDERMODE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YRangeFinder.RANGEFINDERMODE_INVALID
        return self._rangeFinderMode

    def set_rangeFinderMode(self, newval):
        """
        Changes the rangefinder running mode, allowing to put priority on
        precision, speed or maximum range.

        @param newval : a value among YRangeFinder.RANGEFINDERMODE_DEFAULT,
        YRangeFinder.RANGEFINDERMODE_LONG_RANGE, YRangeFinder.RANGEFINDERMODE_HIGH_ACCURACY and
        YRangeFinder.RANGEFINDERMODE_HIGH_SPEED corresponding to the rangefinder running mode, allowing to
        put priority on
                precision, speed or maximum range

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("rangeFinderMode", rest_val)

    def get_command(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YRangeFinder.COMMAND_INVALID
        return self._command

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindRangeFinder(func):
        """
        Retrieves a range finder for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the range finder is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRangeFinder.isOnline() to test if the range finder is
        indeed online at a given time. In case of ambiguity when looking for
        a range finder by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the range finder

        @return a YRangeFinder object allowing you to drive the range finder.
        """
        # obj
        obj = YFunction._FindFromCache("RangeFinder", func)
        if obj is None:
            obj = YRangeFinder(func)
            YFunction._AddToCache("RangeFinder", func, obj)
        return obj

    def triggerTempCalibration(self):
        """
        Triggers a sensor calibration according to the current ambient temperature. That
        calibration process needs no physical interaction with the sensor. It is performed
        automatically at device startup, but it is recommended to start it again when the
        temperature delta since last calibration exceeds 8°C.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("T")

    def nextRangeFinder(self):
        """
        Continues the enumeration of range finders started using yFirstRangeFinder().

        @return a pointer to a YRangeFinder object, corresponding to
                a range finder currently online, or a None pointer
                if there are no more range finders to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YRangeFinder.FindRangeFinder(hwidRef.value)

#--- (end of YRangeFinder implementation)

#--- (RangeFinder functions)

    @staticmethod
    def FirstRangeFinder():
        """
        Starts the enumeration of range finders currently accessible.
        Use the method YRangeFinder.nextRangeFinder() to iterate on
        next range finders.

        @return a pointer to a YRangeFinder object, corresponding to
                the first range finder currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("RangeFinder", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YRangeFinder.FindRangeFinder(serialRef.value + "." + funcIdRef.value)

#--- (end of RangeFinder functions)
