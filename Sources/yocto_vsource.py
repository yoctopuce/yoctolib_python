#*********************************************************************
#*
#* $Id: yocto_vsource.py 10263 2013-03-11 17:25:38Z seb $
#*
#* Implements yFindVSource(), the high-level API for VSource functions
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
class YVSource(YFunction):
    """
    Yoctopuce application programming interface allows you to control
    the module voltage output. You affect absolute output values or make
    transitions
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YVSource definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    UNIT_INVALID                    = YAPI.INVALID_STRING
    VOLTAGE_INVALID                 = YAPI.INVALID_LONG
    MOVE_INVALID                    = None
    PULSETIMER_INVALID              = None

    FAILURE_FALSE                   = 0
    FAILURE_TRUE                    = 1
    FAILURE_INVALID                 = -1
    OVERHEAT_FALSE                  = 0
    OVERHEAT_TRUE                   = 1
    OVERHEAT_INVALID                = -1
    OVERCURRENT_FALSE               = 0
    OVERCURRENT_TRUE                = 1
    OVERCURRENT_INVALID             = -1
    OVERLOAD_FALSE                  = 0
    OVERLOAD_TRUE                   = 1
    OVERLOAD_INVALID                = -1
    REGULATIONFAILURE_FALSE         = 0
    REGULATIONFAILURE_TRUE          = 1
    REGULATIONFAILURE_INVALID       = -1
    EXTPOWERFAILURE_FALSE           = 0
    EXTPOWERFAILURE_TRUE            = 1
    EXTPOWERFAILURE_INVALID         = -1


    _VSourceCache ={}

    #--- (end of YVSource definitions)

    #--- (YVSource implementation)

    def __init__(self,func):
        super(YVSource,self).__init__("VSource", func)
        #--- (YVSource implementation)
        self._callback = None
        self._logicalName = YVSource.LOGICALNAME_INVALID
        self._advertisedValue = YVSource.ADVERTISEDVALUE_INVALID
        self._unit = YVSource.UNIT_INVALID
        self._voltage = YVSource.VOLTAGE_INVALID
        self._failure = YVSource.FAILURE_INVALID
        self._overHeat = YVSource.OVERHEAT_INVALID
        self._overCurrent = YVSource.OVERCURRENT_INVALID
        self._overLoad = YVSource.OVERLOAD_INVALID
        self._regulationFailure = YVSource.REGULATIONFAILURE_INVALID
        self._extPowerFailure = YVSource.EXTPOWERFAILURE_INVALID
        self._move = YVSource.MOVE_INVALID
        self._pulseTimer = YVSource.PULSETIMER_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "unit":
                self._unit = member.svalue
            elif member.name == "voltage":
                self._voltage = member.ivalue
            elif member.name == "failure":
                self._failure = member.ivalue
            elif member.name == "overHeat":
                self._overHeat = member.ivalue
            elif member.name == "overCurrent":
                self._overCurrent = member.ivalue
            elif member.name == "overLoad":
                self._overLoad = member.ivalue
            elif member.name == "regulationFailure":
                self._regulationFailure = member.ivalue
            elif member.name == "extPowerFailure":
                self._extPowerFailure = member.ivalue
            elif member.name == "move":
                if member.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: self._move = -1
                self._move = {"moving":None,"target":None,"ms":None }
                for submemb in member.members:
                    if submemb.name == "moving":
                        self._move["moving"]  = submemb.ivalue
                    elif submemb.name == "target": 
                        self._move["target"] = submemb.ivalue
                    elif submemb.name == "ms": 
                        self._move["ms"] = submemb.ivalue
            elif member.name == "pulseTimer":
                if member.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: self._pulseTimer = -1
                self._pulseTimer = {"moving":None,"target":None,"ms":None }
                for submemb in member.members:
                    if submemb.name == "moving":
                        self._pulseTimer["moving"]  = submemb.ivalue
                    elif submemb.name == "target": 
                        self._pulseTimer["target"] = submemb.ivalue
                    elif submemb.name == "ms": 
                        self._pulseTimer["ms"] = submemb.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the voltage source.
        
        @return a string corresponding to the logical name of the voltage source
        
        On failure, throws an exception or returns YVSource.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the voltage source. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the voltage source
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the voltage source (no more than 6 characters).
        
        @return a string corresponding to the current value of the voltage source (no more than 6 characters)
        
        On failure, throws an exception or returns YVSource.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_unit(self):
        """
        Returns the measuring unit for the voltage.
        
        @return a string corresponding to the measuring unit for the voltage
        
        On failure, throws an exception or returns YVSource.UNIT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.UNIT_INVALID
        return self._unit

    def get_voltage(self):
        """
        Returns the voltage output command (mV)
        
        @return an integer corresponding to the voltage output command (mV)
        
        On failure, throws an exception or returns YVSource.VOLTAGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.VOLTAGE_INVALID
        return self._voltage

    def set_voltage(self, newval):
        """
        Tunes the device output voltage (milliVolts).
        
        @param newval : an integer
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("voltage", rest_val)


    def get_failure(self):
        """
        Returns true if the  module is in failure mode. More information can be obtained by testing
        get_overheat, get_overcurrent etc... When a error condition is met, the output voltage is
        set to zéro and cannot be changed until the reset() function is called.
        
        @return either YVSource.FAILURE_FALSE or YVSource.FAILURE_TRUE, according to true if the  module is
        in failure mode
        
        On failure, throws an exception or returns YVSource.FAILURE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.FAILURE_INVALID
        return self._failure

    def set_failure(self, newval):
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("failure", rest_val)


    def get_overHeat(self):
        """
        Returns TRUE if the  module is overheating.
        
        @return either YVSource.OVERHEAT_FALSE or YVSource.OVERHEAT_TRUE, according to TRUE if the  module
        is overheating
        
        On failure, throws an exception or returns YVSource.OVERHEAT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.OVERHEAT_INVALID
        return self._overHeat

    def get_overCurrent(self):
        """
        Returns true if the appliance connected to the device is too greedy .
        
        @return either YVSource.OVERCURRENT_FALSE or YVSource.OVERCURRENT_TRUE, according to true if the
        appliance connected to the device is too greedy
        
        On failure, throws an exception or returns YVSource.OVERCURRENT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.OVERCURRENT_INVALID
        return self._overCurrent

    def get_overLoad(self):
        """
        Returns true if the device is not able to maintaint the requested voltage output  .
        
        @return either YVSource.OVERLOAD_FALSE or YVSource.OVERLOAD_TRUE, according to true if the device
        is not able to maintaint the requested voltage output
        
        On failure, throws an exception or returns YVSource.OVERLOAD_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.OVERLOAD_INVALID
        return self._overLoad

    def get_regulationFailure(self):
        """
        Returns true if the voltage output is too high regarding the requested voltage  .
        
        @return either YVSource.REGULATIONFAILURE_FALSE or YVSource.REGULATIONFAILURE_TRUE, according to
        true if the voltage output is too high regarding the requested voltage
        
        On failure, throws an exception or returns YVSource.REGULATIONFAILURE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.REGULATIONFAILURE_INVALID
        return self._regulationFailure

    def get_extPowerFailure(self):
        """
        Returns true if external power supply voltage is too low.
        
        @return either YVSource.EXTPOWERFAILURE_FALSE or YVSource.EXTPOWERFAILURE_TRUE, according to true
        if external power supply voltage is too low
        
        On failure, throws an exception or returns YVSource.EXTPOWERFAILURE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.EXTPOWERFAILURE_INVALID
        return self._extPowerFailure

    def get_move(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.MOVE_INVALID
        return self._move

    def set_move(self, newval):
        rest_val = str(newval.target)+":"+str(newval.ms)
        return self._setAttr("move", rest_val)


    def voltageMove(self , target,ms_duration):
        """
        Performs a smooth move at constant speed toward a given value.
        
        @param target      : new output value at end of transition, in milliVolts.
        @param ms_duration : transition duration, in milliseconds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(target)+":"+str(ms_duration)
        return self._setAttr("move", rest_val)

    def get_pulseTimer(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YVSource.PULSETIMER_INVALID
        return self._pulseTimer

    def set_pulseTimer(self, newval):
        rest_val = str(newval.target)+":"+str(newval.ms)
        return self._setAttr("pulseTimer", rest_val)


    def pulse(self , voltage,ms_duration):
        """
        Sets device output to a specific volatage, for a specified duration, then brings it
        automatically to 0V.
        
        @param voltage : pulse voltage, in millivolts
        @param ms_duration : pulse duration, in millisecondes
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(voltage)+":"+str(ms_duration)
        return self._setAttr("pulseTimer", rest_val)

    def nextVSource(self):
        """
        Continues the enumeration of voltage sources started using yFirstVSource().
        
        @return a pointer to a YVSource object, corresponding to
                a voltage source currently online, or a None pointer
                if there are no more voltage sources to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YVSource.FindVSource(hwidRef.value)

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

#--- (end of YVSource implementation)

#--- (VSource functions)

    @staticmethod 
    def FindVSource(func):
        """
        Retrieves a voltage source for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the voltage source is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YVSource.isOnline() to test if the voltage source is
        indeed online at a given time. In case of ambiguity when looking for
        a voltage source by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the voltage source
        
        @return a YVSource object allowing you to drive the voltage source.
        """
        if func in YVSource._VSourceCache:
            return YVSource._VSourceCache[func]
        res =YVSource(func)
        YVSource._VSourceCache[func] =  res
        return res

    @staticmethod 
    def  FirstVSource():
        """
        Starts the enumeration of voltage sources currently accessible.
        Use the method YVSource.nextVSource() to iterate on
        next voltage sources.
        
        @return a pointer to a YVSource object, corresponding to
                the first voltage source currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("VSource", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YVSource.FindVSource(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _VSourceCleanup():
        pass

  #--- (end of VSource functions)

