#*********************************************************************
#*
#* $Id: yocto_current.py 11112 2013-04-16 14:51:20Z mvuilleu $
#*
#* Implements yFindCurrent(), the high-level API for Current functions
#*
#* - - - - - - - - - License information: - - - - - - - - - 
#*
#* Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#*
#* 1) If you have obtained this file from www.yoctopuce.com,
#*    Yoctopuce Sarl licenses to you (hereafter Licensee) the
#*    right to use, modify, copy, and integrate this source file
#*    into your own solution for the sole purpose of interfacing
#*    a Yoctopuce product with Licensee's solution.
#*
#*    The use of this file and all relationship between Yoctopuce 
#*    and Licensee are governed by Yoctopuce General Terms and 
#*    Conditions.
#*
#*    THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#*    WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING 
#*    WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS 
#*    FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#*    EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#*    INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, 
#*    COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR 
#*    SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT 
#*    LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#*    CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#*    BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#*    WARRANTY, OR OTHERWISE.
#*
#* 2) If your intent is not to interface with Yoctopuce products,
#*    you are not entitled to use, read or create any derived
#*    material from this source file.
#*
#*********************************************************************/


__docformat__ = 'restructuredtext en'
from yocto_api import *
class YCurrent(YFunction):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YCurrent definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    UNIT_INVALID                    = YAPI.INVALID_STRING
    CURRENTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    LOWESTVALUE_INVALID             = YAPI.INVALID_DOUBLE
    HIGHESTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    CURRENTRAWVALUE_INVALID         = YAPI.INVALID_DOUBLE
    RESOLUTION_INVALID              = YAPI.INVALID_DOUBLE
    CALIBRATIONPARAM_INVALID        = YAPI.INVALID_STRING
    CALIBRATIONOFFSET_INVALID       = YAPI.INVALID_LONG



    _CurrentCache ={}

    #--- (end of YCurrent definitions)

    #--- (YCurrent implementation)

    def __init__(self,func):
        super(YCurrent,self).__init__("Current", func)
        #--- (YCurrent implementation)
        self._callback = None
        self._logicalName = YCurrent.LOGICALNAME_INVALID
        self._advertisedValue = YCurrent.ADVERTISEDVALUE_INVALID
        self._unit = YCurrent.UNIT_INVALID
        self._currentValue = YCurrent.CURRENTVALUE_INVALID
        self._lowestValue = YCurrent.LOWESTVALUE_INVALID
        self._highestValue = YCurrent.HIGHESTVALUE_INVALID
        self._currentRawValue = YCurrent.CURRENTRAWVALUE_INVALID
        self._resolution = YCurrent.RESOLUTION_INVALID
        self._calibrationParam = YCurrent.CALIBRATIONPARAM_INVALID
        self._calibrationOffset = -32767

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "unit":
                self._unit = member.svalue
            elif member.name == "currentValue":
                self._currentValue = round(member.ivalue/65536.0)
            elif member.name == "lowestValue":
                self._lowestValue = round(member.ivalue/65536.0)
            elif member.name == "highestValue":
                self._highestValue = round(member.ivalue/65536.0)
            elif member.name == "currentRawValue":
                self._currentRawValue = member.ivalue/65536.0
            elif member.name == "resolution":
                self._resolution = 1.0 / round(65536.0/member.ivalue)
            elif member.name == "calibrationParam":
                self._calibrationParam = member.svalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the current sensor.
        
        @return a string corresponding to the logical name of the current sensor
        
        On failure, throws an exception or returns YCurrent.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the current sensor. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the current sensor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the current sensor (no more than 6 characters).
        
        @return a string corresponding to the current value of the current sensor (no more than 6 characters)
        
        On failure, throws an exception or returns YCurrent.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_unit(self):
        """
        Returns the measuring unit for the measured value.
        
        @return a string corresponding to the measuring unit for the measured value
        
        On failure, throws an exception or returns YCurrent.UNIT_INVALID.
        """
        if self._unit == YCurrent.UNIT_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.UNIT_INVALID
        return self._unit

    def get_currentValue(self):
        """
        Returns the current measured value.
        
        @return a floating point number corresponding to the current measured value
        
        On failure, throws an exception or returns YCurrent.CURRENTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.CURRENTVALUE_INVALID
        res = YAPI._applyCalibration(self._currentRawValue, self._calibrationParam, self._calibrationOffset, self._resolution)
        if res != YCurrent.CURRENTVALUE_INVALID:
            return res
        return self._currentValue

    def set_lowestValue(self, newval):
        """
        Changes the recorded minimal value observed.
        
        @param newval : a floating point number corresponding to the recorded minimal value observed
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("lowestValue", rest_val)


    def get_lowestValue(self):
        """
        Returns the minimal value observed.
        
        @return a floating point number corresponding to the minimal value observed
        
        On failure, throws an exception or returns YCurrent.LOWESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.LOWESTVALUE_INVALID
        return self._lowestValue

    def set_highestValue(self, newval):
        """
        Changes the recorded maximal value observed.
        
        @param newval : a floating point number corresponding to the recorded maximal value observed
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("highestValue", rest_val)


    def get_highestValue(self):
        """
        Returns the maximal value observed.
        
        @return a floating point number corresponding to the maximal value observed
        
        On failure, throws an exception or returns YCurrent.HIGHESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.HIGHESTVALUE_INVALID
        return self._highestValue

    def get_currentRawValue(self):
        """
        Returns the uncalibrated, unrounded raw value returned by the sensor.
        
        @return a floating point number corresponding to the uncalibrated, unrounded raw value returned by the sensor
        
        On failure, throws an exception or returns YCurrent.CURRENTRAWVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.CURRENTRAWVALUE_INVALID
        return self._currentRawValue

    def set_resolution(self, newval):
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("resolution", rest_val)


    def get_resolution(self):
        """
        Returns the resolution of the measured values. The resolution corresponds to the numerical precision
        of the values, which is not always the same as the actual precision of the sensor.
        
        @return a floating point number corresponding to the resolution of the measured values
        
        On failure, throws an exception or returns YCurrent.RESOLUTION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.RESOLUTION_INVALID
        return self._resolution

    def get_calibrationParam(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YCurrent.CALIBRATIONPARAM_INVALID
        return self._calibrationParam

    def set_calibrationParam(self, newval):
        rest_val = newval
        return self._setAttr("calibrationParam", rest_val)


    def calibrateFromPoints(self , rawValues,refValues):
        """
        Configures error correction data points, in particular to compensate for
        a possible perturbation of the measure caused by an enclosure. It is possible
        to configure up to five correction points. Correction points must be provided
        in ascending order, and be in the range of the sensor. The device will automatically
        perform a lineat interpolatation of the error correction between specified
        points. Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        For more information on advanced capabilities to refine the calibration of
        sensors, please contact support@yoctopuce.com.
        
        @param rawValues : array of floating point numbers, corresponding to the raw
                values returned by the sensor for the correction points.
        @param refValues : array of floating point numbers, corresponding to the corrected
                values for the correction points.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = YAPI._encodeCalibrationPoints(rawValues,refValues,self._resolution,self._calibrationOffset,self._calibrationParam)
        return self._setAttr("calibrationParam", rest_val)

    def loadCalibrationPoints(self , rawValues,refValues):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return self._lastErrorType
        return YAPI._decodeCalibrationPoints(self._calibrationParam,None,rawValues,refValues,self._resolution,self._calibrationOffset)

    def nextCurrent(self):
        """
        Continues the enumeration of current sensors started using yFirstCurrent().
        
        @return a pointer to a YCurrent object, corresponding to
                a current sensor currently online, or a None pointer
                if there are no more current sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YCurrent.FindCurrent(hwidRef.value)

    def registerValueCallback(self, callback):
        """
        Registers the callback function that is invoked on every change of advertised value.
        The callback is invoked only during the execution of ySleep or yHandleEvents.
        This provides control over the time when the callback is triggered. For good responsiveness, remember to call
        one of these two functions periodically. To unregister a callback, pass a None pointer as argument.
        
        @param callback : the callback function to call, or a None pointer. The callback function should take two
                arguments: the function object of which the value has changed, and the character string describing
                the new advertised value.
        @noreturn
        """
        if callback is not None:
            self._registerFuncCallback(self)
        else:
            self._unregisterFuncCallback(self)
        self._callback = callback

    def set_callback(self, callback):
        self.registerValueCallback(callback)

    def setCallback(self, callback):
        self.registerValueCallback(callback)


    def advertiseValue(self,value):
        if self._callback is not None:
            self._callback(self, value)

#--- (end of YCurrent implementation)

#--- (Current functions)

    @staticmethod 
    def FindCurrent(func):
        """
        Retrieves a current sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the current sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCurrent.isOnline() to test if the current sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a current sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the current sensor
        
        @return a YCurrent object allowing you to drive the current sensor.
        """
        if func in YCurrent._CurrentCache:
            return YCurrent._CurrentCache[func]
        res =YCurrent(func)
        YCurrent._CurrentCache[func] =  res
        return res

    @staticmethod 
    def  FirstCurrent():
        """
        Starts the enumeration of current sensors currently accessible.
        Use the method YCurrent.nextCurrent() to iterate on
        next current sensors.
        
        @return a pointer to a YCurrent object, corresponding to
                the first current sensor currently online, or a None pointer
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
        p = (ctypes.c_int*1)()
        err = YAPI.apiGetFunctionsByClass("Current", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YCurrent.FindCurrent(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _CurrentCleanup():
        pass

  #--- (end of Current functions)

