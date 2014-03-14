#*********************************************************************
#*
#* $Id: yocto_power.py 14275 2014-01-09 14:20:38Z seb $
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


#--- (YPower class start)
#noinspection PyProtectedMember
class YPower(YSensor):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of YPower class start)
    #--- (YPower return codes)
    #--- (end of YPower return codes)
    #--- (YPower definitions)
    COSPHI_INVALID = YAPI.INVALID_DOUBLE
    METER_INVALID = YAPI.INVALID_DOUBLE
    METERTIMER_INVALID = YAPI.INVALID_UINT
    #--- (end of YPower definitions)

    def __init__(self, func):
        super(YPower, self).__init__(func)
        self._className = 'Power'
        #--- (YPower attributes)
        self._callback = None
        self._cosPhi = YPower.COSPHI_INVALID
        self._meter = YPower.METER_INVALID
        self._meterTimer = YPower.METERTIMER_INVALID
        #--- (end of YPower attributes)

    #--- (YPower implementation)
    def _parseAttr(self, member):
        if member.name == "cosPhi":
            self._cosPhi = member.ivalue / 65536.0
            return 1
        if member.name == "meter":
            self._meter = member.ivalue / 65536.0
            return 1
        if member.name == "meterTimer":
            self._meterTimer = member.ivalue
            return 1
        super(YPower, self)._parseAttr(member)

    def get_cosPhi(self):
        """
        Returns the power factor (the ratio between the real power consumed,
        measured in W, and the apparent power provided, measured in VA).
        
        @return a floating point number corresponding to the power factor (the ratio between the real power consumed,
                measured in W, and the apparent power provided, measured in VA)
        
        On failure, throws an exception or returns YPower.COSPHI_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPower.COSPHI_INVALID
        return self._cosPhi

    def set_meter(self, newval):
        rest_val = str(round(newval * 65536.0, 1))
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
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPower.METER_INVALID
        return self._meter

    def get_meterTimer(self):
        """
        Returns the elapsed time since last energy counter reset, in seconds.
        
        @return an integer corresponding to the elapsed time since last energy counter reset, in seconds
        
        On failure, throws an exception or returns YPower.METERTIMER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YPower.METERTIMER_INVALID
        return self._meterTimer

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
        # obj
        obj = YFunction._FindFromCache("Power", func)
        if obj is None:
            obj = YPower(func)
            YFunction._AddToCache("Power", func, obj)
        return obj

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

#--- (end of YPower implementation)

#--- (Power functions)

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

#--- (end of Power functions)
