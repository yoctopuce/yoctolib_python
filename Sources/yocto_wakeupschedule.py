#*********************************************************************
#*
#* $Id: yocto_wakeupschedule.py 12469 2013-08-22 10:11:58Z seb $
#*
#* Implements yFindWakeUpSchedule(), the high-level API for WakeUpSchedule functions
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
class YWakeUpSchedule(YFunction):
    """
    The WakeUpSchedule function implements a wake-up condition. The wake-up time is
    specified as a set of months and/or days and/or hours and/or minutes where the
    wake-up should happen.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YWakeUpSchedule definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    MINUTESA_INVALID                = YAPI.INVALID_LONG
    MINUTESB_INVALID                = YAPI.INVALID_LONG
    HOURS_INVALID                   = YAPI.INVALID_LONG
    WEEKDAYS_INVALID                = YAPI.INVALID_LONG
    MONTHDAYS_INVALID               = YAPI.INVALID_LONG
    MONTHS_INVALID                  = YAPI.INVALID_LONG
    NEXTOCCURENCE_INVALID           = YAPI.INVALID_LONG



    _WakeUpScheduleCache ={}

    #--- (end of YWakeUpSchedule definitions)

    #--- (YWakeUpSchedule implementation)

    def __init__(self,func):
        super(YWakeUpSchedule,self).__init__("WakeUpSchedule", func)
        self._callback = None
        self._logicalName = YWakeUpSchedule.LOGICALNAME_INVALID
        self._advertisedValue = YWakeUpSchedule.ADVERTISEDVALUE_INVALID
        self._minutesA = YWakeUpSchedule.MINUTESA_INVALID
        self._minutesB = YWakeUpSchedule.MINUTESB_INVALID
        self._hours = YWakeUpSchedule.HOURS_INVALID
        self._weekDays = YWakeUpSchedule.WEEKDAYS_INVALID
        self._monthDays = YWakeUpSchedule.MONTHDAYS_INVALID
        self._months = YWakeUpSchedule.MONTHS_INVALID
        self._nextOccurence = YWakeUpSchedule.NEXTOCCURENCE_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "minutesA":
                self._minutesA = member.ivalue
            elif member.name == "minutesB":
                self._minutesB = member.ivalue
            elif member.name == "hours":
                self._hours = member.ivalue
            elif member.name == "weekDays":
                self._weekDays = member.ivalue
            elif member.name == "monthDays":
                self._monthDays = member.ivalue
            elif member.name == "months":
                self._months = member.ivalue
            elif member.name == "nextOccurence":
                self._nextOccurence = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the wake-up schedule.
        
        @return a string corresponding to the logical name of the wake-up schedule
        
        On failure, throws an exception or returns YWakeUpSchedule.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the wake-up schedule. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the wake-up schedule
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the wake-up schedule (no more than 6 characters).
        
        @return a string corresponding to the current value of the wake-up schedule (no more than 6 characters)
        
        On failure, throws an exception or returns YWakeUpSchedule.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_minutesA(self):
        """
        Returns the minutes 00-29 of each hour scheduled for wake-up.
        
        @return an integer corresponding to the minutes 00-29 of each hour scheduled for wake-up
        
        On failure, throws an exception or returns YWakeUpSchedule.MINUTESA_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.MINUTESA_INVALID
        return self._minutesA

    def set_minutesA(self, newval):
        """
        Changes the minutes 00-29 where a wake up must take place.
        
        @param newval : an integer corresponding to the minutes 00-29 where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("minutesA", rest_val)


    def get_minutesB(self):
        """
        Returns the minutes 30-59 of each hour scheduled for wake-up.
        
        @return an integer corresponding to the minutes 30-59 of each hour scheduled for wake-up
        
        On failure, throws an exception or returns YWakeUpSchedule.MINUTESB_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.MINUTESB_INVALID
        return self._minutesB

    def set_minutesB(self, newval):
        """
        Changes the minutes 30-59 where a wake up must take place.
        
        @param newval : an integer corresponding to the minutes 30-59 where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("minutesB", rest_val)


    def get_hours(self):
        """
        Returns the hours  scheduled for wake-up.
        
        @return an integer corresponding to the hours  scheduled for wake-up
        
        On failure, throws an exception or returns YWakeUpSchedule.HOURS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.HOURS_INVALID
        return self._hours

    def set_hours(self, newval):
        """
        Changes the hours where a wake up must take place.
        
        @param newval : an integer corresponding to the hours where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("hours", rest_val)


    def get_weekDays(self):
        """
        Returns the days of week scheduled for wake-up.
        
        @return an integer corresponding to the days of week scheduled for wake-up
        
        On failure, throws an exception or returns YWakeUpSchedule.WEEKDAYS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.WEEKDAYS_INVALID
        return self._weekDays

    def set_weekDays(self, newval):
        """
        Changes the days of the week where a wake up must take place.
        
        @param newval : an integer corresponding to the days of the week where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("weekDays", rest_val)


    def get_monthDays(self):
        """
        Returns the days of week scheduled for wake-up.
        
        @return an integer corresponding to the days of week scheduled for wake-up
        
        On failure, throws an exception or returns YWakeUpSchedule.MONTHDAYS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.MONTHDAYS_INVALID
        return self._monthDays

    def set_monthDays(self, newval):
        """
        Changes the days of the week where a wake up must take place.
        
        @param newval : an integer corresponding to the days of the week where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("monthDays", rest_val)


    def get_months(self):
        """
        Returns the days of week scheduled for wake-up.
        
        @return an integer corresponding to the days of week scheduled for wake-up
        
        On failure, throws an exception or returns YWakeUpSchedule.MONTHS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.MONTHS_INVALID
        return self._months

    def set_months(self, newval):
        """
        Changes the days of the week where a wake up must take place.
        
        @param newval : an integer corresponding to the days of the week where a wake up must take place
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("months", rest_val)


    def get_nextOccurence(self):
        """
        Returns the  nextwake up date/time (seconds) wake up occurence
        
        @return an integer corresponding to the  nextwake up date/time (seconds) wake up occurence
        
        On failure, throws an exception or returns YWakeUpSchedule.NEXTOCCURENCE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWakeUpSchedule.NEXTOCCURENCE_INVALID
        return self._nextOccurence
    def get_minutes(self ):
        """
        Returns every the minutes of each hour scheduled for wake-up.
        """
        
        res = self.get_minutesB()
        res = res << 30
        res = res + self.get_minutesA()
        return res

    def set_minutes(self, bitmap):
        """
        Changes all the minutes where a wake up must take place.
        
        @param bitmap : Minutes 00-59 of each hour scheduled for wake-up.,
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        self.set_minutesA(bitmap & 0x3fffffff)
        bitmap = bitmap >> 30
        return self.set_minutesB(bitmap & 0x3fffffff)
        


    def nextWakeUpSchedule(self):
        """
        Continues the enumeration of wake-up schedules started using yFirstWakeUpSchedule().
        
        @return a pointer to a YWakeUpSchedule object, corresponding to
                a wake-up schedule currently online, or a None pointer
                if there are no more wake-up schedules to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YWakeUpSchedule.FindWakeUpSchedule(hwidRef.value)

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

