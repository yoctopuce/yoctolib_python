#*********************************************************************
#*
#* $Id: yocto_tilt.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindTilt(), the high-level API for Tilt functions
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


#--- (YTilt class start)
#noinspection PyProtectedMember
class YTilt(YSensor):
    """
    The YSensor class is the parent class for all Yoctopuce sensors. It can be
    used to read the current value and unit of any sensor, read the min/max
    value, configure autonomous recording frequency and access recorded data.
    It also provide a function to register a callback invoked each time the
    observed value changes, or at a predefined interval. Using this class rather
    than a specific subclass makes it possible to create generic applications
    that work with any Yoctopuce sensor, even those that do not yet exist.
    Note: The YAnButton class is the only analog input which does not inherit
    from YSensor.

    """
#--- (end of YTilt class start)
    #--- (YTilt return codes)
    #--- (end of YTilt return codes)
    #--- (YTilt dlldef)
    #--- (end of YTilt dlldef)
    #--- (YTilt definitions)
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2
    AXIS_INVALID = -1
    #--- (end of YTilt definitions)

    def __init__(self, func):
        super(YTilt, self).__init__(func)
        self._className = 'Tilt'
        #--- (YTilt attributes)
        self._callback = None
        self._axis = YTilt.AXIS_INVALID
        #--- (end of YTilt attributes)

    #--- (YTilt implementation)
    def _parseAttr(self, member):
        if member.name == "axis":
            self._axis = member.ivalue
            return 1
        super(YTilt, self)._parseAttr(member)

    def get_axis(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YTilt.AXIS_INVALID
        return self._axis

    @staticmethod
    def FindTilt(func):
        """
        Retrieves a tilt sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the tilt sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YTilt.isOnline() to test if the tilt sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a tilt sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the tilt sensor

        @return a YTilt object allowing you to drive the tilt sensor.
        """
        # obj
        obj = YFunction._FindFromCache("Tilt", func)
        if obj is None:
            obj = YTilt(func)
            YFunction._AddToCache("Tilt", func, obj)
        return obj

    def nextTilt(self):
        """
        Continues the enumeration of tilt sensors started using yFirstTilt().

        @return a pointer to a YTilt object, corresponding to
                a tilt sensor currently online, or a None pointer
                if there are no more tilt sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YTilt.FindTilt(hwidRef.value)

#--- (end of YTilt implementation)

#--- (Tilt functions)

    @staticmethod
    def FirstTilt():
        """
        Starts the enumeration of tilt sensors currently accessible.
        Use the method YTilt.nextTilt() to iterate on
        next tilt sensors.

        @return a pointer to a YTilt object, corresponding to
                the first tilt sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Tilt", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YTilt.FindTilt(serialRef.value + "." + funcIdRef.value)

#--- (end of Tilt functions)
