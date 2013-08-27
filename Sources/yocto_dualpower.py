#*********************************************************************
#*
#* $Id: yocto_dualpower.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindDualPower(), the high-level API for DualPower functions
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
class YDualPower(YFunction):
    """
    Yoctopuce application programming interface allows you to control
    the power source to use for module functions that require high current.
    The module can also automatically disconnect the external power
    when a voltage drop is observed on the external power source
    (external battery running out of power).
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YDualPower definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    EXTVOLTAGE_INVALID              = YAPI.INVALID_LONG

    POWERSTATE_OFF                  = 0
    POWERSTATE_FROM_USB             = 1
    POWERSTATE_FROM_EXT             = 2
    POWERSTATE_INVALID              = -1
    POWERCONTROL_AUTO               = 0
    POWERCONTROL_FROM_USB           = 1
    POWERCONTROL_FROM_EXT           = 2
    POWERCONTROL_OFF                = 3
    POWERCONTROL_INVALID            = -1


    _DualPowerCache ={}

    #--- (end of YDualPower definitions)

    #--- (YDualPower implementation)

    def __init__(self,func):
        super(YDualPower,self).__init__("DualPower", func)
        self._callback = None
        self._logicalName = YDualPower.LOGICALNAME_INVALID
        self._advertisedValue = YDualPower.ADVERTISEDVALUE_INVALID
        self._powerState = YDualPower.POWERSTATE_INVALID
        self._powerControl = YDualPower.POWERCONTROL_INVALID
        self._extVoltage = YDualPower.EXTVOLTAGE_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "powerState":
                self._powerState = member.ivalue
            elif member.name == "powerControl":
                self._powerControl = member.ivalue
            elif member.name == "extVoltage":
                self._extVoltage = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the power control.
        
        @return a string corresponding to the logical name of the power control
        
        On failure, throws an exception or returns YDualPower.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDualPower.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the power control. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the power control
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the power control (no more than 6 characters).
        
        @return a string corresponding to the current value of the power control (no more than 6 characters)
        
        On failure, throws an exception or returns YDualPower.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDualPower.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_powerState(self):
        """
        Returns the current power source for module functions that require lots of current.
        
        @return a value among YDualPower.POWERSTATE_OFF, YDualPower.POWERSTATE_FROM_USB and
        YDualPower.POWERSTATE_FROM_EXT corresponding to the current power source for module functions that
        require lots of current
        
        On failure, throws an exception or returns YDualPower.POWERSTATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDualPower.POWERSTATE_INVALID
        return self._powerState

    def get_powerControl(self):
        """
        Returns the selected power source for module functions that require lots of current.
        
        @return a value among YDualPower.POWERCONTROL_AUTO, YDualPower.POWERCONTROL_FROM_USB,
        YDualPower.POWERCONTROL_FROM_EXT and YDualPower.POWERCONTROL_OFF corresponding to the selected
        power source for module functions that require lots of current
        
        On failure, throws an exception or returns YDualPower.POWERCONTROL_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDualPower.POWERCONTROL_INVALID
        return self._powerControl

    def set_powerControl(self, newval):
        """
        Changes the selected power source for module functions that require lots of current.
        
        @param newval : a value among YDualPower.POWERCONTROL_AUTO, YDualPower.POWERCONTROL_FROM_USB,
        YDualPower.POWERCONTROL_FROM_EXT and YDualPower.POWERCONTROL_OFF corresponding to the selected
        power source for module functions that require lots of current
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("powerControl", rest_val)


    def get_extVoltage(self):
        """
        Returns the measured voltage on the external power source, in millivolts.
        
        @return an integer corresponding to the measured voltage on the external power source, in millivolts
        
        On failure, throws an exception or returns YDualPower.EXTVOLTAGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDualPower.EXTVOLTAGE_INVALID
        return self._extVoltage

    def nextDualPower(self):
        """
        Continues the enumeration of dual power controls started using yFirstDualPower().
        
        @return a pointer to a YDualPower object, corresponding to
                a dual power control currently online, or a None pointer
                if there are no more dual power controls to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YDualPower.FindDualPower(hwidRef.value)

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

#--- (end of YDualPower implementation)

#--- (DualPower functions)

    @staticmethod 
    def FindDualPower(func):
        """
        Retrieves a dual power control for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the power control is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YDualPower.isOnline() to test if the power control is
        indeed online at a given time. In case of ambiguity when looking for
        a dual power control by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the power control
        
        @return a YDualPower object allowing you to drive the power control.
        """
        if func in YDualPower._DualPowerCache:
            return YDualPower._DualPowerCache[func]
        res =YDualPower(func)
        YDualPower._DualPowerCache[func] =  res
        return res

    @staticmethod 
    def  FirstDualPower():
        """
        Starts the enumeration of dual power controls currently accessible.
        Use the method YDualPower.nextDualPower() to iterate on
        next dual power controls.
        
        @return a pointer to a YDualPower object, corresponding to
                the first dual power control currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("DualPower", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YDualPower.FindDualPower(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _DualPowerCleanup():
        pass

  #--- (end of DualPower functions)

