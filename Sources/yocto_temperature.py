#*********************************************************************
#*
#* $Id: yocto_temperature.py 17368 2014-08-29 16:46:36Z seb $
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


#--- (YTemperature class start)
#noinspection PyProtectedMember
class YTemperature(YSensor):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of YTemperature class start)
    #--- (YTemperature return codes)
    #--- (end of YTemperature return codes)
    #--- (YTemperature dlldef)
    #--- (end of YTemperature dlldef)
    #--- (YTemperature definitions)
    SENSORTYPE_DIGITAL = 0
    SENSORTYPE_TYPE_K = 1
    SENSORTYPE_TYPE_E = 2
    SENSORTYPE_TYPE_J = 3
    SENSORTYPE_TYPE_N = 4
    SENSORTYPE_TYPE_R = 5
    SENSORTYPE_TYPE_S = 6
    SENSORTYPE_TYPE_T = 7
    SENSORTYPE_PT100_4WIRES = 8
    SENSORTYPE_PT100_3WIRES = 9
    SENSORTYPE_PT100_2WIRES = 10
    SENSORTYPE_INVALID = -1
    #--- (end of YTemperature definitions)

    def __init__(self, func):
        super(YTemperature, self).__init__(func)
        self._className = 'Temperature'
        #--- (YTemperature attributes)
        self._callback = None
        self._sensorType = YTemperature.SENSORTYPE_INVALID
        #--- (end of YTemperature attributes)

    #--- (YTemperature implementation)
    def _parseAttr(self, member):
        if member.name == "sensorType":
            self._sensorType = member.ivalue
            return 1
        super(YTemperature, self)._parseAttr(member)

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
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
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
        # obj
        obj = YFunction._FindFromCache("Temperature", func)
        if obj is None:
            obj = YTemperature(func)
            YFunction._AddToCache("Temperature", func, obj)
        return obj

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

#--- (end of YTemperature implementation)

#--- (Temperature functions)

    @staticmethod
    def FirstTemperature():
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
        p = (ctypes.c_int * 1)()
        err = YAPI.apiGetFunctionsByClass("Temperature", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YTemperature.FindTemperature(serialRef.value + "." + funcIdRef.value)

#--- (end of Temperature functions)
