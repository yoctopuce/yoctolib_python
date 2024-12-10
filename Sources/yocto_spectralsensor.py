# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindSpectralSensor(), the high-level API for SpectralSensor functions
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


#--- (YSpectralSensor class start)
#noinspection PyProtectedMember
class YSpectralSensor(YFunction):
    """
    The YSpectralSensor class allows you to read and configure Yoctopuce spectral sensors.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    #--- (end of YSpectralSensor class start)
    #--- (YSpectralSensor return codes)
    #--- (end of YSpectralSensor return codes)
    #--- (YSpectralSensor dlldef)
    #--- (end of YSpectralSensor dlldef)
    #--- (YSpectralSensor yapiwrapper)
    #--- (end of YSpectralSensor yapiwrapper)
    #--- (YSpectralSensor definitions)
    LEDCURRENT_INVALID = YAPI.INVALID_INT
    RESOLUTION_INVALID = YAPI.INVALID_DOUBLE
    INTEGRATIONTIME_INVALID = YAPI.INVALID_INT
    GAIN_INVALID = YAPI.INVALID_INT
    SATURATION_INVALID = YAPI.INVALID_UINT
    ESTIMATEDRGB_INVALID = YAPI.INVALID_UINT
    ESTIMATEDHSL_INVALID = YAPI.INVALID_UINT
    ESTIMATEDXYZ_INVALID = YAPI.INVALID_STRING
    ESTIMATEDOKLAB_INVALID = YAPI.INVALID_STRING
    NEARRAL1_INVALID = YAPI.INVALID_STRING
    NEARRAL2_INVALID = YAPI.INVALID_STRING
    NEARRAL3_INVALID = YAPI.INVALID_STRING
    LEDCURRENTATPOWERON_INVALID = YAPI.INVALID_INT
    INTEGRATIONTIMEATPOWERON_INVALID = YAPI.INVALID_INT
    GAINATPOWERON_INVALID = YAPI.INVALID_INT
    ESTIMATIONMODEL_REFLECTION = 0
    ESTIMATIONMODEL_EMISSION = 1
    ESTIMATIONMODEL_INVALID = -1
    #--- (end of YSpectralSensor definitions)

    def __init__(self, func):
        super(YSpectralSensor, self).__init__(func)
        self._className = 'SpectralSensor'
        #--- (YSpectralSensor attributes)
        self._callback = None
        self._ledCurrent = YSpectralSensor.LEDCURRENT_INVALID
        self._resolution = YSpectralSensor.RESOLUTION_INVALID
        self._integrationTime = YSpectralSensor.INTEGRATIONTIME_INVALID
        self._gain = YSpectralSensor.GAIN_INVALID
        self._estimationModel = YSpectralSensor.ESTIMATIONMODEL_INVALID
        self._saturation = YSpectralSensor.SATURATION_INVALID
        self._estimatedRGB = YSpectralSensor.ESTIMATEDRGB_INVALID
        self._estimatedHSL = YSpectralSensor.ESTIMATEDHSL_INVALID
        self._estimatedXYZ = YSpectralSensor.ESTIMATEDXYZ_INVALID
        self._estimatedOkLab = YSpectralSensor.ESTIMATEDOKLAB_INVALID
        self._nearRAL1 = YSpectralSensor.NEARRAL1_INVALID
        self._nearRAL2 = YSpectralSensor.NEARRAL2_INVALID
        self._nearRAL3 = YSpectralSensor.NEARRAL3_INVALID
        self._ledCurrentAtPowerOn = YSpectralSensor.LEDCURRENTATPOWERON_INVALID
        self._integrationTimeAtPowerOn = YSpectralSensor.INTEGRATIONTIMEATPOWERON_INVALID
        self._gainAtPowerOn = YSpectralSensor.GAINATPOWERON_INVALID
        #--- (end of YSpectralSensor attributes)

    #--- (YSpectralSensor implementation)
    def _parseAttr(self, json_val):
        if json_val.has("ledCurrent"):
            self._ledCurrent = json_val.getInt("ledCurrent")
        if json_val.has("resolution"):
            self._resolution = round(json_val.getDouble("resolution") / 65.536) / 1000.0
        if json_val.has("integrationTime"):
            self._integrationTime = json_val.getInt("integrationTime")
        if json_val.has("gain"):
            self._gain = json_val.getInt("gain")
        if json_val.has("estimationModel"):
            self._estimationModel = json_val.getInt("estimationModel")
        if json_val.has("saturation"):
            self._saturation = json_val.getInt("saturation")
        if json_val.has("estimatedRGB"):
            self._estimatedRGB = json_val.getInt("estimatedRGB")
        if json_val.has("estimatedHSL"):
            self._estimatedHSL = json_val.getInt("estimatedHSL")
        if json_val.has("estimatedXYZ"):
            self._estimatedXYZ = json_val.getString("estimatedXYZ")
        if json_val.has("estimatedOkLab"):
            self._estimatedOkLab = json_val.getString("estimatedOkLab")
        if json_val.has("nearRAL1"):
            self._nearRAL1 = json_val.getString("nearRAL1")
        if json_val.has("nearRAL2"):
            self._nearRAL2 = json_val.getString("nearRAL2")
        if json_val.has("nearRAL3"):
            self._nearRAL3 = json_val.getString("nearRAL3")
        if json_val.has("ledCurrentAtPowerOn"):
            self._ledCurrentAtPowerOn = json_val.getInt("ledCurrentAtPowerOn")
        if json_val.has("integrationTimeAtPowerOn"):
            self._integrationTimeAtPowerOn = json_val.getInt("integrationTimeAtPowerOn")
        if json_val.has("gainAtPowerOn"):
            self._gainAtPowerOn = json_val.getInt("gainAtPowerOn")
        super(YSpectralSensor, self)._parseAttr(json_val)

    def get_ledCurrent(self):
        """
        Returns the current value of the LED.
        This method retrieves the current flowing through the LED
        and returns it as an integer or an object.

        @return an integer corresponding to the current value of the LED

        On failure, throws an exception or returns YSpectralSensor.LEDCURRENT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.LEDCURRENT_INVALID
        res = self._ledCurrent
        return res

    def set_ledCurrent(self, newval):
        """
        Changes the luminosity of the module leds. The parameter is a
        value between 0 and 100.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : an integer corresponding to the luminosity of the module leds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("ledCurrent", rest_val)

    def set_resolution(self, newval):
        """
        Changes the resolution of the measured physical values. The resolution corresponds to the numerical precision
        when displaying value. It does not change the precision of the measure itself.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : a floating point number corresponding to the resolution of the measured physical values

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("resolution", rest_val)

    def get_resolution(self):
        """
        Returns the resolution of the measured values. The resolution corresponds to the numerical precision
        of the measures, which is not always the same as the actual precision of the sensor.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @return a floating point number corresponding to the resolution of the measured values

        On failure, throws an exception or returns YSpectralSensor.RESOLUTION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.RESOLUTION_INVALID
        res = self._resolution
        return res

    def get_integrationTime(self):
        """
        Returns the current integration time.
        This method retrieves the integration time value
        used for data processing and returns it as an integer or an object.

        @return an integer corresponding to the current integration time

        On failure, throws an exception or returns YSpectralSensor.INTEGRATIONTIME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.INTEGRATIONTIME_INVALID
        res = self._integrationTime
        return res

    def set_integrationTime(self, newval):
        """
        Sets the integration time for data processing.
        This method takes a parameter `val` and assigns it
        as the new integration time. This affects the duration
        for which data is integrated before being processed.

        @param newval : an integer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("integrationTime", rest_val)

    def get_gain(self):
        """
        Retrieves the current gain.
        This method updates the gain value.

        @return an integer

        On failure, throws an exception or returns YSpectralSensor.GAIN_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.GAIN_INVALID
        res = self._gain
        return res

    def set_gain(self, newval):
        """
        Sets the gain for signal processing.
        This method takes a parameter `val` and assigns it
        as the new gain. This affects the sensitivity and
        intensity of the processed signal.

        @param newval : an integer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("gain", rest_val)

    def get_estimationModel(self):
        """
        Return the model for the estimation colors.

        @return either YSpectralSensor.ESTIMATIONMODEL_REFLECTION or YSpectralSensor.ESTIMATIONMODEL_EMISSION

        On failure, throws an exception or returns YSpectralSensor.ESTIMATIONMODEL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.ESTIMATIONMODEL_INVALID
        res = self._estimationModel
        return res

    def set_estimationModel(self, newval):
        """
        Change the model for the estimation colors.

        @param newval : either YSpectralSensor.ESTIMATIONMODEL_REFLECTION or YSpectralSensor.ESTIMATIONMODEL_EMISSION

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("estimationModel", rest_val)

    def get_saturation(self):
        """
        Returns the current saturation of the sensor.
        This function updates the sensor's saturation value.

        @return an integer corresponding to the current saturation of the sensor

        On failure, throws an exception or returns YSpectralSensor.SATURATION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.SATURATION_INVALID
        res = self._saturation
        return res

    def get_estimatedRGB(self):
        """
        Returns the estimated color in RGB format.
        This method retrieves the estimated color values
        and returns them as an RGB object or structure.

        @return an integer corresponding to the estimated color in RGB format

        On failure, throws an exception or returns YSpectralSensor.ESTIMATEDRGB_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.ESTIMATEDRGB_INVALID
        res = self._estimatedRGB
        return res

    def get_estimatedHSL(self):
        """
        Returns the estimated color in HSL format.
        This method retrieves the estimated color values
        and returns them as an HSL object or structure.

        @return an integer corresponding to the estimated color in HSL format

        On failure, throws an exception or returns YSpectralSensor.ESTIMATEDHSL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.ESTIMATEDHSL_INVALID
        res = self._estimatedHSL
        return res

    def get_estimatedXYZ(self):
        """
        Returns the estimated color in XYZ format.
        This method retrieves the estimated color values
        and returns them as an XYZ object or structure.

        @return a string corresponding to the estimated color in XYZ format

        On failure, throws an exception or returns YSpectralSensor.ESTIMATEDXYZ_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.ESTIMATEDXYZ_INVALID
        res = self._estimatedXYZ
        return res

    def get_estimatedOkLab(self):
        """
        Returns the estimated color in OkLab format.
        This method retrieves the estimated color values
        and returns them as an OkLab object or structure.

        @return a string corresponding to the estimated color in OkLab format

        On failure, throws an exception or returns YSpectralSensor.ESTIMATEDOKLAB_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.ESTIMATEDOKLAB_INVALID
        res = self._estimatedOkLab
        return res

    def get_nearRAL1(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.NEARRAL1_INVALID
        res = self._nearRAL1
        return res

    def get_nearRAL2(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.NEARRAL2_INVALID
        res = self._nearRAL2
        return res

    def get_nearRAL3(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.NEARRAL3_INVALID
        res = self._nearRAL3
        return res

    def get_ledCurrentAtPowerOn(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.LEDCURRENTATPOWERON_INVALID
        res = self._ledCurrentAtPowerOn
        return res

    def set_ledCurrentAtPowerOn(self, newval):
        """
        Sets the LED current at power-on.
        This method takes a parameter `val` and assigns it to startupLumin, representing the LED current defined
        at startup.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("ledCurrentAtPowerOn", rest_val)

    def get_integrationTimeAtPowerOn(self):
        """
        Retrieves the integration time at power-on.
        This method updates the power-on integration time value.

        @return an integer

        On failure, throws an exception or returns YSpectralSensor.INTEGRATIONTIMEATPOWERON_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.INTEGRATIONTIMEATPOWERON_INVALID
        res = self._integrationTimeAtPowerOn
        return res

    def set_integrationTimeAtPowerOn(self, newval):
        """
        Sets the integration time at power-on.
        This method takes a parameter `val` and assigns it to startupIntegTime, representing the integration time
        defined at startup.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("integrationTimeAtPowerOn", rest_val)

    def get_gainAtPowerOn(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YSpectralSensor.GAINATPOWERON_INVALID
        res = self._gainAtPowerOn
        return res

    def set_gainAtPowerOn(self, newval):
        """
        Sets the gain at power-on.
        This method takes a parameter `val` and assigns it to startupGain, representing the gain defined at startup.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("gainAtPowerOn", rest_val)

    @staticmethod
    def FindSpectralSensor(func):
        """
        Retrieves a spectral sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the spectral sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSpectralSensor.isOnline() to test if the spectral sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a spectral sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the spectral sensor, for instance
                MyDevice.spectralSensor.

        @return a YSpectralSensor object allowing you to drive the spectral sensor.
        """
        # obj
        obj = YFunction._FindFromCache("SpectralSensor", func)
        if obj is None:
            obj = YSpectralSensor(func)
            YFunction._AddToCache("SpectralSensor", func, obj)
        return obj

    def nextSpectralSensor(self):
        """
        Continues the enumeration of spectral sensors started using yFirstSpectralSensor().
        Caution: You can't make any assumption about the returned spectral sensors order.
        If you want to find a specific a spectral sensor, use SpectralSensor.findSpectralSensor()
        and a hardwareID or a logical name.

        @return a pointer to a YSpectralSensor object, corresponding to
                a spectral sensor currently online, or a None pointer
                if there are no more spectral sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YSpectralSensor.FindSpectralSensor(hwidRef.value)

#--- (end of YSpectralSensor implementation)

#--- (YSpectralSensor functions)

    @staticmethod
    def FirstSpectralSensor():
        """
        Starts the enumeration of spectral sensors currently accessible.
        Use the method YSpectralSensor.nextSpectralSensor() to iterate on
        next spectral sensors.

        @return a pointer to a YSpectralSensor object, corresponding to
                the first spectral sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("SpectralSensor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YSpectralSensor.FindSpectralSensor(serialRef.value + "." + funcIdRef.value)

#--- (end of YSpectralSensor functions)
