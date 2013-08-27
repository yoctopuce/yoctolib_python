#*********************************************************************
#*
#* $Id: yocto_network.py 12337 2013-08-14 15:22:22Z mvuilleu $
#*
#* Implements yFindNetwork(), the high-level API for Network functions
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
class YNetwork(YFunction):
    """
    YNetwork objects provide access to TCP/IP parameters of Yoctopuce
    modules that include a built-in network interface.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (YNetwork definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    MACADDRESS_INVALID              = YAPI.INVALID_STRING
    IPADDRESS_INVALID               = YAPI.INVALID_STRING
    SUBNETMASK_INVALID              = YAPI.INVALID_STRING
    ROUTER_INVALID                  = YAPI.INVALID_STRING
    IPCONFIG_INVALID                = YAPI.INVALID_STRING
    PRIMARYDNS_INVALID              = YAPI.INVALID_STRING
    SECONDARYDNS_INVALID            = YAPI.INVALID_STRING
    USERPASSWORD_INVALID            = YAPI.INVALID_STRING
    ADMINPASSWORD_INVALID           = YAPI.INVALID_STRING
    WWWWATCHDOGDELAY_INVALID        = YAPI.INVALID_LONG
    CALLBACKURL_INVALID             = YAPI.INVALID_STRING
    CALLBACKCREDENTIALS_INVALID     = YAPI.INVALID_STRING
    CALLBACKMINDELAY_INVALID        = YAPI.INVALID_LONG
    CALLBACKMAXDELAY_INVALID        = YAPI.INVALID_LONG
    POECURRENT_INVALID              = YAPI.INVALID_LONG

    READINESS_DOWN                  = 0
    READINESS_EXISTS                = 1
    READINESS_LINKED                = 2
    READINESS_LAN_OK                = 3
    READINESS_WWW_OK                = 4
    READINESS_INVALID               = -1
    DISCOVERABLE_FALSE              = 0
    DISCOVERABLE_TRUE               = 1
    DISCOVERABLE_INVALID            = -1
    CALLBACKMETHOD_POST             = 0
    CALLBACKMETHOD_GET              = 1
    CALLBACKMETHOD_PUT              = 2
    CALLBACKMETHOD_INVALID          = -1
    CALLBACKENCODING_FORM           = 0
    CALLBACKENCODING_JSON           = 1
    CALLBACKENCODING_JSON_ARRAY     = 2
    CALLBACKENCODING_CSV            = 3
    CALLBACKENCODING_YOCTO_API      = 4
    CALLBACKENCODING_INVALID        = -1


    _NetworkCache ={}

    #--- (end of YNetwork definitions)

    #--- (YNetwork implementation)

    def __init__(self,func):
        super(YNetwork,self).__init__("Network", func)
        self._callback = None
        self._logicalName = YNetwork.LOGICALNAME_INVALID
        self._advertisedValue = YNetwork.ADVERTISEDVALUE_INVALID
        self._readiness = YNetwork.READINESS_INVALID
        self._macAddress = YNetwork.MACADDRESS_INVALID
        self._ipAddress = YNetwork.IPADDRESS_INVALID
        self._subnetMask = YNetwork.SUBNETMASK_INVALID
        self._router = YNetwork.ROUTER_INVALID
        self._ipConfig = YNetwork.IPCONFIG_INVALID
        self._primaryDNS = YNetwork.PRIMARYDNS_INVALID
        self._secondaryDNS = YNetwork.SECONDARYDNS_INVALID
        self._userPassword = YNetwork.USERPASSWORD_INVALID
        self._adminPassword = YNetwork.ADMINPASSWORD_INVALID
        self._discoverable = YNetwork.DISCOVERABLE_INVALID
        self._wwwWatchdogDelay = YNetwork.WWWWATCHDOGDELAY_INVALID
        self._callbackUrl = YNetwork.CALLBACKURL_INVALID
        self._callbackMethod = YNetwork.CALLBACKMETHOD_INVALID
        self._callbackEncoding = YNetwork.CALLBACKENCODING_INVALID
        self._callbackCredentials = YNetwork.CALLBACKCREDENTIALS_INVALID
        self._callbackMinDelay = YNetwork.CALLBACKMINDELAY_INVALID
        self._callbackMaxDelay = YNetwork.CALLBACKMAXDELAY_INVALID
        self._poeCurrent = YNetwork.POECURRENT_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "readiness":
                self._readiness = member.ivalue
            elif member.name == "macAddress":
                self._macAddress = member.svalue
            elif member.name == "ipAddress":
                self._ipAddress = member.svalue
            elif member.name == "subnetMask":
                self._subnetMask = member.svalue
            elif member.name == "router":
                self._router = member.svalue
            elif member.name == "ipConfig":
                self._ipConfig = member.svalue
            elif member.name == "primaryDNS":
                self._primaryDNS = member.svalue
            elif member.name == "secondaryDNS":
                self._secondaryDNS = member.svalue
            elif member.name == "userPassword":
                self._userPassword = member.svalue
            elif member.name == "adminPassword":
                self._adminPassword = member.svalue
            elif member.name == "discoverable":
                self._discoverable = member.ivalue
            elif member.name == "wwwWatchdogDelay":
                self._wwwWatchdogDelay = member.ivalue
            elif member.name == "callbackUrl":
                self._callbackUrl = member.svalue
            elif member.name == "callbackMethod":
                self._callbackMethod = member.ivalue
            elif member.name == "callbackEncoding":
                self._callbackEncoding = member.ivalue
            elif member.name == "callbackCredentials":
                self._callbackCredentials = member.svalue
            elif member.name == "callbackMinDelay":
                self._callbackMinDelay = member.ivalue
            elif member.name == "callbackMaxDelay":
                self._callbackMaxDelay = member.ivalue
            elif member.name == "poeCurrent":
                self._poeCurrent = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the network interface, corresponding to the network name of the module.
        
        @return a string corresponding to the logical name of the network interface, corresponding to the
        network name of the module
        
        On failure, throws an exception or returns YNetwork.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the network interface, corresponding to the network name of the module.
        You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the network interface, corresponding
        to the network name of the module
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the network interface (no more than 6 characters).
        
        @return a string corresponding to the current value of the network interface (no more than 6 characters)
        
        On failure, throws an exception or returns YNetwork.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_readiness(self):
        """
        Returns the current established working mode of the network interface.
        Level zero (DOWN_0) means that no hardware link has been detected. Either there is no signal
        on the network cable, or the selected wireless access point cannot be detected.
        Level 1 (LIVE_1) is reached when the network is detected, but is not yet connected,
        For a wireless network, this shows that the requested SSID is present.
        Level 2 (LINK_2) is reached when the hardware connection is established.
        For a wired network connection, level 2 means that the cable is attached at both ends.
        For a connection to a wireless access point, it shows that the security parameters
        are properly configured. For an ad-hoc wireless connection, it means that there is
        at least one other device connected on the ad-hoc network.
        Level 3 (DHCP_3) is reached when an IP address has been obtained using DHCP.
        Level 4 (DNS_4) is reached when the DNS server is reachable on the network.
        Level 5 (WWW_5) is reached when global connectivity is demonstrated by properly loading the
        current time from an NTP server.
        
        @return a value among YNetwork.READINESS_DOWN, YNetwork.READINESS_EXISTS,
        YNetwork.READINESS_LINKED, YNetwork.READINESS_LAN_OK and YNetwork.READINESS_WWW_OK corresponding to
        the current established working mode of the network interface
        
        On failure, throws an exception or returns YNetwork.READINESS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.READINESS_INVALID
        return self._readiness

    def get_macAddress(self):
        """
        Returns the MAC address of the network interface. The MAC address is also available on a sticker
        on the module, in both numeric and barcode forms.
        
        @return a string corresponding to the MAC address of the network interface
        
        On failure, throws an exception or returns YNetwork.MACADDRESS_INVALID.
        """
        if self._macAddress == YNetwork.MACADDRESS_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.MACADDRESS_INVALID
        return self._macAddress

    def get_ipAddress(self):
        """
        Returns the IP address currently in use by the device. The adress may have been configured
        statically, or provided by a DHCP server.
        
        @return a string corresponding to the IP address currently in use by the device
        
        On failure, throws an exception or returns YNetwork.IPADDRESS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.IPADDRESS_INVALID
        return self._ipAddress

    def get_subnetMask(self):
        """
        Returns the subnet mask currently used by the device.
        
        @return a string corresponding to the subnet mask currently used by the device
        
        On failure, throws an exception or returns YNetwork.SUBNETMASK_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.SUBNETMASK_INVALID
        return self._subnetMask

    def get_router(self):
        """
        Returns the IP address of the router on the device subnet (default gateway).
        
        @return a string corresponding to the IP address of the router on the device subnet (default gateway)
        
        On failure, throws an exception or returns YNetwork.ROUTER_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.ROUTER_INVALID
        return self._router

    def get_ipConfig(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.IPCONFIG_INVALID
        return self._ipConfig

    def set_ipConfig(self, newval):
        rest_val = newval
        return self._setAttr("ipConfig", rest_val)


    def useDHCP(self , fallbackIpAddr,fallbackSubnetMaskLen,fallbackRouter):
        """
        Changes the configuration of the network interface to enable the use of an
        IP address received from a DHCP server. Until an address is received from a DHCP
        server, the module uses the IP parameters specified to this function.
        Remember to call the saveToFlash() method and then to reboot the module to apply this setting.
        
        @param fallbackIpAddr : fallback IP address, to be used when no DHCP reply is received
        @param fallbackSubnetMaskLen : fallback subnet mask length when no DHCP reply is received, as an
                integer (eg. 24 means 255.255.255.0)
        @param fallbackRouter : fallback router IP address, to be used when no DHCP reply is received
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "DHCP:"+fallbackIpAddr+"/"+str(fallbackSubnetMaskLen)+"/"+fallbackRouter
        return self._setAttr("ipConfig", rest_val)

    def useStaticIP(self , ipAddress,subnetMaskLen,router):
        """
        Changes the configuration of the network interface to use a static IP address.
        Remember to call the saveToFlash() method and then to reboot the module to apply this setting.
        
        @param ipAddress : device IP address
        @param subnetMaskLen : subnet mask length, as an integer (eg. 24 means 255.255.255.0)
        @param router : router IP address (default gateway)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "STATIC:"+ipAddress+"/"+str(subnetMaskLen)+"/"+router
        return self._setAttr("ipConfig", rest_val)

    def get_primaryDNS(self):
        """
        Returns the IP address of the primary name server to be used by the module.
        
        @return a string corresponding to the IP address of the primary name server to be used by the module
        
        On failure, throws an exception or returns YNetwork.PRIMARYDNS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.PRIMARYDNS_INVALID
        return self._primaryDNS

    def set_primaryDNS(self, newval):
        """
        Changes the IP address of the primary name server to be used by the module.
        When using DHCP, if a value is specified, it overrides the value received from the DHCP server.
        Remember to call the saveToFlash() method and then to reboot the module to apply this setting.
        
        @param newval : a string corresponding to the IP address of the primary name server to be used by the module
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("primaryDNS", rest_val)


    def get_secondaryDNS(self):
        """
        Returns the IP address of the secondary name server to be used by the module.
        
        @return a string corresponding to the IP address of the secondary name server to be used by the module
        
        On failure, throws an exception or returns YNetwork.SECONDARYDNS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.SECONDARYDNS_INVALID
        return self._secondaryDNS

    def set_secondaryDNS(self, newval):
        """
        Changes the IP address of the secondarz name server to be used by the module.
        When using DHCP, if a value is specified, it overrides the value received from the DHCP server.
        Remember to call the saveToFlash() method and then to reboot the module to apply this setting.
        
        @param newval : a string corresponding to the IP address of the secondarz name server to be used by the module
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("secondaryDNS", rest_val)


    def get_userPassword(self):
        """
        Returns a hash string if a password has been set for "user" user,
        or an empty string otherwise.
        
        @return a string corresponding to a hash string if a password has been set for "user" user,
                or an empty string otherwise
        
        On failure, throws an exception or returns YNetwork.USERPASSWORD_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.USERPASSWORD_INVALID
        return self._userPassword

    def set_userPassword(self, newval):
        """
        Changes the password for the "user" user. This password becomes instantly required
        to perform any use of the module. If the specified value is an
        empty string, a password is not required anymore.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the password for the "user" user
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("userPassword", rest_val)


    def get_adminPassword(self):
        """
        Returns a hash string if a password has been set for user "admin",
        or an empty string otherwise.
        
        @return a string corresponding to a hash string if a password has been set for user "admin",
                or an empty string otherwise
        
        On failure, throws an exception or returns YNetwork.ADMINPASSWORD_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.ADMINPASSWORD_INVALID
        return self._adminPassword

    def set_adminPassword(self, newval):
        """
        Changes the password for the "admin" user. This password becomes instantly required
        to perform any change of the module state. If the specified value is an
        empty string, a password is not required anymore.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the password for the "admin" user
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("adminPassword", rest_val)


    def get_discoverable(self):
        """
        Returns the activation state of the multicast announce protocols to allow easy
        discovery of the module in the network neighborhood (uPnP/Bonjour protocol).
        
        @return either YNetwork.DISCOVERABLE_FALSE or YNetwork.DISCOVERABLE_TRUE, according to the
        activation state of the multicast announce protocols to allow easy
                discovery of the module in the network neighborhood (uPnP/Bonjour protocol)
        
        On failure, throws an exception or returns YNetwork.DISCOVERABLE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.DISCOVERABLE_INVALID
        return self._discoverable

    def set_discoverable(self, newval):
        """
        Changes the activation state of the multicast announce protocols to allow easy
        discovery of the module in the network neighborhood (uPnP/Bonjour protocol).
        
        @param newval : either YNetwork.DISCOVERABLE_FALSE or YNetwork.DISCOVERABLE_TRUE, according to the
        activation state of the multicast announce protocols to allow easy
                discovery of the module in the network neighborhood (uPnP/Bonjour protocol)
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("discoverable", rest_val)


    def get_wwwWatchdogDelay(self):
        """
        Returns the allowed downtime of the WWW link (in seconds) before triggering an automated
        reboot to try to recover Internet connectivity. A zero value disables automated reboot
        in case of Internet connectivity loss.
        
        @return an integer corresponding to the allowed downtime of the WWW link (in seconds) before
        triggering an automated
                reboot to try to recover Internet connectivity
        
        On failure, throws an exception or returns YNetwork.WWWWATCHDOGDELAY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.WWWWATCHDOGDELAY_INVALID
        return self._wwwWatchdogDelay

    def set_wwwWatchdogDelay(self, newval):
        """
        Changes the allowed downtime of the WWW link (in seconds) before triggering an automated
        reboot to try to recover Internet connectivity. A zero value disable automated reboot
        in case of Internet connectivity loss. The smallest valid non-zero timeout is
        90 seconds.
        
        @param newval : an integer corresponding to the allowed downtime of the WWW link (in seconds)
        before triggering an automated
                reboot to try to recover Internet connectivity
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("wwwWatchdogDelay", rest_val)


    def get_callbackUrl(self):
        """
        Returns the callback URL to notify of significant state changes.
        
        @return a string corresponding to the callback URL to notify of significant state changes
        
        On failure, throws an exception or returns YNetwork.CALLBACKURL_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.CALLBACKURL_INVALID
        return self._callbackUrl

    def set_callbackUrl(self, newval):
        """
        Changes the callback URL to notify significant state changes. Remember to call the
        saveToFlash() method of the module if the modification must be kept.
        
        @param newval : a string corresponding to the callback URL to notify significant state changes
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("callbackUrl", rest_val)


    def get_callbackMethod(self):
        """
        Returns the HTTP method used to notify callbacks for significant state changes.
        
        @return a value among YNetwork.CALLBACKMETHOD_POST, YNetwork.CALLBACKMETHOD_GET and
        YNetwork.CALLBACKMETHOD_PUT corresponding to the HTTP method used to notify callbacks for
        significant state changes
        
        On failure, throws an exception or returns YNetwork.CALLBACKMETHOD_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.CALLBACKMETHOD_INVALID
        return self._callbackMethod

    def set_callbackMethod(self, newval):
        """
        Changes the HTTP method used to notify callbacks for significant state changes.
        
        @param newval : a value among YNetwork.CALLBACKMETHOD_POST, YNetwork.CALLBACKMETHOD_GET and
        YNetwork.CALLBACKMETHOD_PUT corresponding to the HTTP method used to notify callbacks for
        significant state changes
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("callbackMethod", rest_val)


    def get_callbackEncoding(self):
        """
        Returns the encoding standard to use for representing notification values.
        
        @return a value among YNetwork.CALLBACKENCODING_FORM, YNetwork.CALLBACKENCODING_JSON,
        YNetwork.CALLBACKENCODING_JSON_ARRAY, YNetwork.CALLBACKENCODING_CSV and
        YNetwork.CALLBACKENCODING_YOCTO_API corresponding to the encoding standard to use for representing
        notification values
        
        On failure, throws an exception or returns YNetwork.CALLBACKENCODING_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.CALLBACKENCODING_INVALID
        return self._callbackEncoding

    def set_callbackEncoding(self, newval):
        """
        Changes the encoding standard to use for representing notification values.
        
        @param newval : a value among YNetwork.CALLBACKENCODING_FORM, YNetwork.CALLBACKENCODING_JSON,
        YNetwork.CALLBACKENCODING_JSON_ARRAY, YNetwork.CALLBACKENCODING_CSV and
        YNetwork.CALLBACKENCODING_YOCTO_API corresponding to the encoding standard to use for representing
        notification values
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("callbackEncoding", rest_val)


    def get_callbackCredentials(self):
        """
        Returns a hashed version of the notification callback credentials if set,
        or an empty string otherwise.
        
        @return a string corresponding to a hashed version of the notification callback credentials if set,
                or an empty string otherwise
        
        On failure, throws an exception or returns YNetwork.CALLBACKCREDENTIALS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.CALLBACKCREDENTIALS_INVALID
        return self._callbackCredentials

    def set_callbackCredentials(self, newval):
        """
        Changes the credentials required to connect to the callback address. The credentials
        must be provided as returned by function get_callbackCredentials,
        in the form username:hash. The method used to compute the hash varies according
        to the the authentication scheme implemented by the callback, For Basic authentication,
        the hash is the MD5 of the string username:password. For Digest authentication,
        the hash is the MD5 of the string username:realm:password. For a simpler
        way to configure callback credentials, use function callbackLogin instead.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the credentials required to connect to the callback address
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("callbackCredentials", rest_val)


    def callbackLogin(self , username,password):
        """
        Connects to the notification callback and saves the credentials required to
        log into it. The password is not stored into the module, only a hashed
        copy of the credentials are saved. Remember to call the
        saveToFlash() method of the module if the modification must be kept.
        
        @param username : username required to log to the callback
        @param password : password required to log to the callback
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = username+":"+password
        return self._setAttr("callbackCredentials", rest_val)

    def get_callbackMinDelay(self):
        """
        Returns the minimum waiting time between two callback notifications, in seconds.
        
        @return an integer corresponding to the minimum waiting time between two callback notifications, in seconds
        
        On failure, throws an exception or returns YNetwork.CALLBACKMINDELAY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.CALLBACKMINDELAY_INVALID
        return self._callbackMinDelay

    def set_callbackMinDelay(self, newval):
        """
        Changes the minimum waiting time between two callback notifications, in seconds.
        
        @param newval : an integer corresponding to the minimum waiting time between two callback
        notifications, in seconds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("callbackMinDelay", rest_val)


    def get_callbackMaxDelay(self):
        """
        Returns the maximum waiting time between two callback notifications, in seconds.
        
        @return an integer corresponding to the maximum waiting time between two callback notifications, in seconds
        
        On failure, throws an exception or returns YNetwork.CALLBACKMAXDELAY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.CALLBACKMAXDELAY_INVALID
        return self._callbackMaxDelay

    def set_callbackMaxDelay(self, newval):
        """
        Changes the maximum waiting time between two callback notifications, in seconds.
        
        @param newval : an integer corresponding to the maximum waiting time between two callback
        notifications, in seconds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("callbackMaxDelay", rest_val)


    def get_poeCurrent(self):
        """
        Returns the current consumed by the module from Power-over-Ethernet (PoE), in milli-amps.
        The current consumption is measured after converting PoE source to 5 Volt, and should
        never exceed 1800 mA.
        
        @return an integer corresponding to the current consumed by the module from Power-over-Ethernet
        (PoE), in milli-amps
        
        On failure, throws an exception or returns YNetwork.POECURRENT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YNetwork.POECURRENT_INVALID
        return self._poeCurrent
    def ping(self, host):
        """
        Pings str_host to test the network connectivity. Sends four requests ICMP ECHO_REQUEST from the
        module to the target str_host. This method returns a string with the result of the
        4 ICMP ECHO_REQUEST result.
        
        @param host : the hostname or the IP address of the target
        
        @return a string with the result of the ping.
        """
        
        content = self._download("ping.txt?host="+host)
        return content
        


    def nextNetwork(self):
        """
        Continues the enumeration of network interfaces started using yFirstNetwork().
        
        @return a pointer to a YNetwork object, corresponding to
                a network interface currently online, or a None pointer
                if there are no more network interfaces to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YNetwork.FindNetwork(hwidRef.value)

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

#--- (end of YNetwork implementation)

#--- (Network functions)

    @staticmethod 
    def FindNetwork(func):
        """
        Retrieves a network interface for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the network interface is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YNetwork.isOnline() to test if the network interface is
        indeed online at a given time. In case of ambiguity when looking for
        a network interface by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the network interface
        
        @return a YNetwork object allowing you to drive the network interface.
        """
        if func in YNetwork._NetworkCache:
            return YNetwork._NetworkCache[func]
        res =YNetwork(func)
        YNetwork._NetworkCache[func] =  res
        return res

    @staticmethod 
    def  FirstNetwork():
        """
        Starts the enumeration of network interfaces currently accessible.
        Use the method YNetwork.nextNetwork() to iterate on
        next network interfaces.
        
        @return a pointer to a YNetwork object, corresponding to
                the first network interface currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Network", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YNetwork.FindNetwork(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _NetworkCleanup():
        pass

  #--- (end of Network functions)

