# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id:yocto_micropython.py version 2.1.16635 (build 76635) $
#
#  Implements yFindMicroPython(), the high-level API for MicroPython functions
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

#--- (generated code: YMicroPython class start)
#noinspection PyProtectedMember
class YMicroPython(YFunction):
    """
    The YMicroPython class provides control of the MicroPython interpreter
    that can be found on some Yoctopuce devices.

    """
    #--- (end of generated code: YMicroPython class start)
    #--- (generated code: YMicroPython return codes)
    #--- (end of generated code: YMicroPython return codes)
    #--- (generated code: YMicroPython dlldef)
    #--- (end of generated code: YMicroPython dlldef)
    #--- (generated code: YMicroPython yapiwrapper)
    #--- (end of generated code: YMicroPython yapiwrapper)
    #--- (generated code: YMicroPython definitions)
    LASTMSG_INVALID = YAPI.INVALID_STRING
    HEAPUSAGE_INVALID = YAPI.INVALID_UINT
    HEAPFRAG_INVALID = YAPI.INVALID_UINT
    XHEAPUSAGE_INVALID = YAPI.INVALID_UINT
    STACKUSAGE_INVALID = YAPI.INVALID_UINT
    CURRENTSCRIPT_INVALID = YAPI.INVALID_STRING
    STARTUPSCRIPT_INVALID = YAPI.INVALID_STRING
    STARTUPDELAY_INVALID = YAPI.INVALID_DOUBLE
    COMMAND_INVALID = YAPI.INVALID_STRING
    VMSTATE_UNAVAILABLE = 0
    VMSTATE_RESET = 1
    VMSTATE_PENDING = 2
    VMSTATE_RUNNING = 3
    VMSTATE_PAUSED = 4
    VMSTATE_IDLE = 5
    VMSTATE_ERROR = 6
    VMSTATE_INVALID = -1
    DEBUGMODE_OFF = 0
    DEBUGMODE_ON = 1
    DEBUGMODE_INVALID = -1
    #--- (end of generated code: YMicroPython definitions)

    def __init__(self, func):
        super(YMicroPython, self).__init__(func)
        self._className = 'MicroPython'
        #--- (generated code: YMicroPython attributes)
        self._callback = None
        self._lastMsg = YMicroPython.LASTMSG_INVALID
        self._heapUsage = YMicroPython.HEAPUSAGE_INVALID
        self._heapFrag = YMicroPython.HEAPFRAG_INVALID
        self._xheapUsage = YMicroPython.XHEAPUSAGE_INVALID
        self._stackUsage = YMicroPython.STACKUSAGE_INVALID
        self._vmState = YMicroPython.VMSTATE_INVALID
        self._currentScript = YMicroPython.CURRENTSCRIPT_INVALID
        self._startupScript = YMicroPython.STARTUPSCRIPT_INVALID
        self._startupDelay = YMicroPython.STARTUPDELAY_INVALID
        self._debugMode = YMicroPython.DEBUGMODE_INVALID
        self._command = YMicroPython.COMMAND_INVALID
        self._logCallback = None
        self._isFirstCb = 0
        self._prevCbPos = 0
        self._logPos = 0
        self._prevPartialLog = ''
        #--- (end of generated code: YMicroPython attributes)

    #--- (generated code: YMicroPython implementation)
    def _parseAttr(self, json_val):
        if json_val.has("lastMsg"):
            self._lastMsg = json_val.getString("lastMsg")
        if json_val.has("heapUsage"):
            self._heapUsage = json_val.getInt("heapUsage")
        if json_val.has("heapFrag"):
            self._heapFrag = json_val.getInt("heapFrag")
        if json_val.has("xheapUsage"):
            self._xheapUsage = json_val.getInt("xheapUsage")
        if json_val.has("stackUsage"):
            self._stackUsage = json_val.getInt("stackUsage")
        if json_val.has("vmState"):
            self._vmState = json_val.getInt("vmState")
        if json_val.has("currentScript"):
            self._currentScript = json_val.getString("currentScript")
        if json_val.has("startupScript"):
            self._startupScript = json_val.getString("startupScript")
        if json_val.has("startupDelay"):
            self._startupDelay = round(json_val.getDouble("startupDelay") / 65.536) / 1000.0
        if json_val.has("debugMode"):
            self._debugMode = json_val.getInt("debugMode") > 0
        if json_val.has("command"):
            self._command = json_val.getString("command")
        super(YMicroPython, self)._parseAttr(json_val)

    def get_lastMsg(self):
        """
        Returns the last message produced by a python script.

        @return a string corresponding to the last message produced by a python script

        On failure, throws an exception or returns YMicroPython.LASTMSG_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.LASTMSG_INVALID
        res = self._lastMsg
        return res

    def get_heapUsage(self):
        """
        Returns the percentage of MicroPython main memory in use,
        as observed at the end of the last garbage collection.

        @return an integer corresponding to the percentage of MicroPython main memory in use,
                as observed at the end of the last garbage collection

        On failure, throws an exception or returns YMicroPython.HEAPUSAGE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.HEAPUSAGE_INVALID
        res = self._heapUsage
        return res

    def get_heapFrag(self):
        """
        Returns the fragmentation ratio of MicroPython main memory,
        as observed at the end of the last garbage collection.

        @return an integer corresponding to the fragmentation ratio of MicroPython main memory,
                as observed at the end of the last garbage collection

        On failure, throws an exception or returns YMicroPython.HEAPFRAG_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.HEAPFRAG_INVALID
        res = self._heapFrag
        return res

    def get_xheapUsage(self):
        """
        Returns the percentage of MicroPython external memory in use,
        as observed at the end of the last garbage collection.

        @return an integer corresponding to the percentage of MicroPython external memory in use,
                as observed at the end of the last garbage collection

        On failure, throws an exception or returns YMicroPython.XHEAPUSAGE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.XHEAPUSAGE_INVALID
        res = self._xheapUsage
        return res

    def get_stackUsage(self):
        """
        Returns the maximum percentage of MicroPython call stack in use,
        as observed at the end of the last garbage collection.

        @return an integer corresponding to the maximum percentage of MicroPython call stack in use,
                as observed at the end of the last garbage collection

        On failure, throws an exception or returns YMicroPython.STACKUSAGE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.STACKUSAGE_INVALID
        res = self._stackUsage
        return res

    def get_vmState(self):
        """
        Returns the current state of the virtual machine.

        @return a value among YMicroPython.VMSTATE_UNAVAILABLE, YMicroPython.VMSTATE_RESET,
        YMicroPython.VMSTATE_PENDING, YMicroPython.VMSTATE_RUNNING, YMicroPython.VMSTATE_PAUSED,
        YMicroPython.VMSTATE_IDLE and YMicroPython.VMSTATE_ERROR corresponding to the current state of the
        virtual machine

        On failure, throws an exception or returns YMicroPython.VMSTATE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.VMSTATE_INVALID
        res = self._vmState
        return res

    def get_currentScript(self):
        """
        Returns the name of currently active script, if any.

        @return a string corresponding to the name of currently active script, if any

        On failure, throws an exception or returns YMicroPython.CURRENTSCRIPT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.CURRENTSCRIPT_INVALID
        res = self._currentScript
        return res

    def set_currentScript(self, newval):
        """
        Stops current running script, and/or selects a script to run immediately in a
        fresh new environment. If the MicroPython interpreter is busy running a script,
        this function will abort it immediately and reset the execution environment.
        If a non-empty string is given as argument, the new script will be started.

        @param newval : a string

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("currentScript", rest_val)

    def get_startupScript(self):
        """
        Returns the name of the script to run when the device is powered on.

        @return a string corresponding to the name of the script to run when the device is powered on

        On failure, throws an exception or returns YMicroPython.STARTUPSCRIPT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.STARTUPSCRIPT_INVALID
        res = self._startupScript
        return res

    def set_startupScript(self, newval):
        """
        Changes the script to run when the device is powered on.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : a string corresponding to the script to run when the device is powered on

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("startupScript", rest_val)

    def set_startupDelay(self, newval):
        """
        Changes the wait time before running the startup script on power on, between 0.1
        second and 25 seconds. Remember to call the saveToFlash() method of the
        module if the modification must be kept.

        @param newval : a floating point number corresponding to the wait time before running the startup
        script on power on, between 0.1
                second and 25 seconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("startupDelay", rest_val)

    def get_startupDelay(self):
        """
        Returns the wait time before running the startup script on power on,
        measured in seconds.

        @return a floating point number corresponding to the wait time before running the startup script on power on,
                measured in seconds

        On failure, throws an exception or returns YMicroPython.STARTUPDELAY_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.STARTUPDELAY_INVALID
        res = self._startupDelay
        return res

    def get_debugMode(self):
        """
        Returns the activation state of MicroPython debugging interface.

        @return either YMicroPython.DEBUGMODE_OFF or YMicroPython.DEBUGMODE_ON, according to the activation
        state of MicroPython debugging interface

        On failure, throws an exception or returns YMicroPython.DEBUGMODE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.DEBUGMODE_INVALID
        res = self._debugMode
        return res

    def set_debugMode(self, newval):
        """
        Changes the activation state of MicroPython debugging interface.

        @param newval : either YMicroPython.DEBUGMODE_OFF or YMicroPython.DEBUGMODE_ON, according to the
        activation state of MicroPython debugging interface

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("debugMode", rest_val)

    def get_command(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YMicroPython.COMMAND_INVALID
        res = self._command
        return res

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindMicroPython(func):
        """
        Retrieves a MicroPython interpreter for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the MicroPython interpreter is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YMicroPython.isOnline() to test if the MicroPython interpreter is
        indeed online at a given time. In case of ambiguity when looking for
        a MicroPython interpreter by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the MicroPython interpreter, for instance
                MyDevice.microPython.

        @return a YMicroPython object allowing you to drive the MicroPython interpreter.
        """
        # obj
        obj = YFunction._FindFromCache("MicroPython", func)
        if obj is None:
            obj = YMicroPython(func)
            YFunction._AddToCache("MicroPython", func, obj)
        return obj

    def eval(self, pythonExpr):
        """
        Submit a short expression to MicroPython interpreter, and return
        the output produced by its evaluation.

        There is no implicit reset of the MicroPython virtual machine
        with this function: all global symbols defined by code that
        has run since last reset can be accessed freely. But if the
        interpreter is not at rest when the function is invoked, the
        call will fail.

        Use method reset() if you need to start
        from a fresh environment before starting the evaluation.

        The expression is limited to about 120 ASCII characters.
        If you need to evaluate more complex code, use the exec()
        method to define it as a function, check for exec completion
        using get_vmState() and then use eval()
        actually run that function and capture its output.

        @param pythonExpr : Short Python expression to be evaluated

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # state
        # content
        # endPos
        # lenLen
        # lenStr
        # res
        # url
        # contentStr
        # // Make sure the VM is ready to handle the evaluation

        state = (self.get_advertisedValue())[0: 0 + 1]
        if not ("zix".find(state) >= 0):
            self._throw(YAPI.DEVICE_BUSY, "MicroPython VM is not at rest")
            return ""
        # // Retrieve current MicroPython console position (avoid transmitting current content if possible)
        content = self._download("mpy.txt?pos=2111222333")
        endPos = len(content) - 1
        while (endPos >= 0) and (content[endPos] != 64):
            endPos = endPos - 1
        if not (endPos > 0):
            self._throw(YAPI.IO_ERROR, "failed to download MicroPython logs")
            return ""
        lenLen = len(content) - endPos - 1
        lenStr = content[endPos + 1:endPos + 1+lenLen].decode('utf-8')
        # // trigger the evaluation
        res = self.set_command("?" + pythonExpr)
        if not (res == YAPI.SUCCESS):
            self._throw(res, "failed to trigger evaluation")
            return ""
        # // wait for the evaluation to complete
        state = (self.get_advertisedValue())[0: 0 + 1]
        while "ix".find(state) < 0:
            YAPI.Sleep(50)
            state = (self.get_advertisedValue())[0: 0 + 1]
        # // download the logs after the evaluation
        url = "mpy.txt?pos=" + lenStr
        content = self._download(url)
        endPos = len(content) - 1
        while (endPos >= 0) and (content[endPos] != 64):
            endPos = endPos - 1
        if not (endPos > 0):
            self._throw(YAPI.IO_ERROR, "failed to download MicroPython logs")
            return ""
        contentStr = content[0:0+endPos - 1].decode('utf-8')
        return contentStr

    def exec(self, codeName, mpyCode):
        """
        Submit Python code for execution in the MicroPython interpreter.
        If the MicroPython interpreter is busy, this function will
        block until it becomes available. The code is then uploaded,
        compiled unless it is already a MicroPython precompiled file,
        and executed on the fly, without beeing stored on the device
        filesystem. This method does not wait for the completion
        if the code execution.

        There is no implicit reset of the MicroPython interpreter with
        this function. Use method reset() if you need to start
        from a fresh environment to run your code.

        Note that although MicroPython is mostly compatible with recent Python 3.x
        interpreters, the limited ressources on the device impose some restrictions,
        in particular regarding the libraries that can be used. Please refer to
        the documentation for more details.

        @param codeName : name of the code buffer, with a .py extension
                for source code and a .mpy extension for a precompiled file.
        @param mpyCode : binary buffer containing MicroPython code to execute

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # fullname
        # res
        fullname = "mpy:" + codeName
        res = self._upload(fullname, mpyCode)
        return res

    def reset(self):
        """
        Stops current execution, and reset the MicroPython interpreter to initial state.
        All global variables are cleared, and all imports are forgotten.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # res
        # state

        res = self.set_command("Z")
        if not (res == YAPI.SUCCESS):
            self._throw(YAPI.IO_ERROR, "unable to trigger MicroPython reset")
            return YAPI.IO_ERROR
        # // Wait until the reset is effective
        state = (self.get_advertisedValue())[0: 0 + 1]
        while not (state == "z"):
            YAPI.Sleep(50)
            state = (self.get_advertisedValue())[0: 0 + 1]
        return YAPI.SUCCESS

    def run(self, codeFileName):
        """
        Reset the MicroPython interpreter to its initial state, and start the specified
        program, which must have been previously uploaded to the device.

        @param codeFileName : filename of the MicroPython code to run

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # currentScript

        currentScript = self.get_currentScript()
        if currentScript == codeFileName:
            # // set_currentScript does nothing when the script name is unchanged,
            # // so in this case we need to force a VM reset
            self.set_command("Z")
        return self.set_currentScript(codeFileName)

    def clearLogs(self):
        """
        Clears MicroPython interpreter console log buffer.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # res

        res = self.set_command("z")
        return res

    def get_lastLogs(self):
        """
        Returns a string with last logs of the MicroPython interpreter.
        This method return only logs that are still in the module.

        @return a string with last MicroPython logs.
                On failure, throws an exception or returns  YAPI.INVALID_STRING.
        """
        # buff
        # bufflen

        buff = self._download("mpy.txt")
        bufflen = len(buff) - 1
        while (bufflen > 0) and (buff[bufflen] != 64):
            bufflen = bufflen - 1
        return buff[0:0+bufflen].decode('utf-8')

    def registerLogCallback(self, callback):
        """
        Registers a device log callback function. This callback will be called each time
        microPython sends a new log message.

        @param callback : the callback function to invoke, or a None pointer.
                The callback function should take two arguments:
                the module object that emitted the log message,
                and the character string containing the log.
                On failure, throws an exception or returns a negative error code.
        """
        # serial

        serial = self.get_serialNumber()
        if serial == YAPI.INVALID_STRING:
            return YAPI.DEVICE_NOT_FOUND
        self._logCallback = callback
        self._isFirstCb = True
        if callback is not None:
            self.registerValueCallback(yInternalEventCallback)
        else:
            self.registerValueCallback(None)
        return 0

    def get_logCallback(self):
        return self._logCallback

    def _internalEventHandler(self, cbVal):
        # cbPos
        # cbDPos
        # url
        # content
        # endPos
        # lenLen
        # lenStr
        # msgPos
        # msgEnd
        # logMsg
        # // detect possible power cycle of the reader to clear event pointer
        cbPos = int((cbVal)[1: 1 + len(cbVal)-1], 16)
        cbDPos = ((cbPos - self._prevCbPos) & (0xfffff))
        self._prevCbPos = cbPos
        if cbDPos > 65536:
            self._logPos = 0
        if not (self._logCallback is not None):
            return YAPI.SUCCESS
        if self._isFirstCb:
            # // use first emulated value callback caused by registerValueCallback:
            # // to retrieve current logs position
            self._logPos = 0
            self._prevPartialLog = ""
            url = "mpy.txt"
        else:
            # // load all messages since previous call
            url = "mpy.txt?pos=" + str(int(self._logPos))

        content = self._download(url)
        # // look for new position indicator at end of logs
        endPos = len(content) - 1
        while (endPos >= 0) and (content[endPos] != 64):
            endPos = endPos - 1
        if not (endPos > 0):
            self._throw(YAPI.IO_ERROR, "fail to download MicroPython logs")
            return YAPI.IO_ERROR
        lenLen = len(content) - endPos - 1
        lenStr = content[endPos + 1:endPos + 1+lenLen].decode('utf-8')
        # // update processed event position pointer
        self._logPos = YAPI._atoi(lenStr)
        if self._isFirstCb:
            # // don't generate callbacks log messages before call to registerLogCallback
            self._isFirstCb = False
            return YAPI.SUCCESS
        endPos = endPos - 1
        if not (content[endPos] == 10):
            self._throw(YAPI.IO_ERROR, "fail to download MicroPython logs")
            return YAPI.IO_ERROR
        if endPos == 0:
            return YAPI.SUCCESS
        # // now generate callbacks for each complete log line
        msgPos = 0
        msgEnd = 0
        while (msgEnd < endPos) and (content[msgEnd] != 10):
            msgEnd = msgEnd + 1
        logMsg = content[msgPos:msgPos+msgEnd - msgPos].decode('utf-8')
        logMsg = "" + self._prevPartialLog + "" + logMsg
        if msgEnd < endPos:
            if self._logCallback is not None:
                self._logCallback(self, logMsg)
        else:
            self._prevPartialLog = logMsg
        while msgEnd < endPos:
            msgPos = msgEnd + 1
            msgEnd = msgPos
            while (msgEnd < endPos) and (content[msgEnd] != 10):
                msgEnd = msgEnd + 1
            logMsg = content[msgPos:msgPos+msgEnd - msgPos].decode('utf-8')
            if msgEnd < endPos:
                if self._logCallback is not None:
                    self._logCallback(self, logMsg)
            else:
                self._prevPartialLog = logMsg
        return YAPI.SUCCESS

    def nextMicroPython(self):
        """
        Continues the enumeration of MicroPython interpreters started using yFirstMicroPython().
        Caution: You can't make any assumption about the returned MicroPython interpreters order.
        If you want to find a specific a MicroPython interpreter, use MicroPython.findMicroPython()
        and a hardwareID or a logical name.

        @return a pointer to a YMicroPython object, corresponding to
                a MicroPython interpreter currently online, or a None pointer
                if there are no more MicroPython interpreters to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YMicroPython.FindMicroPython(hwidRef.value)

#--- (end of generated code: YMicroPython implementation)

#--- (generated code: YMicroPython functions)

    @staticmethod
    def FirstMicroPython():
        """
        Starts the enumeration of MicroPython interpreters currently accessible.
        Use the method YMicroPython.nextMicroPython() to iterate on
        next MicroPython interpreters.

        @return a pointer to a YMicroPython object, corresponding to
                the first MicroPython interpreter currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("MicroPython", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YMicroPython.FindMicroPython(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: YMicroPython functions)
