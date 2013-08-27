#*********************************************************************
#*
#* $Id: yocto_power.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindPower(), the high-level API for Power functions
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
class YPower(YFunction):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YPower definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    UNIT_INVALID                    = YAPI.INVALID_STRING
    CURRENTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    LOWESTVALUE_INVALID             = YAPI.INVALID_DOUBLE
    HIGHESTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    CURRENTRAWVALUE_INVALID         = YAPI.INVALID_DOUBLE
    CALIBRATIONPARAM_INVALID        = YAPI.INVALID_STRING
    RESOLUTION_INVALID              = YAPI.INVALID_DOUBLE
    COSPHI_INVALID                  = YAPI.INVALID_DOUBLE
    METER_INVALID                   = YAPI.INVALID_DOUBLE
    METERTIMER_INVALID              = YAPI.INVALID_LONG
    CALIBRATIONOFFSET_INVALID       = YAPI.INVALID_LONG



    _PowerCache ={}

    #--- (end of YPower definitions)

    #--- (YPower implementation)

    def __init__(self,func):
        super(YPower,self).__init__("Power", func)
        self._callback = None
        self._logicalName = YPower.LOGICALNAME_INVALID
        self._advertisedValue = YPower.ADVERTISEDVALUE_INVALID
        self._unit = YPower.UNIT_INVALID
        self._currentValue = YPower.CURRENTVALUE_INVALID
        self._lowestValue = YPower.LOWESTVALUE_INVALID
        self._highestValue = YPower.HIGHESTVALUE_INVALID
        self._currentRawValue = YPower.CURRENTRAWVALUE_INVALID
        self._calibrationParam = YPower.CALIBRATIONPARAM_INVALID
        self._resolution = YPower.RESOLUTION_INVALID
        self._cosPhi = YPower.COSPHI_INVALID
        self._meter = YPower.METER_INVALID
        self._meterTimer = YPower.METERTIMER_INVALID
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
                self._currentValue = round(member.ivalue/65.536) / 1000
            elif member.name == "lowestValue":
                self._lowestValue = round(member.ivalue/65.536) / 1000
            elif member.name == "highestValue":
                self._highestValue = round(member.ivalue/65.536) / 1000
            elif member.name == "currentRawValue":
                self._currentRawValue = member.ivalue/65536.0
            elif member.name == "calibrationParam":
                self._calibrationParam = member.svalue
            elif member.name == "resolution":
                self._resolution = 1.0 / round(65536.0/member.ivalue) if member.ivalue > 100 else 0.001 / round(67.0/member.ivalue)
            elif member.name == "cosPhi":
                self._cosPhi = round(member.ivalue/655.36) / 100
            elif member.name == "meter":
                self._meter = round(member.ivalue/65.536) / 1000
            elif member.name == "meterTimer":
                self._meterTimer = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the electrical power sensor.
        
        @return a string corresponding to the logical name of the electrical power sensor
        
        On failure, throws an exception or returns YPower.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the electrical power sensor. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the electrical power sensor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the electrical power sensor (no more than 6 characters).
        
        @return a string corresponding to the current value of the electrical power sensor (no more than 6 characters)
        
        On failure, throws an exception or returns YPower.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_unit(self):
        """
        Returns the measuring unit for the measured value.
        
        @return a string corresponding to the measuring unit for the measured value
        
        On failure, throws an exception or returns YPower.UNIT_INVALID.
        """
        if self._unit == YPower.UNIT_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.UNIT_INVALID
        return self._unit

    def get_currentValue(self):
        """
        Returns the current measured value.
        
        @return a floating point number corresponding to the current measured value
        
        On failure, throws an exception or returns YPower.CURRENTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.CURRENTVALUE_INVALID
        res = YAPI._applyCalibration(self._currentRawValue, self._calibrationParam, self._calibrationOffset, self._resolution)
        if res != YPower.CURRENTVALUE_INVALID:
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
        
        On failure, throws an exception or returns YPower.LOWESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.LOWESTVALUE_INVALID
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
        
        On failure, throws an exception or returns YPower.HIGHESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.HIGHESTVALUE_INVALID
        return self._highestValue

    def get_currentRawValue(self):
        """
        Returns the uncalibrated, unrounded raw value returned by the sensor.
        
        @return a floating point number corresponding to the uncalibrated, unrounded raw value returned by the sensor
        
        On failure, throws an exception or returns YPower.CURRENTRAWVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.CURRENTRAWVALUE_INVALID
        return self._currentRawValue

    def get_calibrationParam(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.CALIBRATIONPARAM_INVALID
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

    def set_resolution(self, newval):
        """
        Changes the resolution of the measured values. The resolution corresponds to the numerical precision
        when displaying value. It does not change the precision of the measure itself.
        
        @param newval : a floating point number corresponding to the resolution of the measured values
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("resolution", rest_val)


    def get_resolution(self):
        """
        Returns the resolution of the measured values. The resolution corresponds to the numerical precision
        when displaying value, which is not always the same as the actual precision of the sensor.
        
        @return a floating point number corresponding to the resolution of the measured values
        
        On failure, throws an exception or returns YPower.RESOLUTION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.RESOLUTION_INVALID
        return self._resolution

    def get_cosPhi(self):
        """
        Returns the power factor (the ratio between the real power consumed,
        measured in W, and the apparent power provided, measured in VA).
        
        @return a floating point number corresponding to the power factor (the ratio between the real power consumed,
                measured in W, and the apparent power provided, measured in VA)
        
        On failure, throws an exception or returns YPower.COSPHI_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.COSPHI_INVALID
        return self._cosPhi

    def set_meter(self, newval):
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("meter", rest_val)


    def get_meter(self):
        """
        Returns the energy counter, maintained by the wattmeter by integrating the power consumption over time.
        Note that this counter is reset at each start of the device.
        
        @return a floating point number corresponding to the energy counter, maintained by the wattmeter by
        integrating the power consumption over time
        
        On failure, throws an exception or returns YPower.METER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.METER_INVALID
        return self._meter

    def get_meterTimer(self):
        """
        Returns the elapsed time since last energy counter reset, in seconds.
        
        @return an integer corresponding to the elapsed time since last energy counter reset, in seconds
        
        On failure, throws an exception or returns YPower.METERTIMER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.METERTIMER_INVALID
        return self._meterTimer

    def nextPower(self):
        """
        Continues the enumeration of electrical power sensors started using yFirstPower().
        
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

#--- (end of YPower implementation)

#--- (Power functions)

    @staticmethod 
    def FindPower(func):
        """
        Retrieves a electrical power sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the electrical power sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPower.isOnline() to test if the electrical power sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a electrical power sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the electrical power sensor
        
        @return a YPower object allowing you to drive the electrical power sensor.
        """
        if func in YPower._PowerCache:
            return YPower._PowerCache[func]
        res =YPower(func)
        YPower._PowerCache[func] =  res
        return res

    @staticmethod 
    def  FirstPower():
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
        p = (ctypes.c_int*1)()
        err = YAPI.apiGetFunctionsByClass("Power", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YPower.FindPower(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _PowerCleanup():
        pass

  #--- (end of Power functions)