#--- (end of YWakeUpSchedule implementation)

#--- (WakeUpSchedule functions)

    @staticmethod 
    def FindWakeUpSchedule(func):
        """
        Retrieves a wake-up schedule for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the wake-up schedule is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWakeUpSchedule.isOnline() to test if the wake-up schedule is
        indeed online at a given time. In case of ambiguity when looking for
        a wake-up schedule by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the wake-up schedule
        
        @return a YWakeUpSchedule object allowing you to drive the wake-up schedule.
        """
        if func in YWakeUpSchedule._WakeUpScheduleCache:
            return YWakeUpSchedule._WakeUpScheduleCache[func]
        res =YWakeUpSchedule(func)
        YWakeUpSchedule._WakeUpScheduleCache[func] =  res
        return res

    @staticmethod 
    def  FirstWakeUpSchedule():
        """
        Starts the enumeration of wake-up schedules currently accessible.
        Use the method YWakeUpSchedule.nextWakeUpSchedule() to iterate on
        next wake-up schedules.
        
        @return a pointer to a YWakeUpSchedule object, corresponding to
                the first wake-up schedule currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("WakeUpSchedule", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YWakeUpSchedule.FindWakeUpSchedule(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _WakeUpScheduleCleanup():
        pass

  #--- (end of WakeUpSchedule functions)

