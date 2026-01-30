# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindCounter(), the high-level API for Counter functions
#
#  - - - - - - - - - License information: - - - - - - - - -
#
#  Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#
#  Yoctopuce Sarl (hereafter Licensor) grants to you a perpetual
#  non-exclusive license to use, modify, copy and integrate this
#  file into your software for the sole purpose of interfacing
#  with Yoctopuce products.
#
#  You may reproduce and distribute copies of this file in
#  source or object form, as long as the sole purpose of this
#  code is to interface with Yoctopuce products. You must retain
#  this notice in the distributed source file.
#
#  You should refer to Yoctopuce General Terms and Conditions
#  for additional information regarding your rights and
#  obligations.
#
#  THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#  WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING
#  WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#  EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#  INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA,
#  COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR
#  SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT
#  LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#  CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#  BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#  WARRANTY, OR OTHERWISE.
#
# *********************************************************************


__docformat__ = 'restructuredtext en'
from yocto_api import *


#--- (YCounter class start)
#noinspection PyProtectedMember
class YCounter(YSensor):
    """
    The YCounter class allows you to read and configure Yoctopuce gcounters.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YCounter class start)
    #--- (YCounter return codes)
    #--- (end of YCounter return codes)
    #--- (YCounter dlldef)
    #--- (end of YCounter dlldef)
    #--- (YCounter yapiwrapper)
    #--- (end of YCounter yapiwrapper)
    #--- (YCounter definitions)
    #--- (end of YCounter definitions)

    def __init__(self, func):
        super(YCounter, self).__init__(func)
        self._className = 'Counter'
        #--- (YCounter attributes)
        self._callback = None
        #--- (end of YCounter attributes)

    #--- (YCounter implementation)
    def _parseAttr(self, json_val):
        super(YCounter, self)._parseAttr(json_val)

    @staticmethod
    def FindCounter(func):
        """
        Retrieves a counter for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the counter is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCounter.isOnline() to test if the counter is
        indeed online at a given time. In case of ambiguity when looking for
        a counter by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the counter, for instance
                MyDevice.counter.

        @return a YCounter object allowing you to drive the counter.
        """
        # obj
        obj = YFunction._FindFromCache("Counter", func)
        if obj is None:
            obj = YCounter(func)
            YFunction._AddToCache("Counter", func, obj)
        return obj

    def nextCounter(self):
        """
        Continues the enumeration of gcounters started using yFirstCounter().
        Caution: You can't make any assumption about the returned gcounters order.
        If you want to find a specific a counter, use Counter.findCounter()
        and a hardwareID or a logical name.

        @return a pointer to a YCounter object, corresponding to
                a counter currently online, or a None pointer
                if there are no more gcounters to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YCounter.FindCounter(hwidRef.value)

#--- (end of YCounter implementation)

#--- (YCounter functions)

    @staticmethod
    def FirstCounter():
        """
        Starts the enumeration of gcounters currently accessible.
        Use the method YCounter.nextCounter() to iterate on
        next gcounters.

        @return a pointer to a YCounter object, corresponding to
                the first counter currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Counter", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YCounter.FindCounter(serialRef.value + "." + funcIdRef.value)

#--- (end of YCounter functions)
