# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: yocto_sdi12port.py 52939 2023-01-26 11:12:44Z mvuilleu $
#
#  Implements yFindSdi12Port(), the high-level API for Sdi12Port functions
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


#--- (generated code: YSdi12SnoopingRecord class start)
#noinspection PyProtectedMember
class YSdi12SnoopingRecord(object):
    #--- (end of generated code: YSdi12SnoopingRecord class start)
    #--- (generated code: YSdi12SnoopingRecord definitions)
    #--- (end of generated code: YSdi12SnoopingRecord definitions)

    def __init__(self, json_str):
        #--- (generated code: YSdi12SnoopingRecord attributes)
        self._tim = 0
        self._pos = 0
        self._dir = 0
        self._msg = ''
        #--- (end of generated code: YSdi12SnoopingRecord attributes)
        json = YJSONObject(json_str, 0, len(json_str))
        json.parse()
        if json.has("t"):
            self._tim = json.getInt("t")
        if json.has("p"):
            self._pos = json.getInt("p")
        if json.has("m"):
            m = json.getString("m")
            if m[0] == '<':
                self._dir = 1
            else:
                self._dir = 0
            self._msg = m[1:]

    #--- (generated code: YSdi12SnoopingRecord implementation)
    def get_time(self):
        """
        Returns the elapsed time, in ms, since the beginning of the preceding message.

        @return the elapsed time, in ms, since the beginning of the preceding message.
        """
        return self._tim

    def get_pos(self):
        """
        Returns the absolute position of the message end.

        @return the absolute position of the message end.
        """
        return self._pos

    def get_direction(self):
        """
        Returns the message direction (RX=0, TX=1).

        @return the message direction (RX=0, TX=1).
        """
        return self._dir

    def get_message(self):
        """
        Returns the message content.

        @return the message content.
        """
        return self._msg

#--- (end of generated code: YSdi12SnoopingRecord implementation)

#--- (generated code: YSdi12SnoopingRecord functions)
#--- (end of generated code: YSdi12SnoopingRecord functions)

#--- (generated code: YSdi12SensorInfo class start)
#noinspection PyProtectedMember
class YSdi12SensorInfo(object):
    #--- (end of generated code: YSdi12SensorInfo class start)
    #--- (generated code: YSdi12SensorInfo definitions)
    #--- (end of generated code: YSdi12SensorInfo definitions)

    def __init__(self, YSdi12Port, json_str):
        #--- (generated code: YSdi12SensorInfo attributes)
        self._sdi12Port = None
        self._isValid = 0
        self._addr = ''
        self._proto = ''
        self._mfg = ''
        self._model = ''
        self._ver = ''
        self._sn = ''
        self._valuesDesc = []
        #--- (end of generated code: YSdi12SensorInfo attributes)
        self._sdi12Port = YSdi12Port
        self._parseInfoStr(json_str)

    def _throw(self, errcode, msg):
        self._sdi12Port._throw(errcode,msg)

    #--- (generated code: YSdi12SensorInfo implementation)
    def isValid(self):
        """
        Returns the sensor state.

        @return the sensor state.
        """
        return self._isValid

    def get_sensorAddress(self):
        """
        Returns the sensor address.

        @return the sensor address.
        """
        return self._addr

    def get_sensorProtocol(self):
        """
        Returns the compatible SDI-12 version of the sensor.

        @return the compatible SDI-12 version of the sensor.
        """
        return self._proto

    def get_sensorVendor(self):
        """
        Returns the sensor vendor identification.

        @return the sensor vendor identification.
        """
        return self._mfg

    def get_sensorModel(self):
        """
        Returns the sensor model number.

        @return the sensor model number.
        """
        return self._model

    def get_sensorVersion(self):
        """
        Returns the sensor version.

        @return the sensor version.
        """
        return self._ver

    def get_sensorSerial(self):
        """
        Returns the sensor serial number.

        @return the sensor serial number.
        """
        return self._sn

    def get_measureCount(self):
        """
        Returns the number of sensor measurements.
        This function only works if the sensor is in version 1.4 SDI-12
        and supports metadata commands.

        @return the number of sensor measurements.
        """
        return len(self._valuesDesc)

    def get_measureCommand(self, measureIndex):
        """
        Returns the sensor measurement command.
        This function only works if the sensor is in version 1.4 SDI-12
        and supports metadata commands.

        @param measureIndex : measurement index

        @return the sensor measurement command.
                On failure, throws an exception or returns an empty string.
        """
        if not (measureIndex < len(self._valuesDesc)):
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid measure index")
            return ""
        return self._valuesDesc[measureIndex][0]

    def get_measurePosition(self, measureIndex):
        """
        Returns sensor measurement position.
        This function only works if the sensor is in version 1.4 SDI-12
        and supports metadata commands.

        @param measureIndex : measurement index

        @return the sensor measurement command.
                On failure, throws an exception or returns 0.
        """
        if not (measureIndex < len(self._valuesDesc)):
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid measure index")
            return 0
        return YAPI._atoi(self._valuesDesc[measureIndex][2])

    def get_measureSymbol(self, measureIndex):
        """
        Returns the measured value symbol.
        This function only works if the sensor is in version 1.4 SDI-12
        and supports metadata commands.

        @param measureIndex : measurement index

        @return the sensor measurement command.
                On failure, throws an exception or returns an empty string.
        """
        if not (measureIndex < len(self._valuesDesc)):
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid measure index")
            return ""
        return self._valuesDesc[measureIndex][3]

    def get_measureUnit(self, measureIndex):
        """
        Returns the unit of the measured value.
        This function only works if the sensor is in version 1.4 SDI-12
        and supports metadata commands.

        @param measureIndex : measurement index

        @return the sensor measurement command.
                On failure, throws an exception or returns an empty string.
        """
        if not (measureIndex < len(self._valuesDesc)):
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid measure index")
            return ""
        return self._valuesDesc[measureIndex][4]

    def get_measureDescription(self, measureIndex):
        """
        Returns the description of the measured value.
        This function only works if the sensor is in version 1.4 SDI-12
        and supports metadata commands.

        @param measureIndex : measurement index

        @return the sensor measurement command.
                On failure, throws an exception or returns an empty string.
        """
        if not (measureIndex < len(self._valuesDesc)):
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid measure index")
            return ""
        return self._valuesDesc[measureIndex][5]

    def get_typeMeasure(self):
        return self._valuesDesc

    def _parseInfoStr(self, infoStr):
        # errmsg

        if len(infoStr) > 1:
            if (infoStr)[0: 0 + 2] == "ER":
                errmsg = (infoStr)[2: 2 + len(infoStr)-2]
                self._addr = errmsg
                self._proto = errmsg
                self._mfg = errmsg
                self._model = errmsg
                self._ver = errmsg
                self._sn = errmsg
                self._isValid = False
            else:
                self._addr = (infoStr)[0: 0 + 1]
                self._proto = (infoStr)[1: 1 + 2]
                self._mfg = (infoStr)[3: 3 + 8]
                self._model = (infoStr)[11: 11 + 6]
                self._ver = (infoStr)[17: 17 + 3]
                self._sn = (infoStr)[20: 20 + len(infoStr)-20]
                self._isValid = True

    def _queryValueInfo(self):
        val = []
        data = []
        # infoNbVal
        # cmd
        # infoVal
        # value
        # nbVal
        # k
        # i
        # j
        listVal = []
        # size

        k = 0
        size = 4
        while k < 10:
            infoNbVal = self._sdi12Port.querySdi12(self._addr, "IM" + str(int(k)), 5000)
            if len(infoNbVal) > 1:
                value = (infoNbVal)[4: 4 + len(infoNbVal)-4]
                nbVal = YAPI._atoi(value)
                if nbVal != 0:
                    del val[:]
                    i = 0
                    while i < nbVal:
                        cmd = "IM" + str(int(k)) + "_00" + str(int(i+1))
                        infoVal = self._sdi12Port.querySdi12(self._addr, cmd, 5000)
                        data = (infoVal).split(';')
                        data = (data[0]).split(',')
                        del listVal[:]
                        listVal.append("M" + str(int(k)))
                        listVal.append(str(i+1))
                        j = 0
                        while len(data) < size:
                            data.append("")
                        while j < len(data):
                            listVal.append(data[j])
                            j = j + 1
                        val.append(listVal[:])
                        i = i + 1
            k = k + 1
        self._valuesDesc = val

