#*********************************************************************
#*
#* $Id: yocto_servo.py 14275 2014-01-09 14:20:38Z seb $
#*
#* Implements yFindServo(), the high-level API for Servo functions
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


#--- (YServo class start)
#noinspection PyProtectedMember
class YServo(YFunction):
    """
    Yoctopuce application programming interface allows you not only to move
    a servo to a given position, but also to specify the time interval
    in which the move should be performed. This makes it possible to
    synchronize two servos involved in a same move.
    
    """
#--- (end of YServo class start)
    #--- (YServo return codes)
    #--- (end of YServo return codes)
    #--- (YServo definitions)
    POSITION_INVALID = YAPI.INVALID_INT
    RANGE_INVALID = YAPI.INVALID_UINT
    NEUTRAL_INVALID = YAPI.INVALID_UINT
    MOVE_INVALID = None
    #--- (end of YServo definitions)

    def __init__(self, func):
        super(YServo, self).__init__(func)
        self._className = 'Servo'
        #--- (YServo attributes)
        self._callback = None
        self._position = YServo.POSITION_INVALID
        self._range = YServo.RANGE_INVALID
        self._neutral = YServo.NEUTRAL_INVALID
        self._move = YServo.MOVE_INVALID
        #--- (end of YServo attributes)

    #--- (YServo implementation)
    def _parseAttr(self, member):
        if member.name == "position":
            self._position = member.ivalue
            return 1
        if member.name == "range":
            self._range = member.ivalue
            return 1
        if member.name == "neutral":
            self._neutral = member.ivalue
            return 1
        if member.name == "move":
            if member.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                self._move = -1
            self._move = {"moving": None, "target": None, "ms": None}
            for submemb in member.members:
                if submemb.name == "moving":
                    self._move["moving"] = submemb.ivalue
                elif submemb.name == "target":
                    self._move["target"] = submemb.ivalue
                elif submemb.name == "ms":
                    self._move["ms"] = submemb.ivalue
            return 1
        super(YServo, self)._parseAttr(member)

    def get_position(self):
        """
        Returns the current servo position.
        
        @return an integer corresponding to the current servo position
        
        On failure, throws an exception or returns YServo.POSITION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YServo.POSITION_INVALID
        return self._position

    def set_position(self, newval):
        """
        Changes immediately the servo driving position.
        
        @param newval : an integer corresponding to immediately the servo driving position
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("position", rest_val)

    def get_range(self):
        """
        Returns the current range of use of the servo.
        
        @return an integer corresponding to the current range of use of the servo
        
        On failure, throws an exception or returns YServo.RANGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YServo.RANGE_INVALID
        return self._range

    def set_range(self, newval):
        """
        Changes the range of use of the servo, specified in per cents.
        A range of 100% corresponds to a standard control signal, that varies
        from 1 [ms] to 2 [ms], When using a servo that supports a double range,
        from 0.5 [ms] to 2.5 [ms], you can select a range of 200%.
        Be aware that using a range higher than what is supported by the servo
        is likely to damage the servo.
        
        @param newval : an integer corresponding to the range of use of the servo, specified in per cents
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("range", rest_val)

    def get_neutral(self):
        """
        Returns the duration in microseconds of a neutral pulse for the servo.
        
        @return an integer corresponding to the duration in microseconds of a neutral pulse for the servo
        
        On failure, throws an exception or returns YServo.NEUTRAL_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YServo.NEUTRAL_INVALID
        return self._neutral

    def set_neutral(self, newval):
        """
        Changes the duration of the pulse corresponding to the neutral position of the servo.
        The duration is specified in microseconds, and the standard value is 1500 [us].
        This setting makes it possible to shift the range of use of the servo.
        Be aware that using a range higher than what is supported by the servo is
        likely to damage the servo.
        
        @param newval : an integer corresponding to the duration of the pulse corresponding to the neutral
        position of the servo
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("neutral", rest_val)

    def get_move(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YServo.MOVE_INVALID
        return self._move

    def set_move(self, newval):
        rest_val = str(newval.target) + ":" + str(newval.ms)
        return self._setAttr("move", rest_val)

    def move(self, target, ms_duration):
        """
        Performs a smooth move at constant speed toward a given position.
        
        @param target      : new position at the end of the move
        @param ms_duration : total duration of the move, in milliseconds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(target) + ":" + str(ms_duration)
        return self._setAttr("move", rest_val)

    @staticmethod
    def FindServo(func):
        """
        Retrieves a servo for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the servo is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YServo.isOnline() to test if the servo is
        indeed online at a given time. In case of ambiguity when looking for
        a servo by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the servo
        
        @return a YServo object allowing you to drive the servo.
        """
        # obj
        obj = YFunction._FindFromCache("Servo", func)
        if obj is None:
            obj = YServo(func)
            YFunction._AddToCache("Servo", func, obj)
        return obj

    def nextServo(self):
        """
        Continues the enumeration of servos started using yFirstServo().
        
        @return a pointer to a YServo object, corresponding to
                a servo currently online, or a None pointer
                if there are no more servos to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YServo.FindServo(hwidRef.value)

#--- (end of YServo implementation)

#--- (Servo functions)

    @staticmethod
    def FirstServo():
        """
        Starts the enumeration of servos currently accessible.
        Use the method YServo.nextServo() to iterate on
        next servos.
        
        @return a pointer to a YServo object, corresponding to
                the first servo currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Servo", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YServo.FindServo(serialRef.value + "." + funcIdRef.value)

#--- (end of Servo functions)
