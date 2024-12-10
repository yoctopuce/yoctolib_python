# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindInputChain(), the high-level API for InputChain functions
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

def yInternalEventCallback(obj, value):
    obj._internalEventHandler(value)

#--- (YInputChain class start)
#noinspection PyProtectedMember
class YInputChain(YFunction):
    """
    The YInputChain class provides access to separate
    digital inputs connected in a chain.

    """
    #--- (end of YInputChain class start)
    #--- (YInputChain return codes)
    #--- (end of YInputChain return codes)
    #--- (YInputChain dlldef)
    #--- (end of YInputChain dlldef)
    #--- (YInputChain yapiwrapper)
    #--- (end of YInputChain yapiwrapper)
    #--- (YInputChain definitions)
    EXPECTEDNODES_INVALID = YAPI.INVALID_UINT
    DETECTEDNODES_INVALID = YAPI.INVALID_UINT
    REFRESHRATE_INVALID = YAPI.INVALID_UINT
    BITCHAIN1_INVALID = YAPI.INVALID_STRING
    BITCHAIN2_INVALID = YAPI.INVALID_STRING
    BITCHAIN3_INVALID = YAPI.INVALID_STRING
    BITCHAIN4_INVALID = YAPI.INVALID_STRING
    BITCHAIN5_INVALID = YAPI.INVALID_STRING
    BITCHAIN6_INVALID = YAPI.INVALID_STRING
    BITCHAIN7_INVALID = YAPI.INVALID_STRING
    WATCHDOGPERIOD_INVALID = YAPI.INVALID_UINT
    CHAINDIAGS_INVALID = YAPI.INVALID_UINT
    LOOPBACKTEST_OFF = 0
    LOOPBACKTEST_ON = 1
    LOOPBACKTEST_INVALID = -1
    #--- (end of YInputChain definitions)

    def __init__(self, func):
        super(YInputChain, self).__init__(func)
        self._className = 'InputChain'
        #--- (YInputChain attributes)
        self._callback = None
        self._expectedNodes = YInputChain.EXPECTEDNODES_INVALID
        self._detectedNodes = YInputChain.DETECTEDNODES_INVALID
        self._loopbackTest = YInputChain.LOOPBACKTEST_INVALID
        self._refreshRate = YInputChain.REFRESHRATE_INVALID
        self._bitChain1 = YInputChain.BITCHAIN1_INVALID
        self._bitChain2 = YInputChain.BITCHAIN2_INVALID
        self._bitChain3 = YInputChain.BITCHAIN3_INVALID
        self._bitChain4 = YInputChain.BITCHAIN4_INVALID
        self._bitChain5 = YInputChain.BITCHAIN5_INVALID
        self._bitChain6 = YInputChain.BITCHAIN6_INVALID
        self._bitChain7 = YInputChain.BITCHAIN7_INVALID
        self._watchdogPeriod = YInputChain.WATCHDOGPERIOD_INVALID
        self._chainDiags = YInputChain.CHAINDIAGS_INVALID
        self._stateChangeCallback = None
        self._prevPos = 0
        self._eventPos = 0
        self._eventStamp = 0
        self._eventChains = []
        #--- (end of YInputChain attributes)

    #--- (YInputChain implementation)
    def _parseAttr(self, json_val):
        if json_val.has("expectedNodes"):
            self._expectedNodes = json_val.getInt("expectedNodes")
        if json_val.has("detectedNodes"):
            self._detectedNodes = json_val.getInt("detectedNodes")
        if json_val.has("loopbackTest"):
            self._loopbackTest = json_val.getInt("loopbackTest") > 0
        if json_val.has("refreshRate"):
            self._refreshRate = json_val.getInt("refreshRate")
        if json_val.has("bitChain1"):
            self._bitChain1 = json_val.getString("bitChain1")
        if json_val.has("bitChain2"):
            self._bitChain2 = json_val.getString("bitChain2")
        if json_val.has("bitChain3"):
            self._bitChain3 = json_val.getString("bitChain3")
        if json_val.has("bitChain4"):
            self._bitChain4 = json_val.getString("bitChain4")
        if json_val.has("bitChain5"):
            self._bitChain5 = json_val.getString("bitChain5")
        if json_val.has("bitChain6"):
            self._bitChain6 = json_val.getString("bitChain6")
        if json_val.has("bitChain7"):
            self._bitChain7 = json_val.getString("bitChain7")
        if json_val.has("watchdogPeriod"):
            self._watchdogPeriod = json_val.getInt("watchdogPeriod")
        if json_val.has("chainDiags"):
            self._chainDiags = json_val.getInt("chainDiags")
        super(YInputChain, self)._parseAttr(json_val)

    def get_expectedNodes(self):
        """
        Returns the number of nodes expected in the chain.

        @return an integer corresponding to the number of nodes expected in the chain

        On failure, throws an exception or returns YInputChain.EXPECTEDNODES_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.EXPECTEDNODES_INVALID
        res = self._expectedNodes
        return res

    def set_expectedNodes(self, newval):
        """
        Changes the number of nodes expected in the chain.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : an integer corresponding to the number of nodes expected in the chain

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("expectedNodes", rest_val)

    def get_detectedNodes(self):
        """
        Returns the number of nodes detected in the chain.

        @return an integer corresponding to the number of nodes detected in the chain

        On failure, throws an exception or returns YInputChain.DETECTEDNODES_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.DETECTEDNODES_INVALID
        res = self._detectedNodes
        return res

    def get_loopbackTest(self):
        """
        Returns the activation state of the exhaustive chain connectivity test.
        The connectivity test requires a cable connecting the end of the chain
        to the loopback test connector.

        @return either YInputChain.LOOPBACKTEST_OFF or YInputChain.LOOPBACKTEST_ON, according to the
        activation state of the exhaustive chain connectivity test

        On failure, throws an exception or returns YInputChain.LOOPBACKTEST_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.LOOPBACKTEST_INVALID
        res = self._loopbackTest
        return res

    def set_loopbackTest(self, newval):
        """
        Changes the activation state of the exhaustive chain connectivity test.
        The connectivity test requires a cable connecting the end of the chain
        to the loopback test connector.

        If you want the change to be kept after a device reboot,
        make sure  to call the matching module saveToFlash().

        @param newval : either YInputChain.LOOPBACKTEST_OFF or YInputChain.LOOPBACKTEST_ON, according to
        the activation state of the exhaustive chain connectivity test

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("loopbackTest", rest_val)

    def get_refreshRate(self):
        """
        Returns the desired refresh rate, measured in Hz.
        The higher the refresh rate is set, the higher the
        communication speed on the chain will be.

        @return an integer corresponding to the desired refresh rate, measured in Hz

        On failure, throws an exception or returns YInputChain.REFRESHRATE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.REFRESHRATE_INVALID
        res = self._refreshRate
        return res

    def set_refreshRate(self, newval):
        """
        Changes the desired refresh rate, measured in Hz.
        The higher the refresh rate is set, the higher the
        communication speed on the chain will be.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : an integer corresponding to the desired refresh rate, measured in Hz

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("refreshRate", rest_val)

    def get_bitChain1(self):
        """
        Returns the state of input 1 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 1 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN1_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN1_INVALID
        res = self._bitChain1
        return res

    def get_bitChain2(self):
        """
        Returns the state of input 2 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 2 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN2_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN2_INVALID
        res = self._bitChain2
        return res

    def get_bitChain3(self):
        """
        Returns the state of input 3 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 3 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN3_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN3_INVALID
        res = self._bitChain3
        return res

    def get_bitChain4(self):
        """
        Returns the state of input 4 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 4 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN4_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN4_INVALID
        res = self._bitChain4
        return res

    def get_bitChain5(self):
        """
        Returns the state of input 5 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 5 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN5_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN5_INVALID
        res = self._bitChain5
        return res

    def get_bitChain6(self):
        """
        Returns the state of input 6 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 6 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN6_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN6_INVALID
        res = self._bitChain6
        return res

    def get_bitChain7(self):
        """
        Returns the state of input 7 for all nodes of the input chain,
        as a hexadecimal string. The node nearest to the controller
        is the lowest bit of the result.

        @return a string corresponding to the state of input 7 for all nodes of the input chain,
                as a hexadecimal string

        On failure, throws an exception or returns YInputChain.BITCHAIN7_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.BITCHAIN7_INVALID
        res = self._bitChain7
        return res

    def get_watchdogPeriod(self):
        """
        Returns the wait time in seconds before triggering an inactivity
        timeout error.

        @return an integer corresponding to the wait time in seconds before triggering an inactivity
                timeout error

        On failure, throws an exception or returns YInputChain.WATCHDOGPERIOD_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.WATCHDOGPERIOD_INVALID
        res = self._watchdogPeriod
        return res

    def set_watchdogPeriod(self, newval):
        """
        Changes the wait time in seconds before triggering an inactivity
        timeout error. Remember to call the saveToFlash() method
        of the module if the modification must be kept.

        @param newval : an integer corresponding to the wait time in seconds before triggering an inactivity
                timeout error

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("watchdogPeriod", rest_val)

    def get_chainDiags(self):
        """
        Returns the controller state diagnostics. Bit 0 indicates a chain length
        error, bit 1 indicates an inactivity timeout and bit 2 indicates
        a loopback test failure.

        @return an integer corresponding to the controller state diagnostics

        On failure, throws an exception or returns YInputChain.CHAINDIAGS_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YInputChain.CHAINDIAGS_INVALID
        res = self._chainDiags
        return res

    @staticmethod
    def FindInputChain(func):
        """
        Retrieves a digital input chain for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the digital input chain is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YInputChain.isOnline() to test if the digital input chain is
        indeed online at a given time. In case of ambiguity when looking for
        a digital input chain by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the digital input chain, for instance
                MyDevice.inputChain.

        @return a YInputChain object allowing you to drive the digital input chain.
        """
        # obj
        obj = YFunction._FindFromCache("InputChain", func)
        if obj is None:
            obj = YInputChain(func)
            YFunction._AddToCache("InputChain", func, obj)
        return obj

    def resetWatchdog(self):
        """
        Resets the application watchdog countdown.
        If you have set up a non-zero watchdogPeriod, you should
        call this function on a regular basis to prevent the application
        inactivity error to be triggered.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_watchdogPeriod(-1)

    def get_lastEvents(self):
        """
        Returns a string with last events observed on the digital input chain.
        This method return only events that are still buffered in the device memory.

        @return a string with last events observed (one per line).

        On failure, throws an exception or returns  YAPI.INVALID_STRING.
        """
        # content

        content = self._download("events.txt")
        return content.decode(YAPI.DefaultEncoding)

    def registerStateChangeCallback(self, callback):
        """
        Registers a callback function to be called each time that an event is detected on the
        input chain.The callback is invoked only during the execution of
        ySleep or yHandleEvents. This provides control over the time when
        the callback is triggered. For good responsiveness, remember to call one of these
        two functions periodically. To unregister a callback, pass a None pointer as argument.

        @param callback : the callback function to call, or a None pointer.
                The callback function should take four arguments:
                the YInputChain object that emitted the event, the
                UTC timestamp of the event, a character string describing
                the type of event and a character string with the event data.
                On failure, throws an exception or returns a negative error code.
        """
        if callback is not None:
            self.registerValueCallback(yInternalEventCallback)
        else:
            self.registerValueCallback(None)
        # // register user callback AFTER the internal pseudo-event,
        # // to make sure we start with future events only
        self._stateChangeCallback = callback
        return 0

    def _internalEventHandler(self, cbpos):
        # newPos
        # url
        # content
        # contentStr
        eventArr = []
        # arrLen
        # lenStr
        # arrPos
        # eventStr
        # eventLen
        # hexStamp
        # typePos
        # dataPos
        # evtStamp
        # evtType
        # evtData
        # evtChange
        # chainIdx
        newPos = YAPI._atoi(cbpos)
        if newPos < self._prevPos:
            self._eventPos = 0
        self._prevPos = newPos
        if newPos < self._eventPos:
            return YAPI.SUCCESS
        if not (self._stateChangeCallback is not None):
            # // first simulated event, use it to initialize reference values
            self._eventPos = newPos
            del self._eventChains[:]
            self._eventChains.append(self.get_bitChain1())
            self._eventChains.append(self.get_bitChain2())
            self._eventChains.append(self.get_bitChain3())
            self._eventChains.append(self.get_bitChain4())
            self._eventChains.append(self.get_bitChain5())
            self._eventChains.append(self.get_bitChain6())
            self._eventChains.append(self.get_bitChain7())
            return YAPI.SUCCESS
        url = "events.txt?pos=" + str(int(self._eventPos))

        content = self._download(url)
        contentStr = content.decode(YAPI.DefaultEncoding)
        eventArr = (contentStr).split('\n')
        arrLen = len(eventArr)
        if not (arrLen > 0):
            self._throw(YAPI.IO_ERROR, "fail to download events")
            return YAPI.IO_ERROR
        # // last element of array is the new position preceeded by '@'
        arrLen = arrLen - 1
        lenStr = eventArr[arrLen]
        lenStr = (lenStr)[1: 1 + len(lenStr)-1]
        # // update processed event position pointer
        self._eventPos = YAPI._atoi(lenStr)
        # // now generate callbacks for each event received
        arrPos = 0
        while arrPos < arrLen:
            eventStr = eventArr[arrPos]
            eventLen = len(eventStr)
            if eventLen >= 1:
                hexStamp = (eventStr)[0: 0 + 8]
                evtStamp = int(hexStamp, 16)
                typePos = eventStr.find(":")+1
                if (evtStamp >= self._eventStamp) and (typePos > 8):
                    self._eventStamp = evtStamp
                    dataPos = eventStr.find("=")+1
                    evtType = (eventStr)[typePos: typePos + 1]
                    evtData = ""
                    evtChange = ""
                    if dataPos > 10:
                        evtData = (eventStr)[dataPos: dataPos + len(eventStr)-dataPos]
                        if "1234567".find(evtType) >= 0:
                            chainIdx = YAPI._atoi(evtType) - 1
                            evtChange = self._strXor(evtData, self._eventChains[chainIdx])
                            self._eventChains[chainIdx] = evtData
                    self._stateChangeCallback(self, evtStamp, evtType, evtData, evtChange)
            arrPos = arrPos + 1
        return YAPI.SUCCESS

    def _strXor(self, a, b):
        # lenA
        # lenB
        # res
        # idx
        # digitA
        # digitB
        # // make sure the result has the same length as first argument
        lenA = len(a)
        lenB = len(b)
        if lenA > lenB:
            res = (a)[0: 0 + lenA-lenB]
            a = (a)[lenA-lenB: lenA-lenB + lenB]
            lenA = lenB
        else:
            res = ""
            b = (b)[lenA-lenB: lenA-lenB + lenA]
        # // scan strings and compare digit by digit
        idx = 0
        while idx < lenA:
            digitA = int((a)[idx: idx + 1], 16)
            digitB = int((b)[idx: idx + 1], 16)
            res = "" + res + "" + ("%x" % (digitA ^ digitB))
            idx = idx + 1
        return res

    def hex2array(self, hexstr):
        # hexlen
        res = []
        # idx
        # digit
        hexlen = len(hexstr)
        del res[:]

        idx = hexlen
        while idx > 0:
            idx = idx - 1
            digit = int((hexstr)[idx: idx + 1], 16)
            res.append(((digit) & (1)))
            res.append((((digit >> 1)) & (1)))
            res.append((((digit >> 2)) & (1)))
            res.append((((digit >> 3)) & (1)))

        return res

    def nextInputChain(self):
        """
        Continues the enumeration of digital input chains started using yFirstInputChain().
        Caution: You can't make any assumption about the returned digital input chains order.
        If you want to find a specific a digital input chain, use InputChain.findInputChain()
        and a hardwareID or a logical name.

        @return a pointer to a YInputChain object, corresponding to
                a digital input chain currently online, or a None pointer
                if there are no more digital input chains to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YInputChain.FindInputChain(hwidRef.value)

#--- (end of YInputChain implementation)

#--- (YInputChain functions)

    @staticmethod
    def FirstInputChain():
        """
        Starts the enumeration of digital input chains currently accessible.
        Use the method YInputChain.nextInputChain() to iterate on
        next digital input chains.

        @return a pointer to a YInputChain object, corresponding to
                the first digital input chain currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("InputChain", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YInputChain.FindInputChain(serialRef.value + "." + funcIdRef.value)

#--- (end of YInputChain functions)
