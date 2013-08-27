#*********************************************************************
#*
#* $Id: yocto_hubport.py 12337 2013-08-14 15:22:22Z mvuilleu $
#*
#* Implements yFindHubPort(), the high-level API for HubPort functions
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
class YHubPort(YFunction):
    #--- (globals)


    #--- (end of globals)

    #--- (YHubPort definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    BAUDRATE_INVALID                = YAPI.INVALID_LONG

    ENABLED_FALSE                   = 0
    ENABLED_TRUE                    = 1
    ENABLED_INVALID                 = -1
    PORTSTATE_OFF                   = 0
    PORTSTATE_OVRLD                 = 1
    PORTSTATE_ON                    = 2
    PORTSTATE_RUN                   = 3
    PORTSTATE_PROG                  = 4
    PORTSTATE_INVALID               = -1


    _HubPortCache ={}

    #--- (end of YHubPort definitions)

    #--- (YHubPort implementation)

    def __init__(self,func):
        super(YHubPort,self).__init__("HubPort", func)
        self._callback = None
        self._logicalName = YHubPort.LOGICALNAME_INVALID
        self._advertisedValue = YHubPort.ADVERTISEDVALUE_INVALID
        self._enabled = YHubPort.ENABLED_INVALID
        self._portState = YHubPort.PORTSTATE_INVALID
        self._baudRate = YHubPort.BAUDRATE_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "enabled":
                self._enabled = member.ivalue
            elif member.name == "portState":
                self._portState = member.ivalue
            elif member.name == "baudRate":
                self._baudRate = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the Yocto-hub port, which is always the serial number of the
        connected module.
        
        @return a string corresponding to the logical name of the Yocto-hub port, which is always the
        serial number of the
                connected module
        
        On failure, throws an exception or returns YHubPort.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YHubPort.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        It is not possible to configure the logical name of a Yocto-hub port. The logical
        name is automatically set to the serial number of the connected module.
        
        @param newval : a string
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the Yocto-hub port (no more than 6 characters).
        
        @return a string corresponding to the current value of the Yocto-hub port (no more than 6 characters)
        
        On failure, throws an exception or returns YHubPort.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YHubPort.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_enabled(self):
        """
        Returns true if the Yocto-hub port is powered, false otherwise.
        
        @return either YHubPort.ENABLED_FALSE or YHubPort.ENABLED_TRUE, according to true if the Yocto-hub
        port is powered, false otherwise
        
        On failure, throws an exception or returns YHubPort.ENABLED_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YHubPort.ENABLED_INVALID
        return self._enabled

    def set_enabled(self, newval):
        """
        Changes the activation of the Yocto-hub port. If the port is enabled, the
        *      connected module is powered. Otherwise, port power is shut down.
        
        @param newval : either YHubPort.ENABLED_FALSE or YHubPort.ENABLED_TRUE, according to the activation
        of the Yocto-hub port
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("enabled", rest_val)


    def get_portState(self):
        """
        Returns the current state of the Yocto-hub port.
        
        @return a value among YHubPort.PORTSTATE_OFF, YHubPort.PORTSTATE_OVRLD, YHubPort.PORTSTATE_ON,
        YHubPort.PORTSTATE_RUN and YHubPort.PORTSTATE_PROG corresponding to the current state of the Yocto-hub port
        
        On failure, throws an exception or returns YHubPort.PORTSTATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YHubPort.PORTSTATE_INVALID
        return self._portState

    def get_baudRate(self):
        """
        Returns the current baud rate used by this Yocto-hub port, in kbps.
        The default value is 1000 kbps, but a slower rate may be used if communication
        problems are encountered.
        
        @return an integer corresponding to the current baud rate used by this Yocto-hub port, in kbps
        
        On failure, throws an exception or returns YHubPort.BAUDRATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YHubPort.BAUDRATE_INVALID
        return self._baudRate

    def nextHubPort(self):
        """
        Continues the enumeration of Yocto-hub ports started using yFirstHubPort().
        
        @return a pointer to a YHubPort object, corresponding to
                a Yocto-hub port currently online, or a None pointer
                if there are no more Yocto-hub ports to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YHubPort.FindHubPort(hwidRef.value)

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

#--- (end of YHubPort implementation)

#--- (HubPort functions)

    @staticmethod 
    def FindHubPort(func):
        """
        Retrieves a Yocto-hub port for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the Yocto-hub port is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YHubPort.isOnline() to test if the Yocto-hub port is
        indeed online at a given time. In case of ambiguity when looking for
        a Yocto-hub port by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the Yocto-hub port
        
        @return a YHubPort object allowing you to drive the Yocto-hub port.
        """
        if func in YHubPort._HubPortCache:
            return YHubPort._HubPortCache[func]
        res =YHubPort(func)
        YHubPort._HubPortCache[func] =  res
        return res

    @staticmethod 
    def  FirstHubPort():
        """
        Starts the enumeration of Yocto-hub ports currently accessible.
        Use the method YHubPort.nextHubPort() to iterate on
        next Yocto-hub ports.
        
        @return a pointer to a YHubPort object, corresponding to
                the first Yocto-hub port currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("HubPort", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YHubPort.FindHubPort(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _HubPortCleanup():
        pass

  #--- (end of HubPort functions)