#--- (end of generated code: YSdi12SensorInfo implementation)

#--- (generated code: YSdi12SensorInfo functions)
#--- (end of generated code: YSdi12SensorInfo functions)


#--- (generated code: YSdi12Port class start)
#noinspection PyProtectedMember
class YSdi12Port(YFunction):
    """
    The YSdi12Port class allows you to fully drive a Yoctopuce SDI12 port.
    It can be used to send and receive data, and to configure communication
    parameters (baud rate, bit count, parity, flow control and protocol).
    Note that Yoctopuce SDI12 ports are not exposed as virtual COM ports.
    They are meant to be used in the same way as all Yoctopuce devices.

    """
    #--- (end of generated code: YSdi12Port class start)
    #--- (generated code: YSdi12Port return codes)
    #--- (end of generated code: YSdi12Port return codes)
    #--- (generated code: YSdi12Port dlldef)
    #--- (end of generated code: YSdi12Port dlldef)
    #--- (generated code: YSdi12Port yapiwrapper)
    #--- (end of generated code: YSdi12Port yapiwrapper)
    #--- (generated code: YSdi12Port definitions)
    RXCOUNT_INVALID = YAPI.INVALID_UINT
    TXCOUNT_INVALID = YAPI.INVALID_UINT
    ERRCOUNT_INVALID = YAPI.INVALID_UINT
    RXMSGCOUNT_INVALID = YAPI.INVALID_UINT
    TXMSGCOUNT_INVALID = YAPI.INVALID_UINT
    LASTMSG_INVALID = YAPI.INVALID_STRING
    CURRENTJOB_INVALID = YAPI.INVALID_STRING
    STARTUPJOB_INVALID = YAPI.INVALID_STRING
    JOBMAXTASK_INVALID = YAPI.INVALID_UINT
    JOBMAXSIZE_INVALID = YAPI.INVALID_UINT
    COMMAND_INVALID = YAPI.INVALID_STRING
    PROTOCOL_INVALID = YAPI.INVALID_STRING
    SERIALMODE_INVALID = YAPI.INVALID_STRING
    VOLTAGELEVEL_OFF = 0
    VOLTAGELEVEL_TTL3V = 1
    VOLTAGELEVEL_TTL3VR = 2
    VOLTAGELEVEL_TTL5V = 3
    VOLTAGELEVEL_TTL5VR = 4
    VOLTAGELEVEL_RS232 = 5
    VOLTAGELEVEL_RS485 = 6
    VOLTAGELEVEL_TTL1V8 = 7
    VOLTAGELEVEL_SDI12 = 8
    VOLTAGELEVEL_INVALID = -1
    #--- (end of generated code: YSdi12Port definitions)

    def __init__(self, func):
        super(YSdi12Port, self).__init__(func)
        self._className = 'Sdi12Port'
        #--- (generated code: YSdi12Port attributes)
        self._callback = None
        self._rxCount = YSdi12Port.RXCOUNT_INVALID
        self._txCount = YSdi12Port.TXCOUNT_INVALID
        self._errCount = YSdi12Port.ERRCOUNT_INVALID
        self._rxMsgCount = YSdi12Port.RXMSGCOUNT_INVALID
        self._txMsgCount = YSdi12Port.TXMSGCOUNT_INVALID
        self._lastMsg = YSdi12Port.LASTMSG_INVALID
        self._currentJob = YSdi12Port.CURRENTJOB_INVALID
        self._startupJob = YSdi12Port.STARTUPJOB_INVALID
        self._jobMaxTask = YSdi12Port.JOBMAXTASK_INVALID
        self._jobMaxSize = YSdi12Port.JOBMAXSIZE_INVALID
        self._command = YSdi12Port.COMMAND_INVALID
        self._protocol = YSdi12Port.PROTOCOL_INVALID
        self._voltageLevel = YSdi12Port.VOLTAGELEVEL_INVALID
        self._serialMode = YSdi12Port.SERIALMODE_INVALID
        self._rxptr = 0
        self._rxbuff = bytearray()
        self._rxbuffptr = 0
        self._eventPos = 0
        #--- (end of generated code: YSdi12Port attributes)

    #--- (generated code: YSdi12Port implementation)
    def _parseAttr(self, json_val):
        if json_val.has("rxCount"):
            self._rxCount = json_val.getInt("rxCount")
        if json_val.has("txCount"):
            self._txCount = json_val.getInt("txCount")
        if json_val.has("errCount"):
            self._errCount = json_val.getInt("errCount")
        if json_val.has("rxMsgCount"):
            self._rxMsgCount = json_val.getInt("rxMsgCount")
        if json_val.has("txMsgCount"):
            self._txMsgCount = json_val.getInt("txMsgCount")
        if json_val.has("lastMsg"):
            self._lastMsg = json_val.getString("lastMsg")
        if json_val.has("currentJob"):
            self._currentJob = json_val.getString("currentJob")
        if json_val.has("startupJob"):
            self._startupJob = json_val.getString("startupJob")
        if json_val.has("jobMaxTask"):
            self._jobMaxTask = json_val.getInt("jobMaxTask")
        if json_val.has("jobMaxSize"):
            self._jobMaxSize = json_val.getInt("jobMaxSize")
        if json_val.has("command"):
            self._command = json_val.getString("command")
        if json_val.has("protocol"):
            self._protocol = json_val.getString("protocol")
        if json_val.has("voltageLevel"):
            self._voltageLevel = json_val.getInt("voltageLevel")
        if json_val.has("serialMode"):
            self._serialMode = json_val.getString("serialMode")
        super(YSdi12Port, self)._parseAttr(json_val)

    def get_rxCount(self):
        """
        Returns the total number of bytes received since last reset.

        @return an integer corresponding to the total number of bytes received since last reset

        On failure, throws an exception or returns YSdi12Port.RXCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.RXCOUNT_INVALID
        res = self._rxCount
        return res

    def get_txCount(self):
        """
        Returns the total number of bytes transmitted since last reset.

        @return an integer corresponding to the total number of bytes transmitted since last reset

        On failure, throws an exception or returns YSdi12Port.TXCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.TXCOUNT_INVALID
        res = self._txCount
        return res

    def get_errCount(self):
        """
        Returns the total number of communication errors detected since last reset.

        @return an integer corresponding to the total number of communication errors detected since last reset

        On failure, throws an exception or returns YSdi12Port.ERRCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.ERRCOUNT_INVALID
        res = self._errCount
        return res

    def get_rxMsgCount(self):
        """
        Returns the total number of messages received since last reset.

        @return an integer corresponding to the total number of messages received since last reset

        On failure, throws an exception or returns YSdi12Port.RXMSGCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.RXMSGCOUNT_INVALID
        res = self._rxMsgCount
        return res

    def get_txMsgCount(self):
        """
        Returns the total number of messages send since last reset.

        @return an integer corresponding to the total number of messages send since last reset

        On failure, throws an exception or returns YSdi12Port.TXMSGCOUNT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.TXMSGCOUNT_INVALID
        res = self._txMsgCount
        return res

    def get_lastMsg(self):
        """
        Returns the latest message fully received.

        @return a string corresponding to the latest message fully received

        On failure, throws an exception or returns YSdi12Port.LASTMSG_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.LASTMSG_INVALID
        res = self._lastMsg
        return res

    def get_currentJob(self):
        """
        Returns the name of the job file currently in use.

        @return a string corresponding to the name of the job file currently in use

        On failure, throws an exception or returns YSdi12Port.CURRENTJOB_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.CURRENTJOB_INVALID
        res = self._currentJob
        return res

    def set_currentJob(self, newval):
        """
        Selects a job file to run immediately. If an empty string is
        given as argument, stops running current job file.

        @param newval : a string

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("currentJob", rest_val)

    def get_startupJob(self):
        """
        Returns the job file to use when the device is powered on.

        @return a string corresponding to the job file to use when the device is powered on

        On failure, throws an exception or returns YSdi12Port.STARTUPJOB_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.STARTUPJOB_INVALID
        res = self._startupJob
        return res

    def set_startupJob(self, newval):
        """
        Changes the job to use when the device is powered on.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : a string corresponding to the job to use when the device is powered on

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("startupJob", rest_val)

    def get_jobMaxTask(self):
        """
        Returns the maximum number of tasks in a job that the device can handle.

        @return an integer corresponding to the maximum number of tasks in a job that the device can handle

        On failure, throws an exception or returns YSdi12Port.JOBMAXTASK_INVALID.
        """
        # res
        if self._cacheExpiration == datetime.datetime.fromtimestamp(86400):
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.JOBMAXTASK_INVALID
        res = self._jobMaxTask
        return res

    def get_jobMaxSize(self):
        """
        Returns maximum size allowed for job files.

        @return an integer corresponding to maximum size allowed for job files

        On failure, throws an exception or returns YSdi12Port.JOBMAXSIZE_INVALID.
        """
        # res
        if self._cacheExpiration == datetime.datetime.fromtimestamp(86400):
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.JOBMAXSIZE_INVALID
        res = self._jobMaxSize
        return res

    def get_command(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.COMMAND_INVALID
        res = self._command
        return res

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    def get_protocol(self):
        """
        Returns the type of protocol used over the serial line, as a string.
        Possible values are "Line" for ASCII messages separated by CR and/or LF,
        "Frame:[timeout]ms" for binary messages separated by a delay time,
        "Char" for a continuous ASCII stream or
        "Byte" for a continuous binary stream.

        @return a string corresponding to the type of protocol used over the serial line, as a string

        On failure, throws an exception or returns YSdi12Port.PROTOCOL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.PROTOCOL_INVALID
        res = self._protocol
        return res

    def set_protocol(self, newval):
        """
        Changes the type of protocol used over the serial line.
        Possible values are "Line" for ASCII messages separated by CR and/or LF,
        "Frame:[timeout]ms" for binary messages separated by a delay time,
        "Char" for a continuous ASCII stream or
        "Byte" for a continuous binary stream.
        The suffix "/[wait]ms" can be added to reduce the transmit rate so that there
        is always at lest the specified number of milliseconds between each bytes sent.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : a string corresponding to the type of protocol used over the serial line

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("protocol", rest_val)

    def get_voltageLevel(self):
        """
        Returns the voltage level used on the serial line.

        @return a value among YSdi12Port.VOLTAGELEVEL_OFF, YSdi12Port.VOLTAGELEVEL_TTL3V,
        YSdi12Port.VOLTAGELEVEL_TTL3VR, YSdi12Port.VOLTAGELEVEL_TTL5V, YSdi12Port.VOLTAGELEVEL_TTL5VR,
        YSdi12Port.VOLTAGELEVEL_RS232, YSdi12Port.VOLTAGELEVEL_RS485, YSdi12Port.VOLTAGELEVEL_TTL1V8 and
        YSdi12Port.VOLTAGELEVEL_SDI12 corresponding to the voltage level used on the serial line

        On failure, throws an exception or returns YSdi12Port.VOLTAGELEVEL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.VOLTAGELEVEL_INVALID
        res = self._voltageLevel
        return res

    def set_voltageLevel(self, newval):
        """
        Changes the voltage type used on the serial line. Valid
        values  will depend on the Yoctopuce device model featuring
        the serial port feature.  Check your device documentation
        to find out which values are valid for that specific model.
        Trying to set an invalid value will have no effect.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : a value among YSdi12Port.VOLTAGELEVEL_OFF, YSdi12Port.VOLTAGELEVEL_TTL3V,
        YSdi12Port.VOLTAGELEVEL_TTL3VR, YSdi12Port.VOLTAGELEVEL_TTL5V, YSdi12Port.VOLTAGELEVEL_TTL5VR,
        YSdi12Port.VOLTAGELEVEL_RS232, YSdi12Port.VOLTAGELEVEL_RS485, YSdi12Port.VOLTAGELEVEL_TTL1V8 and
        YSdi12Port.VOLTAGELEVEL_SDI12 corresponding to the voltage type used on the serial line

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("voltageLevel", rest_val)

    def get_serialMode(self):
        """
        Returns the serial port communication parameters, as a string such as
        "1200,7E1,Simplex". The string includes the baud rate, the number of data bits,
        the parity, and the number of stop bits. The suffix "Simplex" denotes
        the fact that transmission in both directions is multiplexed on the
        same transmission line.

        @return a string corresponding to the serial port communication parameters, as a string such as
                "1200,7E1,Simplex"

        On failure, throws an exception or returns YSdi12Port.SERIALMODE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSdi12Port.SERIALMODE_INVALID
        res = self._serialMode
        return res

    def set_serialMode(self, newval):
        """
        Changes the serial port communication parameters, with a string such as
        "1200,7E1,Simplex". The string includes the baud rate, the number of data bits,
        the parity, and the number of stop bits. The suffix "Simplex" denotes
        the fact that transmission in both directions is multiplexed on the
        same transmission line.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : a string corresponding to the serial port communication parameters, with a string such as
                "1200,7E1,Simplex"

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("serialMode", rest_val)

    @staticmethod
    def FindSdi12Port(func):
        """
        Retrieves an SDI12 port for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the SDI12 port is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSdi12Port.isOnline() to test if the SDI12 port is
        indeed online at a given time. In case of ambiguity when looking for
        an SDI12 port by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the SDI12 port, for instance
                MyDevice.sdi12Port.

        @return a YSdi12Port object allowing you to drive the SDI12 port.
        """
        # obj
        obj = YFunction._FindFromCache("Sdi12Port", func)
        if obj is None:
            obj = YSdi12Port(func)
            YFunction._AddToCache("Sdi12Port", func, obj)
        return obj

    def sendCommand(self, text):
        return self.set_command(text)

    def readLine(self):
        """
        Reads a single line (or message) from the receive buffer, starting at current stream position.
        This function is intended to be used when the serial port is configured for a message protocol,
        such as 'Line' mode or frame protocols.

        If data at current stream position is not available anymore in the receive buffer,
        the function returns the oldest available line and moves the stream position just after.
        If no new full line is received, the function returns an empty line.

        @return a string with a single line of text

        On failure, throws an exception or returns a negative error code.
        """
        # url
        # msgbin
        msgarr = []
        # msglen
        # res

        url = "rxmsg.json?pos=" + str(int(self._rxptr)) + "&len=1&maxw=1"
        msgbin = self._download(url)
        msgarr = self._json_get_array(msgbin)
        msglen = len(msgarr)
        if msglen == 0:
            return ""
        # // last element of array is the new position
        msglen = msglen - 1
        self._rxptr = self._decode_json_int(msgarr[msglen])
        if msglen == 0:
            return ""
        res = self._json_get_string(msgarr[0])
        return res

    def readMessages(self, pattern, maxWait):
        """
        Searches for incoming messages in the serial port receive buffer matching a given pattern,
        starting at current position. This function will only compare and return printable characters
        in the message strings. Binary protocols are handled as hexadecimal strings.

        The search returns all messages matching the expression provided as argument in the buffer.
        If no matching message is found, the search waits for one up to the specified maximum timeout
        (in milliseconds).

        @param pattern : a limited regular expression describing the expected message format,
                or an empty string if all messages should be returned (no filtering).
                When using binary protocols, the format applies to the hexadecimal
                representation of the message.
        @param maxWait : the maximum number of milliseconds to wait for a message if none is found
                in the receive buffer.

        @return an array of strings containing the messages found, if any.
                Binary messages are converted to hexadecimal representation.

        On failure, throws an exception or returns an empty array.
        """
        # url
        # msgbin
        msgarr = []
        # msglen
        res = []
        # idx

        url = "rxmsg.json?pos=" + str(int(self._rxptr)) + "&maxw=" + str(int(maxWait)) + "&pat=" + pattern
        msgbin = self._download(url)
        msgarr = self._json_get_array(msgbin)
        msglen = len(msgarr)
        if msglen == 0:
            return res
        # // last element of array is the new position
        msglen = msglen - 1
        self._rxptr = self._decode_json_int(msgarr[msglen])
        idx = 0

        while idx < msglen:
            res.append(self._json_get_string(msgarr[idx]))
            idx = idx + 1

        return res

    def read_seek(self, absPos):
        """
        Changes the current internal stream position to the specified value. This function
        does not affect the device, it only changes the value stored in the API object
        for the next read operations.

        @param absPos : the absolute position index for next read operations.

        @return nothing.
        """
        self._rxptr = absPos
        return YAPI.SUCCESS

    def read_tell(self):
        """
        Returns the current absolute stream position pointer of the API object.

        @return the absolute position index for next read operations.
        """
        return self._rxptr

    def read_avail(self):
        """
        Returns the number of bytes available to read in the input buffer starting from the
        current absolute stream position pointer of the API object.

        @return the number of bytes available to read
        """
        # availPosStr
        # atPos
        # res
        # databin

        databin = self._download("rxcnt.bin?pos=" + str(int(self._rxptr)))
        availPosStr = databin.decode(YAPI.DefaultEncoding)
        atPos = availPosStr.find("@")
        res = YAPI._atoi((availPosStr)[0: 0 + atPos])
        return res

    def end_tell(self):
        # availPosStr
        # atPos
        # res
        # databin

        databin = self._download("rxcnt.bin?pos=" + str(int(self._rxptr)))
        availPosStr = databin.decode(YAPI.DefaultEncoding)
        atPos = availPosStr.find("@")
        res = YAPI._atoi((availPosStr)[atPos+1: atPos+1 + len(availPosStr)-atPos-1])
        return res

    def queryLine(self, query, maxWait):
        """
        Sends a text line query to the serial port, and reads the reply, if any.
        This function is intended to be used when the serial port is configured for 'Line' protocol.

        @param query : the line query to send (without CR/LF)
        @param maxWait : the maximum number of milliseconds to wait for a reply.

        @return the next text line received after sending the text query, as a string.
                Additional lines can be obtained by calling readLine or readMessages.

        On failure, throws an exception or returns an empty string.
        """
        # prevpos
        # url
        # msgbin
        msgarr = []
        # msglen
        # res
        if len(query) <= 80:
            # // fast query
            url = "rxmsg.json?len=1&maxw=" + str(int(maxWait)) + "&cmd=!" + self._escapeAttr(query)
        else:
            # // long query
            prevpos = self.end_tell()
            self._upload("txdata", bytearray(query + "\r\n", YAPI.DefaultEncoding))
            url = "rxmsg.json?len=1&maxw=" + str(int(maxWait)) + "&pos=" + str(int(prevpos))

        msgbin = self._download(url)
        msgarr = self._json_get_array(msgbin)
        msglen = len(msgarr)
        if msglen == 0:
            return ""
        # // last element of array is the new position
        msglen = msglen - 1
        self._rxptr = self._decode_json_int(msgarr[msglen])
        if msglen == 0:
            return ""
        res = self._json_get_string(msgarr[0])
        return res

    def queryHex(self, hexString, maxWait):
        """
        Sends a binary message to the serial port, and reads the reply, if any.
        This function is intended to be used when the serial port is configured for
        Frame-based protocol.

        @param hexString : the message to send, coded in hexadecimal
        @param maxWait : the maximum number of milliseconds to wait for a reply.

        @return the next frame received after sending the message, as a hex string.
                Additional frames can be obtained by calling readHex or readMessages.

        On failure, throws an exception or returns an empty string.
        """
        # prevpos
        # url
        # msgbin
        msgarr = []
        # msglen
        # res
        if len(hexString) <= 80:
            # // fast query
            url = "rxmsg.json?len=1&maxw=" + str(int(maxWait)) + "&cmd=$" + hexString
        else:
            # // long query
            prevpos = self.end_tell()
            self._upload("txdata", YAPI._hexStrToBin(hexString))
            url = "rxmsg.json?len=1&maxw=" + str(int(maxWait)) + "&pos=" + str(int(prevpos))

        msgbin = self._download(url)
        msgarr = self._json_get_array(msgbin)
        msglen = len(msgarr)
        if msglen == 0:
            return ""
        # // last element of array is the new position
        msglen = msglen - 1
        self._rxptr = self._decode_json_int(msgarr[msglen])
        if msglen == 0:
            return ""
        res = self._json_get_string(msgarr[0])
        return res

    def uploadJob(self, jobfile, jsonDef):
        """
        Saves the job definition string (JSON data) into a job file.
        The job file can be later enabled using selectJob().

        @param jobfile : name of the job file to save on the device filesystem
        @param jsonDef : a string containing a JSON definition of the job

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        self._upload(jobfile, bytearray(jsonDef, YAPI.DefaultEncoding))
        return YAPI.SUCCESS

    def selectJob(self, jobfile):
        """
        Load and start processing the specified job file. The file must have
        been previously created using the user interface or uploaded on the
        device filesystem using the uploadJob() function.

        @param jobfile : name of the job file (on the device filesystem)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_currentJob(jobfile)

    def reset(self):
        """
        Clears the serial port buffer and resets counters to zero.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        self._eventPos = 0
        self._rxptr = 0
        self._rxbuffptr = 0
        self._rxbuff = bytearray(0)

        return self.sendCommand("Z")

    def writeByte(self, code):
        """
        Sends a single byte to the serial port.

        @param code : the byte to send

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("$" + ("%02X" % code))

    def writeStr(self, text):
        """
        Sends an ASCII string to the serial port, as is.

        @param text : the text string to send

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # idx
        # ch
        buff = bytearray(text, YAPI.DefaultEncoding)
        bufflen = len(buff)
        if bufflen < 100:
            # // if string is pure text, we can send it as a simple command (faster)
            ch = 0x20
            idx = 0
            while (idx < bufflen) and (ch != 0):
                ch = buff[idx]
                if (ch >= 0x20) and (ch < 0x7f):
                    idx = idx + 1
                else:
                    ch = 0
            if idx >= bufflen:
                return self.sendCommand("+" + text)
        # // send string using file upload
        return self._upload("txdata", buff)

    def writeBin(self, buff):
        """
        Sends a binary buffer to the serial port, as is.

        @param buff : the binary buffer to send

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self._upload("txdata", buff)

    def writeArray(self, byteList):
        """
        Sends a byte sequence (provided as a list of bytes) to the serial port.

        @param byteList : a list of byte codes

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # idx
        # hexb
        # res
        bufflen = len(byteList)
        buff = bytearray(bufflen)
        idx = 0
        while idx < bufflen:
            hexb = byteList[idx]
            buff[idx] = hexb
            idx = idx + 1

        res = self._upload("txdata", buff)
        return res

    def writeHex(self, hexString):
        """
        Sends a byte sequence (provided as a hexadecimal string) to the serial port.

        @param hexString : a string of hexadecimal byte codes

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # idx
        # hexb
        # res
        bufflen = len(hexString)
        if bufflen < 100:
            return self.sendCommand("$" + hexString)
        bufflen = (bufflen >> 1)
        buff = bytearray(bufflen)
        idx = 0
        while idx < bufflen:
            hexb = int((hexString)[2 * idx: 2 * idx + 2], 16)
            buff[idx] = hexb
            idx = idx + 1

        res = self._upload("txdata", buff)
        return res

    def writeLine(self, text):
        """
        Sends an ASCII string to the serial port, followed by a line break (CR LF).

        @param text : the text string to send

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # idx
        # ch
        buff = bytearray("" + text + "\r\n", YAPI.DefaultEncoding)
        bufflen = len(buff)-2
        if bufflen < 100:
            # // if string is pure text, we can send it as a simple command (faster)
            ch = 0x20
            idx = 0
            while (idx < bufflen) and (ch != 0):
                ch = buff[idx]
                if (ch >= 0x20) and (ch < 0x7f):
                    idx = idx + 1
                else:
                    ch = 0
            if idx >= bufflen:
                return self.sendCommand("!" + text)
        # // send string using file upload
        return self._upload("txdata", buff)

    def readByte(self):
        """
        Reads one byte from the receive buffer, starting at current stream position.
        If data at current stream position is not available anymore in the receive buffer,
        or if there is no data available yet, the function returns YAPI.NO_MORE_DATA.

        @return the next byte

        On failure, throws an exception or returns a negative error code.
        """
        # currpos
        # reqlen
        # buff
        # bufflen
        # mult
        # endpos
        # res
        # // first check if we have the requested character in the look-ahead buffer
        bufflen = len(self._rxbuff)
        if (self._rxptr >= self._rxbuffptr) and (self._rxptr < self._rxbuffptr+bufflen):
            res = self._rxbuff[self._rxptr-self._rxbuffptr]
            self._rxptr = self._rxptr + 1
            return res
        # // try to preload more than one byte to speed-up byte-per-byte access
        currpos = self._rxptr
        reqlen = 1024
        buff = self.readBin(reqlen)
        bufflen = len(buff)
        if (bufflen > 0) and (self._rxptr == currpos+bufflen):
            # // up to 1024 bytes in buffer, all in direction Rx
            res = buff[0]
            self._rxptr = currpos+1
            self._rxbuffptr = currpos
            self._rxbuff = buff
            return res
        # // mixed bidirectional data, retry with a smaller block
        self._rxptr = currpos
        reqlen = 16
        buff = self.readBin(reqlen)
        bufflen = len(buff)
        if (bufflen > 0) and (self._rxptr == currpos+bufflen):
            # // up to 16 bytes in buffer, all in direction Rx
            res = buff[0]
            self._rxptr = currpos+1
            self._rxbuffptr = currpos
            self._rxbuff = buff
            return res
        # // still mixed, need to process character by character
        self._rxptr = currpos

        buff = self._download("rxdata.bin?pos=" + str(int(self._rxptr)) + "&len=1")
        bufflen = len(buff) - 1
        endpos = 0
        mult = 1
        while (bufflen > 0) and (buff[bufflen] != 64):
            endpos = endpos + mult * (buff[bufflen] - 48)
            mult = mult * 10
            bufflen = bufflen - 1
        self._rxptr = endpos
        if bufflen == 0:
            return YAPI.NO_MORE_DATA
        res = buff[0]
        return res

    def readStr(self, nChars):
        """
        Reads data from the receive buffer as a string, starting at current stream position.
        If data at current stream position is not available anymore in the receive buffer, the
        function performs a short read.

        @param nChars : the maximum number of characters to read

        @return a string with receive buffer contents

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # mult
        # endpos
        # res
        if nChars > 65535:
            nChars = 65535

        buff = self._download("rxdata.bin?pos=" + str(int(self._rxptr)) + "&len=" + str(int(nChars)))
        bufflen = len(buff) - 1
        endpos = 0
        mult = 1
        while (bufflen > 0) and (buff[bufflen] != 64):
            endpos = endpos + mult * (buff[bufflen] - 48)
            mult = mult * 10
            bufflen = bufflen - 1
        self._rxptr = endpos
        res = (buff.decode(YAPI.DefaultEncoding))[0: 0 + bufflen]
        return res

    def readBin(self, nChars):
        """
        Reads data from the receive buffer as a binary buffer, starting at current stream position.
        If data at current stream position is not available anymore in the receive buffer, the
        function performs a short read.

        @param nChars : the maximum number of bytes to read

        @return a binary object with receive buffer contents

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # mult
        # endpos
        # idx
        # res
        if nChars > 65535:
            nChars = 65535

        buff = self._download("rxdata.bin?pos=" + str(int(self._rxptr)) + "&len=" + str(int(nChars)))
        bufflen = len(buff) - 1
        endpos = 0
        mult = 1
        while (bufflen > 0) and (buff[bufflen] != 64):
            endpos = endpos + mult * (buff[bufflen] - 48)
            mult = mult * 10
            bufflen = bufflen - 1
        self._rxptr = endpos
        res = bytearray(bufflen)
        idx = 0
        while idx < bufflen:
            res[idx] = buff[idx]
            idx = idx + 1
        return res

    def readArray(self, nChars):
        """
        Reads data from the receive buffer as a list of bytes, starting at current stream position.
        If data at current stream position is not available anymore in the receive buffer, the
        function performs a short read.

        @param nChars : the maximum number of bytes to read

        @return a sequence of bytes with receive buffer contents

        On failure, throws an exception or returns an empty array.
        """
        # buff
        # bufflen
        # mult
        # endpos
        # idx
        # b
        res = []
        if nChars > 65535:
            nChars = 65535

        buff = self._download("rxdata.bin?pos=" + str(int(self._rxptr)) + "&len=" + str(int(nChars)))
        bufflen = len(buff) - 1
        endpos = 0
        mult = 1
        while (bufflen > 0) and (buff[bufflen] != 64):
            endpos = endpos + mult * (buff[bufflen] - 48)
            mult = mult * 10
            bufflen = bufflen - 1
        self._rxptr = endpos
        del res[:]
        idx = 0
        while idx < bufflen:
            b = buff[idx]
            res.append(b)
            idx = idx + 1

        return res

    def readHex(self, nBytes):
        """
        Reads data from the receive buffer as a hexadecimal string, starting at current stream position.
        If data at current stream position is not available anymore in the receive buffer, the
        function performs a short read.

        @param nBytes : the maximum number of bytes to read

        @return a string with receive buffer contents, encoded in hexadecimal

        On failure, throws an exception or returns a negative error code.
        """
        # buff
        # bufflen
        # mult
        # endpos
        # ofs
        # res
        if nBytes > 65535:
            nBytes = 65535

        buff = self._download("rxdata.bin?pos=" + str(int(self._rxptr)) + "&len=" + str(int(nBytes)))
        bufflen = len(buff) - 1
        endpos = 0
        mult = 1
        while (bufflen > 0) and (buff[bufflen] != 64):
            endpos = endpos + mult * (buff[bufflen] - 48)
            mult = mult * 10
            bufflen = bufflen - 1
        self._rxptr = endpos
        res = ""
        ofs = 0
        while ofs + 3 < bufflen:
            res = "" + res + "" + ("%02X" % buff[ofs]) + "" + ("%02X" % buff[ofs + 1]) + "" + ("%02X" % buff[ofs + 2]) + "" + ("%02X" % buff[ofs + 3])
            ofs = ofs + 4
        while ofs < bufflen:
            res = "" + res + "" + ("%02X" % buff[ofs])
            ofs = ofs + 1
        return res

    def querySdi12(self, sensorAddr, cmd, maxWait):
        """
        Sends a SDI-12 query to the bus, and reads the sensor immediate reply.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @param sensorAddr : the sensor address, as a string
        @param cmd : the SDI12 query to send (without address and exclamation point)
        @param maxWait : the maximum timeout to wait for a reply from sensor, in millisecond

        @return the reply returned by the sensor, without newline, as a string.

        On failure, throws an exception or returns an empty string.
        """
        # fullCmd
        # cmdChar
        # pattern
        # url
        # msgbin
        msgarr = []
        # msglen
        # res
        cmdChar  = ""

        pattern = sensorAddr
        if len(cmd) > 0:
            cmdChar = (cmd)[0: 0 + 1]
        if sensorAddr == "?":
            pattern = ".*"
        else:
            if cmdChar == "M" or cmdChar == "D":
                pattern = "" + sensorAddr + ":.*"
            else:
                pattern = "" + sensorAddr + ".*"
        pattern = self._escapeAttr(pattern)
        fullCmd = self._escapeAttr("+" + sensorAddr + "" + cmd + "!")
        url = "rxmsg.json?len=1&maxw=" + str(int(maxWait)) + "&cmd=" + fullCmd + "&pat=" + pattern

        msgbin = self._download(url)
        if len(msgbin)<2:
            return ""
        msgarr = self._json_get_array(msgbin)
        msglen = len(msgarr)
        if msglen == 0:
            return ""
        # // last element of array is the new position
        msglen = msglen - 1
        self._rxptr = self._decode_json_int(msgarr[msglen])
        if msglen == 0:
            return ""
        res = self._json_get_string(msgarr[0])
        return res

    def discoverSingleSensor(self):
        """
        Sends a discovery command to the bus, and reads the sensor information reply.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.
        This function work when only one sensor is connected.

        @return the reply returned by the sensor, as a YSdi12SensorInfo object.

        On failure, throws an exception or returns an empty string.
        """
        # resStr

        resStr = self.querySdi12("?","",5000)
        if resStr == "":
            return YSdi12SensorInfo(self, "ERSensor Not Found")

        return self.getSensorInformation(resStr)

    def discoverAllSensors(self):
        """
        Sends a discovery command to the bus, and reads all sensors information reply.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @return all the information from every connected sensor, as an array of YSdi12SensorInfo object.

        On failure, throws an exception or returns an empty string.
        """
        sensors = []
        idSens = []
        # res
        # i
        # lettreMin
        # lettreMaj

        # // 1. Search for sensors present
        del idSens[:]
        i = 0
        while i < 10:
            res = self.querySdi12(str(i),"!",500)
            if len(res) >= 1:
                idSens.append(res)
            i = i+1
        lettreMin = "abcdefghijklmnopqrstuvwxyz"
        lettreMaj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        i = 0
        while i<26:
            res = self.querySdi12((lettreMin)[i: i + 1],"!",500)
            if len(res) >= 1:
                idSens.append(res)
            i = i +1
        while i<26:
            res = self.querySdi12((lettreMaj)[i: i + 1],"!",500)
            if len(res) >= 1:
                idSens.append(res)
            i = i +1

        # // 2. Query existing sensors information
        i = 0
        del sensors[:]
        while i < len(idSens):
            sensors.append(self.getSensorInformation(idSens[i]))
            i = i + 1

        return sensors

    def readSensor(self, sensorAddr, measCmd, maxWait):
        """
        Sends a mesurement command to the SDI-12 bus, and reads the sensor immediate reply.
        The supported commands are:
        M: Measurement start control
        M1...M9: Additional measurement start command
        D: Measurement reading control
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @param sensorAddr : the sensor address, as a string
        @param measCmd : the SDI12 query to send (without address and exclamation point)
        @param maxWait : the maximum timeout to wait for a reply from sensor, in millisecond

        @return the reply returned by the sensor, without newline, as a list of float.

        On failure, throws an exception or returns an empty string.
        """
        # resStr
        res = []
        tab = []
        split = []
        # i
        # valdouble

        resStr = self.querySdi12(sensorAddr,measCmd,maxWait)
        tab = (resStr).split(',')
        split = (tab[0]).split(':')
        if len(split) < 2:
            return res

        valdouble = YAPI._atof(split[1])
        res.append(valdouble)
        i = 1
        while i < len(tab):
            valdouble = YAPI._atof(tab[i])
            res.append(valdouble)
            i = i + 1

        return res

    def changeAddress(self, oldAddress, newAddress):
        """
        Changes the address of the selected sensor, and returns the sensor information with the new address.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @param oldAddress : Actual sensor address, as a string
        @param newAddress : New sensor address, as a string

        @return the sensor address and information , as a YSdi12SensorInfo object.

        On failure, throws an exception or returns an empty string.
        """
        # addr

        self.querySdi12(oldAddress, "A" + newAddress,1000)
        addr = self.getSensorInformation(newAddress)
        return addr

    def getSensorInformation(self, sensorAddr):
        """
        Sends a information command to the bus, and reads sensors information selected.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @param sensorAddr : Sensor address, as a string

        @return the reply returned by the sensor, as a YSdi12Port object.

        On failure, throws an exception or returns an empty string.
        """
        # res
        # sensor

        res = self.querySdi12(sensorAddr,"I",1000)
        if res == "":
            return YSdi12SensorInfo(self, "ERSensor Not Found")
        sensor = YSdi12SensorInfo(self, res)
        sensor._queryValueInfo()
        return sensor

    def readConcurrentMeasurements(self, sensorAddr):
        """
        Sends a information command to the bus, and reads sensors information selected.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @param sensorAddr : Sensor address, as a string

        @return the reply returned by the sensor, as a YSdi12Port object.

        On failure, throws an exception or returns an empty string.
        """
        res = []

        res= self.readSensor(sensorAddr,"D",1000)
        return res

    def requestConcurrentMeasurements(self, sensorAddr):
        """
        Sends a information command to the bus, and reads sensors information selected.
        This function is intended to be used when the serial port is configured for 'SDI-12' protocol.

        @param sensorAddr : Sensor address, as a string

        @return the reply returned by the sensor, as a YSdi12Port object.

        On failure, throws an exception or returns an empty string.
        """
        # timewait
        # wait

        wait = self.querySdi12(sensorAddr,"C",1000)
        wait = (wait)[1: 1 + 3]
        timewait = YAPI._atoi(wait) * 1000
        return timewait

    def snoopMessagesEx(self, maxWait, maxMsg):
        """
        Retrieves messages (both direction) in the SDI12 port buffer, starting at current position.

        If no message is found, the search waits for one up to the specified maximum timeout
        (in milliseconds).

        @param maxWait : the maximum number of milliseconds to wait for a message if none is found
                in the receive buffer.
        @param maxMsg : the maximum number of messages to be returned by the function; up to 254.

        @return an array of YSdi12SnoopingRecord objects containing the messages found, if any.

        On failure, throws an exception or returns an empty array.
        """
        # url
        # msgbin
        msgarr = []
        # msglen
        res = []
        # idx

        url = "rxmsg.json?pos=" + str(int(self._rxptr)) + "&maxw=" + str(int(maxWait)) + "&t=0&len=" + str(int(maxMsg))
        msgbin = self._download(url)
        msgarr = self._json_get_array(msgbin)
        msglen = len(msgarr)
        if msglen == 0:
            return res
        # // last element of array is the new position
        msglen = msglen - 1
        self._rxptr = self._decode_json_int(msgarr[msglen])
        idx = 0

        while idx < msglen:
            res.append(YSdi12SnoopingRecord(msgarr[idx].decode(YAPI.DefaultEncoding)))
            idx = idx + 1

        return res

    def snoopMessages(self, maxWait):
        """
        Retrieves messages (both direction) in the SDI12 port buffer, starting at current position.

        If no message is found, the search waits for one up to the specified maximum timeout
        (in milliseconds).

        @param maxWait : the maximum number of milliseconds to wait for a message if none is found
                in the receive buffer.

        @return an array of YSdi12SnoopingRecord objects containing the messages found, if any.

        On failure, throws an exception or returns an empty array.
        """
        return self.snoopMessagesEx(maxWait, 255)

    def nextSdi12Port(self):
        """
        Continues the enumeration of SDI12 ports started using yFirstSdi12Port().
        Caution: You can't make any assumption about the returned SDI12 ports order.
        If you want to find a specific an SDI12 port, use Sdi12Port.findSdi12Port()
        and a hardwareID or a logical name.

        @return a pointer to a YSdi12Port object, corresponding to
                an SDI12 port currently online, or a None pointer
                if there are no more SDI12 ports to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YSdi12Port.FindSdi12Port(hwidRef.value)

#--- (end of generated code: YSdi12Port implementation)

#--- (generated code: YSdi12Port functions)

    @staticmethod
    def FirstSdi12Port():
        """
        Starts the enumeration of SDI12 ports currently accessible.
        Use the method YSdi12Port.nextSdi12Port() to iterate on
        next SDI12 ports.

        @return a pointer to a YSdi12Port object, corresponding to
                the first SDI12 port currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Sdi12Port", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YSdi12Port.FindSdi12Port(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: YSdi12Port functions)
