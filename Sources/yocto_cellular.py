#*********************************************************************
#*
#* $Id: yocto_cellular.py 20167 2015-04-27 14:24:03Z seb $
#*
#* Implements yFindCellular(), the high-level API for Cellular functions
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


#--- (generated code: YCellRecord class start)
#noinspection PyProtectedMember
class YCellRecord(object):
#--- (end of generated code: YCellRecord class start)
    #--- (generated code: YCellRecord return codes)
    #--- (end of generated code: YCellRecord return codes)
    #--- (generated code: YCellRecord dlldef)
    #--- (end of generated code: YCellRecord dlldef)
    #--- (generated code: YCellRecord definitions)
    #--- (end of generated code: YCellRecord definitions)

    def __init__(self, int_mcc, int_mnc, int_lac, int_cellId, int_dbm, int_tad, str_oper):
        #--- (generated code: YCellRecord attributes)
        self._oper = ''
        self._mcc = 0
        self._mnc = 0
        self._lac = 0
        self._cid = 0
        self._dbm = 0
        self._tad = 0
        #--- (end of generated code: YCellRecord attributes)
        self._oper = str_oper
        self._mcc = int_mcc
        self._mnc = int_mnc
        self._lac = int_lac
        self._cid = int_cellId
        self._dbm = int_dbm
        self._tad = int_tad

#--- (generated code: YCellRecord implementation)
    def get_cellOperator(self):
        return self._oper

    def get_mobileCountryCode(self):
        return self._mcc

    def get_mobileNetworkCode(self):
        return self._mnc

    def get_locationAreaCode(self):
        return self._lac

    def get_cellId(self):
        return self._cid

    def get_signalStrength(self):
        return self._dbm

    def get_timingAdvance(self):
        return self._tad

#--- (end of generated code: YCellRecord implementation)

#--- (generated code: CellRecord functions)
#--- (end of generated code: CellRecord functions)


#--- (generated code: YCellular class start)
#noinspection PyProtectedMember
class YCellular(YFunction):
    """
    YCellular functions provides control over cellular network parameters
    and status for devices that are GSM-enabled.

    """
