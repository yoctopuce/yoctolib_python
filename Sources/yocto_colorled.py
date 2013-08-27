#*********************************************************************
#*
#* $Id: yocto_colorled.py 12324 2013-08-13 15:10:31Z mvuilleu $
#*
#* Implements yFindColorLed(), the high-level API for ColorLed functions
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
class YColorLed(YFunction):
    """
    Yoctopuce application programming interface
    allows you to drive a color led using RGB coordinates as well as HSL coordinates.
    The module performs all conversions form RGB to HSL automatically. It is then
    self-evident to turn on a led with a given hue and to progressively vary its
    saturation or lightness. If needed, you can find more information on the
    difference between RGB and HSL in the section following this one.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YColorLed definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    RGBCOLOR_INVALID                = YAPI.INVALID_LONG
    HSLCOLOR_INVALID                = YAPI.INVALID_LONG
    RGBMOVE_INVALID                 = None
    HSLMOVE_INVALID                 = None
    RGBCOLORATPOWERON_INVALID       = YAPI.INVALID_LONG



    _ColorLedCache ={}

    #--- (end of YColorLed definitions)

    #--- (YColorLed implementation)

    def __init__(self,func):
        super(YColorLed,self).__init__("ColorLed", func)
        self._callback = None
        self._logicalName = YColorLed.LOGICALNAME_INVALID
        self._advertisedValue = YColorLed.ADVERTISEDVALUE_INVALID
        self._rgbColor = YColorLed.RGBCOLOR_INVALID
        self._hslColor = YColorLed.HSLCOLOR_INVALID
        self._rgbMove = YColorLed.RGBMOVE_INVALID
        self._hslMove = YColorLed.HSLMOVE_INVALID
        self._rgbColorAtPowerOn = YColorLed.RGBCOLORATPOWERON_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "rgbColor":
                self._rgbColor = member.ivalue
            elif member.name == "hslColor":
                self._hslColor = member.ivalue
            elif member.name == "rgbMove":
                if member.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: self._rgbMove = -1
                self._rgbMove = {"moving":None,"target":None,"ms":None }
                for submemb in member.members:
                    if submemb.name == "moving":
                        self._rgbMove["moving"]  = submemb.ivalue
                    elif submemb.name == "target": 
                        self._rgbMove["target"] = submemb.ivalue
                    elif submemb.name == "ms": 
                        self._rgbMove["ms"] = submemb.ivalue
            elif member.name == "hslMove":
                if member.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: self._hslMove = -1
                self._hslMove = {"moving":None,"target":None,"ms":None }
                for submemb in member.members:
                    if submemb.name == "moving":
                        self._hslMove["moving"]  = submemb.ivalue
                    elif submemb.name == "target": 
                        self._hslMove["target"] = submemb.ivalue
                    elif submemb.name == "ms": 
                        self._hslMove["ms"] = submemb.ivalue
            elif member.name == "rgbColorAtPowerOn":
                self._rgbColorAtPowerOn = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the RGB led.
        
        @return a string corresponding to the logical name of the RGB led
        
        On failure, throws an exception or returns YColorLed.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the RGB led. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the RGB led
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the RGB led (no more than 6 characters).
        
        @return a string corresponding to the current value of the RGB led (no more than 6 characters)
        
        On failure, throws an exception or returns YColorLed.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_rgbColor(self):
        """
        Returns the current RGB color of the led.
        
        @return an integer corresponding to the current RGB color of the led
        
        On failure, throws an exception or returns YColorLed.RGBCOLOR_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.RGBCOLOR_INVALID
        return self._rgbColor

    def set_rgbColor(self, newval):
        """
        Changes the current color of the led, using a RGB color. Encoding is done as follows: 0xRRGGBB.
        
        @param newval : an integer corresponding to the current color of the led, using a RGB color
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "0x"+'%X' % newval
        return self._setAttr("rgbColor", rest_val)


    def get_hslColor(self):
        """
        Returns the current HSL color of the led.
        
        @return an integer corresponding to the current HSL color of the led
        
        On failure, throws an exception or returns YColorLed.HSLCOLOR_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.HSLCOLOR_INVALID
        return self._hslColor

    def set_hslColor(self, newval):
        """
        Changes the current color of the led, using a color HSL. Encoding is done as follows: 0xHHSSLL.
        
        @param newval : an integer corresponding to the current color of the led, using a color HSL
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "0x"+'%X' % newval
        return self._setAttr("hslColor", rest_val)


    def get_rgbMove(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.RGBMOVE_INVALID
        return self._rgbMove

    def set_rgbMove(self, newval):
        rest_val = str(newval.target)+":"+str(newval.ms)
        return self._setAttr("rgbMove", rest_val)


    def rgbMove(self , rgb_target,ms_duration):
        """
        Performs a smooth transition in the RGB color space between the current color and a target color.
        
        @param rgb_target  : desired RGB color at the end of the transition
        @param ms_duration : duration of the transition, in millisecond
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(rgb_target)+":"+str(ms_duration)
        return self._setAttr("rgbMove", rest_val)

    def get_hslMove(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.HSLMOVE_INVALID
        return self._hslMove

    def set_hslMove(self, newval):
        rest_val = str(newval.target)+":"+str(newval.ms)
        return self._setAttr("hslMove", rest_val)


    def hslMove(self , hsl_target,ms_duration):
        """
        Performs a smooth transition in the HSL color space between the current color and a target color.
        
        @param hsl_target  : desired HSL color at the end of the transition
        @param ms_duration : duration of the transition, in millisecond
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(hsl_target)+":"+str(ms_duration)
        return self._setAttr("hslMove", rest_val)

    def get_rgbColorAtPowerOn(self):
        """
        Returns the configured color to be displayed when the module is turned on.
        
        @return an integer corresponding to the configured color to be displayed when the module is turned on
        
        On failure, throws an exception or returns YColorLed.RGBCOLORATPOWERON_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YColorLed.RGBCOLORATPOWERON_INVALID
        return self._rgbColorAtPowerOn

    def set_rgbColorAtPowerOn(self, newval):
        """
        Changes the color that the led will display by default when the module is turned on.
        This color will be displayed as soon as the module is powered on.
        Remember to call the saveToFlash() method of the module if the
        change should be kept.
        
        @param newval : an integer corresponding to the color that the led will display by default when the
        module is turned on
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "0x"+'%X' % newval
        return self._setAttr("rgbColorAtPowerOn", rest_val)


    def nextColorLed(self):
        """
        Continues the enumeration of RGB leds started using yFirstColorLed().
        
        @return a pointer to a YColorLed object, corresponding to
                an RGB led currently online, or a None pointer
                if there are no more RGB leds to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YColorLed.FindColorLed(hwidRef.value)

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

#--- (end of YColorLed implementation)

#--- (ColorLed functions)

    @staticmethod 
    def FindColorLed(func):
        """
        Retrieves an RGB led for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the RGB led is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YColorLed.isOnline() to test if the RGB led is
        indeed online at a given time. In case of ambiguity when looking for
        an RGB led by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the RGB led
        
        @return a YColorLed object allowing you to drive the RGB led.
        """
        if func in YColorLed._ColorLedCache:
            return YColorLed._ColorLedCache[func]
        res =YColorLed(func)
        YColorLed._ColorLedCache[func] =  res
        return res

    @staticmethod 
    def  FirstColorLed():
        """
        Starts the enumeration of RGB leds currently accessible.
        Use the method YColorLed.nextColorLed() to iterate on
        next RGB leds.
        
        @return a pointer to a YColorLed object, corresponding to
                the first RGB led currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("ColorLed", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YColorLed.FindColorLed(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _ColorLedCleanup():
        pass

  #--- (end of ColorLed functions)

