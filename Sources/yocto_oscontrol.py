#*********************************************************************
#*
#* $Id: yocto_oscontrol.py 12337 2013-08-14 15:22:22Z mvuilleu $
#*
#* Implements yFindOsControl(), the high-level API for OsControl functions
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
class YOsControl(YFunction):
    """
    The OScontrol object allows some control over the operating system running a VirtualHub.
    OsControl is available on the VirtualHub software only. This feature must be activated at the VirtualHub
    start up with -o option.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YOsControl definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    SHUTDOWNCOUNTDOWN_INVALID       = YAPI.INVALID_LONG



    _OsControlCache ={}

    #--- (end of YOsControl definitions)

    #--- (YOsControl implementation)

    def __init__(self,func):
        super(YOsControl,self).__init__("OsControl", func)
        self._callback = None
        self._logicalName = YOsControl.LOGICALNAME_INVALID
        self._advertisedValue = YOsControl.ADVERTISEDVALUE_INVALID
        self._shutdownCountdown = YOsControl.SHUTDOWNCOUNTDOWN_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "shutdownCountdown":
                self._shutdownCountdown = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the OS control, corresponding to the network name of the module.
        
        @return a string corresponding to the logical name of the OS control, corresponding to the network
        name of the module
        
        On failure, throws an exception or returns YOsControl.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YOsControl.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the OS control. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the OS control
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the OS control (no more than 6 characters).
        
        @return a string corresponding to the current value of the OS control (no more than 6 characters)
        
        On failure, throws an exception or returns YOsControl.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YOsControl.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_shutdownCountdown(self):
        """
        Returns the remaining number of seconds before the OS shutdown, or zero when no
        shutdown has been scheduled.
        
        @return an integer corresponding to the remaining number of seconds before the OS shutdown, or zero when no
                shutdown has been scheduled
        
        On failure, throws an exception or returns YOsControl.SHUTDOWNCOUNTDOWN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YOsControl.SHUTDOWNCOUNTDOWN_INVALID
        return self._shutdownCountdown

    def set_shutdownCountdown(self, newval):
        rest_val = str(newval)
        return self._setAttr("shutdownCountdown", rest_val)


    def shutdown(self , secBeforeShutDown):
        """
        Schedules an OS shutdown after a given number of seconds.
        
        @param secBeforeShutDown : number of seconds before shutdown
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(secBeforeShutDown)
        return self._setAttr("shutdownCountdown", rest_val)

    def nextOsControl(self):
        """
        Continues the enumeration of OS control started using yFirstOsControl().
        
        @return a pointer to a YOsControl object, corresponding to
                OS control currently online, or a None pointer
                if there are no more OS control to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YOsControl.FindOsControl(hwidRef.value)

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

#--- (end of YOsControl implementation)

#--- (OsControl functions)

    @staticmethod 
    def FindOsControl(func):
        """
        Retrieves OS control for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the OS control is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YOsControl.isOnline() to test if the OS control is
        indeed online at a given time. In case of ambiguity when looking for
        OS control by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the OS control
        
        @return a YOsControl object allowing you to drive the OS control.
        """
        if func in YOsControl._OsControlCache:
            return YOsControl._OsControlCache[func]
        res =YOsControl(func)
        YOsControl._OsControlCache[func] =  res
        return res

    @staticmethod 
    def  FirstOsControl():
        """
        Starts the enumeration of OS control currently accessible.
        Use the method YOsControl.nextOsControl() to iterate on
        next OS control.
        
        @return a pointer to a YOsControl object, corresponding to
                the first OS control currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("OsControl", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YOsControl.FindOsControl(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _OsControlCleanup():
        pass

  #--- (end of OsControl functions)