#--- (end of generated code: YCellular class start)
    #--- (generated code: YCellular return codes)
    #--- (end of generated code: YCellular return codes)
    #--- (generated code: YCellular dlldef)
    #--- (end of generated code: YCellular dlldef)
    #--- (generated code: YCellular definitions)
    LINKQUALITY_INVALID = YAPI.INVALID_UINT
    CELLOPERATOR_INVALID = YAPI.INVALID_STRING
    IMSI_INVALID = YAPI.INVALID_STRING
    MESSAGE_INVALID = YAPI.INVALID_STRING
    PIN_INVALID = YAPI.INVALID_STRING
    LOCKEDOPERATOR_INVALID = YAPI.INVALID_STRING
    APN_INVALID = YAPI.INVALID_STRING
    APNSECRET_INVALID = YAPI.INVALID_STRING
    COMMAND_INVALID = YAPI.INVALID_STRING
    ENABLEDATA_HOMENETWORK = 0
    ENABLEDATA_ROAMING = 1
    ENABLEDATA_NEVER = 2
    ENABLEDATA_INVALID = -1
    #--- (end of generated code: YCellular definitions)

    def __init__(self, func):
        super(YCellular, self).__init__(func)
        self._className = 'Cellular'
        #--- (generated code: YCellular attributes)
        self._callback = None
        self._linkQuality = YCellular.LINKQUALITY_INVALID
        self._cellOperator = YCellular.CELLOPERATOR_INVALID
        self._imsi = YCellular.IMSI_INVALID
        self._message = YCellular.MESSAGE_INVALID
        self._pin = YCellular.PIN_INVALID
        self._lockedOperator = YCellular.LOCKEDOPERATOR_INVALID
        self._enableData = YCellular.ENABLEDATA_INVALID
        self._apn = YCellular.APN_INVALID
        self._apnSecret = YCellular.APNSECRET_INVALID
        self._command = YCellular.COMMAND_INVALID
        #--- (end of generated code: YCellular attributes)

    #--- (generated code: YCellular implementation)
    def _parseAttr(self, member):
        if member.name == "linkQuality":
            self._linkQuality = member.ivalue
            return 1
        if member.name == "cellOperator":
            self._cellOperator = member.svalue
            return 1
        if member.name == "imsi":
            self._imsi = member.svalue
            return 1
        if member.name == "message":
            self._message = member.svalue
            return 1
        if member.name == "pin":
            self._pin = member.svalue
            return 1
        if member.name == "lockedOperator":
            self._lockedOperator = member.svalue
            return 1
        if member.name == "enableData":
            self._enableData = member.ivalue
            return 1
        if member.name == "apn":
            self._apn = member.svalue
            return 1
        if member.name == "apnSecret":
            self._apnSecret = member.svalue
            return 1
        if member.name == "command":
            self._command = member.svalue
            return 1
        super(YCellular, self)._parseAttr(member)

    def get_linkQuality(self):
        """
        Returns the link quality, expressed in percent.

        @return an integer corresponding to the link quality, expressed in percent

        On failure, throws an exception or returns YCellular.LINKQUALITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.LINKQUALITY_INVALID
        return self._linkQuality

    def get_cellOperator(self):
        """
        Returns the name of the cell operator currently in use.

        @return a string corresponding to the name of the cell operator currently in use

        On failure, throws an exception or returns YCellular.CELLOPERATOR_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.CELLOPERATOR_INVALID
        return self._cellOperator

    def get_imsi(self):
        """
        Returns an opaque string if a PIN code has been configured in the device to access
        the SIM card, or an empty string if none has been configured or if the code provided
        was rejected by the SIM card.

        @return a string corresponding to an opaque string if a PIN code has been configured in the device to access
                the SIM card, or an empty string if none has been configured or if the code provided
                was rejected by the SIM card

        On failure, throws an exception or returns YCellular.IMSI_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.IMSI_INVALID
        return self._imsi

    def get_message(self):
        """
        Returns the latest status message from the wireless interface.

        @return a string corresponding to the latest status message from the wireless interface

        On failure, throws an exception or returns YCellular.MESSAGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.MESSAGE_INVALID
        return self._message

    def get_pin(self):
        """
        Returns an opaque string if a PIN code has been configured in the device to access
        the SIM card, or an empty string if none has been configured or if the code provided
        was rejected by the SIM card.

        @return a string corresponding to an opaque string if a PIN code has been configured in the device to access
                the SIM card, or an empty string if none has been configured or if the code provided
                was rejected by the SIM card

        On failure, throws an exception or returns YCellular.PIN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.PIN_INVALID
        return self._pin

    def set_pin(self, newval):
        """
        Changes the PIN code used by the module to access the SIM card.
        This function does not change the code on the SIM card itself, but only changes
        the parameter used by the device to try to get access to it. If the SIM code
        does not work immediately on first try, it will be automatically forgotten
        and the message will be set to "Enter SIM PIN". The method should then be
        invoked again with right correct PIN code. After three failed attempts in a row,
        the message is changed to "Enter SIM PUK" and the SIM card PUK code must be
        provided using method sendPUK.

        Remember to call the saveToFlash() method of the module to save the
        new value in the device flash.

        @param newval : a string corresponding to the PIN code used by the module to access the SIM card

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("pin", rest_val)

    def get_lockedOperator(self):
        """
        Returns the name of the only cell operator to use if automatic choice is disabled,
        or an empty string if the SIM card will automatically choose among available
        cell operators.

        @return a string corresponding to the name of the only cell operator to use if automatic choice is disabled,
                or an empty string if the SIM card will automatically choose among available
                cell operators

        On failure, throws an exception or returns YCellular.LOCKEDOPERATOR_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.LOCKEDOPERATOR_INVALID
        return self._lockedOperator

    def set_lockedOperator(self, newval):
        """
        Changes the name of the cell operator to be used. If the name is an empty
        string, the choice will be made automatically based on the SIM card. Otherwise,
        the selected operator is the only one that will be used.

        @param newval : a string corresponding to the name of the cell operator to be used

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("lockedOperator", rest_val)

    def get_enableData(self):
        """
        Returns the condition for enabling IP data services (GPRS).
        When data services are disabled, SMS are the only mean of communication.

        @return a value among YCellular.ENABLEDATA_HOMENETWORK, YCellular.ENABLEDATA_ROAMING and
        YCellular.ENABLEDATA_NEVER corresponding to the condition for enabling IP data services (GPRS)

        On failure, throws an exception or returns YCellular.ENABLEDATA_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.ENABLEDATA_INVALID
        return self._enableData

    def set_enableData(self, newval):
        """
        Changes the condition for enabling IP data services (GPRS).
        The service can be either fully deactivated, or limited to the SIM home network,
        or enabled for all partner networks (roaming). Caution: enabling data services
        on roaming networks may cause prohibitive communication costs !

        When data services are disabled, SMS are the only mean of communication.

        @param newval : a value among YCellular.ENABLEDATA_HOMENETWORK, YCellular.ENABLEDATA_ROAMING and
        YCellular.ENABLEDATA_NEVER corresponding to the condition for enabling IP data services (GPRS)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("enableData", rest_val)

    def get_apn(self):
        """
        Returns the Access Point Name (APN) to be used, if needed.
        When left blank, the APN suggested by the cell operator will be used.

        @return a string corresponding to the Access Point Name (APN) to be used, if needed

        On failure, throws an exception or returns YCellular.APN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.APN_INVALID
        return self._apn

    def set_apn(self, newval):
        """
        Returns the Access Point Name (APN) to be used, if needed.
        When left blank, the APN suggested by the cell operator will be used.

        @param newval : a string

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("apn", rest_val)

    def get_apnSecret(self):
        """
        Returns an opaque string if APN authentication parameters have been configured
        in the device, or an empty string otherwise.
        To configure these parameters, use set_apnAuth().

        @return a string corresponding to an opaque string if APN authentication parameters have been configured
                in the device, or an empty string otherwise

        On failure, throws an exception or returns YCellular.APNSECRET_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.APNSECRET_INVALID
        return self._apnSecret

    def set_apnSecret(self, newval):
        rest_val = newval
        return self._setAttr("apnSecret", rest_val)

    def get_command(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YCellular.COMMAND_INVALID
        return self._command

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindCellular(func):
        """
        Retrieves a cellular interface for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the cellular interface is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCellular.isOnline() to test if the cellular interface is
        indeed online at a given time. In case of ambiguity when looking for
        a cellular interface by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the cellular interface

        @return a YCellular object allowing you to drive the cellular interface.
        """
        # obj
        obj = YFunction._FindFromCache("Cellular", func)
        if obj is None:
            obj = YCellular(func)
            YFunction._AddToCache("Cellular", func, obj)
        return obj

    def sendPUK(self, puk, newPin):
        """
        Sends a PUK code to unlock the SIM card after three failed PIN code attempts, and
        setup a new PIN into the SIM card. Only ten consecutives tentatives are permitted:
        after that, the SIM card will be blocked permanently without any mean of recovery
        to use it again. Note that after calling this method, you have usually to invoke
        method set_pin() to tell the YoctoHub which PIN to use in the future.

        @param puk : the SIM PUK code
        @param newPin : new PIN code to configure into the SIM card

        @return YAPI.SUCCESS when the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # gsmMsg
        
        gsmMsg = self.get_message()
        if not (gsmMsg == "Enter SIM PUK"):
            self._throw(YAPI.INVALID_ARGUMENT, "PUK not expected at this time")
        if newPin == "":
            return self.set_command("AT+CPIN=" + puk + ",0000;+CLCK=SC,0,0000")
        return self.set_command("AT+CPIN=" + puk + "," + newPin)

    def set_apnAuth(self, username, password):
        """
        Configure authentication parameters to connect to the APN. Both
        PAP and CHAP authentication are supported.

        @param username : APN username
        @param password : APN password

        @return YAPI.SUCCESS when the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_apnSecret("" + username + "," + password)

    def _AT(self, cmd):
        """
        Sends an AT command to the GSM module and returns the command output.
        The command will only execute when the GSM module is in standard
        command state, and should leave it in the exact same state.
        Use this function with great care !

        @param cmd : the AT command to execute, like for instance: "+CCLK?".

        @return a string with the result of the commands. Empty lines are
                automatically removed from the output.
        """
        # chrPos
        # cmdLen
        # content
        # // quote dangerous characters used in AT commands
        cmdLen = len(cmd)
        chrPos = cmd.find("#")
        while chrPos >= 0:
            cmd = "" + (cmd)[0: 0 + chrPos] + "" + str(chr(37)) + "23" + (cmd)[chrPos+1: chrPos+1 + cmdLen-chrPos-1]
            cmdLen = cmdLen + 2
            chrPos = cmd.find("#")
        chrPos = cmd.find("+")
        while chrPos >= 0:
            cmd = "" + (cmd)[0: 0 + chrPos] + "" + str(chr(37)) + "2B" + (cmd)[chrPos+1: chrPos+1 + cmdLen-chrPos-1]
            cmdLen = cmdLen + 2
            chrPos = cmd.find("+")
        chrPos = cmd.find("=")
        while chrPos >= 0:
            cmd = "" + (cmd)[0: 0 + chrPos] + "" + str(chr(37)) + "3D" + (cmd)[chrPos+1: chrPos+1 + cmdLen-chrPos-1]
            cmdLen = cmdLen + 2
            chrPos = cmd.find("=")
        
        # // may throw an exception
        content = self._download("at.txt?cmd=" + cmd)
        return YByte2String(content)

    def quickCellSurvey(self):
        """
        Returns a list of nearby cellular antennas, as required for quick
        geolocation of the device. The first cell listed is the serving
        cell, and the next ones are the neighboor cells reported by the
        serving cell.

        @return a list of YCellRecords.
        """
        # moni
        recs = []
        # llen
        # mccs
        # mcc
        # mncs
        # mnc
        # lac
        # cellId
        # dbms
        # dbm
        # tads
        # tad
        # oper
        res = []
        # // may throw an exception
        moni = self._AT("+CCED=0;#MONI=7;#MONI")
        mccs = (moni)[7: 7 + 3]
        if (mccs)[0: 0 + 1] == "0":
            mccs = (mccs)[1: 1 + 2]
        if (mccs)[0: 0 + 1] == "0":
            mccs = (mccs)[1: 1 + 1]
        mcc = int(mccs)
        mncs = (moni)[11: 11 + 3]
        if (mncs)[2: 2 + 1] == ",":
            mncs = (mncs)[0: 0 + 2]
        if (mncs)[0: 0 + 1] == "0":
            mncs = (mncs)[1: 1 + len(mncs)-1]
        mnc = int(mncs)
        recs = (moni).split('#')
        # // process each line in turn
        del res[:]
        for y in recs:
            llen = len(y) - 2
            if llen >= 44:
                if (y)[41: 41 + 3] == "dbm":
                    lac = int((y)[16: 16 + 4], 16)
                    cellId = int((y)[23: 23 + 4], 16)
                    dbms = (y)[37: 37 + 4]
                    if (dbms)[0: 0 + 1] == " ":
                        dbms = (dbms)[1: 1 + 3]
                    dbm = int(dbms)
                    if llen > 66:
                        tads = (y)[54: 54 + 2]
                        if (tads)[0: 0 + 1] == " ":
                            tads = (tads)[1: 1 + 3]
                        tad = int(tads)
                        oper = (y)[66: 66 + llen-66]
                    else:
                        tad = -1
                        oper = ""
                    if lac < 65535:
                        res.append(YCellRecord(mcc, mnc, lac, cellId, dbm, tad, oper))
        return res

    def nextCellular(self):
        """
        Continues the enumeration of cellular interfaces started using yFirstCellular().

        @return a pointer to a YCellular object, corresponding to
                a cellular interface currently online, or a None pointer
                if there are no more cellular interfaces to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YCellular.FindCellular(hwidRef.value)

#--- (end of generated code: YCellular implementation)

#--- (generated code: Cellular functions)

    @staticmethod
    def FirstCellular():
        """
        Starts the enumeration of cellular interfaces currently accessible.
        Use the method YCellular.nextCellular() to iterate on
        next cellular interfaces.

        @return a pointer to a YCellular object, corresponding to
                the first cellular interface currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Cellular", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YCellular.FindCellular(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: Cellular functions)
