#*********************************************************************
#*
#* $Id: yocto_anbutton.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindAnButton(), the high-level API for AnButton functions
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
class YAnButton(YFunction):
    """
    Yoctopuce application programming interface allows you to measure the state
    of a simple button as well as to read an analog potentiometer (variable resistance).
    This can be use for instance with a continuous rotating knob, a throttle grip
    or a joystick. The module is capable to calibrate itself on min and max values,
    in order to compute a calibrated value that varies proportionally with the
    potentiometer position, regardless of its total resistance.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YAnButton definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    CALIBRATEDVALUE_INVALID         = YAPI.INVALID_LONG
    RAWVALUE_INVALID                = YAPI.INVALID_LONG
    CALIBRATIONMAX_INVALID          = YAPI.INVALID_LONG
    CALIBRATIONMIN_INVALID          = YAPI.INVALID_LONG
    SENSITIVITY_INVALID             = YAPI.INVALID_LONG
    LASTTIMEPRESSED_INVALID         = YAPI.INVALID_LONG
    LASTTIMERELEASED_INVALID        = YAPI.INVALID_LONG
    PULSECOUNTER_INVALID            = YAPI.INVALID_LONG
    PULSETIMER_INVALID              = YAPI.INVALID_LONG

    ANALOGCALIBRATION_OFF           = 0
    ANALOGCALIBRATION_ON            = 1
    ANALOGCALIBRATION_INVALID       = -1
    ISPRESSED_FALSE                 = 0
    ISPRESSED_TRUE                  = 1
    ISPRESSED_INVALID               = -1


    _AnButtonCache ={}

    #--- (end of YAnButton definitions)

    #--- (YAnButton implementation)

    def __init__(self,func):
        super(YAnButton,self).__init__("AnButton", func)
        self._callback = None
        self._logicalName = YAnButton.LOGICALNAME_INVALID
        self._advertisedValue = YAnButton.ADVERTISEDVALUE_INVALID
        self._calibratedValue = YAnButton.CALIBRATEDVALUE_INVALID
        self._rawValue = YAnButton.RAWVALUE_INVALID
        self._analogCalibration = YAnButton.ANALOGCALIBRATION_INVALID
        self._calibrationMax = YAnButton.CALIBRATIONMAX_INVALID
        self._calibrationMin = YAnButton.CALIBRATIONMIN_INVALID
        self._sensitivity = YAnButton.SENSITIVITY_INVALID
        self._isPressed = YAnButton.ISPRESSED_INVALID
        self._lastTimePressed = YAnButton.LASTTIMEPRESSED_INVALID
        self._lastTimeReleased = YAnButton.LASTTIMERELEASED_INVALID
        self._pulseCounter = YAnButton.PULSECOUNTER_INVALID
        self._pulseTimer = YAnButton.PULSETIMER_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "calibratedValue":
                self._calibratedValue = member.ivalue
            elif member.name == "rawValue":
                self._rawValue = member.ivalue
            elif member.name == "analogCalibration":
                self._analogCalibration = member.ivalue
            elif member.name == "calibrationMax":
                self._calibrationMax = member.ivalue
            elif member.name == "calibrationMin":
                self._calibrationMin = member.ivalue
            elif member.name == "sensitivity":
                self._sensitivity = member.ivalue
            elif member.name == "isPressed":
                self._isPressed = member.ivalue
            elif member.name == "lastTimePressed":
                self._lastTimePressed = member.ivalue
            elif member.name == "lastTimeReleased":
                self._lastTimeReleased = member.ivalue
            elif member.name == "pulseCounter":
                self._pulseCounter = member.ivalue
            elif member.name == "pulseTimer":
                self._pulseTimer = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the analog input.
        
        @return a string corresponding to the logical name of the analog input
        
        On failure, throws an exception or returns YAnButton.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the analog input. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the analog input
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the analog input (no more than 6 characters).
        
        @return a string corresponding to the current value of the analog input (no more than 6 characters)
        
        On failure, throws an exception or returns YAnButton.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_calibratedValue(self):
        """
        Returns the current calibrated input value (between 0 and 1000, included).
        
        @return an integer corresponding to the current calibrated input value (between 0 and 1000, included)
        
        On failure, throws an exception or returns YAnButton.CALIBRATEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.CALIBRATEDVALUE_INVALID
        return self._calibratedValue

    def get_rawValue(self):
        """
        Returns the current measured input value as-is (between 0 and 4095, included).
        
        @return an integer corresponding to the current measured input value as-is (between 0 and 4095, included)
        
        On failure, throws an exception or returns YAnButton.RAWVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.RAWVALUE_INVALID
        return self._rawValue

    def get_analogCalibration(self):
        """
        Tells if a calibration process is currently ongoing.
        
        @return either YAnButton.ANALOGCALIBRATION_OFF or YAnButton.ANALOGCALIBRATION_ON
        
        On failure, throws an exception or returns YAnButton.ANALOGCALIBRATION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.ANALOGCALIBRATION_INVALID
        return self._analogCalibration

    def set_analogCalibration(self, newval):
        """
        Starts or stops the calibration process. Remember to call the saveToFlash()
        method of the module at the end of the calibration if the modification must be kept.
        
        @param newval : either YAnButton.ANALOGCALIBRATION_OFF or YAnButton.ANALOGCALIBRATION_ON
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("analogCalibration", rest_val)


    def get_calibrationMax(self):
        """
        Returns the maximal value measured during the calibration (between 0 and 4095, included).
        
        @return an integer corresponding to the maximal value measured during the calibration (between 0
        and 4095, included)
        
        On failure, throws an exception or returns YAnButton.CALIBRATIONMAX_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.CALIBRATIONMAX_INVALID
        return self._calibrationMax

    def set_calibrationMax(self, newval):
        """
        Changes the maximal calibration value for the input (between 0 and 4095, included), without actually
        starting the automated calibration.  Remember to call the saveToFlash()
        method of the module if the modification must be kept.
        
        @param newval : an integer corresponding to the maximal calibration value for the input (between 0
        and 4095, included), without actually
                starting the automated calibration
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("calibrationMax", rest_val)


    def get_calibrationMin(self):
        """
        Returns the minimal value measured during the calibration (between 0 and 4095, included).
        
        @return an integer corresponding to the minimal value measured during the calibration (between 0
        and 4095, included)
        
        On failure, throws an exception or returns YAnButton.CALIBRATIONMIN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.CALIBRATIONMIN_INVALID
        return self._calibrationMin

    def set_calibrationMin(self, newval):
        """
        Changes the minimal calibration value for the input (between 0 and 4095, included), without actually
        starting the automated calibration.  Remember to call the saveToFlash()
        method of the module if the modification must be kept.
        
        @param newval : an integer corresponding to the minimal calibration value for the input (between 0
        and 4095, included), without actually
                starting the automated calibration
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("calibrationMin", rest_val)


    def get_sensitivity(self):
        """
        Returns the sensibility for the input (between 1 and 1000) for triggering user callbacks.
        
        @return an integer corresponding to the sensibility for the input (between 1 and 1000) for
        triggering user callbacks
        
        On failure, throws an exception or returns YAnButton.SENSITIVITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.SENSITIVITY_INVALID
        return self._sensitivity

    def set_sensitivity(self, newval):
        """
        Changes the sensibility for the input (between 1 and 1000) for triggering user callbacks.
        The sensibility is used to filter variations around a fixed value, but does not preclude the
        transmission of events when the input value evolves constantly in the same direction.
        Special case: when the value 1000 is used, the callback will only be thrown when the logical state
        of the input switches from pressed to released and back.
        Remember to call the saveToFlash() method of the module if the modification must be kept.
        
        @param newval : an integer corresponding to the sensibility for the input (between 1 and 1000) for
        triggering user callbacks
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("sensitivity", rest_val)


    def get_isPressed(self):
        """
        Returns true if the input (considered as binary) is active (closed contact), and false otherwise.
        
        @return either YAnButton.ISPRESSED_FALSE or YAnButton.ISPRESSED_TRUE, according to true if the
        input (considered as binary) is active (closed contact), and false otherwise
        
        On failure, throws an exception or returns YAnButton.ISPRESSED_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.ISPRESSED_INVALID
        return self._isPressed

    def get_lastTimePressed(self):
        """
        Returns the number of elapsed milliseconds between the module power on and the last time
        the input button was pressed (the input contact transitionned from open to closed).
        
        @return an integer corresponding to the number of elapsed milliseconds between the module power on
        and the last time
                the input button was pressed (the input contact transitionned from open to closed)
        
        On failure, throws an exception or returns YAnButton.LASTTIMEPRESSED_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.LASTTIMEPRESSED_INVALID
        return self._lastTimePressed

    def get_lastTimeReleased(self):
        """
        Returns the number of elapsed milliseconds between the module power on and the last time
        the input button was released (the input contact transitionned from closed to open).
        
        @return an integer corresponding to the number of elapsed milliseconds between the module power on
        and the last time
                the input button was released (the input contact transitionned from closed to open)
        
        On failure, throws an exception or returns YAnButton.LASTTIMERELEASED_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.LASTTIMERELEASED_INVALID
        return self._lastTimeReleased

    def get_pulseCounter(self):
        """
        Returns the pulse counter value
        
        @return an integer corresponding to the pulse counter value
        
        On failure, throws an exception or returns YAnButton.PULSECOUNTER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.PULSECOUNTER_INVALID
        return self._pulseCounter

    def set_pulseCounter(self, newval):
        rest_val = str(newval)
        return self._setAttr("pulseCounter", rest_val)


    def resetCounter(self):
        """
        Returns the pulse counter value as well as his timer
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "0"
        return self._setAttr("pulseCounter", rest_val)

    def get_pulseTimer(self):
        """
        Returns the timer of the pulses counter (ms)
        
        @return an integer corresponding to the timer of the pulses counter (ms)
        
        On failure, throws an exception or returns YAnButton.PULSETIMER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YAnButton.PULSETIMER_INVALID
        return self._pulseTimer

    def nextAnButton(self):
        """
        Continues the enumeration of analog inputs started using yFirstAnButton().
        
        @return a pointer to a YAnButton object, corresponding to
                an analog input currently online, or a None pointer
                if there are no more analog inputs to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YAnButton.FindAnButton(hwidRef.value)

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

#--- (end of YAnButton implementation)

#--- (AnButton functions)

    @staticmethod 
    def FindAnButton(func):
        """
        Retrieves an analog input for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the analog input is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YAnButton.isOnline() to test if the analog input is
        indeed online at a given time. In case of ambiguity when looking for
        an analog input by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the analog input
        
        @return a YAnButton object allowing you to drive the analog input.
        """
        if func in YAnButton._AnButtonCache:
            return YAnButton._AnButtonCache[func]
        res =YAnButton(func)
        YAnButton._AnButtonCache[func] =  res
        return res

    @staticmethod 
    def  FirstAnButton():
        """
        Starts the enumeration of analog inputs currently accessible.
        Use the method YAnButton.nextAnButton() to iterate on
        next analog inputs.
        
        @return a pointer to a YAnButton object, corresponding to
                the first analog input currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("AnButton", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YAnButton.FindAnButton(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _AnButtonCleanup():
        pass

  #--- (end of AnButton functions)

