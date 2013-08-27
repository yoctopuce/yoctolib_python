#*********************************************************************
#*
#* $Id: yocto_wireless.py 12337 2013-08-14 15:22:22Z mvuilleu $
#*
#* Implements yFindWireless(), the high-level API for Wireless functions
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

class YWlanRecord:
    """
    
    """

    #--- (generated code: YWlanRecord definitions)



    _WlanRecordCache ={}

    #--- (end of generated code: YWlanRecord definitions)



    def __init__(self,json):
        self._ssid = ""
        self._channel  = -1
        self._sec = ""
        self._rssi = -1
        for member in json.members:
            if member.name == "ssid":
                self._ssid = member.svalue
            if member.name == "sec":
                self._sec = member.svalue
            elif member.name == "channel":
                self._channel = member.ivalue
            elif member.name == "rssi":
                self._rssi = member.ivalue


    #--- (generated code: YWlanRecord implementation)

    def get_ssid(self ):
        return self._ssid

    def get_channel(self ):
        return self._channel

    def get_security(self ):
        return self._sec

    def get_linkQuality(self ):
        return self._rssi

#--- (end of generated code: YWlanRecord implementation)

#--- (WlanRecord generated code: functions)


#--- (end of WlanRecord generated code: functions)



class YWireless(YFunction):
    #--- (generated code: globals)


    #--- (end of generated code: globals)

    #--- (generated code: YWireless definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    LINKQUALITY_INVALID             = YAPI.INVALID_LONG
    SSID_INVALID                    = YAPI.INVALID_STRING
    CHANNEL_INVALID                 = YAPI.INVALID_LONG
    MESSAGE_INVALID                 = YAPI.INVALID_STRING
    WLANCONFIG_INVALID              = YAPI.INVALID_STRING

    SECURITY_UNKNOWN                = 0
    SECURITY_OPEN                   = 1
    SECURITY_WEP                    = 2
    SECURITY_WPA                    = 3
    SECURITY_WPA2                   = 4
    SECURITY_INVALID                = -1


    _WirelessCache ={}

    #--- (end of generated code: YWireless definitions)

    #--- (generated code: YWireless implementation)

    def __init__(self,func):
        super(YWireless,self).__init__("Wireless", func)
        self._callback = None
        self._logicalName = YWireless.LOGICALNAME_INVALID
        self._advertisedValue = YWireless.ADVERTISEDVALUE_INVALID
        self._linkQuality = YWireless.LINKQUALITY_INVALID
        self._ssid = YWireless.SSID_INVALID
        self._channel = YWireless.CHANNEL_INVALID
        self._security = YWireless.SECURITY_INVALID
        self._message = YWireless.MESSAGE_INVALID
        self._wlanConfig = YWireless.WLANCONFIG_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "linkQuality":
                self._linkQuality = member.ivalue
            elif member.name == "ssid":
                self._ssid = member.svalue
            elif member.name == "channel":
                self._channel = member.ivalue
            elif member.name == "security":
                self._security = member.ivalue
            elif member.name == "message":
                self._message = member.svalue
            elif member.name == "wlanConfig":
                self._wlanConfig = member.svalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the wireless lan interface.
        
        @return a string corresponding to the logical name of the wireless lan interface
        
        On failure, throws an exception or returns YWireless.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the wireless lan interface. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the wireless lan interface
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the wireless lan interface (no more than 6 characters).
        
        @return a string corresponding to the current value of the wireless lan interface (no more than 6 characters)
        
        On failure, throws an exception or returns YWireless.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_linkQuality(self):
        """
        Returns the link quality, expressed in per cents.
        
        @return an integer corresponding to the link quality, expressed in per cents
        
        On failure, throws an exception or returns YWireless.LINKQUALITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.LINKQUALITY_INVALID
        return self._linkQuality

    def get_ssid(self):
        """
        Returns the wireless network name (SSID).
        
        @return a string corresponding to the wireless network name (SSID)
        
        On failure, throws an exception or returns YWireless.SSID_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.SSID_INVALID
        return self._ssid

    def get_channel(self):
        """
        Returns the 802.11 channel currently used, or 0 when the selected network has not been found.
        
        @return an integer corresponding to the 802
        
        On failure, throws an exception or returns YWireless.CHANNEL_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.CHANNEL_INVALID
        return self._channel

    def get_security(self):
        """
        Returns the security algorithm used by the selected wireless network.
        
        @return a value among YWireless.SECURITY_UNKNOWN, YWireless.SECURITY_OPEN, YWireless.SECURITY_WEP,
        YWireless.SECURITY_WPA and YWireless.SECURITY_WPA2 corresponding to the security algorithm used by
        the selected wireless network
        
        On failure, throws an exception or returns YWireless.SECURITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.SECURITY_INVALID
        return self._security

    def get_message(self):
        """
        Returns the last status message from the wireless interface.
        
        @return a string corresponding to the last status message from the wireless interface
        
        On failure, throws an exception or returns YWireless.MESSAGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.MESSAGE_INVALID
        return self._message

    def get_wlanConfig(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YWireless.WLANCONFIG_INVALID
        return self._wlanConfig

    def set_wlanConfig(self, newval):
        rest_val = newval
        return self._setAttr("wlanConfig", rest_val)


    def joinNetwork(self , ssid,securityKey):
        """
        Changes the configuration of the wireless lan interface to connect to an existing
        access point (infrastructure mode).
        Remember to call the saveToFlash() method and then to reboot the module to apply this setting.
        
        @param ssid : the name of the network to connect to
        @param securityKey : the network key, as a character string
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "INFRA:"+ssid+"\\"+securityKey
        return self._setAttr("wlanConfig", rest_val)

    def adhocNetwork(self , ssid,securityKey):
        """
        Changes the configuration of the wireless lan interface to create an ad-hoc
        wireless network, without using an access point. If a security key is specified,
        the network is protected by WEP128, since WPA is not standardized for
        ad-hoc networks.
        Remember to call the saveToFlash() method and then to reboot the module to apply this setting.
        
        @param ssid : the name of the network to connect to
        @param securityKey : the network key, as a character string
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "ADHOC:"+ssid+"\\"+securityKey
        return self._setAttr("wlanConfig", rest_val)
    def get_detectedWlans(self ):
        """
        Returns a list of YWlanRecord objects which describe detected Wireless networks.
        This list is not updated when the module is already connected to an acces point (infrastructure mode).
        To force an update of this list, adhocNetwork() must be called to disconnect
        the module from the current network. The returned list must be unallocated by caller,
        
        @return a list of YWlanRecord objects, containing the SSID, channel,
                link quality and the type of security of the wireless network.
        
        On failure, throws an exception or returns an empty list.
        """
        
        list = []
        res = []
        json = self._download("wlan.json?by=name")
        list = self._json_get_array(json)
        for y in list : res.append( YWlanRecord(y))
        return res


    def nextWireless(self):
        """
        Continues the enumeration of wireless lan interfaces started using yFirstWireless().
        
        @return a pointer to a YWireless object, corresponding to
                a wireless lan interface currently online, or a None pointer
                if there are no more wireless lan interfaces to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YWireless.FindWireless(hwidRef.value)

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

#--- (end of generated code: YWireless implementation)

#--- (generated code: Wireless functions)

    @staticmethod 
    def FindWireless(func):
        """
        Retrieves a wireless lan interface for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the wireless lan interface is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWireless.isOnline() to test if the wireless lan interface is
        indeed online at a given time. In case of ambiguity when looking for
        a wireless lan interface by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the wireless lan interface
        
        @return a YWireless object allowing you to drive the wireless lan interface.
        """
        if func in YWireless._WirelessCache:
            return YWireless._WirelessCache[func]
        res =YWireless(func)
        YWireless._WirelessCache[func] =  res
        return res

    @staticmethod 
    def  FirstWireless():
        """
        Starts the enumeration of wireless lan interfaces currently accessible.
        Use the method YWireless.nextWireless() to iterate on
        next wireless lan interfaces.
        
        @return a pointer to a YWireless object, corresponding to
                the first wireless lan interface currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Wireless", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YWireless.FindWireless(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _WirelessCleanup():
        pass

  #--- (end of generated code: Wireless functions)

