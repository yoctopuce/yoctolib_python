# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindColorSensor(), the high-level API for ColorSensor functions
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


#--- (YColorSensor class start)
#noinspection PyProtectedMember
class YColorSensor(YFunction):
    """
    The YColorSensor class allows you to read and configure Yoctopuce color sensors.

    """
    #--- (end of YColorSensor class start)
    #--- (YColorSensor return codes)
    #--- (end of YColorSensor return codes)
    #--- (YColorSensor dlldef)
    #--- (end of YColorSensor dlldef)
    #--- (YColorSensor yapiwrapper)
    #--- (end of YColorSensor yapiwrapper)
    #--- (YColorSensor definitions)
    LEDCURRENT_INVALID = YAPI.INVALID_UINT
    LEDCALIBRATION_INVALID = YAPI.INVALID_UINT
    INTEGRATIONTIME_INVALID = YAPI.INVALID_UINT
    GAIN_INVALID = YAPI.INVALID_UINT
    AUTOGAIN_INVALID = YAPI.INVALID_STRING
    SATURATION_INVALID = YAPI.INVALID_UINT
    ESTIMATEDRGB_INVALID = YAPI.INVALID_UINT
    ESTIMATEDHSL_INVALID = YAPI.INVALID_UINT
    ESTIMATEDXYZ_INVALID = YAPI.INVALID_STRING
    ESTIMATEDOKLAB_INVALID = YAPI.INVALID_STRING
    NEARRAL1_INVALID = YAPI.INVALID_STRING
    NEARRAL2_INVALID = YAPI.INVALID_STRING
    NEARRAL3_INVALID = YAPI.INVALID_STRING
    NEARHTMLCOLOR_INVALID = YAPI.INVALID_STRING
    NEARSIMPLECOLOR_INVALID = YAPI.INVALID_STRING
    ESTIMATIONMODEL_REFLECTION = 0
    ESTIMATIONMODEL_EMISSION = 1
    ESTIMATIONMODEL_INVALID = -1
    WORKINGMODE_AUTO = 0
    WORKINGMODE_EXPERT = 1
    WORKINGMODE_AUTOGAIN = 2
    WORKINGMODE_INVALID = -1
    NEARSIMPLECOLORINDEX_BROWN = 0
    NEARSIMPLECOLORINDEX_RED = 1
    NEARSIMPLECOLORINDEX_ORANGE = 2
    NEARSIMPLECOLORINDEX_YELLOW = 3
    NEARSIMPLECOLORINDEX_WHITE = 4
    NEARSIMPLECOLORINDEX_GRAY = 5
    NEARSIMPLECOLORINDEX_BLACK = 6
    NEARSIMPLECOLORINDEX_GREEN = 7
    NEARSIMPLECOLORINDEX_BLUE = 8
    NEARSIMPLECOLORINDEX_PURPLE = 9
    NEARSIMPLECOLORINDEX_PINK = 10
    NEARSIMPLECOLORINDEX_INVALID = -1
    #--- (end of YColorSensor definitions)

    def __init__(self, func):
        super(YColorSensor, self).__init__(func)
        self._className = 'ColorSensor'
        #--- (YColorSensor attributes)
        self._callback = None
        self._estimationModel = YColorSensor.ESTIMATIONMODEL_INVALID
        self._workingMode = YColorSensor.WORKINGMODE_INVALID
        self._ledCurrent = YColorSensor.LEDCURRENT_INVALID
        self._ledCalibration = YColorSensor.LEDCALIBRATION_INVALID
        self._integrationTime = YColorSensor.INTEGRATIONTIME_INVALID
        self._gain = YColorSensor.GAIN_INVALID
        self._autoGain = YColorSensor.AUTOGAIN_INVALID
        self._saturation = YColorSensor.SATURATION_INVALID
        self._estimatedRGB = YColorSensor.ESTIMATEDRGB_INVALID
        self._estimatedHSL = YColorSensor.ESTIMATEDHSL_INVALID
        self._estimatedXYZ = YColorSensor.ESTIMATEDXYZ_INVALID
        self._estimatedOkLab = YColorSensor.ESTIMATEDOKLAB_INVALID
        self._nearRAL1 = YColorSensor.NEARRAL1_INVALID
        self._nearRAL2 = YColorSensor.NEARRAL2_INVALID
        self._nearRAL3 = YColorSensor.NEARRAL3_INVALID
        self._nearHTMLColor = YColorSensor.NEARHTMLCOLOR_INVALID
        self._nearSimpleColorIndex = YColorSensor.NEARSIMPLECOLORINDEX_INVALID
        self._nearSimpleColor = YColorSensor.NEARSIMPLECOLOR_INVALID
        #--- (end of YColorSensor attributes)

    #--- (YColorSensor implementation)
    def _parseAttr(self, json_val):
        if json_val.has("estimationModel"):
            self._estimationModel = json_val.getInt("estimationModel")
        if json_val.has("workingMode"):
            self._workingMode = json_val.getInt("workingMode")
        if json_val.has("ledCurrent"):
            self._ledCurrent = json_val.getInt("ledCurrent")
        if json_val.has("ledCalibration"):
            self._ledCalibration = json_val.getInt("ledCalibration")
        if json_val.has("integrationTime"):
            self._integrationTime = json_val.getInt("integrationTime")
        if json_val.has("gain"):
            self._gain = json_val.getInt("gain")
        if json_val.has("autoGain"):
            self._autoGain = json_val.getString("autoGain")
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
        if json_val.has("nearHTMLColor"):
            self._nearHTMLColor = json_val.getString("nearHTMLColor")
        if json_val.has("nearSimpleColorIndex"):
            self._nearSimpleColorIndex = json_val.getInt("nearSimpleColorIndex")
        if json_val.has("nearSimpleColor"):
            self._nearSimpleColor = json_val.getString("nearSimpleColor")
        super(YColorSensor, self)._parseAttr(json_val)

    def get_estimationModel(self):
        """
        Returns the predictive model used for color estimation (reflective or emissive).

        @return either YColorSensor.ESTIMATIONMODEL_REFLECTION or YColorSensor.ESTIMATIONMODEL_EMISSION,
        according to the predictive model used for color estimation (reflective or emissive)

        On failure, throws an exception or returns YColorSensor.ESTIMATIONMODEL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.ESTIMATIONMODEL_INVALID
        res = self._estimationModel
        return res

    def set_estimationModel(self, newval):
        """
        Changes the predictive model to be used for color estimation (reflective or emissive).
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : either YColorSensor.ESTIMATIONMODEL_REFLECTION or
        YColorSensor.ESTIMATIONMODEL_EMISSION, according to the predictive model to be used for color
        estimation (reflective or emissive)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("estimationModel", rest_val)

    def get_workingMode(self):
        """
        Returns the sensor working mode.
        In Auto mode, sensor parameters are automatically set based on the selected estimation model.
        In Expert mode, sensor parameters such as gain and integration time are configured manually.

        @return a value among YColorSensor.WORKINGMODE_AUTO, YColorSensor.WORKINGMODE_EXPERT and
        YColorSensor.WORKINGMODE_AUTOGAIN corresponding to the sensor working mode

        On failure, throws an exception or returns YColorSensor.WORKINGMODE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.WORKINGMODE_INVALID
        res = self._workingMode
        return res

    def set_workingMode(self, newval):
        """
        Changes the sensor working mode.
        In Auto mode, sensor parameters are automatically set based on the selected estimation model.
        In Expert mode, sensor parameters such as gain and integration time are configured manually.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : a value among YColorSensor.WORKINGMODE_AUTO, YColorSensor.WORKINGMODE_EXPERT and
        YColorSensor.WORKINGMODE_AUTOGAIN corresponding to the sensor working mode

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("workingMode", rest_val)

    def get_ledCurrent(self):
        """
        Returns the amount of current sent to the illumination LEDs, for reflection measures.
        The value is an integer ranging from 0 (LEDs off) to 254 (LEDs at maximum intensity).

        @return an integer corresponding to the amount of current sent to the illumination LEDs, for reflection measures

        On failure, throws an exception or returns YColorSensor.LEDCURRENT_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.LEDCURRENT_INVALID
        res = self._ledCurrent
        return res

    def set_ledCurrent(self, newval):
        """
        Changes the amount of current sent to the illumination LEDs, for reflection measures.
        The value is an integer ranging from 0 (LEDs off) to 254 (LEDs at maximum intensity).

        @param newval : an integer corresponding to the amount of current sent to the illumination LEDs,
        for reflection measures

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("ledCurrent", rest_val)

    def get_ledCalibration(self):
        """
        Returns the current sent to the illumination LEDs during the latest calibration.

        @return an integer corresponding to the current sent to the illumination LEDs during the latest calibration

        On failure, throws an exception or returns YColorSensor.LEDCALIBRATION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.LEDCALIBRATION_INVALID
        res = self._ledCalibration
        return res

    def set_ledCalibration(self, newval):
        """
        Remember the LED current sent to the illumination LEDs during a calibration.
        Thanks to this, the device is able to use the same current when taking measures.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("ledCalibration", rest_val)

    def get_integrationTime(self):
        """
        Returns the current integration time for spectral measure, in milliseconds.
        A longer integration time increase the sensitivity for low light conditions,
        but reduces the measure taking rate and may lead to saturation for lighter colors.

        @return an integer corresponding to the current integration time for spectral measure, in milliseconds

        On failure, throws an exception or returns YColorSensor.INTEGRATIONTIME_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.INTEGRATIONTIME_INVALID
        res = self._integrationTime
        return res

    def set_integrationTime(self, newval):
        """
        Changes the integration time for spectral measure, in milliseconds.
        A longer integration time increase the sensitivity for low light conditions,
        but reduces the measure taking rate and may lead to saturation for lighter colors.
        This method can only be used when the sensor is configured in expert mode;
        when running in auto mode, the change is ignored.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the integration time for spectral measure, in milliseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("integrationTime", rest_val)

    def get_gain(self):
        """
        Returns the current spectral channel detector gain exponent.
        For a value n ranging from 0 to 12, the applied gain is 2^(n-1).
        0 corresponds to a gain of 0.5, and 12 corresponds to a gain of 2048.

        @return an integer corresponding to the current spectral channel detector gain exponent

        On failure, throws an exception or returns YColorSensor.GAIN_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.GAIN_INVALID
        res = self._gain
        return res

    def set_gain(self, newval):
        """
        Changes the spectral channel detector gain exponent.
        For a value n ranging from 0 to 12, the applied gain is 2^(n-1).
        0 corresponds to a gain of 0.5, and 12 corresponds to a gain of 2048.
        This method can only be used when the sensor is configured in expert mode;
        when running in auto mode, the change is ignored.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the spectral channel detector gain exponent

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("gain", rest_val)

    def get_autoGain(self):
        """
        Returns the current autogain parameters of the sensor as a character string.
        The returned parameter format is: "Min &lt; Channel &lt; Max:Saturation".

        @return a string corresponding to the current autogain parameters of the sensor as a character string

        On failure, throws an exception or returns YColorSensor.AUTOGAIN_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.AUTOGAIN_INVALID
        res = self._autoGain
        return res

    def set_autoGain(self, newval):
        """
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : a string

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("autoGain", rest_val)

    def get_saturation(self):
        """
        Returns the current saturation state of the sensor, as an integer.
        Bit 0 indicates saturation of the analog sensor, which can only
        be corrected by reducing the gain parameters or the luminosity.
        Bit 1 indicates saturation of the digital interface, which can
        be corrected by reducing the integration time or the gain.

        @return an integer corresponding to the current saturation state of the sensor, as an integer

        On failure, throws an exception or returns YColorSensor.SATURATION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.SATURATION_INVALID
        res = self._saturation
        return res

    def get_estimatedRGB(self):
        """
        Returns the estimated color in RGB color model (0xRRGGBB).
        The RGB color model describes each color using a combination of 3 components:
        - Red (R): the intensity of red, in the 0...255 range
        - Green (G): the intensity of green, in the 0...255 range
        - Blue (B): the intensity of blue, in the 0...255 range

        @return an integer corresponding to the estimated color in RGB color model (0xRRGGBB)

        On failure, throws an exception or returns YColorSensor.ESTIMATEDRGB_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.ESTIMATEDRGB_INVALID
        res = self._estimatedRGB
        return res

    def get_estimatedHSL(self):
        """
        Returns the estimated color in HSL color model (0xHHSSLL).
        The HSL color model describes each color using a combination of 3 components:
        - Hue (H): the angle on the color wheel (0-360 degrees), mapped to 0...255
        - Saturation (S): the intensity of the color (0-100%), mapped to 0...255
        - Lightness (L): the brightness of the color (0-100%), mapped to 0...255

        @return an integer corresponding to the estimated color in HSL color model (0xHHSSLL)

        On failure, throws an exception or returns YColorSensor.ESTIMATEDHSL_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.ESTIMATEDHSL_INVALID
        res = self._estimatedHSL
        return res

    def get_estimatedXYZ(self):
        """
        Returns the estimated color according to the CIE XYZ color model.
        This color model is based on human vision and light perception, with three components
        represented by real numbers between 0 and 1:
        - X: corresponds to a component mixing sensitivity to red and green
        - Y: represents luminance (perceived brightness)
        - Z: corresponds to sensitivity to blue

        @return a string corresponding to the estimated color according to the CIE XYZ color model

        On failure, throws an exception or returns YColorSensor.ESTIMATEDXYZ_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.ESTIMATEDXYZ_INVALID
        res = self._estimatedXYZ
        return res

    def get_estimatedOkLab(self):
        """
        Returns the estimated color according to the OkLab color model.
        OkLab is a perceptual color model that aims to align human color perception with numerical
        values, so that colors that are visually near are also numerically near. Colors are represented
        using three components:
        - L: lightness, a real number between 0 and 1
        - a: color variations between green and red, between -0.5 and 0.5
        - b: color variations between blue and yellow, between -0.5 and 0.5.

        @return a string corresponding to the estimated color according to the OkLab color model

        On failure, throws an exception or returns YColorSensor.ESTIMATEDOKLAB_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.ESTIMATEDOKLAB_INVALID
        res = self._estimatedOkLab
        return res

    def get_nearRAL1(self):
        """
        Returns the RAL Classic color closest to the estimated color, with a similarity ratio.

        @return a string corresponding to the RAL Classic color closest to the estimated color, with a similarity ratio

        On failure, throws an exception or returns YColorSensor.NEARRAL1_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.NEARRAL1_INVALID
        res = self._nearRAL1
        return res

    def get_nearRAL2(self):
        """
        Returns the second closest RAL Classic color to the estimated color, with a similarity ratio.

        @return a string corresponding to the second closest RAL Classic color to the estimated color, with
        a similarity ratio

        On failure, throws an exception or returns YColorSensor.NEARRAL2_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.NEARRAL2_INVALID
        res = self._nearRAL2
        return res

    def get_nearRAL3(self):
        """
        Returns the third closest RAL Classic color to the estimated color, with a similarity ratio.

        @return a string corresponding to the third closest RAL Classic color to the estimated color, with
        a similarity ratio

        On failure, throws an exception or returns YColorSensor.NEARRAL3_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.NEARRAL3_INVALID
        res = self._nearRAL3
        return res

    def get_nearHTMLColor(self):
        """
        Returns the name of the HTML color closest to the estimated color.

        @return a string corresponding to the name of the HTML color closest to the estimated color

        On failure, throws an exception or returns YColorSensor.NEARHTMLCOLOR_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.NEARHTMLCOLOR_INVALID
        res = self._nearHTMLColor
        return res

    def get_nearSimpleColorIndex(self):
        """
        Returns the index of the basic color typically used to refer to the estimated color (enumerated value).
        The list of basic colors recognized is:
        - 0 - Brown
        - 1 - Red
        - 2 - Orange
        - 3 - Yellow
        - 4 - White
        - 5 - Gray
        - 6 - Black
        - 7 - Green
        - 8 - Blue
        - 9 - Purple
        - 10 - Pink

        @return a value among YColorSensor.NEARSIMPLECOLORINDEX_BROWN,
        YColorSensor.NEARSIMPLECOLORINDEX_RED, YColorSensor.NEARSIMPLECOLORINDEX_ORANGE,
        YColorSensor.NEARSIMPLECOLORINDEX_YELLOW, YColorSensor.NEARSIMPLECOLORINDEX_WHITE,
        YColorSensor.NEARSIMPLECOLORINDEX_GRAY, YColorSensor.NEARSIMPLECOLORINDEX_BLACK,
        YColorSensor.NEARSIMPLECOLORINDEX_GREEN, YColorSensor.NEARSIMPLECOLORINDEX_BLUE,
        YColorSensor.NEARSIMPLECOLORINDEX_PURPLE and YColorSensor.NEARSIMPLECOLORINDEX_PINK corresponding
        to the index of the basic color typically used to refer to the estimated color (enumerated value)

        On failure, throws an exception or returns YColorSensor.NEARSIMPLECOLORINDEX_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.NEARSIMPLECOLORINDEX_INVALID
        res = self._nearSimpleColorIndex
        return res

    def get_nearSimpleColor(self):
        """
        Returns the name of the basic color typically used to refer to the estimated color.

        @return a string corresponding to the name of the basic color typically used to refer to the estimated color

        On failure, throws an exception or returns YColorSensor.NEARSIMPLECOLOR_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YColorSensor.NEARSIMPLECOLOR_INVALID
        res = self._nearSimpleColor
        return res

    @staticmethod
    def FindColorSensor(func):
        """
        Retrieves a color sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the color sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YColorSensor.isOnline() to test if the color sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a color sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the color sensor, for instance
                MyDevice.colorSensor.

        @return a YColorSensor object allowing you to drive the color sensor.
        """
        # obj
        obj = YFunction._FindFromCache("ColorSensor", func)
        if obj is None:
            obj = YColorSensor(func)
            YFunction._AddToCache("ColorSensor", func, obj)
        return obj

    def configureAutoGain(self, channel, minRaw, maxRaw, noSatur):
        """
        Changes the sensor automatic gain control settings.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param channel : reference channel to use for automated gain control.
        @param minRaw : lower threshold for the measured raw value, below which the gain is
                automatically increased as long as possible.
        @param maxRaw : high threshold for the measured raw value, over which the gain is
                automatically decreased as long as possible.
        @param noSatur : enables gain reduction in case of sensor saturation.

        @return YAPI.SUCCESS if the operation completes successfully.
                On failure, throws an exception or returns a negative error code.
        """
        # opt
        if noSatur:
            opt = "nosat"
        else:
            opt = ""

        return self.set_autoGain("" + str(int(minRaw)) + " < " + channel + " < " + str(int(maxRaw)) + ":" + opt)

    def turnLedOn(self):
        """
        Turns on the built-in illumination LEDs using the same current as used during the latest calibration.
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_ledCurrent(self.get_ledCalibration())

    def turnLedOff(self):
        """
        Turns off the built-in illumination LEDs.
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_ledCurrent(0)

    def nextColorSensor(self):
        """
        Continues the enumeration of color sensors started using yFirstColorSensor().
        Caution: You can't make any assumption about the returned color sensors order.
        If you want to find a specific a color sensor, use ColorSensor.findColorSensor()
        and a hardwareID or a logical name.

        @return a pointer to a YColorSensor object, corresponding to
                a color sensor currently online, or a None pointer
                if there are no more color sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YColorSensor.FindColorSensor(hwidRef.value)

#--- (end of YColorSensor implementation)

#--- (YColorSensor functions)

    @staticmethod
    def FirstColorSensor():
        """
        Starts the enumeration of color sensors currently accessible.
        Use the method YColorSensor.nextColorSensor() to iterate on
        next color sensors.

        @return a pointer to a YColorSensor object, corresponding to
                the first color sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("ColorSensor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YColorSensor.FindColorSensor(serialRef.value + "." + funcIdRef.value)

#--- (end of YColorSensor functions)
