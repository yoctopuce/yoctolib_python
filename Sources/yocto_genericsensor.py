#*********************************************************************
#*
#* $Id: yocto_genericsensor.py 15257 2014-03-06 10:19:36Z seb $
#*
#* Implements yFindGenericSensor(), the high-level API for GenericSensor functions
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


#--- (YGenericSensor class start)
#noinspection PyProtectedMember
class YGenericSensor(YSensor):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of YGenericSensor class start)
    #--- (YGenericSensor return codes)
    #--- (end of YGenericSensor return codes)
    #--- (YGenericSensor definitions)
    SIGNALVALUE_INVALID = YAPI.INVALID_DOUBLE
    SIGNALUNIT_INVALID = YAPI.INVALID_STRING
    SIGNALRANGE_INVALID = YAPI.INVALID_STRING
    VALUERANGE_INVALID = YAPI.INVALID_STRING
    #--- (end of YGenericSensor definitions)

    def __init__(self, func):
        super(YGenericSensor, self).__init__(func)
        self._className = 'GenericSensor'
        #--- (YGenericSensor attributes)
        self._callback = None
        self._signalValue = YGenericSensor.SIGNALVALUE_INVALID
        self._signalUnit = YGenericSensor.SIGNALUNIT_INVALID
        self._signalRange = YGenericSensor.SIGNALRANGE_INVALID
        self._valueRange = YGenericSensor.VALUERANGE_INVALID
        #--- (end of YGenericSensor attributes)

    #--- (YGenericSensor implementation)
    def _parseAttr(self, member):
        if member.name == "signalValue":
            self._signalValue = member.ivalue / 65536.0
            return 1
        if member.name == "signalUnit":
            self._signalUnit = member.svalue
            return 1
        if member.name == "signalRange":
            self._signalRange = member.svalue
            return 1
        if member.name == "valueRange":
            self._valueRange = member.svalue
            return 1
        super(YGenericSensor, self)._parseAttr(member)

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

    def get_signalValue(self):
        """
        Returns the measured value of the electrical signal used by the sensor.
        
        @return a floating point number corresponding to the measured value of the electrical signal used by the sensor
        
        On failure, throws an exception or returns YGenericSensor.SIGNALVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGenericSensor.SIGNALVALUE_INVALID
        return round(self._signalValue * 1000) / 1000

    def get_signalUnit(self):
        """
        Returns the measuring unit of the electrical signal used by the sensor.
        
        @return a string corresponding to the measuring unit of the electrical signal used by the sensor
        
        On failure, throws an exception or returns YGenericSensor.SIGNALUNIT_INVALID.
        """
        if self._cacheExpiration == datetime.datetime.fromtimestamp(0):
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGenericSensor.SIGNALUNIT_INVALID
        return self._signalUnit

    def get_signalRange(self):
        """
        Returns the electric signal range used by the sensor.
        
        @return a string corresponding to the electric signal range used by the sensor
        
        On failure, throws an exception or returns YGenericSensor.SIGNALRANGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGenericSensor.SIGNALRANGE_INVALID
        return self._signalRange

    def set_signalRange(self, newval):
        """
        Changes the electric signal range used by the sensor.
        
        @param newval : a string corresponding to the electric signal range used by the sensor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("signalRange", rest_val)

    def get_valueRange(self):
        """
        Returns the physical value range measured by the sensor.
        
        @return a string corresponding to the physical value range measured by the sensor
        
        On failure, throws an exception or returns YGenericSensor.VALUERANGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YGenericSensor.VALUERANGE_INVALID
        return self._valueRange

    def set_valueRange(self, newval):
        """
        Changes the physical value range measured by the sensor. The range change may have a side effect
        on the display resolution, as it may be adapted automatically.
        
        @param newval : a string corresponding to the physical value range measured by the sensor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("valueRange", rest_val)

    @staticmethod
    def FindGenericSensor(func):
        """
        Retrieves a generic sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the generic sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YGenericSensor.isOnline() to test if the generic sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a generic sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the generic sensor
        
        @return a YGenericSensor object allowing you to drive the generic sensor.
        """
        # obj
        obj = YFunction._FindFromCache("GenericSensor", func)
        if obj is None:
            obj = YGenericSensor(func)
            YFunction._AddToCache("GenericSensor", func, obj)
        return obj

    def nextGenericSensor(self):
        """
        Continues the enumeration of generic sensors started using yFirstGenericSensor().
        
        @return a pointer to a YGenericSensor object, corresponding to
                a generic sensor currently online, or a None pointer
                if there are no more generic sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YGenericSensor.FindGenericSensor(hwidRef.value)

#--- (end of YGenericSensor implementation)

#--- (GenericSensor functions)

    @staticmethod
    def FirstGenericSensor():
        """
        Starts the enumeration of generic sensors currently accessible.
        Use the method YGenericSensor.nextGenericSensor() to iterate on
        next generic sensors.
        
        @return a pointer to a YGenericSensor object, corresponding to
                the first generic sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("GenericSensor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YGenericSensor.FindGenericSensor(serialRef.value + "." + funcIdRef.value)

#--- (end of GenericSensor functions)
