#*********************************************************************
#*
#* $Id: pic24config.php 12323 2013-08-13 15:09:18Z mvuilleu $
#*
#* Implements yFindDigitalIO(), the high-level API for DigitalIO functions
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
class YDigitalIO(YFunction):
    """
    ....
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YDigitalIO definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    PORTSTATE_INVALID               = YAPI.INVALID_LONG
    PORTDIRECTION_INVALID           = YAPI.INVALID_LONG
    PORTOPENDRAIN_INVALID           = YAPI.INVALID_LONG
    PORTSIZE_INVALID                = YAPI.INVALID_LONG
    COMMAND_INVALID                 = YAPI.INVALID_STRING

    OUTPUTVOLTAGE_USB_5V            = 0
    OUTPUTVOLTAGE_USB_3V3           = 1
    OUTPUTVOLTAGE_EXT_V             = 2
    OUTPUTVOLTAGE_INVALID           = -1


    _DigitalIOCache ={}

    #--- (end of YDigitalIO definitions)

    #--- (YDigitalIO implementation)

    def __init__(self,func):
        super(YDigitalIO,self).__init__("DigitalIO", func)
        self._callback = None
        self._logicalName = YDigitalIO.LOGICALNAME_INVALID
        self._advertisedValue = YDigitalIO.ADVERTISEDVALUE_INVALID
        self._portState = YDigitalIO.PORTSTATE_INVALID
        self._portDirection = YDigitalIO.PORTDIRECTION_INVALID
        self._portOpenDrain = YDigitalIO.PORTOPENDRAIN_INVALID
        self._portSize = YDigitalIO.PORTSIZE_INVALID
        self._outputVoltage = YDigitalIO.OUTPUTVOLTAGE_INVALID
        self._command = YDigitalIO.COMMAND_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "portState":
                self._portState = member.ivalue
            elif member.name == "portDirection":
                self._portDirection = member.ivalue
            elif member.name == "portOpenDrain":
                self._portOpenDrain = member.ivalue
            elif member.name == "portSize":
                self._portSize = member.ivalue
            elif member.name == "outputVoltage":
                self._outputVoltage = member.ivalue
            elif member.name == "command":
                self._command = member.svalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the digital IO port.
        
        @return a string corresponding to the logical name of the digital IO port
        
        On failure, throws an exception or returns YDigitalIO.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the digital IO port. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the digital IO port
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the digital IO port (no more than 6 characters).
        
        @return a string corresponding to the current value of the digital IO port (no more than 6 characters)
        
        On failure, throws an exception or returns YDigitalIO.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_portState(self):
        """
        Returns the digital IO port state: bit 0 represents input 0, and so on.
        
        @return an integer corresponding to the digital IO port state: bit 0 represents input 0, and so on
        
        On failure, throws an exception or returns YDigitalIO.PORTSTATE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.PORTSTATE_INVALID
        return self._portState

    def set_portState(self, newval):
        """
        Changes the digital IO port state: bit 0 represents input 0, and so on. This function has no effect
        on bits configured as input in portDirection.
        
        @param newval : an integer corresponding to the digital IO port state: bit 0 represents input 0, and so on
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("portState", rest_val)


    def get_portDirection(self):
        """
        Returns the IO direction of all bits of the port: 0 makes a bit an input, 1 makes it an output.
        
        @return an integer corresponding to the IO direction of all bits of the port: 0 makes a bit an
        input, 1 makes it an output
        
        On failure, throws an exception or returns YDigitalIO.PORTDIRECTION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.PORTDIRECTION_INVALID
        return self._portDirection

    def set_portDirection(self, newval):
        """
        Changes the IO direction of all bits of the port: 0 makes a bit an input, 1 makes it an output.
        Remember to call the saveToFlash() method  to make sure the setting will be kept after a reboot.
        
        @param newval : an integer corresponding to the IO direction of all bits of the port: 0 makes a bit
        an input, 1 makes it an output
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("portDirection", rest_val)


    def get_portOpenDrain(self):
        """
        Returns the electrical interface for each bit of the port. 0 makes a bit a regular input/output, 1 makes
        it an open-drain (open-collector) input/output.
        
        @return an integer corresponding to the electrical interface for each bit of the port
        
        On failure, throws an exception or returns YDigitalIO.PORTOPENDRAIN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.PORTOPENDRAIN_INVALID
        return self._portOpenDrain

    def set_portOpenDrain(self, newval):
        """
        Changes the electrical interface for each bit of the port. 0 makes a bit a regular input/output, 1 makes
        it an open-drain (open-collector) input/output. Remember to call the
        saveToFlash() method  to make sure the setting will be kept after a reboot.
        
        @param newval : an integer corresponding to the electrical interface for each bit of the port
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("portOpenDrain", rest_val)


    def get_portSize(self):
        """
        Returns the number of bits implemented in the I/O port.
        
        @return an integer corresponding to the number of bits implemented in the I/O port
        
        On failure, throws an exception or returns YDigitalIO.PORTSIZE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.PORTSIZE_INVALID
        return self._portSize

    def get_outputVoltage(self):
        """
        Returns the voltage source used to drive output bits.
        
        @return a value among YDigitalIO.OUTPUTVOLTAGE_USB_5V, YDigitalIO.OUTPUTVOLTAGE_USB_3V3 and
        YDigitalIO.OUTPUTVOLTAGE_EXT_V corresponding to the voltage source used to drive output bits
        
        On failure, throws an exception or returns YDigitalIO.OUTPUTVOLTAGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.OUTPUTVOLTAGE_INVALID
        return self._outputVoltage

    def set_outputVoltage(self, newval):
        """
        Changes the voltage source used to drive output bits.
        Remember to call the saveToFlash() method  to make sure the setting will be kept after a reboot.
        
        @param newval : a value among YDigitalIO.OUTPUTVOLTAGE_USB_5V, YDigitalIO.OUTPUTVOLTAGE_USB_3V3 and
        YDigitalIO.OUTPUTVOLTAGE_EXT_V corresponding to the voltage source used to drive output bits
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("outputVoltage", rest_val)


    def get_command(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YDigitalIO.COMMAND_INVALID
        return self._command

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    def set_bitState(self, bitno, bitval):
        """
        Set a single bit of the I/O port.
        
        @param bitno: the bit number; lowest bit is index 0
        @param bitval: the value of the bit (1 or 0)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        if not (bitval >= 0) : self._throw( YAPI.INVALID_ARGUMENT,  "invalid bitval")
        if not (bitval <= 1) : self._throw( YAPI.INVALID_ARGUMENT,  "invalid bitval")
        return self.set_command(""+str(chr(82+bitval))+""+ str(int( bitno)))
        

    def get_bitState(self, bitno):
        """
        Returns the value of a single bit of the I/O port.
        
        @param bitno: the bit number; lowest bit is index 0
        
        @return the bit value (0 or 1)
        
        On failure, throws an exception or returns a negative error code.
        """
        
        portVal = self.get_portState()
        return ((((portVal) >> (bitno))) & (1))
        

    def toggle_bitState(self, bitno):
        """
        Revert a single bit of the I/O port.
        
        @param bitno: the bit number; lowest bit is index 0
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("T"+ str(int( bitno)))
        

    def set_bitDirection(self, bitno, bitdirection):
        """
        Change  the direction of a single bit from the I/O port.
        
        @param bitno: the bit number; lowest bit is index 0
        @param bitdirection: direction to set, 0 makes the bit an input, 1 makes it an output.
                Remember to call the   saveToFlash() method to make sure the setting will be kept after a reboot.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        if not (bitdirection >= 0) : self._throw( YAPI.INVALID_ARGUMENT,  "invalid direction")
        if not (bitdirection <= 1) : self._throw( YAPI.INVALID_ARGUMENT,  "invalid direction")
        return self.set_command(""+str(chr(73+6*bitdirection))+""+ str(int( bitno)))
        

    def get_bitDirection(self, bitno):
        """
        Change  the direction of a single bit from the I/O port (0 means the bit is an input, 1  an output).
        
        @param bitno: the bit number; lowest bit is index 0
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        portDir = self.get_portDirection()
        return ((((portDir) >> (bitno))) & (1))
        

    def set_bitOpenDrain(self, bitno, opendrain):
        """
        Change  the electrical interface of a single bit from the I/O port.
        
        @param bitno: the bit number; lowest bit is index 0
        @param opendrain: value to set, 0 makes a bit a regular input/output, 1 makes
                it an open-drain (open-collector) input/output. Remember to call the
                saveToFlash() method to make sure the setting will be kept after a reboot.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        if not (opendrain >= 0) : self._throw( YAPI.INVALID_ARGUMENT,  "invalid state")
        if not (opendrain <= 1) : self._throw( YAPI.INVALID_ARGUMENT,  "invalid state")
        return self.set_command(""+str(chr(100-32*opendrain))+""+ str(int( bitno)))
        

    def get_bitOpenDrain(self, bitno):
        """
        Returns the type of electrical interface of a single bit from the I/O port. (0 means the bit is an
        input, 1  an output).
        
        @param bitno: the bit number; lowest bit is index 0
        
        @return   0 means the a bit is a regular input/output, 1means the b it an open-drain
        (open-collector) input/output.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        portOpenDrain = self.get_portOpenDrain()
        return ((((portOpenDrain) >> (bitno))) & (1))
        


    def nextDigitalIO(self):
        """
        Continues the enumeration of digital IO port started using yFirstDigitalIO().
        
        @return a pointer to a YDigitalIO object, corresponding to
                a digital IO port currently online, or a None pointer
                if there are no more digital IO port to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YDigitalIO.FindDigitalIO(hwidRef.value)

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

#--- (end of YDigitalIO implementation)

#--- (DigitalIO functions)

    @staticmethod 
    def FindDigitalIO(func):
        """
        Retrieves a digital IO port for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the digital IO port is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YDigitalIO.isOnline() to test if the digital IO port is
        indeed online at a given time. In case of ambiguity when looking for
        a digital IO port by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the digital IO port
        
        @return a YDigitalIO object allowing you to drive the digital IO port.
        """
        if func in YDigitalIO._DigitalIOCache:
            return YDigitalIO._DigitalIOCache[func]
        res =YDigitalIO(func)
        YDigitalIO._DigitalIOCache[func] =  res
        return res

    @staticmethod 
    def  FirstDigitalIO():
        """
        Starts the enumeration of digital IO port currently accessible.
        Use the method YDigitalIO.nextDigitalIO() to iterate on
        next digital IO port.
        
        @return a pointer to a YDigitalIO object, corresponding to
                the first digital IO port currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("DigitalIO", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YDigitalIO.FindDigitalIO(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _DigitalIOCleanup():
        pass

  #--- (end of DigitalIO functions)

