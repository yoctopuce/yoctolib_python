#*********************************************************************
#*
#* $Id: yocto_buzzer.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindBuzzer(), the high-level API for Buzzer functions
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


#--- (YBuzzer class start)
#noinspection PyProtectedMember
class YBuzzer(YFunction):
    """
    The Yoctopuce application programming interface allows you to
    choose the frequency and volume at which the buzzer must sound.
    You can also pre-program a play sequence.

    """
#--- (end of YBuzzer class start)
    #--- (YBuzzer return codes)
    #--- (end of YBuzzer return codes)
    #--- (YBuzzer dlldef)
    #--- (end of YBuzzer dlldef)
    #--- (YBuzzer definitions)
    FREQUENCY_INVALID = YAPI.INVALID_DOUBLE
    VOLUME_INVALID = YAPI.INVALID_UINT
    PLAYSEQSIZE_INVALID = YAPI.INVALID_UINT
    PLAYSEQMAXSIZE_INVALID = YAPI.INVALID_UINT
    PLAYSEQSIGNATURE_INVALID = YAPI.INVALID_UINT
    COMMAND_INVALID = YAPI.INVALID_STRING
    #--- (end of YBuzzer definitions)

    def __init__(self, func):
        super(YBuzzer, self).__init__(func)
        self._className = 'Buzzer'
        #--- (YBuzzer attributes)
        self._callback = None
        self._frequency = YBuzzer.FREQUENCY_INVALID
        self._volume = YBuzzer.VOLUME_INVALID
        self._playSeqSize = YBuzzer.PLAYSEQSIZE_INVALID
        self._playSeqMaxSize = YBuzzer.PLAYSEQMAXSIZE_INVALID
        self._playSeqSignature = YBuzzer.PLAYSEQSIGNATURE_INVALID
        self._command = YBuzzer.COMMAND_INVALID
        #--- (end of YBuzzer attributes)

    #--- (YBuzzer implementation)
    def _parseAttr(self, member):
        if member.name == "frequency":
            self._frequency = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "volume":
            self._volume = member.ivalue
            return 1
        if member.name == "playSeqSize":
            self._playSeqSize = member.ivalue
            return 1
        if member.name == "playSeqMaxSize":
            self._playSeqMaxSize = member.ivalue
            return 1
        if member.name == "playSeqSignature":
            self._playSeqSignature = member.ivalue
            return 1
        if member.name == "command":
            self._command = member.svalue
            return 1
        super(YBuzzer, self)._parseAttr(member)

    def set_frequency(self, newval):
        """
        Changes the frequency of the signal sent to the buzzer. A zero value stops the buzzer.

        @param newval : a floating point number corresponding to the frequency of the signal sent to the buzzer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("frequency", rest_val)

    def get_frequency(self):
        """
        Returns the  frequency of the signal sent to the buzzer/speaker.

        @return a floating point number corresponding to the  frequency of the signal sent to the buzzer/speaker

        On failure, throws an exception or returns YBuzzer.FREQUENCY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBuzzer.FREQUENCY_INVALID
        return self._frequency

    def get_volume(self):
        """
        Returns the volume of the signal sent to the buzzer/speaker.

        @return an integer corresponding to the volume of the signal sent to the buzzer/speaker

        On failure, throws an exception or returns YBuzzer.VOLUME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBuzzer.VOLUME_INVALID
        return self._volume

    def set_volume(self, newval):
        """
        Changes the volume of the signal sent to the buzzer/speaker.

        @param newval : an integer corresponding to the volume of the signal sent to the buzzer/speaker

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("volume", rest_val)

    def get_playSeqSize(self):
        """
        Returns the current length of the playing sequence

        @return an integer corresponding to the current length of the playing sequence

        On failure, throws an exception or returns YBuzzer.PLAYSEQSIZE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBuzzer.PLAYSEQSIZE_INVALID
        return self._playSeqSize

    def get_playSeqMaxSize(self):
        """
        Returns the maximum length of the playing sequence

        @return an integer corresponding to the maximum length of the playing sequence

        On failure, throws an exception or returns YBuzzer.PLAYSEQMAXSIZE_INVALID.
        """
        if self._cacheExpiration == datetime.datetime.fromtimestamp(0):
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBuzzer.PLAYSEQMAXSIZE_INVALID
        return self._playSeqMaxSize

    def get_playSeqSignature(self):
        """
        Returns the playing sequence signature. As playing
        sequences cannot be read from the device, this can be used
        to detect if a specific playing sequence is already
        programmed.

        @return an integer corresponding to the playing sequence signature

        On failure, throws an exception or returns YBuzzer.PLAYSEQSIGNATURE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBuzzer.PLAYSEQSIGNATURE_INVALID
        return self._playSeqSignature

    def get_command(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YBuzzer.COMMAND_INVALID
        return self._command

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindBuzzer(func):
        """
        Retrieves a buzzer for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the buzzer is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YBuzzer.isOnline() to test if the buzzer is
        indeed online at a given time. In case of ambiguity when looking for
        a buzzer by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the buzzer

        @return a YBuzzer object allowing you to drive the buzzer.
        """
        # obj
        obj = YFunction._FindFromCache("Buzzer", func)
        if obj is None:
            obj = YBuzzer(func)
            YFunction._AddToCache("Buzzer", func, obj)
        return obj

    def sendCommand(self, command):
        # //may throw an exception
                return self.set_command(command)

    def addFreqMoveToPlaySeq(self, freq, msDelay):
        """
        Adds a new frequency transition to the playing sequence.

        @param freq    : desired frequency when the transition is completed, in Hz
        @param msDelay : duration of the frequency transition, in milliseconds.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("A" + str(int(freq)) + "," + str(int(msDelay)))

    def addPulseToPlaySeq(self, freq, msDuration):
        """
        Adds a pulse to the playing sequence.

        @param freq : pulse frequency, in Hz
        @param msDuration : pulse duration, in milliseconds.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("B" + str(int(freq)) + "," + str(int(msDuration)))

    def addVolMoveToPlaySeq(self, volume, msDuration):
        """
        Adds a new volume transition to the playing sequence. Frequency stays untouched:
        if frequency is at zero, the transition has no effect.

        @param volume    : desired volume when the transition is completed, as a percentage.
        @param msDuration : duration of the volume transition, in milliseconds.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("C" + str(int(volume)) + "," + str(int(msDuration)))

    def startPlaySeq(self):
        """
        Starts the preprogrammed playing sequence. The sequence
        runs in loop until it is stopped by stopPlaySeq or an explicit
        change.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("S")

    def stopPlaySeq(self):
        """
        Stops the preprogrammed playing sequence and sets the frequency to zero.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("X")

    def resetPlaySeq(self):
        """
        Resets the preprogrammed playing sequence and sets the frequency to zero.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return self.sendCommand("Z")

    def pulse(self, frequency, duration):
        """
        Activates the buzzer for a short duration.

        @param frequency : pulse frequency, in hertz
        @param duration : pulse duration in millseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("P" + str(int(frequency)) + "," + str(int(duration)))

    def freqMove(self, frequency, duration):
        """
        Makes the buzzer frequency change over a period of time.

        @param frequency : frequency to reach, in hertz. A frequency under 25Hz stops the buzzer.
        @param duration :  pulse duration in millseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("F" + str(int(frequency)) + "," + str(int(duration)))

    def volumeMove(self, volume, duration):
        """
        Makes the buzzer volume change over a period of time, frequency  stays untouched.

        @param volume : volume to reach in %
        @param duration : change duration in millseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("V" + str(int(volume)) + "," + str(int(duration)))

    def nextBuzzer(self):
        """
        Continues the enumeration of buzzers started using yFirstBuzzer().

        @return a pointer to a YBuzzer object, corresponding to
                a buzzer currently online, or a None pointer
                if there are no more buzzers to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YBuzzer.FindBuzzer(hwidRef.value)

#--- (end of YBuzzer implementation)

#--- (Buzzer functions)

    @staticmethod
    def FirstBuzzer():
        """
        Starts the enumeration of buzzers currently accessible.
        Use the method YBuzzer.nextBuzzer() to iterate on
        next buzzers.

        @return a pointer to a YBuzzer object, corresponding to
                the first buzzer currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Buzzer", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YBuzzer.FindBuzzer(serialRef.value + "." + funcIdRef.value)

#--- (end of Buzzer functions)
