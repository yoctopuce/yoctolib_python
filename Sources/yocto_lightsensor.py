#*********************************************************************
#*
#* $Id: yocto_lightsensor.py 14227 2014-01-02 14:47:46Z seb $
#*
#* Implements yFindLightSensor(), the high-level API for LightSensor functions
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


#--- (YLightSensor class start)
#noinspection PyProtectedMember
class YLightSensor(YSensor):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of YLightSensor class start)
    #--- (YLightSensor return codes)
    #--- (end of YLightSensor return codes)
    #--- (YLightSensor definitions)
    #--- (end of YLightSensor definitions)

    def __init__(self, func):
        super(YLightSensor, self).__init__(func)
        self._className = 'LightSensor'
        #--- (YLightSensor attributes)
        self._callback = None
        #--- (end of YLightSensor attributes)

    #--- (YLightSensor implementation)
    def _parseAttr(self, member):
        super(YLightSensor, self)._parseAttr(member)

    def set_currentValue(self, newval):
        rest_val = str(round(newval * 65536.0, 1))
        return self._setAttr("currentValue", rest_val)

    def calibrate(self, calibratedVal):
        """
        Changes the sensor-specific calibration parameter so that the current value
        matches a desired target (linear scaling).
        
        @param calibratedVal : the desired target value.
        
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(calibratedVal * 65536.0, 1))
        return self._setAttr("currentValue", rest_val)

    @staticmethod
    def FindLightSensor(func):
        """
        Retrieves a light sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the light sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YLightSensor.isOnline() to test if the light sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a light sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the light sensor
        
        @return a YLightSensor object allowing you to drive the light sensor.
        """
        # obj
        obj = YFunction._FindFromCache("LightSensor", func)
        if obj is None:
            obj = YLightSensor(func)
            YFunction._AddToCache("LightSensor", func, obj)
        return obj

    def nextLightSensor(self):
        """
        Continues the enumeration of light sensors started using yFirstLightSensor().
        
        @return a pointer to a YLightSensor object, corresponding to
                a light sensor currently online, or a None pointer
                if there are no more light sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YLightSensor.FindLightSensor(hwidRef.value)

#--- (end of YLightSensor implementation)

#--- (LightSensor functions)

    @staticmethod
    def FirstLightSensor():
        """
        Starts the enumeration of light sensors currently accessible.
        Use the method YLightSensor.nextLightSensor() to iterate on
        next light sensors.
        
        @return a pointer to a YLightSensor object, corresponding to
                the first light sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("LightSensor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YLightSensor.FindLightSensor(serialRef.value + "." + funcIdRef.value)

#--- (end of LightSensor functions)
