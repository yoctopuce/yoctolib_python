#*********************************************************************
#*
#* $Id: yocto_audioin.py 20797 2015-07-06 16:49:40Z mvuilleu $
#*
#* Implements yFindAudioIn(), the high-level API for AudioIn functions
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


#--- (YAudioIn class start)
#noinspection PyProtectedMember
class YAudioIn(YFunction):
    """
    The Yoctopuce application programming interface allows you to configure the volume of the input channel.

    """
#--- (end of YAudioIn class start)
    #--- (YAudioIn return codes)
    #--- (end of YAudioIn return codes)
    #--- (YAudioIn dlldef)
    #--- (end of YAudioIn dlldef)
    #--- (YAudioIn definitions)
    VOLUME_INVALID = YAPI.INVALID_UINT
    VOLUMERANGE_INVALID = YAPI.INVALID_STRING
    SIGNAL_INVALID = YAPI.INVALID_INT
    NOSIGNALFOR_INVALID = YAPI.INVALID_INT
    MUTE_FALSE = 0
    MUTE_TRUE = 1
    MUTE_INVALID = -1
    #--- (end of YAudioIn definitions)

    def __init__(self, func):
        super(YAudioIn, self).__init__(func)
        self._className = 'AudioIn'
        #--- (YAudioIn attributes)
        self._callback = None
        self._volume = YAudioIn.VOLUME_INVALID
        self._mute = YAudioIn.MUTE_INVALID
        self._volumeRange = YAudioIn.VOLUMERANGE_INVALID
        self._signal = YAudioIn.SIGNAL_INVALID
        self._noSignalFor = YAudioIn.NOSIGNALFOR_INVALID
        #--- (end of YAudioIn attributes)

    #--- (YAudioIn implementation)
    def _parseAttr(self, member):
        if member.name == "volume":
            self._volume = member.ivalue
            return 1
        if member.name == "mute":
            self._mute = member.ivalue
            return 1
        if member.name == "volumeRange":
            self._volumeRange = member.svalue
            return 1
        if member.name == "signal":
            self._signal = member.ivalue
            return 1
        if member.name == "noSignalFor":
            self._noSignalFor = member.ivalue
            return 1
        super(YAudioIn, self)._parseAttr(member)

    def get_volume(self):
        """
        Returns audio input gain, in per cents.

        @return an integer corresponding to audio input gain, in per cents

        On failure, throws an exception or returns YAudioIn.VOLUME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAudioIn.VOLUME_INVALID
        return self._volume

    def set_volume(self, newval):
        """
        Changes audio input gain, in per cents.

        @param newval : an integer corresponding to audio input gain, in per cents

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("volume", rest_val)

    def get_mute(self):
        """
        Returns the state of the mute function.

        @return either YAudioIn.MUTE_FALSE or YAudioIn.MUTE_TRUE, according to the state of the mute function

        On failure, throws an exception or returns YAudioIn.MUTE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAudioIn.MUTE_INVALID
        return self._mute

    def set_mute(self, newval):
        """
        Changes the state of the mute function. Remember to call the matching module
        saveToFlash() method to save the setting permanently.

        @param newval : either YAudioIn.MUTE_FALSE or YAudioIn.MUTE_TRUE, according to the state of the mute function

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("mute", rest_val)

    def get_volumeRange(self):
        """
        Returns the supported volume range. The low value of the
        range corresponds to the minimal audible value. To
        completely mute the sound, use set_mute()
        instead of the set_volume().

        @return a string corresponding to the supported volume range

        On failure, throws an exception or returns YAudioIn.VOLUMERANGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAudioIn.VOLUMERANGE_INVALID
        return self._volumeRange

    def get_signal(self):
        """
        Returns the detected input signal level.

        @return an integer corresponding to the detected input signal level

        On failure, throws an exception or returns YAudioIn.SIGNAL_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAudioIn.SIGNAL_INVALID
        return self._signal

    def get_noSignalFor(self):
        """
        Returns the number of seconds elapsed without detecting a signal

        @return an integer corresponding to the number of seconds elapsed without detecting a signal

        On failure, throws an exception or returns YAudioIn.NOSIGNALFOR_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAudioIn.NOSIGNALFOR_INVALID
        return self._noSignalFor

    @staticmethod
    def FindAudioIn(func):
        """
        Retrieves an audio input for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the audio input is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YAudioIn.isOnline() to test if the audio input is
        indeed online at a given time. In case of ambiguity when looking for
        an audio input by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the audio input

        @return a YAudioIn object allowing you to drive the audio input.
        """
        # obj
        obj = YFunction._FindFromCache("AudioIn", func)
        if obj is None:
            obj = YAudioIn(func)
            YFunction._AddToCache("AudioIn", func, obj)
        return obj

    def nextAudioIn(self):
        """
        Continues the enumeration of audio inputs started using yFirstAudioIn().

        @return a pointer to a YAudioIn object, corresponding to
                an audio input currently online, or a None pointer
                if there are no more audio inputs to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YAudioIn.FindAudioIn(hwidRef.value)

#--- (end of YAudioIn implementation)

#--- (AudioIn functions)

    @staticmethod
    def FirstAudioIn():
        """
        Starts the enumeration of audio inputs currently accessible.
        Use the method YAudioIn.nextAudioIn() to iterate on
        next audio inputs.

        @return a pointer to a YAudioIn object, corresponding to
                the first audio input currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("AudioIn", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YAudioIn.FindAudioIn(serialRef.value + "." + funcIdRef.value)

#--- (end of AudioIn functions)
