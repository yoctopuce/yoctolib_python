#*********************************************************************
#*
#* $Id: yocto_temperature.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindTemperature(), the high-level API for Temperature functions
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
class YTemperature(YFunction):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YTemperature definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    UNIT_INVALID                    = YAPI.INVALID_STRING
    CURRENTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    LOWESTVALUE_INVALID             = YAPI.INVALID_DOUBLE
    HIGHESTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    CURRENTRAWVALUE_INVALID         = YAPI.INVALID_DOUBLE
    CALIBRATIONPARAM_INVALID        = YAPI.INVALID_STRING
    RESOLUTION_INVALID              = YAPI.INVALID_DOUBLE
    CALIBRATIONOFFSET_INVALID       = YAPI.INVALID_LONG

    SENSORTYPE_DIGITAL              = 0
    SENSORTYPE_TYPE_K               = 1
    SENSORTYPE_TYPE_E               = 2
    SENSORTYPE_TYPE_J               = 3
    SENSORTYPE_TYPE_N               = 4
    SENSORTYPE_TYPE_R               = 5
    SENSORTYPE_TYPE_S               = 6
    SENSORTYPE_TYPE_T               = 7
    SENSORTYPE_PT100_4WIRES         = 8
    SENSORTYPE_PT100_3WIRES         = 9
    SENSORTYPE_PT100_2WIRES         = 10
    SENSORTYPE_INVALID              = -1


    _TemperatureCache ={}

    #--- (end of YTemperature definitions)

    #--- (YTemperature implementation)

    def __init__(self,func):
        super(YTemperature,self).__init__("Temperature", func)
        self._callback = None
        self._logicalName = YTemperature.LOGICALNAME_INVALID
        self._advertisedValue = YTemperature.ADVERTISEDVALUE_INVALID
        self._unit = YTemperature.UNIT_INVALID
        self._currentValue = YTemperature.CURRENTVALUE_INVALID
        self._lowestValue = YTemperature.LOWESTVALUE_INVALID
        self._highestValue = YTemperature.HIGHESTVALUE_INVALID
        self._currentRawValue = YTemperature.CURRENTRAWVALUE_INVALID
        self._calibrationParam = YTemperature.CALIBRATIONPARAM_INVALID
        self._resolution = YTemperature.RESOLUTION_INVALID
        self._sensorType = YTemperature.SENSORTYPE_INVALID
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
                self._currentValue = round(member.ivalue/6553.6) / 10
            elif member.name == "lowestValue":
                self._lowestValue = round(member.ivalue/6553.6) / 10
            elif member.name == "highestValue":
                self._highestValue = round(member.ivalue/6553.6) / 10
            elif member.name == "currentRawValue":
                self._currentRawValue = member.ivalue/65536.0
            elif member.name == "calibrationParam":
                self._calibrationParam = member.svalue
            elif member.name == "resolution":
                self._resolution = 1.0 / round(65536.0/member.ivalue) if member.ivalue > 100 else 0.001 / round(67.0/member.ivalue)
            elif member.name == "sensorType":
                self._sensorType = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the temperature sensor.
        
        @return a string corresponding to the logical name of the temperature sensor
        
        On failure, throws an exception or returns YTemperature.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the temperature sensor. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the temperature sensor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the temperature sensor (no more than 6 characters).
        
        @return a string corresponding to the current value of the temperature sensor (no more than 6 characters)
        
        On failure, throws an exception or returns YTemperature.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_unit(self):
        """
        Returns the measuring unit for the measured value.
        
        @return a string corresponding to the measuring unit for the measured value
        
        On failure, throws an exception or returns YTemperature.UNIT_INVALID.
        """
        if self._unit == YTemperature.UNIT_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.UNIT_INVALID
        return self._unit

    def get_currentValue(self):
        """
        Returns the current measured value.
        
        @return a floating point number corresponding to the current measured value
        
        On failure, throws an exception or returns YTemperature.CURRENTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.CURRENTVALUE_INVALID
        res = YAPI._applyCalibration(self._currentRawValue, self._calibrationParam, self._calibrationOffset, self._resolution)
        if res != YTemperature.CURRENTVALUE_INVALID:
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
        
        On failure, throws an exception or returns YTemperature.LOWESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.LOWESTVALUE_INVALID
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
        
        On failure, throws an exception or returns YTemperature.HIGHESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.HIGHESTVALUE_INVALID
        return self._highestValue

    def get_currentRawValue(self):
        """
        Returns the uncalibrated, unrounded raw value returned by the sensor.
        
        @return a floating point number corresponding to the uncalibrated, unrounded raw value returned by the sensor
        
        On failure, throws an exception or returns YTemperature.CURRENTRAWVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.CURRENTRAWVALUE_INVALID
        return self._currentRawValue

    def get_calibrationParam(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.CALIBRATIONPARAM_INVALID
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
        perform a linear interpolation of the error correction between specified
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

    def get_resolution(self):
        """
        Returns the resolution of the measured values. The resolution corresponds to the numerical precision
        of the values, which is not always the same as the actual precision of the sensor.
        
        @return a floating point number corresponding to the resolution of the measured values
        
        On failure, throws an exception or returns YTemperature.RESOLUTION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.RESOLUTION_INVALID
        return self._resolution

    def get_sensorType(self):
        """
        Returns the temperature sensor type.
        
        @return a value among YTemperature.SENSORTYPE_DIGITAL, YTemperature.SENSORTYPE_TYPE_K,
        YTemperature.SENSORTYPE_TYPE_E, YTemperature.SENSORTYPE_TYPE_J, YTemperature.SENSORTYPE_TYPE_N,
        YTemperature.SENSORTYPE_TYPE_R, YTemperature.SENSORTYPE_TYPE_S, YTemperature.SENSORTYPE_TYPE_T,
        YTemperature.SENSORTYPE_PT100_4WIRES, YTemperature.SENSORTYPE_PT100_3WIRES and
        YTemperature.SENSORTYPE_PT100_2WIRES corresponding to the temperature sensor type
        
        On failure, throws an exception or returns YTemperature.SENSORTYPE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YTemperature.SENSORTYPE_INVALID
        return self._sensorType

    def set_sensorType(self, newval):
        """
        Modify the temperature sensor type.  This function is used to
        to define the type of thermocouple (K,E...) used with the device.
        This will have no effect if module is using a digital sensor.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a value among YTemperature.SENSORTYPE_DIGITAL, YTemperature.SENSORTYPE_TYPE_K,
        YTemperature.SENSORTYPE_TYPE_E, YTemperature.SENSORTYPE_TYPE_J, YTemperature.SENSORTYPE_TYPE_N,
        YTemperature.SENSORTYPE_TYPE_R, YTemperature.SENSORTYPE_TYPE_S, YTemperature.SENSORTYPE_TYPE_T,
        YTemperature.SENSORTYPE_PT100_4WIRES, YTemperature.SENSORTYPE_PT100_3WIRES and
        YTemperature.SENSORTYPE_PT100_2WIRES
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("sensorType", rest_val)


    def nextTemperature(self):
        """
        Continues the enumeration of temperature sensors started using yFirstTemperature().
        
        @return a pointer to a YTemperature object, corresponding to
                a temperature sensor currently online, or a None pointer
                if there are no more temperature sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YTemperature.FindTemperature(hwidRef.value)

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

#--- (end of YTemperature implementation)

#--- (Temperature functions)

    @staticmethod 
    def FindTemperature(func):
        """
        Retrieves a temperature sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the temperature sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YTemperature.isOnline() to test if the temperature sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a temperature sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the temperature sensor
        
        @return a YTemperature object allowing you to drive the temperature sensor.
        """
        if func in YTemperature._TemperatureCache:
            return YTemperature._TemperatureCache[func]
        res =YTemperature(func)
        YTemperature._TemperatureCache[func] =  res
        return res

    @staticmethod 
    def  FirstTemperature():
        """
        Starts the enumeration of temperature sensors currently accessible.
        Use the method YTemperature.nextTemperature() to iterate on
        next temperature sensors.
        
        @return a pointer to a YTemperature object, corresponding to
                the first temperature sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Temperature", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YTemperature.FindTemperature(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _TemperatureCleanup():
        pass

  #--- (end of Temperature functions)

