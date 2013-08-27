#*********************************************************************
#*
#* $Id: yocto_api.py 12326 2013-08-13 15:52:20Z mvuilleu $
#*
#* High-level programming interface, common to all modules
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
import ctypes
import platform
#import abc  (not supported in 2.5.x)
import random
import sys
import os
import datetime
import array
from ctypes import *

#
#  PYTHON 2.x VS PYTHON 3.x compatibility check
#

YByte2String = None
YString2Byte = None
YGetByte = None
YAddByte = None

def YByte2StringPython2x(binBuffer):
    return binBuffer.decode("latin-1")
    #return str(binBuffer)

def YString2BytePython2x(strBuffer):
    return strBuffer.encode("latin-1")
    #return str(strBuffer)

def YGetBytePython2x(binBuffer,idx):
    return ord(binBuffer[idx])

def YAddBytePython2x(binBuffer,b):
    return binBuffer + chr(b)

def YByte2StringPython3x(binBuffer):
    return binBuffer.decode("latin-1")

def YString2BytePython3x(strBuffer):
    return strBuffer.encode("latin-1")

def YGetBytePython3x(binBuffer,l):
    return binBuffer[l]

def YAddBytePython3x(binBuffer,b):
    return binBuffer + bytes([b])


if sys.version_info < (3, 0):
    YByte2String = YByte2StringPython2x
    YString2Byte = YString2BytePython2x
    YGetByte = YGetBytePython2x
    YAddByte = YAddBytePython2x
else:
    YByte2String = YByte2StringPython3x
    YString2Byte = YString2BytePython3x
    YGetByte = YGetBytePython3x
    YAddByte = YAddBytePython3x

# Ugly global var for Python 2 compatibility    
yLogFct  = None
yArrivalFct = None
yRemovalFct = None
yChangeFct  = None


# This class is used to mimic "ByReference" parameter in function calls
class YRefParam:
    def __init__(self,initialValue=None):
        self.value=initialValue
    def __str__(self):
        return str(self.value)

class YAPI:

    #noinspection PyUnresolvedReferences
    class YPCHAR(ctypes.Structure):
        _fields_ = [ ("buffer",ctypes.c_char_p) ]

    class JsonError(Exception):
        def __init__(self, msg):
           self.msg = msg
           Exception.__init__(self)


    class TJSONRECORDTYPE:
        JSON_NONE, JSON_STRING,JSON_INTEGER, JSON_BOOLEAN, JSON_STRUCT, JSON_ARRAY  = range(6)


    class TJSONRECORD:
        def __init__(self,name,datatype):
           self.name = name
           self.recordtype = datatype
           self.svalue = ""
           self.ivalue = 0
           self.bvalue = False
           self.members = []
           self.items = []

        def memberscount(self):
           return len(self.members)

        def itemscount(self):
            return len(self.items)



    class TJsonParser:

        class Tjstate:
            JSTART,JWAITFORNAME,JWAITFORENDOFNAME, JWAITFORCOLON,JWAITFORDATA,JWAITFORNEXTSTRUCTMEMBER,JWAITFORNEXTARRAYITEM,JSCOMPLETED,JWAITFORSTRINGVALUE,JWAITFORINTVALUE,JWAITFORBOOLVALUE= range(11)

        def __init__(self,jsonData,withHttpHeader=True):
            jsonData = jsonData.decode("latin1")
            self.httpcode = 0
            self.data =  None
            if withHttpHeader:
                httpheader = "HTTP/1.1 "
                okHeader="OK\r\n"
                CR = "\r\n"
                if jsonData[0: len(okHeader)] == okHeader:
                    self.httpcode = 200
                else:
                    if jsonData[0: len(httpheader)] != httpheader:
                        errmsgRef =("data should start with " + httpheader)
                        raise YAPI.JsonError(errmsgRef)

                    p1 = jsonData.find(" ", len(httpheader) - 1)
                    p2 = jsonData.find(" ", p1 + 1)

                    self.httpcode = int(jsonData[p1: p2])

                    if self.httpcode != 200: return
                p1 = jsonData.find(CR + CR + "{") #json data is a structure
                if p1 < 0:
                    p1 = jsonData.find(CR + CR + "[") # json data is an array
                if p1 < 0:
                    errmsgRef = "data  does not contain JSON data"
                    raise YAPI.JsonError(errmsgRef)
                p1+=4
                jsonData = jsonData[p1: len(jsonData)]
            else:
                start_struct = jsonData.find("{") #json data is a structure
                start_array  = jsonData.find("[") # json data is an array
                if start_array < 0 and start_struct < 0 :
                    errmsgRef = "data  does not contain JSON data"
                    raise YAPI.JsonError(errmsgRef)
            self.data = self._Parse(jsonData)

        def __del__(self):
            self._freestructure()

        def GetRootNode(self):
            return  self.data

        class refidx:
            def __init__(self):
              self.i = 0

        def _Parse(self,st):
            idx = self.refidx()
            st = "\"root\" : " + st + " "
            return self._ParseEx(self.Tjstate.JWAITFORNAME, "", st,  idx)

        def _ParseError(self,st, i,  errmsgRef):
            ststart = i - 10
            stend = i + 10
            if ststart < 0: ststart = 0
            if stend > len(st): stend = len(st) - 1
            errmsgRef = errmsgRef + " near " + st[ststart:i] + "*" + st[i: stend]
            raise YAPI.JsonError(errmsgRef)

        def _createStructRecord(self,name):
            return  YAPI.TJSONRECORD(name,YAPI.TJSONRECORDTYPE.JSON_STRUCT)

        def _createArrayRecord(self, name):
            return  YAPI.TJSONRECORD(name,YAPI.TJSONRECORDTYPE.JSON_ARRAY)

        def _createStrRecord(self, name, value):
            res =  YAPI.TJSONRECORD(name,YAPI.TJSONRECORDTYPE.JSON_STRING)
            res.svalue = value
            return res

        def _createIntRecord(self, name, value):
            res = YAPI.TJSONRECORD(name,YAPI.TJSONRECORDTYPE.JSON_INTEGER)
            res.ivalue = value
            return res

        def _createBoolRecord(self, name, value):
            res = YAPI.TJSONRECORD(name,YAPI.TJSONRECORDTYPE.JSON_BOOLEAN)
            res.bvalue = value
            return res

        def _add2StructRecord(self,container, element):
            if container.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                raise YAPI.JsonError("container is not a struct type")
            container.members.append(element)

        def _add2ArrayRecord(self, container,  element):
            if container.recordtype != YAPI.TJSONRECORDTYPE.JSON_ARRAY:
               raise YAPI.JsonError("container is not a struct type")
            container.items.append(element)

        def _Skipgarbage(self,st, idx):
            sti = st[idx.i]
            while idx.i < len(st) and (sti == '\n' or sti == '\r' or sti == ' '):
                idx.i+=1
                if idx.i < len(st): sti = st[idx.i]
            return sti

        def _ParseEx(self,initialstate, defaultname,  st, idx):

            res = YAPI.TJSONRECORD("",YAPI.TJSONRECORDTYPE.JSON_NONE)

            svalue = ""
            name = defaultname
            state = initialstate
            isign = 1
            ivalue = 0

            while idx.i< len(st):
                sti = st[idx.i]
                if state == self.Tjstate.JWAITFORNAME:
                    if sti == "\"":
                        state = self.Tjstate.JWAITFORENDOFNAME
                    elif  sti != " "  and sti != "\n" :
                        self._ParseError(st, idx.i, "invalid char: was expecting \"")

                elif  state == self.Tjstate.JWAITFORENDOFNAME:
                    if sti == "\"":
                        state = self.Tjstate.JWAITFORCOLON
                    elif ord(sti) >= 32:
                        name = name + sti
                    else:
                        self._ParseError(st, idx.i, "invalid char: was expecting an identifier compliant char")

                elif  state ==self.Tjstate.JWAITFORCOLON:
                    if sti == ":":
                        state = self.Tjstate.JWAITFORDATA
                    elif sti != " " and sti != "\n":
                        self._ParseError(st, idx.i, "invalid char: was expecting \"")

                elif  state == self.Tjstate.JWAITFORDATA:
                    if sti == "{":
                        res = self._createStructRecord(name)
                        state = self.Tjstate.JWAITFORNEXTSTRUCTMEMBER
                    elif sti == "[":
                        res = self._createArrayRecord(name)
                        state = self.Tjstate.JWAITFORNEXTARRAYITEM
                    elif sti == "\"":
                        svalue = ""
                        state = self.Tjstate.JWAITFORSTRINGVALUE
                    elif  "0" <= sti <= "9":
                        state = self.Tjstate.JWAITFORINTVALUE
                        ivalue = ord(sti) - 48
                        isign = 1
                    elif sti == "-":
                        state = self.Tjstate.JWAITFORINTVALUE
                        ivalue = 0
                        isign = -1
                    elif sti == "t" or  sti == "f" or sti == "T" or sti == "F":
                        svalue = sti.upper()
                        state = self.Tjstate.JWAITFORBOOLVALUE
                    elif sti != " "  and sti != "\n":
                        self._ParseError(st, idx.i, "invalid char: was expecting  \",0..9,t or f")

                elif state == self.Tjstate.JWAITFORSTRINGVALUE:
                    if sti == "\"":
                        state = self.Tjstate.JSCOMPLETED
                        res = self._createStrRecord(name, svalue)
                    elif ord(sti) < 32:
                        self._ParseError(st, idx.i, "invalid char: was expecting string value")
                    else:
                        svalue = svalue + sti

                elif state ==  self.Tjstate.JWAITFORINTVALUE:
                    if "0" <= sti <= "9":
                        ivalue = (ivalue * 10) + ord(sti) - 48
                    else:
                        res = self._createIntRecord(name, isign * ivalue)
                        state = self.Tjstate.JSCOMPLETED
                        idx.i -=  1

                elif state == self.Tjstate.JWAITFORBOOLVALUE:
                    if sti < "A" or sti > "Z":
                        if svalue != "TRUE" and svalue != "FALSE":
                            self._ParseError(st, idx.i, "unexpected value, was expecting \"true\" or \"false\"")
                        if svalue == "TRUE":
                            res = self._createBoolRecord(name, True)
                        else:
                           res = self._createBoolRecord(name, False)
                        state = self.Tjstate.JSCOMPLETED
                        idx.i -=   1
                    else:
                        svalue = svalue + sti.upper()

                elif state ==  self.Tjstate.JWAITFORNEXTSTRUCTMEMBER:
                    sti = self._Skipgarbage(st, idx)
                    if idx.i < len(st):
                        if sti == "}":
                            idx.i +=  1
                            return res
                        else:
                            value = self._ParseEx(self.Tjstate.JWAITFORNAME, "", st, idx)
                            self._add2StructRecord(res, value)
                            sti = self._Skipgarbage(st, idx)
                            if idx.i < len(st):
                                if sti == "}" and idx.i < len(st):
                                   idx.i -=  1
                                elif sti != " "  and sti != "\n" and   sti != ",":
                                    self._ParseError(st, idx.i, "invalid char: vas expecting , or }")

                elif state ==   self.Tjstate.JWAITFORNEXTARRAYITEM:
                    sti = self._Skipgarbage(st, idx)
                    if idx.i < len(st):
                        if sti == "]":
                            idx.i += 1
                            return res
                        else:
                            value = self._ParseEx(self.Tjstate.JWAITFORDATA, str(len(res.items)), st, idx)
                            self._add2ArrayRecord(res, value)
                            sti = self._Skipgarbage(st, idx)
                            if idx.i < len(st):
                                if sti == "]" and idx.i < len(st):
                                    idx.i -=  1
                                elif sti != " "  and sti != "\n"  and sti != ",":
                                    self._ParseError(st, idx.i, "invalid char: vas expecting , or ]")

                elif state == self.Tjstate.JSCOMPLETED:
                    return res

                idx.i+=1

            self._ParseError(st, idx.i, "unexpected end of data")
            return None


        def _DumpStructureRec(self,p, deep):
            indent = ""
            for i in range(0,deep*2):
                indent += " "
            line = indent + p.name + ":"
            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRING:
                line = line + " str  = " + p.svalue
                print(line)
            elif  p.recordtype == YAPI.TJSONRECORDTYPE.JSON_INTEGER:
                line = line + " int  = " + str(p.ivalue)
                print(line)
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_BOOLEAN:
                if p.bvalue:
                    line +=  " bool = TRUE"
                else:
                    line +=  " bool = FALSE"
                print(line)
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                print (line + " struct")
                for  i in range (0, len(p.members)):
                    self._DumpStructureRec(p.members[i], deep+1)
            elif  p.recordtype ==  YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                print(line + " array")
                for i in range(0,len(p.items)):
                    self._DumpStructureRec(p.items[i], deep+1)

        def _freestructure(self):
            pass

        def DumpStructure(self):
            self._DumpStructureRec(self.data, 0)

        def GetNbChild(self,parent):
            return len(parent.items)

        def GetAllChilds(self,parent):
            res =[]
            p = parent
            if p is None:
                p=self.data
            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                for  i in range (0, len(p.members)):
                    res.append(p.members[i])
            elif  p.recordtype ==  YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                for i in range(0,len(p.items)):
                    res.append(p.items[i])
            return res

        def GetChildNode(self,parent,nodename):
            p = parent
            if p is None:
                p=self.data

            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                for i in range(0,len(p.members) ):
                    if p.members[i].name == nodename:
                       return p.members[i]
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                index = int(nodename)
                if index >= len(p.items):
                    raise YAPI.JsonError("index out of bounds " + nodename + ">=" + str(p.Value.itemcount))
                return  p.items[index]

            return None


    # Switch to turn off exceptions and use return codes instead, for source-code compatibility
    # with languages without exception support like C
    ExceptionsDisabled = False
    _apiInitialized = False
    _ydllLoaded = False

    # Default cache validity (in [ms]) before reloading data from device. This saves a lots of traffic.
    # Note that a value under 2 ms makes little sense since a USB bus itself has a 2ms round-trip period

    DefaultCacheValidity = datetime.timedelta(milliseconds=5)
    INVALID_STRING = "!INVALID!"
    INVALID_DOUBLE = -1.79769313486231E+308
    INVALID_INT = -2147483648
    INVALID_LONG = -9223372036854775807

    INVALID_UNSIGNED = -1
    # yInitAPI argument
    Y_DETECT_NONE = 0
    Y_DETECT_USB = 1
    Y_DETECT_NET = 2

    Y_DETECT_ALL = Y_DETECT_USB | Y_DETECT_NET

    YOCTO_API_VERSION_STR = "1.01"
    YOCTO_API_VERSION_BCD = 0x0101

    YOCTO_API_BUILD_NO = "12553"
    YOCTO_DEFAULT_PORT = 4444
    YOCTO_VENDORID = 0x24e0
    YOCTO_DEVID_FACTORYBOOT = 1

    YOCTO_DEVID_BOOTLOADER = 2
    YOCTO_ERRMSG_LEN = 256
    YOCTO_MANUFACTURER_LEN = 20
    YOCTO_SERIAL_LEN = 20
    YOCTO_BASE_SERIAL_LEN = 8
    YOCTO_PRODUCTNAME_LEN = 28
    YOCTO_FIRMWARE_LEN = 22
    YOCTO_LOGICAL_LEN = 20
    YOCTO_FUNCTION_LEN = 20
    # Size of the data (can be non null terminated)
    YOCTO_PUBVAL_SIZE = 6
    #Temporary storage, > YOCTO_PUBVAL_SIZE
    YOCTO_PUBVAL_LEN = 16
    YOCTO_PASS_LEN = 20
    YOCTO_REALM_LEN = 20
    YIOHDL_SIZE = 8
    INVALID_YHANDLE = 0

    yUnknowSize = 1024

    C_INTSIZE = 4  # we assume an int size is 4 byte

    _PlugEvents = []
    _DataEvents = []
    _CalibHandlers = {}

    #  private extern static void DllCallTest(ref yDeviceSt data);
    #_DllCallTest = yApiCLib.DllCallTest
    #_DllCallTest.restypes = ctypes.c_int
    #_DllCallTest.argtypes = [ctypes.c_void_p]



    _yApiCLibFile=""
    _yApiCLibFileFallback=""
    _yApiCLib = None


    @staticmethod
    def SelectArchitecture(arch):
        """
        Select the architecture or the library to be loaded to access to USB.
        By default, the Python library automatically detects the appropriate
        library to use. However, for Linux ARM, it not possible to reliably
        distinguish between a Hard Float (armhf) and a Soft Float (armel)
        install. For in this case, it is therefore recommended to manually
        select the proper architecture by calling SelectArchitecture()
        before any other call to the library.
        
        @param arch : A string containing the architecture to use.
                Possibles value are: "armhf","armel",
                "i386","x86_64","32bit", "64bit"
        
        @return nothing.
        
        On failure, throws an exception.
        """

        libpath = os.path.dirname(__file__)
        system = platform.system()
        if libpath=='':
            libpath = '.'
        if system=='Windows':
            if arch=='32bit' :
                YAPI._yApiCLibFile= libpath+"\\cdll\\yapi.dll"
            elif arch=='64bit':
                YAPI._yApiCLibFile= libpath+"\\cdll\\yapi64.dll"
            else:
                raise NotImplementedError("unsupported windows architecture ("+arch+"), contact support@yoctopuce.com.")
        #
        #  LINUX (INTEL + ARM)
        #
        elif system=='Linux':
            if arch =="armhf":
                YAPI._yApiCLibFile=libpath+"/cdll/libyapi-armhf.so"
            elif arch =="armel":
                YAPI._yApiCLibFile = libpath+"/cdll/libyapi-armel.so"
            elif arch == 'i386':
                YAPI._yApiCLibFile=libpath+"/cdll/libyapi-i386.so"
            elif arch=='x86_64' :
                YAPI._yApiCLibFile=libpath+"/cdll/libyapi-amd64.so"
            else:
                raise NotImplementedError("unsupported linux architecture ("+arch+"), contact support@yoctopuce.com.")
        #
        #  Mac OS X
        #
        elif system=='Darwin':
            if arch=='x86_64' :
                YAPI._yApiCLibFile=libpath+"/cdll/libyapi.dylib"
            else:
                raise NotImplementedError("unsupported Mac OS architecture ("+arch+"), contact support@yoctopuce.com.")
        #
        #  UNKNOWN, contact Yoctopuce support :-)
        #
        else:
            raise NotImplementedError("unsupported platform "+system+", contact support@yoctopuce.com.")



    @staticmethod
    def yloadYapiCDLL():
        if YAPI._yApiCLibFile=="":
            libpath = os.path.dirname(__file__)
            system = platform.system()
            arch = platform.architecture()[0]
            machine = platform.machine()
            if libpath=='':
                libpath = '.'
            #
            #  WINDOWS
            #
            if system=='Windows':
                if arch=='32bit' :
                    YAPI._yApiCLibFile= libpath+"\\cdll\\yapi.dll"
                elif arch=='64bit':
                    YAPI._yApiCLibFile= libpath+"\\cdll\\yapi64.dll"
                else:
                    raise NotImplementedError("unsupported windows architecture ("+arch+"), contact support@yoctopuce.com.")
            #
            #  LINUX (INTEL + ARM)
            #
            elif platform.system()=='Linux':
                if machine.find("arm")>=0:
                    YAPI._yApiCLibFile=libpath+"/cdll/libyapi-armhf.so"
                    YAPI._yApiCLibFileFallback = libpath+"/cdll/libyapi-armel.so"
                elif machine== 'x86_32' or (machine[0]== 'i' and machine[-2:]== '86') :
                    YAPI._yApiCLibFile=libpath+"/cdll/libyapi-i386.so"
                    YAPI._yApiCLibFileFallback= libpath+"/cdll/libyapi-amd64.so" # just in case
                elif machine=='x86_64' :
                    YAPI._yApiCLibFile=libpath+"/cdll/libyapi-amd64.so"
                    YAPI._yApiCLibFileFallback=libpath+"/cdll/libyapi-i386.so" # just in case
                else:
                    raise NotImplementedError("unsupported linux machine ("+machine+"), contact support@yoctopuce.com.")
            #
            #  Mac OS X
            #
            elif platform.system()=='Darwin':
                if sys.maxsize > 2**32:
                    YAPI._yApiCLibFile=libpath+"/cdll/libyapi.dylib"
                else:
                    raise NotImplementedError("Only Intel 64 bits installation are supported for Mac OS X.")
            #
            #  UNKNOWN, contact Yoctopuce support :-)
            #
            else:
                raise NotImplementedError("unsupported platform "+system+", contact support@yoctopuce.com.")

        if not os.path.exists(YAPI._yApiCLibFile):
            raise ImportError("YAPI shared library is missing ("+YAPI._yApiCLibFile+"), make sure it is available and accessible.")
           
        # try to load main librray
        libloaded = False
        try:
            YAPI._yApiCLib = ctypes.CDLL(YAPI._yApiCLibFile)
            libloaded= True
        except Exception:
            pass

        # try to load fallback library
        if not libloaded and  YAPI._yApiCLibFileFallback!='':
            try:
                YAPI._yApiCLib = ctypes.CDLL(YAPI._yApiCLibFileFallback)
                libloaded= True
            except Exception:
                ImportError("Cannot load "+YAPI._yApiCLibFileFallback+" nor "+YAPI._yApiCLibFile+"  make sure it is available and accessible.")

        if  not libloaded :
            raise ImportError("Unable to import YAPI shared library ("+YAPI._yApiCLibFile+"), make sure it is available and accessible.")

        #  private extern static int _yapiInitAPI(int mode, StringBuilder errmsgRef);
        YAPI._yapiInitAPI = YAPI._yApiCLib.yapiInitAPI
        YAPI._yapiInitAPI.restypes = ctypes.c_int
        YAPI._yapiInitAPI.argtypes = [ctypes.c_int , ctypes.c_char_p]


        #  private extern static void _yapiFreeAPI();
        YAPI._yapiFreeAPI = YAPI._yApiCLib.yapiFreeAPI
        YAPI._yapiFreeAPI.restypes = ctypes.c_int
        YAPI._yapiFreeAPI.argtypes = []

        YAPI._yapiSetTraceFile = YAPI._yApiCLib.yapiSetTraceFile
        YAPI._yapiSetTraceFile.restypes = ctypes.c_int
        YAPI._yapiSetTraceFile.argtypes = [ ctypes.c_char_p]

        #  private extern static void _yapiRegisterLogFunction(IntPtr fct);
        YAPI._yapiRegisterLogFunction = YAPI._yApiCLib.yapiRegisterLogFunction
        YAPI._yapiRegisterLogFunction.restypes = ctypes.c_int
        YAPI._yapiRegisterLogFunction.argtypes = [ctypes.c_void_p]

        #  private extern static void _yapiRegisterDeviceArrivalCallback(IntPtr fct);
        YAPI._yapiRegisterDeviceArrivalCallback = YAPI._yApiCLib.yapiRegisterDeviceArrivalCallback
        YAPI._yapiRegisterDeviceArrivalCallback.restypes = ctypes.c_int
        YAPI._yapiRegisterDeviceArrivalCallback.argtypes = [ctypes.c_void_p]

        #  private extern static void _yapiRegisterDeviceRemovalCallback(IntPtr fct);
        YAPI._yapiRegisterDeviceRemovalCallback = YAPI._yApiCLib.yapiRegisterDeviceRemovalCallback
        YAPI._yapiRegisterDeviceRemovalCallback.restypes = ctypes.c_int
        YAPI._yapiRegisterDeviceRemovalCallback.argtypes = [ctypes.c_void_p]

        #  private extern static void _yapiRegisterDeviceChangeCallback(IntPtr fct);
        YAPI._yapiRegisterDeviceChangeCallback = YAPI._yApiCLib.yapiRegisterDeviceChangeCallback
        YAPI._yapiRegisterDeviceChangeCallback.restypes = ctypes.c_int
        YAPI._yapiRegisterDeviceChangeCallback.argtypes = [ctypes.c_void_p]

        #  private extern static void _yapiRegisterFunctionUpdateCallback(IntPtr fct);
        YAPI._yapiRegisterFunctionUpdateCallback = YAPI._yApiCLib.yapiRegisterFunctionUpdateCallback
        YAPI._yapiRegisterFunctionUpdateCallback.restypes = ctypes.c_int
        YAPI._yapiRegisterFunctionUpdateCallback.argtypes = [ctypes.c_void_p]

        #  private extern static int _yapiLockDeviceCallBack(StringBuilder errmsgRef);
        YAPI._yapiLockDeviceCallBack = YAPI._yApiCLib.yapiLockDeviceCallBack
        YAPI._yapiLockDeviceCallBack.restypes = ctypes.c_int
        YAPI._yapiLockDeviceCallBack.argtypes = [ctypes.c_char_p]

        #  private extern static int _yapiUnlockDeviceCallBack(StringBuilder errmsgRef);
        YAPI._yapiUnlockDeviceCallBack = YAPI._yApiCLib.yapiUnlockDeviceCallBack
        YAPI._yapiUnlockDeviceCallBack.restypes = ctypes.c_int
        YAPI._yapiUnlockDeviceCallBack.argtypes = [ctypes.c_char_p]

        #  private extern static int _yapiLockFunctionCallBack(StringBuilder errmsgRef);
        YAPI._yapiLockFunctionCallBack = YAPI._yApiCLib.yapiLockFunctionCallBack
        YAPI._yapiLockFunctionCallBack.restypes = ctypes.c_int
        YAPI._yapiLockFunctionCallBack.argtypes = [ctypes.c_char_p]

        #  private extern static int _yapiUnlockFunctionCallBack(StringBuilder errmsgRef);
        YAPI._yapiUnlockFunctionCallBack = YAPI._yApiCLib.yapiUnlockFunctionCallBack
        YAPI._yapiUnlockFunctionCallBack.restypes = ctypes.c_int
        YAPI._yapiUnlockFunctionCallBack.argtypes = [ctypes.c_char_p]

        #  private extern static int _yapiRegisterHub(StringBuilder rootUrl, StringBuilder errmsgRef);
        YAPI._yapiRegisterHub = YAPI._yApiCLib.yapiRegisterHub
        YAPI._yapiRegisterHub.restypes = ctypes.c_int
        YAPI._yapiRegisterHub.argtypes = [ctypes.c_char_p , ctypes.c_char_p]

        #  private extern static int _yapiPreregisterHub(StringBuilder rootUrl, StringBuilder errmsgRef);
        YAPI._yapiPreregisterHub = YAPI._yApiCLib.yapiPreregisterHub
        YAPI._yapiPreregisterHub.restypes = ctypes.c_int
        YAPI._yapiPreregisterHub.argtypes = [ctypes.c_char_p , ctypes.c_char_p]

        #  private extern static void _yapiUnregisterHub(StringBuilder rootUrl);
        YAPI._yapiUnregisterHub = YAPI._yApiCLib.yapiUnregisterHub
        YAPI._yapiUnregisterHub.restypes = ctypes.c_int
        YAPI._yapiUnregisterHub.argtypes = [ctypes.c_char_p]

        #  private extern static int _yapiUpdateDeviceList(uint force, StringBuilder errmsgRef);
        YAPI._yapiUpdateDeviceList = YAPI._yApiCLib.yapiUpdateDeviceList
        YAPI._yapiUpdateDeviceList.restypes = ctypes.c_int
        YAPI._yapiUpdateDeviceList.argtypes = [ctypes.c_uint , ctypes.c_char_p]

        #  private extern static int _yapiHandleEvents(StringBuilder errmsgRef);
        YAPI._yapiHandleEvents = YAPI._yApiCLib.yapiHandleEvents
        YAPI._yapiHandleEvents.restypes = ctypes.c_int
        YAPI._yapiHandleEvents.argtypes = [ctypes.c_char_p]

        #  private extern static u64 _yapiGetTickCount();
        YAPI._yapiGetTickCount = YAPI._yApiCLib.yapiGetTickCount
        YAPI._yapiGetTickCount.restypes = ctypes.c_ulonglong
        YAPI._yapiGetTickCount.argtypes = []

        #  private extern static int _yapiCheckLogicalName(StringBuilder name);
        YAPI._yapiCheckLogicalName = YAPI._yApiCLib.yapiCheckLogicalName
        YAPI._yapiCheckLogicalName.restypes = ctypes.c_int
        YAPI._yapiCheckLogicalName.argtypes = [ctypes.c_char_p]

        #  private extern static u16 _yapiGetAPIVersion(ref IntPtr version, ref IntPtr date);
        YAPI._yapiGetAPIVersion = YAPI._yApiCLib.yapiGetAPIVersion
        YAPI._yapiGetAPIVersion.restypes = ctypes.c_ushort
        YAPI._yapiGetAPIVersion.argtypes = [ctypes.c_void_p , ctypes.c_void_p]

        #  private extern static YDEV_DESCR _yapiGetDevice(StringBuilder device_str, StringBuilder errmsgRef);
        YAPI._yapiGetDevice = YAPI._yApiCLib.yapiGetDevice
        YAPI._yapiGetDevice.restypes = ctypes.c_int
        YAPI._yapiGetDevice.argtypes = [ctypes.c_char_p , ctypes.c_char_p]

        #  private extern static int _yapiGetAllDevices(IntPtr buffer, int maxsize, ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetAllDevices = YAPI._yApiCLib.yapiGetAllDevices
        YAPI._yapiGetAllDevices.restypes = ctypes.c_int
        YAPI._yapiGetAllDevices.argtypes = [ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiGetDeviceInfo(YDEV_DESCR d, ref yDeviceSt infos, StringBuilder errmsgRef);
        YAPI._yapiGetDeviceInfo = YAPI._yApiCLib.yapiGetDeviceInfo
        YAPI._yapiGetDeviceInfo.restypes = ctypes.c_int
        YAPI._yapiGetDeviceInfo.argtypes = [ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static YFUN_DESCR _yapiGetFunction(StringBuilder class_str, StringBuilder function_str, StringBuilder errmsgRef);
        YAPI._yapiGetFunction = YAPI._yApiCLib.yapiGetFunction
        YAPI._yapiGetFunction.restypes = ctypes.c_int
        YAPI._yapiGetFunction.argtypes = [ctypes.c_char_p , ctypes.c_char_p , ctypes.c_char_p]

        #  private extern static int _yapiGetFunctionsByClass(StringBuilder class_str, YFUN_DESCR precFuncDesc, IntPtr buffer, int maxsize, ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetFunctionsByClass = YAPI._yApiCLib.yapiGetFunctionsByClass
        YAPI._yapiGetFunctionsByClass.restypes = ctypes.c_int
        YAPI._yapiGetFunctionsByClass.argtypes = [ctypes.c_char_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiGetFunctionsByDevice(YDEV_DESCR device, YFUN_DESCR precFuncDesc, IntPtr buffer, int maxsize, ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetFunctionsByDevice = YAPI._yApiCLib.yapiGetFunctionsByDevice
        YAPI._yapiGetFunctionsByDevice.restypes = ctypes.c_int
        YAPI._yapiGetFunctionsByDevice.argtypes = [ctypes.c_int , ctypes.c_int , ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p]

        #  internal extern static int _yapiGetFunctionInfo(YFUN_DESCR fundesc, ref YDEV_DESCR devdesc, StringBuilder serial, StringBuilder funcId, StringBuilder funcName, StringBuilder funcVal, StringBuilder errmsgRef);
        YAPI._yapiGetFunctionInfo = YAPI._yApiCLib.yapiGetFunctionInfo
        YAPI._yapiGetFunctionInfo.restypes = ctypes.c_int
        YAPI._yapiGetFunctionInfo.argtypes = [ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p , ctypes.c_char_p , ctypes.c_char_p , ctypes.c_char_p , ctypes.c_char_p]

        #  private extern static int _yapiGetErrorString(int errorcode, StringBuilder buffer, int maxsize, StringBuilder errmsgRef);
        #YAPI._yapiGetErrorString = YAPI._yApiCLib.yapiGetErrorString
        #YAPI._yapiGetErrorString.restypes = ctypes.c_int
        #YAPI._yapiGetErrorString.argtypes = [ctypes.c_int , ctypes.c_char_p , ctypes.c_int , ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestSyncStart(YIOHDL *iohdl, const char *device, const char *request, char **reply, int *replysize, char *errmsg);
        YAPI._yapiHTTPRequestSyncStart = YAPI._yApiCLib.yapiHTTPRequestSyncStart
        YAPI._yapiHTTPRequestSyncStart.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestSyncStart.argtypes = [ctypes.c_void_p , ctypes.c_char_p , ctypes.c_char_p , POINTER(POINTER(ctypes.c_ubyte)), ctypes.c_void_p , ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestSyncStartEx(YIOHDL *iohdl, const char *device, const char *request, int requestsize, char **reply, int *replysize, char *errmsg);
        YAPI._yapiHTTPRequestSyncStartEx = YAPI._yApiCLib.yapiHTTPRequestSyncStartEx
        YAPI._yapiHTTPRequestSyncStartEx.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestSyncStartEx.argtypes = [ctypes.c_void_p , ctypes.c_char_p , ctypes.c_char_p , ctypes.c_int , POINTER(POINTER(ctypes.c_ubyte)), ctypes.c_void_p , ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestSyncDone(YIOHDL *iohdl, char *errmsg);
        YAPI._yapiHTTPRequestSyncDone = YAPI._yApiCLib.yapiHTTPRequestSyncDone
        YAPI._yapiHTTPRequestSyncDone.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestSyncDone.argtypes = [ctypes.c_void_p , ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestAsync(const char *device, const char *request, yapiRequestAsyncCallback callback, void *context, char *errmsg);
        YAPI._yapiHTTPRequestAsync = YAPI._yApiCLib.yapiHTTPRequestAsync
        YAPI._yapiHTTPRequestAsync.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestAsync.argtypes = [ctypes.c_char_p , ctypes.c_char_p , ctypes.c_void_p, ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiHTTPRequest(StringBuilder device, StringBuilder url, StringBuilder buffer, int buffsize, ref int fullsize, StringBuilder errmsgRef);
        YAPI._yapiHTTPRequest = YAPI._yApiCLib.yapiHTTPRequest
        YAPI._yapiHTTPRequest.restypes = ctypes.c_int
        YAPI._yapiHTTPRequest.argtypes = [ctypes.c_char_p , ctypes.c_char_p , ctypes.c_char_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiGetBootloadersDevs(StringBuilder serials, u32 maxNbSerial, ref u32 totalBootladers, StringBuilder errmsgRef);
        YAPI._yapiGetBootloadersDevs = YAPI._yApiCLib.yapiGetBootloadersDevs
        YAPI._yapiGetBootloadersDevs.restypes = ctypes.c_int
        YAPI._yapiGetBootloadersDevs.argtypes = [ctypes.c_char_p , ctypes.c_uint32 , ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiFlashDevice(ref yFlashArg args, StringBuilder errmsgRef);
        YAPI._yapiFlashDevice = YAPI._yApiCLib.yapiFlashDevice
        YAPI._yapiFlashDevice.restypes = ctypes.c_int
        YAPI._yapiFlashDevice.argtypes = [ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiVerifyDevice(ref yFlashArg args, StringBuilder errmsgRef);
        YAPI._yapiVerifyDevice = YAPI._yApiCLib.yapiVerifyDevice
        YAPI._yapiVerifyDevice.restypes = ctypes.c_int
        YAPI._yapiVerifyDevice.argtypes = [ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiGetDevicePath(int devdesc, StringBuilder rootdevice, StringBuilder path, int pathsize, ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetDevicePath = YAPI._yApiCLib.yapiGetDevicePath
        YAPI._yapiGetDevicePath.restypes = ctypes.c_int
        YAPI._yapiGetDevicePath.argtypes = [ctypes.c_int , ctypes.c_char_p , ctypes.c_char_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_char_p]

        #  private extern static int _yapiSleep(int duration_ms, StringBuilder errmsgRef);
        YAPI._yapiSleep = YAPI._yApiCLib.yapiSleep
        YAPI._yapiSleep.restypes = ctypes.c_int
        YAPI._yapiSleep.argtypes = [ctypes.c_int , ctypes.c_char_p]
        YAPI._ydllLoaded = True


    #noinspection PyUnresolvedReferences
    class yDeviceSt(ctypes.Structure):
        _pack_=1
        #noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker
        _fields_= [("vendorid",ctypes.c_uint16),
                   ("deviceid",ctypes.c_uint16),
                   ("devrelease",ctypes.c_uint16),
                   ("nbinbterfaces",ctypes.c_uint16),
                   ("manufacturer", ctypes.c_char * 20), # YAPI.YOCTO_MANUFACTURER_LEN),
                   ("productname", ctypes.c_char * 28),  # YAPI.YOCTO_PRODUCTNAME_LEN),
                   ("serial", ctypes.c_char * 20),       # YAPI.YAPI.YOCTO_SERIAL_LEN),
                   ("logicalname", ctypes.c_char * 20),  # YAPI.YOCTO_LOGICAL_LEN),
                   ("firmware", ctypes.c_char * 22),     # YAPI.YOCTO_FIRMWARE_LEN),
                   ("beacon", ctypes.c_int8)]




    #noinspection PyUnresolvedReferences
    class YIOHDL(ctypes.Structure):
        _pack_=1
        _fields_= [("raw",ctypes.c_byte)]

    class yapiEventType:
        YAPI_DEV_ARRIVAL,YAPI_DEV_REMOVAL,YAPI_DEV_CHANGE,YAPI_FUN_UPDATE,YAPI_FUN_VALUE, YAPI_NOP = range(6)

    class yDEVICE_PROP:
        PROP_VENDORID,PROP_DEVICEID,PROP_DEVRELEASE,PROP_FIRMWARELEVEL,PROP_MANUFACTURER,PROP_PRODUCTNAME,PROP_SERIAL,PROP_LOGICALNAME, PROP_URL  = range(9)

    class yFACE_STATUS:
        YFACE_EMPTY,YFACE_RUNNING,YFACE_ERROR = range(3)





    class yapiEvent:
        def __init__(self):
            self.eventtype = 0
            self.modul = None
            self.fun_descr = 0
            self.value = ""





    ##--- (generated code: globals)

    # Yoctopuce error codes, used by default as function return value
    SUCCESS = 0                    # everything worked allright
    NOT_INITIALIZED = -1           # call yInitAPI() first !
    INVALID_ARGUMENT = -2          # one of the arguments passed to the function is invalid
    NOT_SUPPORTED = -3             # the operation attempted is (currently) not supported
    DEVICE_NOT_FOUND = -4          # the requested device is not reachable
    VERSION_MISMATCH = -5          # the device firmware is incompatible with this API version
    DEVICE_BUSY = -6               # the device is busy with another task and cannot answer
    TIMEOUT = -7                   # the device took too long to provide an answer
    IO_ERROR = -8                  # there was an I/O problem while talking to the device
    NO_MORE_DATA = -9              # there is no more data to read from
    EXHAUSTED = -10                # you have run out of a limited ressource, check the documentation
    DOUBLE_ACCES = -11             # you have two process that try to acces to the same device
    UNAUTHORIZED = -12             # unauthorized access to password-protected device
    RTC_NOT_READY = -13            # real-time clock has not been initialized (or time was lost)


    #--- (end of generated code: globals)

    class YAPI_Exception(Exception):
        pass

    YDevice_devCache = []

    # - Types used for internal yapi callbacks
    _yapiLogFunc= ctypes.CFUNCTYPE(None,ctypes.c_char_p, ctypes.c_int)

    _yapiDeviceUpdateFunc= ctypes.CFUNCTYPE(None,ctypes.c_int)

    _yapiFunctionUpdateFunc=ctypes.CFUNCTYPE(None,ctypes.c_int, ctypes.c_char_p )



    @staticmethod
    def YISERR(retcode):
        if retcode < 0 : return True
        return False

    class blockingCallbackCtx:
        res =0
        response =""
        errmsgRef =""

    #noinspection PyUnusedLocal
    @staticmethod
    def YblockingCallback( device,  context,  returnval,  result,  errmsgRef):
        context.res = returnval
        context.response = result
        context.errmsgRef = errmsgRef

    @staticmethod
    def GetTickCount():
        """
        Returns the current value of a monotone millisecond-based time counter.
        This counter can be used to compute delays in relation with
        Yoctopuce devices, which also uses the milisecond as timebase.
        
        @return a long integer corresponding to the millisecond counter.
        """
        #### for python, since some implementations don't support 64bits integers
        #### GetTickCount returns a datetime object instead of a u64
        #noinspection PyUnresolvedReferences
        return datetime.datetime.today()


    @staticmethod
    def SetTraceFile(filename):
       fname =ctypes.create_string_buffer(filename.encode("ASCII"))
       #noinspection PyUnresolvedReferences
       YAPI._yapiSetTraceFile(fname)


    @staticmethod
    def Sleep(ms_duration, errmsgRef = None):
        """
        Pauses the execution flow for a specified duration.
        This function implements a passive waiting loop, meaning that it does not
        consume CPU cycles significatively. The processor is left available for
        other threads and processes. During the pause, the library nevertheless
        reads from time to time information from the Yoctopuce modules by
        calling yHandleEvents(), in order to stay up-to-date.
        
        This function may signal an error in case there is a communication problem
        while contacting a module.
        
        @param ms_duration : an integer corresponding to the duration of the pause,
                in milliseconds.
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        errBuffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        timeout = YAPI.GetTickCount() + datetime.timedelta (milliseconds= ms_duration)
        res = YAPI.SUCCESS

        ok=True
        while ok:
            res = YAPI.HandleEvents(errmsgRef)
            if YAPI.YISERR(res):
                return res

            if YAPI.GetTickCount() < timeout:
                #noinspection PyUnresolvedReferences
                res = YAPI._yapiSleep(1, errBuffer)
                if YAPI.YISERR(res):
                    if not errmsgRef is None: errmsgRef.value =  YByte2String(errBuffer.value)
                    return res
            ok= YAPI.GetTickCount() < timeout
        if errmsgRef is not None: errmsgRef.value =  YByte2String(errBuffer.value)
        return res

    @staticmethod
    def CheckLogicalName(name):
        """
        Checks if a given string is valid as logical name for a module or a function.
        A valid logical name has a maximum of 19 characters, all among
        A..Z, a..z, 0..9, _, and -.
        If you try to configure a logical name with an incorrect string,
        the invalid characters are ignored.
        
        @param name : a string containing the name to check.
        
        @return true if the name is valid, false otherwise.
        """
        #noinspection PyUnresolvedReferences
        if not YAPI._yapiCheckLogicalName(name.encode("ASCII")):
            return False
        return True


    @staticmethod
    def yapiLockFunctionCallBack(errmsgRef = None):
        errBuffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiLockFunctionCallBack(errBuffer)
        if errmsgRef is not None: errmsgRef.value =  YByte2String(errBuffer.value)
        return res

    @staticmethod
    def yapiUnlockFunctionCallBack(errmsgRef= None):
        errBuffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUnlockFunctionCallBack(errBuffer)
        if not errmsgRef is None: errmsgRef.value =  YByte2String(errBuffer.value)
        return res

    @staticmethod
    def _getCalibrationHandler(calType):
        key=str(calType)
        if key in YAPI._CalibHandlers:
            return YAPI._CalibHandlers[key]
        return None

    @staticmethod
    def _setArrayLength(a,length):
        if len(a)>length : del a[length:]
        while len(a)<length:
            a.append(0)





    decExp = [1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1, 1.0, 1.0e1, 1.0e2, 1.0e3, 1.0e4, 1.0e5, 1.0e6, 1.0e7, 1.0e8, 1.0e9 ]

    # Convert Yoctopuce 16-bit decimal floats to standard double-precision floats
    
    @staticmethod
    def _decimalToDouble(val):
        negate=False
        if not val:
            return 0.0
        if val > 32767:
            negate = True
            val = 65536-val
        elif val < 0:
            negate = True
            val = -val
        exp = val >> 11
        res = (val & 2047) * YAPI.decExp[exp]
        if negate :
            return -res
        else:
            return res

    # Convert standard double-precision floats to Yoctopuce 16-bit decimal floats
    @staticmethod
    def _doubleToDecimal(val):
        negate = False

        if val == 0.0:
            return 0
        if val < 0:
            negate = True
            val = -val
        comp = val / 1999.0
        decpow = 0
        while comp > YAPI.decExp[decpow] and decpow < 15:
            decpow+=1
        mant = val / YAPI.decExp[decpow]
        if decpow == 15 and mant > 2047.0:
            res = (15 << 11) + 2047 # overflow
        else:
            res = (decpow << 11) +  round(mant)
        if negate:
            return -res
        else:
            return res


    @staticmethod
    def _encodeCalibrationPoints(rawValues,refValues,resolution,calibrationOffset,actualCparams):
        npt = len(refValues) if len(rawValues) < len(refValues) else len(rawValues)
        if npt == 0:
            return ""

        minRaw = 0
        if actualCparams == "":
            calibType = 10 + npt
        else:
            pos = actualCparams.find(',')
            if pos < 0:
                calibType = 0
            else:
                calibType = int(actualCparams[0:pos])
        if calibType <= 10:
            calibType = npt
        else:
            calibType = 10+npt
        res = str(calibType)
        if calibType <= 10:
            for i in range(0,npt):
                rawVal = int( (rawValues[i] / resolution - calibrationOffset + .5))
                if minRaw <= rawVal < 65536:
                    refVal = int( (refValues[i] / resolution - calibrationOffset + .5))
                    if 0 <= refVal < 65536:
                        res += ",%d,%d" %( rawVal, refVal)
                        minRaw = rawVal + 1
        else :
            # 16-bit floating-point decimal encoding
            for  i in range( 0,npt):
                rawVal = YAPI._doubleToDecimal(rawValues[i])
                refVal = YAPI._doubleToDecimal(refValues[i])
                res += ",%d,%d" % (rawVal, refVal)
        return res


    @staticmethod
    def _decodeCalibrationPoints(calibParams,intPt,rawPt,calPt,resolution,calibrationOffset):
        
        valuesStr = calibParams.split(',')
        if intPt is not None:
            del intPt[0:]
        del rawPt[0:]
        del calPt[0:]

        if len(valuesStr) <=1 :
            return 0
        calibType = int(valuesStr[0])
        # parse calibration parameters
        nval=99
        if calibType < 20 : nval=2*(calibType%10)
        i=1
        while i < nval and i < len(valuesStr) :
            rawval = int(valuesStr[i])
            calval = int(valuesStr[i+1])
            #rawval_d 0
            #calval_d
            if calibType <= 10:
                rawval_d = (rawval + calibrationOffset) * resolution
                calval_d = (calval + calibrationOffset) * resolution
            else:
                rawval_d = YAPI._decimalToDouble(rawval)
                calval_d = YAPI._decimalToDouble(calval)
            if intPt is not None:
                intPt.append(rawval)
                intPt.append(calval)
            rawPt.append(rawval_d)
            calPt.append(calval_d)
            i+=2
        return calibType

    @staticmethod
    def _applyCalibration(rawValue,calibParams,calibOffset,resolution):
        if  rawValue == YAPI.INVALID_DOUBLE or resolution == YAPI.INVALID_DOUBLE:
            return YAPI.INVALID_DOUBLE
        if calibParams is None or calibParams.find(',')<=0:
            return rawValue
        cur_calpar = []
        cur_calraw = []
        cur_calref = []
        calibType = YAPI._decodeCalibrationPoints(calibParams,cur_calpar,cur_calraw,cur_calref,resolution,calibOffset)
        if not calibType:
            return rawValue
        calhdl = YAPI._getCalibrationHandler(calibType)
        if calhdl is None :  return YAPI.INVALID_DOUBLE;
        return calhdl(rawValue,calibType,cur_calpar,cur_calraw,cur_calref)


    @staticmethod
    def HandleEvents(errmsgRef=None):
        """
        Maintains the device-to-library communication channel.
        If your program includes significant loops, you may want to include
        a call to this function to make sure that the library takes care of
        the information pushed by the modules on the communication channels.
        This is not strictly necessary, but it may improve the reactivity
        of the library for the following commands.
        
        This function may signal an error in case there is a communication problem
        while contacting a module.
        
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        errBuffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)

        #noinspection PyUnresolvedReferences
        res = YAPI._yapiHandleEvents(errBuffer)
        if YAPI.YISERR(res):
            if errmsgRef is not None: errmsgRef.value =  YByte2String(errBuffer.value)
            return res

        while len(YAPI._DataEvents) > 0 :
            YAPI.yapiLockFunctionCallBack(errmsgRef)
            if not(len(YAPI._DataEvents)):
                YAPI.yapiUnlockFunctionCallBack(errmsgRef)
                break

            ev = YAPI._DataEvents.pop(0)
            YAPI.yapiUnlockFunctionCallBack(errmsgRef)
            if ev.eventtype == YAPI.yapiEventType.YAPI_FUN_VALUE:
                for i in range (len(YFunction._FunctionCallbacks)):
                     if YFunction._FunctionCallbacks[i].get_functionDescriptor() == ev.fun_descr:
                         YFunction._FunctionCallbacks[i].advertiseValue(ev.value)
        return YAPI.SUCCESS

    @staticmethod
    def yapiUpdateDeviceList(force, errmsgRef=None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUpdateDeviceList(force, buffer)
        if YAPI.YISERR(res):
           if  not errmsgRef is None:  errmsgRef.value = YByte2String(buffer.value)
        return res

    #noinspection PyUnresolvedReferences
    @staticmethod
    def apiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer, maxsize, neededsizeRef, errmsgRef):
         buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
         neededsize = ctypes.c_int()
         res = YAPI._yapiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer, maxsize, ctypes.byref(neededsize), buffer)
         neededsizeRef.value=neededsize.value
         if  not errmsgRef is None:  errmsgRef.value =  YByte2String(buffer.value)
         return res


    @staticmethod
    def DisableExceptions():
         """
         Disables the use of exceptions to report runtime errors.
         When exceptions are disabled, every function returns a specific
         error value which depends on its type and which is documented in
         this reference manual.
         """
         YAPI.ExceptionsDisabled = True

    @staticmethod
    def EnableExceptions():
        """
        Re-enables the use of exceptions for runtime error handling.
        Be aware than when exceptions are enabled, every function that fails
        triggers an exception. If the exception is not caught by the user code,
        it  either fires the debugger or aborts (i.e. crash) the program.
        On failure, throws an exception or returns a negative error code.
        """
        YAPI.ExceptionsDisabled = False

    # - Internal callback registered into YAPI
    #noinspection PyUnusedLocal
    @staticmethod
    def native_yLogFunction(log,  loglen):

        global yLogFct
        if yLogFct is not  None:
            #noinspection PyCallingNonCallable
            yLogFct(YByte2String(log))
        return 0

    @staticmethod
    def RegisterLogFunction(logfun):
        """
        Registers a log callback function. This callback will be called each time
        the API have something to say. Quite usefull to debug the API.
        
        @param logfun : a procedure taking a string parameter, or None
                to unregister a previously registered  callback.
        """
        global yLogFct
        yLogFct = logfun


    @staticmethod
    def emptyDeviceSt():
        infos = YAPI.yDeviceSt()
        infos.vendorid = 0
        infos.deviceid = 0
        infos.devrelease = 0
        infos.nbinbterfaces = 0
        infos.manufacturer = "".encode("ASCII")
        infos.productname = "".encode("ASCII")
        infos.serial = "".encode("ASCII")
        infos.logicalname =  "".encode("ASCII")
        infos.firmware =  "".encode("ASCII")
        infos.beacon = 0
        return infos

    @staticmethod
    def emptyApiEvent():
        ev = YAPI.yapiEvent()
        ev.eventtype = YAPI.yapiEventType.YAPI_NOP
        ev.modul = None
        ev.fun_descr = 0
        ev.value = ""
        return ev


    #noinspection PyUnresolvedReferences
    @staticmethod
    def yapiGetDeviceInfo(d, infos, errmsgRef=None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        res = YAPI._yapiGetDeviceInfo(d, ctypes.byref(infos), buffer)
        if  errmsgRef is not None:  errmsgRef.value =  YByte2String(buffer.value)
        return res

    #noinspection PyUnresolvedReferences
    @staticmethod
    def native_yDeviceArrivalCallback(d):
        infos = YAPI.emptyDeviceSt()
        ev = YAPI.emptyApiEvent()
        errmsgRef = YRefParam()

        ev.eventtype = YAPI.yapiEventType.YAPI_DEV_ARRIVAL
        if YAPI.yapiGetDeviceInfo(d, infos, errmsgRef) != YAPI.SUCCESS:
            return

        ev.modul = YModule.FindModule(YByte2String(infos.serial) + ".module")
        ev.modul.setImmutableAttributes(infos)
        if yArrivalFct is not None:
            YAPI._PlugEvents.append(ev)

    @staticmethod
    def yapiLockDeviceCallBack(errmsgRef = None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiLockDeviceCallBack(buffer)
        if  errmsgRef is not None:  errmsgRef.value =  YByte2String(buffer.value)
        return res

    @staticmethod
    def yapiUnlockDeviceCallBack(errmsgRef = None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUnlockDeviceCallBack(buffer)
        if  errmsgRef is not None:  errmsgRef.value =  YByte2String(buffer.value)
        return res

    @staticmethod
    def RegisterDeviceArrivalCallback(arrivalCallback):
         """
         Register a callback function, to be called each time
         a device is pluged. This callback will be invoked while yUpdateDeviceList
         is running. You will have to call this function on a regular basis.
         
         @param arrivalCallback : a procedure taking a YModule parameter, or None
                 to unregister a previously registered  callback.
         """
         global yArrivalFct
         yArrivalFct = arrivalCallback
         if  arrivalCallback is not None:
              error = YRefParam()
              mod = YModule.FirstModule()
              while mod is not None:
                  if mod.isOnline():
                      YAPI.yapiLockDeviceCallBack(error)
                      YAPI.native_yDeviceArrivalCallback(mod.functionDescriptor())
                      YAPI.yapiUnlockDeviceCallBack(error)
                  mod = mod.nextModule()
         return 0

    @staticmethod
    def  RegisterDeviceRemovalCallback(removalCallback):
        """
        Register a callback function, to be called each time
        a device is unpluged. This callback will be invoked while yUpdateDeviceList
        is running. You will have to call this function on a regular basis.
        
        @param removalCallback : a procedure taking a YModule parameter, or None
                to unregister a previously registered  callback.
        """
        global yRemovalFct
        yRemovalFct = removalCallback

    #noinspection PyUnresolvedReferences
    @staticmethod
    def native_yDeviceChangeCallback(d):
        global yChangeFct
        ev = YAPI.emptyApiEvent()
        infos = YAPI.emptyDeviceSt()
        errmsgRef = YRefParam()

        if yChangeFct is None: return
        ev.eventtype = YAPI.yapiEventType.YAPI_DEV_CHANGE
        if YAPI.yapiGetDeviceInfo(d, infos, errmsgRef) != YAPI.SUCCESS:
             return
        ev.modul = YModule.FindModule(YByte2String(infos.serial) + ".module")
        YAPI._PlugEvents.append(ev)
        return 0

    @staticmethod
    def RegisterDeviceChangeCallback( callback):
        global yChangeFct
        yChangeFct = callback

    @staticmethod
    def queuesCleanUp():
        del YAPI._PlugEvents[:]
        del YAPI._DataEvents[:]

    @staticmethod
    def native_yFunctionUpdateCallback( f,  data):
       ev = YAPI.emptyApiEvent()
       ev.fun_descr = f

       if data is None:
           ev.eventtype = YAPI.yapiEventType.YAPI_FUN_UPDATE
       else:
           ev.eventtype = YAPI.yapiEventType.YAPI_FUN_VALUE
           ev.value = YByte2String(data)

       YAPI._DataEvents.append(ev)
       return 0

    @staticmethod
    def RegisterCalibrationHandler(calibType,callback):
        key = str(calibType)
        YAPI._CalibHandlers[key]=callback

    #noinspection PyUnusedLocal
    @staticmethod
    def LinearCalibrationHandler(rawValue, calibType, params, rawValues,refValues):
        npt= calibType % 10
        x= rawValues[0]
        adj = refValues[0]-x
        i=0
        if npt>len(rawValues)+1:  npt=len(rawValues)+1
        if npt>len(refValues)+1:  npt=len(refValues)+1
        while rawValue>rawValues[i] and i+1<npt:
            i+=1
            x2=x
            adj2=adj
            x=rawValues[i]
            adj=refValues[i]-x
            if  rawValue<x and x>x2:
                adj=adj2+(adj-adj2)*(rawValue-x2)/(x-x2)
        return rawValue + adj

    #noinspection PyUnresolvedReferences
    @staticmethod
    def native_yDeviceRemovalCallback(d):
         global yRemovalFct
         ev = YAPI.emptyApiEvent()
         infos = YAPI.emptyDeviceSt()
         errmsgRef = YRefParam()
         if yRemovalFct is None:
             return
         ev.fun_descr = 0
         ev.value = ""
         ev.eventtype = YAPI.yapiEventType.YAPI_DEV_REMOVAL
         infos.deviceid = 0
         if YAPI.yapiGetDeviceInfo(d, infos, errmsgRef) != YAPI.SUCCESS:
             return
         ev.modul = YModule.FindModule(YByte2String(infos.serial) + ".module")
         YAPI._PlugEvents.append(ev)
         return 0



    #noinspection PyUnresolvedReferences
    @staticmethod
    def apiGetAPIVersion(versionRef, dateRef):
        pversion = YAPI.YPCHAR()
        pdate = YAPI.YPCHAR()
        res = YAPI._yapiGetAPIVersion(ctypes.byref(pversion),ctypes.byref(pdate))
        versionRef.value = YByte2String(pversion.buffer)
        dateRef.value = YByte2String(pdate.buffer)
        return res


    @staticmethod
    def GetAPIVersion():
        """
        Returns the version identifier for the Yoctopuce library in use.
        The version is a string in the form "Major.Minor.Build",
        for instance "1.01.5535". For languages using an external
        DLL (for instance C#, VisualBasic or Delphi), the character string
        includes as well the DLL version, for instance
        "1.01.5535 (1.01.5439)".
        
        If you want to verify in your code that the library version is
        compatible with the version that you have used during development,
        verify that the major number is strictly equal and that the minor
        number is greater or equal. The build number is not relevant
        with respect to the library compatibility.
        
        @return a character string describing the library version.
        """
        version = YRefParam()
        date = YRefParam()
        #load yapi functions form dynamic library  
        if not YAPI._ydllLoaded : YAPI.yloadYapiCDLL()
        YAPI.apiGetAPIVersion(version, date)
        #noinspection PyTypeChecker
        return YAPI.YOCTO_API_VERSION_STR + "." + YAPI.YOCTO_API_BUILD_NO + " (" + version.value + ")"

    @staticmethod
    def InitAPI(mode, errmsgRef=None):
        """
        Initializes the Yoctopuce programming library explicitly.
        It is not strictly needed to call yInitAPI(), as the library is
        automatically  initialized when calling yRegisterHub() for the
        first time.
        
        When YAPI.DETECT_NONE is used as detection mode,
        you must explicitly use yRegisterHub() to point the API to the
        VirtualHub on which your devices are connected before trying to access them.
        
        @param mode : an integer corresponding to the type of automatic
                device detection to use. Possible values are
                YAPI.DETECT_NONE, YAPI.DETECT_USB, YAPI.DETECT_NET,
                and YAPI.DETECT_ALL.
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        if YAPI._apiInitialized:
            return YAPI.SUCCESS
        #load yapi functions form dynamic library  
        if not YAPI._ydllLoaded : YAPI.yloadYapiCDLL()
        version = YRefParam()
        date = YRefParam()
        if YAPI.apiGetAPIVersion(version, date) != YAPI.YOCTO_API_VERSION_BCD:
            if  errmsgRef is not None:
                errmsgRef.value = YAPI._yApiCLibFile+" does does not match the version of the Libary (Libary=" + YAPI.YOCTO_API_VERSION_STR + "." + YAPI.YOCTO_API_BUILD_NO
                #noinspection PyTypeChecker
                errmsgRef.value += " yapi.dll=" + version.value + ")"
                return YAPI.VERSION_MISMATCH

        YAPI.pymodule_initialization()

        #noinspection PyUnresolvedReferences
        res = YAPI._yapiInitAPI(mode, buffer)
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
        if YAPI.YISERR(res):
            return res

        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterDeviceArrivalCallback( native_yDeviceArrivalAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterDeviceRemovalCallback(native_yDeviceRemovalAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterDeviceChangeCallback( native_yDeviceChangeAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterFunctionUpdateCallback(native_yFunctionUpdateAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterLogFunction(native_yLogFunctionAnchor)
        for i in range(21):
            YAPI.RegisterCalibrationHandler(i,YAPI.LinearCalibrationHandler)
        YAPI._apiInitialized = True
        return res

    @staticmethod
    def FreeAPI():
        """
        Frees dynamically allocated memory blocks used by the Yoctopuce library.
        It is generally not required to call this function, unless you
        want to free all dynamically allocated memory blocks in order to
        track a memory leak for instance.
        You should not call any other library function after calling
        yFreeAPI(), or your program will crash.
        """
        if YAPI._apiInitialized:
            #noinspection PyUnresolvedReferences
            YAPI._yapiFreeAPI()
            YAPI.pymodule_cleanup()
            YAPI._apiInitialized = False

    @staticmethod
    def RegisterHub(url,   errmsgRef=None):
        """
        Setup the Yoctopuce library to use modules connected on a given machine.
        When using Yoctopuce modules through the VirtualHub gateway,
        you should provide as parameter the address of the machine on which the
        VirtualHub software is running (typically "http://127.0.0.1:4444",
        which represents the local machine).
        When you use a language which has direct access to the USB hardware,
        you can use the pseudo-URL "usb" instead.
        
        Be aware that only one application can use direct USB access at a
        given time on a machine. Multiple access would cause conflicts
        while trying to access the USB modules. In particular, this means
        that you must stop the VirtualHub software before starting
        an application that uses direct USB access. The workaround
        for this limitation is to setup the library to use the VirtualHub
        rather than direct USB access.
        
        If acces control has been activated on the VirtualHub you want to
        reach, the URL parameter should look like:
        
        http://username:password@adresse:port
        
        @param url : a string containing either "usb" or the
                root URL of the hub to monitor
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN+1)

        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsgRef)
            if YAPI.YISERR(res):
                return res
        p= ctypes.create_string_buffer(url.encode("ASCII"))
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiRegisterHub(p,buffer)


        if YAPI.YISERR(res):
            if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)

        return res

    @staticmethod
    def PreregisterHub(url,   errmsgRef=None):
        """
        doc
        """
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)

        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsgRef)
            if YAPI.YISERR(res):
                return res

        #noinspection PyUnresolvedReferences
        res = YAPI._yapiPreregisterHub(ctypes.create_string_buffer(url.encode("ASCII")), buffer)
        if YAPI.YISERR(res):
            if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)

        return res

    @staticmethod
    def UnregisterHub( url):
      """
      Setup the Yoctopuce library to no more use modules connected on a previously
      registered machine with RegisterHub.
      
      @param url : a string containing either "usb" or the
              root URL of the hub to monitor
      """
      if not YAPI._apiInitialized:
          return

      #noinspection PyUnresolvedReferences
      YAPI._yapiUnregisterHub(ctypes.create_string_buffer(url.encode("ASCII")))

    @staticmethod
    def UpdateDeviceList(errmsgRef=None):
        """
        Triggers a (re)detection of connected Yoctopuce modules.
        The library searches the machines or USB ports previously registered using
        yRegisterHub(), and invokes any user-defined callback function
        in case a change in the list of connected devices is detected.
        
        This function can be called as frequently as desired to refresh the device list
        and to make the application aware of hot-plug events.
        
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        global yArrivalFct
        global yRemovalFct
        global yChangeFct
        
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)

        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsgRef)
            if YAPI.YISERR(res):
                return res

        res = YAPI.yapiUpdateDeviceList(0, errmsgRef)
        if YAPI.YISERR(res): return res


        #noinspection PyUnresolvedReferences
        res = YAPI._yapiHandleEvents(buffer)
        if YAPI.YISERR(res):
            if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
            return res


        while len(YAPI._PlugEvents) > 0:
            YAPI.yapiLockDeviceCallBack(errmsgRef)
            p = YAPI._PlugEvents.pop(0)
            YAPI.yapiUnlockDeviceCallBack(errmsgRef)
            if p.eventtype==YAPI.yapiEventType.YAPI_DEV_ARRIVAL:
               if yArrivalFct is not None:
                   #noinspection PyCallingNonCallable
                  yArrivalFct(p.modul)
            elif  p.eventtype==YAPI.yapiEventType.YAPI_DEV_REMOVAL:
               if yRemovalFct is not None:
                   #noinspection PyCallingNonCallable
                   yRemovalFct(p.modul)
            elif  p.eventtype==YAPI.yapiEventType.YAPI_DEV_CHANGE:
               if  yChangeFct is not None:
                   #noinspection PyCallingNonCallable
                   yChangeFct(p.modul)
        return YAPI.SUCCESS

    #noinspection PyUnresolvedReferences
    @staticmethod
    def yapiGetFunctionInfo(fundesc, devdescRef, serialRef, funcIdRef, funcNameRef, funcValRef,errmsgRef =None):
        serialBuffer = ctypes.create_string_buffer(YAPI.YOCTO_SERIAL_LEN)
        funcIdBuffer = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcNameBuffer = ctypes.create_string_buffer(YAPI.YOCTO_LOGICAL_LEN)
        funcValBuffer = ctypes.create_string_buffer(YAPI.YOCTO_PUBVAL_LEN)
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        p=ctypes.c_int()
        res = YAPI._yapiGetFunctionInfo(fundesc,  ctypes.byref(p),serialBuffer, funcIdBuffer, funcNameBuffer, funcValBuffer, errBuffer)
        devdescRef.value = p.value
        serialRef.value = YByte2String(serialBuffer.value)
        funcIdRef.value = YByte2String(funcIdBuffer.value)
        funcNameRef.value = YByte2String(funcNameBuffer.value)
        funcValRef.value = YByte2String(funcValBuffer.value)
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(errBuffer.value)
        return res

    #noinspection PyUnresolvedReferences,PyUnresolvedReferences
    @staticmethod
    def yapiGetDeviceByFunction(fundesc, errmsgRef = None):
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc = ctypes.c_int()
        res = YAPI._yapiGetFunctionInfo(fundesc, ctypes.byref(devdesc), None, None, None, None, errBuffer)
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(errBuffer.value)
        if res < 0:
            return res
        return devdesc.value

    @staticmethod
    def yapiUpdateDeviceList(force, errmsgRef=None):
         buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
         #noinspection PyUnresolvedReferences
         res = YAPI._yapiUpdateDeviceList(force, buffer)
         if YAPI.YISERR(res):
             if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
         return res

    @staticmethod
    def yapiGetDevice(device_str, errmsgRef=None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        p=ctypes.create_string_buffer(device_str.encode("ASCII"))
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetDevice(p, buffer)
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
        return res

    @staticmethod
    def yapiGetFunction(class_str, function_str, errmsgRef=None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunction(ctypes.create_string_buffer(class_str.encode("ASCII")), ctypes.create_string_buffer(function_str.encode("ASCII")), buffer)
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
        return res

    #noinspection PyUnresolvedReferences
    @staticmethod
    def apiGetFunctionsByClass(class_str, precFuncDesc, dbuffer, maxsize, neededsizeRef, errmsgRef=None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        cneededsize = ctypes.c_int()
        res = YAPI._yapiGetFunctionsByClass(ctypes.create_string_buffer(class_str.encode("ASCII")), precFuncDesc, dbuffer, maxsize, ctypes.byref(cneededsize), buffer)
        #noinspection PyUnresolvedReferences
        neededsizeRef.value = cneededsize.value
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
        return res

    #noinspection PyUnresolvedReferences
    @staticmethod
    def apiGetFunctionsByDevice(devdesc,  precFuncDesc,  dbuffer,  maxsize, neededsizeRef, errmsgRef=None):
        buffer =ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        cneededsize = ctypes.c_int()
        res = YAPI._yapiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer, maxsize, ctypes.byref(cneededsize), buffer)
        #noinspection PyUnresolvedReferences
        neededsizeRef.value = cneededsize.value
        if  errmsgRef is not None:  errmsgRef.value = YByte2String(buffer.value)
        return res

    @staticmethod
    def pymodule_initialization():
        pass

    @staticmethod
    def pymodule_cleanup():
        del YAPI.YDevice_devCache[:]
        del YAPI._PlugEvents[:]
        del YAPI._DataEvents[:]
        YFunction._CalibHandlers.clear()




## ------------------------------------------------------------------------------------
##
## YDevice
##
## ------------------------------------------------------------------------------------

class YDevice:

    def __init__(self,devdesc):
        self._devdescr = devdesc
        self._cacheStamp =datetime.datetime(year=1970,month=1,day=1)
        self._cacheJson = None
        self._functions = []
        self._rootdevice = ""
        self._subpath = ""
        self._subpathinit = False

    def __del__(self):
        if self._cacheJson is not None:
            del self._cacheJson
        self._cacheJson = None

    @staticmethod
    def getDevice(devdescr):
        for idx in range(len(YAPI.YDevice_devCache)):
            if YAPI.YDevice_devCache[idx]._devdescr == devdescr:
                return YAPI.YDevice_devCache[idx]

        dev = YDevice(devdescr)
        YAPI.YDevice_devCache.append(dev)
        return dev


    def _HTTPRequestPrepare(self,request):
        errbuf = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        root = ctypes.create_string_buffer(YAPI.YOCTO_SERIAL_LEN)

        if not self._subpathinit:
            neededsize = ctypes.c_int()
            res = YAPI._yapiGetDevicePath(self._devdescr, root, None, 0, ctypes.byref(neededsize), errbuf)
            if YAPI.YISERR(res):
                return res, YByte2String(errbuf.value)
            #noinspection PyUnresolvedReferences
            b =  ctypes.create_string_buffer(neededsize.value)
            tmp = ctypes.c_int()
            res = YAPI._yapiGetDevicePath(self._devdescr, root, b, neededsize.value, ctypes.byref(tmp), errbuf)
            if YAPI.YISERR(res):
                return res, YByte2String(errbuf.value)
            self._rootdevice = YByte2String(root.value)
            self._subpath =YByte2String(b.value)
            self._subpathinit = True

        # request can be a purely binary buffer or a text string
        if not isinstance(request,bytes):
            request = YString2Byte(request)
        # first / is expected within very first characters of the query
        p = 0
        while p < 10 and YGetByte(request,p) != 47: # chr(47) = '/'
            p += 1
        newrequest = request[0:p]+self._subpath.encode("ASCII")+request[p+1:]
        return YAPI.SUCCESS, newrequest


    #noinspection PyUnresolvedReferences
    def HTTPRequestAsync(self,request, callback, context, errmsgRef = None):
        errbuf = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        self._cacheStamp = YAPI.GetTickCount() #invalidate cache
        (res,newrequest) = self._HTTPRequestPrepare(request)
        if YAPI.YISERR(res):
            if not errmsgRef is None: errmsgRef.value = newrequest
            return res
        res = YAPI._yapiHTTPRequestAsync(ctypes.create_string_buffer(self._rootdevice.encode("ASCII")),ctypes.create_string_buffer(newrequest), None,None, errbuf)
        if YAPI.YISERR(res):
            if not errmsgRef is None: errmsgRef.value = YByte2String(errbuf.value)
            return res
        return YAPI.SUCCESS


    def HTTPRequest(self,request, bufferRef, errmsgRef=None):
        (res,newrequest) = self._HTTPRequestPrepare(request)
        if YAPI.YISERR(res):
            if not errmsgRef is None: errmsgRef.value = newrequest
            return res
        #yapiHTTPRequestSyncStart(&iohdl, _rootdevice, fullrequest.c_str(), &reply, &replysize, errbuff)
        iohdl   = ctypes.create_string_buffer(YAPI.YIOHDL_SIZE)
        errbuf  = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        root_c  = ctypes.create_string_buffer(self._rootdevice.encode("ASCII"))
        newrequest_c = ctypes.create_string_buffer(newrequest)
        reply_c = POINTER(ctypes.c_ubyte)()
        neededsize_c = ctypes.c_int(0)
        res = YAPI._yapiHTTPRequestSyncStartEx(iohdl,root_c,newrequest_c,len(newrequest),ctypes.byref(reply_c),ctypes.byref(neededsize_c), errbuf)
        if YAPI.YISERR(res):
            if not errmsgRef is None: errmsgRef.value = YByte2String(errbuf.value)
            return res
        reply_size = neededsize_c.value
        bb = YString2Byte("")
        for i in range(reply_size):  #(xrange not supported in 2.5.x)
            bb = YAddByte(bb,reply_c[i])
        bufferRef.value = bb
        res = YAPI._yapiHTTPRequestSyncDone(iohdl, errbuf)
        if YAPI.YISERR(res):
            if not errmsgRef is None: errmsgRef.value = YByte2String(errbuf.value)
            return res
        return  YAPI.SUCCESS


    def requestAPI(self,apiresRef, errmsgRef = None):

        buffer =    YRefParam()

        #Check if we have a valid cache value
        if self._cacheStamp > YAPI.GetTickCount():
            apiresRef.value = self._cacheJson
            return YAPI.SUCCESS

        res = self.HTTPRequest("GET /api.json \r\n\r\n", buffer, errmsgRef)
        if YAPI.YISERR(res):
            # make sure a device scan does not solve the issue
            res = YAPI.yapiUpdateDeviceList(1,errmsgRef)
            if YAPI.YISERR(res):
                return res

            res = self.HTTPRequest("GET /api.json \r\n\r\n", buffer, errmsgRef)
            if YAPI.YISERR(res):
                 return res

        try:
           j = YAPI.TJsonParser(buffer.value)
        except YAPI.JsonError :   #( exception handling working in both  in 2.x and 3.x)
           e = sys.exc_info()[1]
           if not errmsgRef is None : errmsgRef.value = "unexpected JSON structure: " + e.msg
           return YAPI.IO_ERROR


        # store result in cache
        self._cacheJson = j
        apiresRef.value = j
        self._cacheStamp = YAPI.GetTickCount() + YAPI.DefaultCacheValidity

        return YAPI.SUCCESS

    #noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker
    def getFunctions(self, functionsRef, errmsgRef= None):

        neededsize = YRefParam()
        if not len(self._functions):
            res = YAPI.apiGetFunctionsByDevice(self._devdescr, 0, None, 64, neededsize,  errmsgRef)
            if YAPI.YISERR(res):
                return res

            count =  int(neededsize.value / YAPI.C_INTSIZE)
            #noinspection PyCallingNonCallable
            p = (ctypes.c_int * count )()

            res = YAPI.apiGetFunctionsByDevice(self._devdescr, 0, p, 64, neededsize, errmsgRef)
            if YAPI.YISERR(res):
                return res

            for i in range(count):
                self._functions.append(p[i])


        functionsRef.value = self._functions
        return YAPI.SUCCESS

## - keeps a reference to our callbacks, to  protect them from GC
## (may
native_yLogFunctionAnchor    =  YAPI._yapiLogFunc(YAPI.native_yLogFunction)
native_yFunctionUpdateAnchor =  YAPI._yapiFunctionUpdateFunc(YAPI.native_yFunctionUpdateCallback)
native_yDeviceArrivalAnchor  =  YAPI._yapiDeviceUpdateFunc(YAPI.native_yDeviceArrivalCallback)
native_yDeviceRemovalAnchor  =  YAPI._yapiDeviceUpdateFunc(YAPI.native_yDeviceRemovalCallback)
native_yDeviceChangeAnchor  =   YAPI._yapiDeviceUpdateFunc(YAPI.native_yDeviceChangeCallback)

class YFunction(object):
    _FunctionCache = []
    _FunctionCallbacks = []
    _CalibHandlers = {}

    FUNCTIONDESCRIPTOR_INVALID = -1
    HARDWAREID_INVALID = YAPI.INVALID_STRING
    FUNCTIONID_INVALID = YAPI.INVALID_STRING
    FRIENDLYNAME_INVALID = YAPI.INVALID_STRING

    def __init__(self,classname,func):
        self._className = classname
        self._func = func
        self._lastErrorType = YAPI.SUCCESS
        self._lastErrorMsg = ""
        self._cacheExpiration = datetime.datetime(year=1970,month=1,day=1)
        self._fundescr = YFunction.FUNCTIONDESCRIPTOR_INVALID
        self._userData = None
        self._genCallback = None
        YFunction._FunctionCache.append(self)

    def _throw(self,errType, errorMessage):
        self._lastErrorType = errType
        self._lastErrorMsg = errorMessage
        if not YAPI.ExceptionsDisabled:
            raise YAPI.YAPI_Exception(errType, "YoctoApi error : " + errorMessage)

    #  Method used to resolve our name to our unique function descriptor (may trigger a hub scan)
    def _getDescriptor(self,fundescrRef, errmsgRef=None):
        tmp_fundescr = YAPI.yapiGetFunction(self._className,self. _func, errmsgRef)
        if YAPI.YISERR(tmp_fundescr):
            res = YAPI.yapiUpdateDeviceList(1, errmsgRef)
            if YAPI.YISERR(res):
                return res
        tmp_fundescr = YAPI.yapiGetFunction(self._className, self._func, errmsgRef)
        if YAPI.YISERR(tmp_fundescr):
            return tmp_fundescr

        self._fundescr = tmp_fundescr
        fundescrRef.value = tmp_fundescr
        return YAPI.SUCCESS

     # Return a pointer to our device caching object (may trigger a hub scan)
    def _getDevice(self,devRef, errmsgRef=None):
        fundescrRef = YRefParam()
        # Resolve function name
        res = self._getDescriptor(fundescrRef, errmsgRef)
        if YAPI.YISERR(res):
            return res

        # Get device descriptor
        devdescr = YAPI.yapiGetDeviceByFunction(fundescrRef.value, errmsgRef)
        if YAPI.YISERR(devdescr):
            return devdescr

        # Get device object
        devRef.value = YDevice.getDevice(devdescr)
        return YAPI.SUCCESS

    # Return the next known function of current class listed in the yellow pages
    def _nextFunction(self, hwidRef):
        fundescrRef = YRefParam()
        devdescrRef = YRefParam()
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        neededsizeRef = YRefParam()
        errmsgRef = YRefParam()
        n_element = 1

        res = self._getDescriptor(fundescrRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        maxsize = n_element * YAPI.C_INTSIZE
        #noinspection PyCallingNonCallable,PyTypeChecker
        p =(ctypes.c_int*n_element)()

        res = YAPI.apiGetFunctionsByClass(self._className, fundescrRef.value, p, maxsize, neededsizeRef,  errmsgRef)

        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        #noinspection PyTypeChecker
        count = neededsizeRef.value / YAPI.C_INTSIZE
        if not count:
            hwidRef.value = ""
            return  YAPI.SUCCESS

        res = YAPI.yapiGetFunctionInfo(p[0], devdescrRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return  YAPI.SUCCESS

        hwidRef.value = serialRef.value + "." + funcIdRef.value
        return YAPI.SUCCESS

    def  _buildSetRequest(self,changeattr, changeval, requestRef, errmsgRef=None):
        fundescRef = YRefParam()
        funcid =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff =  ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if YAPI.YISERR(res):
            return res
        devdesc =ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), None, funcid, None, None, errbuff)
        if YAPI.YISERR(res):
            if not errmsgRef is None: errmsgRef.value = YByte2String(errbuff.value)
            self._throw(res, errmsgRef.value)
            return res
        requestRef.value = "GET /api/" + YByte2String(funcid.value) + "/"
        uchangeval = ""

        if changeattr != "":
            requestRef.value +=  changeattr + "?" + changeattr + "="

        for c in changeval:
            if c <= ' ' or (c > 'z' and c != '~') or c == '"' or c == '%' or c == '&' or c == '+' or \
                            c == '<' or c == '=' or c == '>' or c == '\\' or c == '^' or c == '`':
                uchangeval += "%" + ('%02X' % ord(c))
            else:
                uchangeval +=   c

        requestRef.value +=  uchangeval + " \r\n\r\n"
        return YAPI.SUCCESS


    # Set an attribute in the function, and parse the resulting new function state
    def  _setAttr(self,attrname,  newvalue):
        errmsgRef = YRefParam()
        requestRef = YRefParam()
        devRef = YRefParam()

        #  Execute http request
        res =self._buildSetRequest(attrname, newvalue, requestRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        # Get device Object
        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        res = devRef.value.HTTPRequestAsync(requestRef.value, None, None, errmsgRef)
        if YAPI.YISERR(res):
            # make sure a device scan does not solve the issue
            res = YAPI.yapiUpdateDeviceList(1,errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res
            
            res = devRef.value.HTTPRequestAsync(requestRef.value, None, None, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res
        
        self._cacheExpiration = YAPI.GetTickCount()

        return  YAPI.SUCCESS

    #noinspection PyUnusedLocal
    #@abc.abstractmethod   (not supported in 2.5.x)
    def _parse(self,parser):
        return

    def _request(self, request):
        errmsgRef = YRefParam()
        buffer =    YRefParam()
        devRef = YRefParam()
        # Get device Object
        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, request)
            return b""
        res = devRef.value.HTTPRequest(request, buffer, errmsgRef)
        if YAPI.YISERR(res):
            # make sure a device scan does not solve the issue
            res = YAPI.yapiUpdateDeviceList(1,errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return b""
            res = devRef.value.HTTPRequest(request, buffer, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return b""
        if len(buffer.value) >= 4:
            check = buffer.value[0:4].decode("latin1")
            if check == "OK\r\n":
                return buffer.value
            if len(buffer.value) >= 17:
                check = buffer.value[0:17].decode("latin1")
                if check == "HTTP/1.1 200 OK\r\n":
                    return buffer.value
        self._throw(YAPI.IO_ERROR,"http request failed")
        return b""


    def _upload(self, path,  content):
        body = "Content-Disposition: form-data; name=\""+path+"\"; filename=\"api\"\r\n"
        body += "Content-Type: application/octet-stream\r\n"
        body += "Content-Transfer-Encoding: binary\r\n\r\n"
        if not isinstance(content,bytes):
            if isinstance(content,array.array):
                content = content.tostring()
            else:
                content = content.encode("latin1")
        body = body.encode("ASCII") + content
        boundary = "Zz%06xzZ" %( random.randint(0,0xffffff))
        request  = "POST /upload.html HTTP/1.1\r\n"
        request += "Content-Type: multipart/form-data, boundary="+boundary+"\r\n"
        request += "\r\n--"+boundary+"\r\n"
        request = request.encode("ASCII")+body+str("\r\n--"+boundary+"--\r\n").encode("ASCII")
        buffer = self._request(request)
        if len(buffer) == 0:
            self._throw(YAPI.IO_ERROR,"http request failed")
            return YAPI.IO_ERROR
        return YAPI.SUCCESS

    def _download(self, url):
        request = "GET /"+url+" HTTP/1.1\r\n\r\n"
        buffer = self._request(request)
        found = 0
        while found <= len(buffer) - 4:
            if YGetByte(buffer,found) == 13 and YGetByte(buffer,found+1) == 10 and \
                            YGetByte(buffer,found+2) == 13 and YGetByte(buffer,found+3) == 10:
                break
            found += 1
        if found > len(buffer)-4:
            self._throw(YAPI.IO_ERROR,"http request failed")
            return YAPI.INVALID_STRING
        return buffer[found+4:]

    def _json_get_key(self, json,  key):
        try:
            j = YAPI.TJsonParser(json,False)
        except YAPI.JsonError :   #( exception handling working in both  in 2.x and 3.x
            e = sys.exc_info()[1]
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: " + e.msg)
            return YAPI.IO_ERROR
        node = j.GetChildNode(None,key)
        return node.svalue

    def _json_get_array(self, json):
        try:
            j = YAPI.TJsonParser(json,False)
        except YAPI.JsonError :   #( exception handling working in both  in 2.x and 3.x
            e = sys.exc_info()[1]
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: " + e.msg)
            return YAPI.IO_ERROR
        return j.GetAllChilds(None)


    def get_hardwareId(self):
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        snum =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff =  ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.HARDWAREID_INVALID
        devdesc =ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, None, None, errbuff)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.HARDWAREID_INVALID
        return YByte2String(snum.value)+"."+YByte2String(funcid.value)

    def get_functionId(self):
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        funcid =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff =  ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.FUNCTIONID_INVALID
        devdesc =ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), None, funcid, None, None, errbuff)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.FUNCTIONID_INVALID
        return YByte2String(funcid.value)

    def get_friendlyName(self):
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        fname   =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        snum    =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid  =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff =  ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc =ctypes.c_int()
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if not YAPI.YISERR(res) and not YAPI.YISERR(YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, fname, None, errbuff)):
            if YByte2String(fname.value) != "":
                funcid = fname
            dname   =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
            moddescr = YAPI.yapiGetFunction("Module",YByte2String(snum.value),errmsgRef)
            if not YAPI.YISERR(moddescr) and not YAPI.YISERR(YAPI._yapiGetFunctionInfo(moddescr, ctypes.byref(devdesc), None, None, dname, None, errbuff)):
                if YByte2String(dname.value) != "":
                    return "%s.%s" %(YByte2String(dname.value),YByte2String(funcid.value))
            return "%s.%s" %(YByte2String(snum.value),YByte2String(funcid.value))
        self._throw(YAPI.DEVICE_NOT_FOUND, errmsgRef.value)
        return self.FRIENDLYNAME_INVALID


    def describe(self):
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        snum   =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff =  ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc =ctypes.c_int()
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if not YAPI.YISERR(res) and not YAPI.YISERR(YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, None, None, errbuff)):
            return self._className +"("+self._func+")="+YByte2String(snum.value)+"."+YByte2String(funcid.value)
        return self._className +"("+self._func+")=unresolved"

    def __str__(self):
        return self.describe()

    def get_errorType(self):
        """
        Returns the numerical error code of the latest error with this function.
        This method is mostly useful when using the Yoctopuce library with
        exceptions disabled.
        
        @return a number corresponding to the code of the latest error that occured while
                using this function object
        """
        return self._lastErrorType

    def errorType(self):
        return self._lastErrorType

    def errType(self):
        return self._lastErrorType


    def get_errorMessage(self):
        """
        Returns the error message of the latest error with this function.
        This method is mostly useful when using the Yoctopuce library with
        exceptions disabled.
        
        @return a string corresponding to the latest error message that occured while
                using this function object
        """
        return self._lastErrorMsg

    def errorMessage(self):
        return self._lastErrorMsg

    def  errMessage(self):
        return self._lastErrorMsg

    def isOnline(self):
        """
        Checks if the function is currently reachable, without raising any error.
        If there is a cached value for the function in cache, that has not yet
        expired, the device is considered reachable.
        No exception is raised if there is an error while trying to contact the
        device hosting the requested function.
        
        @return true if the function can be reached, and false otherwise
        """

        devRef = YRefParam()
        errmsgRef = YRefParam()
        apiresRef = YRefParam()

        #  A valid value in cache means that the device is online
        if self._cacheExpiration > YAPI.GetTickCount():
            return True

        #Check that the function is available, without throwing exceptions
        if YAPI.YISERR(self._getDevice(devRef, errmsgRef)):
            return False

        # Try to execute a function request to be positively sure that the device is ready
        if YAPI.YISERR(devRef.value.requestAPI(apiresRef, errmsgRef)):
            return False

        return True

    def load(self,msValidity):
        """
        Preloads the function cache with a specified validity duration.
        By default, whenever accessing a device, all function attributes
        are kept in cache for the standard duration (5 ms). This method can be
        used to temporarily mark the cache as valid for a longer period, in order
        to reduce network trafic for instance.
        
        @param msValidity : an integer corresponding to the validity attributed to the
                loaded function parameters, in milliseconds
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        devRef = YRefParam()
        errmsgRef = YRefParam()
        apiresRef = YRefParam()
        funcIdRef = YRefParam()
        devdescRef = YRefParam()
        serialRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()

        # Resolve our reference to our device, load REST API
        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        res = devRef.value.requestAPI(apiresRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res


        # Get our function Id
        fundescr = YAPI.yapiGetFunction(self._className, self._func, errmsgRef)
        if YAPI.YISERR(fundescr):
            self._throw(res, errmsgRef.value)
            return fundescr

        res = YAPI.yapiGetFunctionInfo(fundescr, devdescRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        node = apiresRef.value.GetChildNode(None, funcIdRef.value)
        if node is None:
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: missing function " + str(funcIdRef.value))
            return YAPI.IO_ERROR

        self._parse(node)
        self._cacheExpiration = YAPI.GetTickCount() + msValidity
        return YAPI.SUCCESS

    def get_module(self):
        """
        Gets the YModule object for the device on which the function is located.
        If the function cannot be located on any module, the returned instance of
        YModule is not shown as on-line.
        
        @return an instance of YModule
        """
        devdescrRef = YRefParam()
        errmsgRef = YRefParam()
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValueRef = YRefParam()

        fundescr = YAPI.yapiGetFunction(self._className, self._func, errmsgRef)
        if  not YAPI.YISERR(fundescr):
            if  not YAPI.YISERR(YAPI.yapiGetFunctionInfo(fundescr, devdescrRef, serialRef, funcIdRef, funcNameRef, funcValueRef, errmsgRef)):
                 return YModule.FindModule(serialRef.value + ".module")

        # return a true YModule object even if it is not a module valid for communicating
        return YModule.FindModule("module_of_" + self._className + "_" + self._func)

    def module(self):
        return self.get_module()

    def get_functionDescriptor(self):
        """
        Returns a unique identifier of type YFUN_DESCR corresponding to the function.
        This identifier can be used to test if two instances of YFunction reference the same
        physical function on the same physical device.
        
        @return an identifier of type YFUN_DESCR.
        
        If the function has never been contacted, the returned value is YFunction.FUNCTIONDESCRIPTOR_INVALID.
        """
        return self._fundescr

    def functionDescriptor(self):
        return self.get_functionDescriptor()

    def get_userData(self):
        """
        Returns the value of the userData attribute, as previously stored using method
        set_userData.
        This attribute is never touched directly by the API, and is at disposal of the caller to
        store a context.
        
        @return the object stored previously by the caller.
        """
        return self._userData

    def userData(self):
        return self.get_userData()

    def set_userData(self, data):
        """
        Stores a user context provided as argument in the userData attribute of the function.
        This attribute is never touched by the API, and is at disposal of the caller to store a context.
        
        @param data : any kind of object to be stored
        @noreturn
        """
        self._userData = data

    def setUserData(self,data):
        self.set_userData(data)

    #noinspection PyUnusedLocal
    def _registerFuncCallback(self,func):
        self.isOnline()
        if self not in YFunction._FunctionCallbacks:
           YFunction._FunctionCallbacks.append(self)

    #noinspection PyUnusedLocal
    def _unregisterFuncCallback(self, func):
        if self in YFunction._FunctionCallbacks:
            index = YFunction._FunctionCallbacks.index(self)
            del YFunction._FunctionCallbacks[index]


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
        self._genCallback = callback

    def  advertiseValue(self,value):
        if self._genCallback is not None:
            self._genCallback(self, value)


class YModule(YFunction):

    #--- (generated code: YModule definitions)


    PRODUCTNAME_INVALID             = YAPI.INVALID_STRING
    SERIALNUMBER_INVALID            = YAPI.INVALID_STRING
    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    PRODUCTID_INVALID               = YAPI.INVALID_LONG
    PRODUCTRELEASE_INVALID          = YAPI.INVALID_LONG
    FIRMWARERELEASE_INVALID         = YAPI.INVALID_STRING
    LUMINOSITY_INVALID              = YAPI.INVALID_LONG
    UPTIME_INVALID                  = YAPI.INVALID_LONG
    USBCURRENT_INVALID              = YAPI.INVALID_LONG
    REBOOTCOUNTDOWN_INVALID         = YAPI.INVALID_LONG

    PERSISTENTSETTINGS_LOADED       = 0
    PERSISTENTSETTINGS_SAVED        = 1
    PERSISTENTSETTINGS_MODIFIED     = 2
    PERSISTENTSETTINGS_INVALID      = -1
    BEACON_OFF                      = 0
    BEACON_ON                       = 1
    BEACON_INVALID                  = -1
    USBBANDWIDTH_SIMPLE             = 0
    USBBANDWIDTH_DOUBLE             = 1
    USBBANDWIDTH_INVALID            = -1


    _ModuleCache ={}

    #--- (end of generated code: YModule definitions)

        #--- (generated code: YModule implementation)

    def __init__(self,func):
        super(YModule,self).__init__("Module", func)
        self._callback = None
        self._productName = YModule.PRODUCTNAME_INVALID
        self._serialNumber = YModule.SERIALNUMBER_INVALID
        self._logicalName = YModule.LOGICALNAME_INVALID
        self._productId = YModule.PRODUCTID_INVALID
        self._productRelease = YModule.PRODUCTRELEASE_INVALID
        self._firmwareRelease = YModule.FIRMWARERELEASE_INVALID
        self._persistentSettings = YModule.PERSISTENTSETTINGS_INVALID
        self._luminosity = YModule.LUMINOSITY_INVALID
        self._beacon = YModule.BEACON_INVALID
        self._upTime = YModule.UPTIME_INVALID
        self._usbCurrent = YModule.USBCURRENT_INVALID
        self._rebootCountdown = YModule.REBOOTCOUNTDOWN_INVALID
        self._usbBandwidth = YModule.USBBANDWIDTH_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "productName":
                self._productName = member.svalue
            elif member.name == "serialNumber":
                self._serialNumber = member.svalue
            elif member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "productId":
                self._productId = member.ivalue
            elif member.name == "productRelease":
                self._productRelease = member.ivalue
            elif member.name == "firmwareRelease":
                self._firmwareRelease = member.svalue
            elif member.name == "persistentSettings":
                self._persistentSettings = member.ivalue
            elif member.name == "luminosity":
                self._luminosity = member.ivalue
            elif member.name == "beacon":
                self._beacon = member.ivalue
            elif member.name == "upTime":
                self._upTime = member.ivalue
            elif member.name == "usbCurrent":
                self._usbCurrent = member.ivalue
            elif member.name == "rebootCountdown":
                self._rebootCountdown = member.ivalue
            elif member.name == "usbBandwidth":
                self._usbBandwidth = member.ivalue
        return 0

    def get_productName(self):
        """
        Returns the commercial name of the module, as set by the factory.
        
        @return a string corresponding to the commercial name of the module, as set by the factory
        
        On failure, throws an exception or returns YModule.PRODUCTNAME_INVALID.
        """
        if self._productName == YModule.PRODUCTNAME_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.PRODUCTNAME_INVALID
        return self._productName

    def get_serialNumber(self):
        """
        Returns the serial number of the module, as set by the factory.
        
        @return a string corresponding to the serial number of the module, as set by the factory
        
        On failure, throws an exception or returns YModule.SERIALNUMBER_INVALID.
        """
        if self._serialNumber == YModule.SERIALNUMBER_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.SERIALNUMBER_INVALID
        return self._serialNumber

    def get_logicalName(self):
        """
        Returns the logical name of the module.
        
        @return a string corresponding to the logical name of the module
        
        On failure, throws an exception or returns YModule.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the module. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the module
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_productId(self):
        """
        Returns the USB device identifier of the module.
        
        @return an integer corresponding to the USB device identifier of the module
        
        On failure, throws an exception or returns YModule.PRODUCTID_INVALID.
        """
        if self._productId == YModule.PRODUCTID_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.PRODUCTID_INVALID
        return self._productId

    def get_productRelease(self):
        """
        Returns the hardware release version of the module.
        
        @return an integer corresponding to the hardware release version of the module
        
        On failure, throws an exception or returns YModule.PRODUCTRELEASE_INVALID.
        """
        if self._productRelease == YModule.PRODUCTRELEASE_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.PRODUCTRELEASE_INVALID
        return self._productRelease

    def get_firmwareRelease(self):
        """
        Returns the version of the firmware embedded in the module.
        
        @return a string corresponding to the version of the firmware embedded in the module
        
        On failure, throws an exception or returns YModule.FIRMWARERELEASE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.FIRMWARERELEASE_INVALID
        return self._firmwareRelease

    def get_persistentSettings(self):
        """
        Returns the current state of persistent module settings.
        
        @return a value among YModule.PERSISTENTSETTINGS_LOADED, YModule.PERSISTENTSETTINGS_SAVED and
        YModule.PERSISTENTSETTINGS_MODIFIED corresponding to the current state of persistent module settings
        
        On failure, throws an exception or returns YModule.PERSISTENTSETTINGS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.PERSISTENTSETTINGS_INVALID
        return self._persistentSettings

    def set_persistentSettings(self, newval):
        rest_val = str(newval)
        return self._setAttr("persistentSettings", rest_val)


    def saveToFlash(self):
        """
        Saves current settings in the nonvolatile memory of the module.
        Warning: the number of allowed save operations during a module life is
        limited (about 100000 cycles). Do not call this function within a loop.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1"
        return self._setAttr("persistentSettings", rest_val)

    def revertFromFlash(self):
        """
        Reloads the settings stored in the nonvolatile memory, as
        when the module is powered on.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "0"
        return self._setAttr("persistentSettings", rest_val)

    def get_luminosity(self):
        """
        Returns the luminosity of the  module informative leds (from 0 to 100).
        
        @return an integer corresponding to the luminosity of the  module informative leds (from 0 to 100)
        
        On failure, throws an exception or returns YModule.LUMINOSITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.LUMINOSITY_INVALID
        return self._luminosity

    def set_luminosity(self, newval):
        """
        Changes the luminosity of the module informative leds. The parameter is a
        value between 0 and 100.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : an integer corresponding to the luminosity of the module informative leds
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("luminosity", rest_val)


    def get_beacon(self):
        """
        Returns the state of the localization beacon.
        
        @return either YModule.BEACON_OFF or YModule.BEACON_ON, according to the state of the localization beacon
        
        On failure, throws an exception or returns YModule.BEACON_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.BEACON_INVALID
        return self._beacon

    def set_beacon(self, newval):
        """
        Turns on or off the module localization beacon.
        
        @param newval : either YModule.BEACON_OFF or YModule.BEACON_ON
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val =  "1" if newval > 0 else "0"
        return self._setAttr("beacon", rest_val)


    def get_upTime(self):
        """
        Returns the number of milliseconds spent since the module was powered on.
        
        @return an integer corresponding to the number of milliseconds spent since the module was powered on
        
        On failure, throws an exception or returns YModule.UPTIME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.UPTIME_INVALID
        return self._upTime

    def get_usbCurrent(self):
        """
        Returns the current consumed by the module on the USB bus, in milli-amps.
        
        @return an integer corresponding to the current consumed by the module on the USB bus, in milli-amps
        
        On failure, throws an exception or returns YModule.USBCURRENT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.USBCURRENT_INVALID
        return self._usbCurrent

    def get_rebootCountdown(self):
        """
        Returns the remaining number of seconds before the module restarts, or zero when no
        reboot has been scheduled.
        
        @return an integer corresponding to the remaining number of seconds before the module restarts, or zero when no
                reboot has been scheduled
        
        On failure, throws an exception or returns YModule.REBOOTCOUNTDOWN_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.REBOOTCOUNTDOWN_INVALID
        return self._rebootCountdown

    def set_rebootCountdown(self, newval):
        rest_val = str(newval)
        return self._setAttr("rebootCountdown", rest_val)


    def reboot(self , secBeforeReboot):
        """
        Schedules a simple module reboot after the given number of seconds.
        
        @param secBeforeReboot : number of seconds before rebooting
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(secBeforeReboot)
        return self._setAttr("rebootCountdown", rest_val)

    def triggerFirmwareUpdate(self , secBeforeReboot):
        """
        Schedules a module reboot into special firmware update mode.
        
        @param secBeforeReboot : number of seconds before rebooting
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(-secBeforeReboot)
        return self._setAttr("rebootCountdown", rest_val)

    def get_usbBandwidth(self):
        """
        Returns the number of USB interfaces used by the module.
        
        @return either YModule.USBBANDWIDTH_SIMPLE or YModule.USBBANDWIDTH_DOUBLE, according to the number
        of USB interfaces used by the module
        
        On failure, throws an exception or returns YModule.USBBANDWIDTH_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YModule.USBBANDWIDTH_INVALID
        return self._usbBandwidth

    def set_usbBandwidth(self, newval):
        """
        Changes the number of USB interfaces used by the module. You must reboot the module
        after changing this setting.
        
        @param newval : either YModule.USBBANDWIDTH_SIMPLE or YModule.USBBANDWIDTH_DOUBLE, according to the
        number of USB interfaces used by the module
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("usbBandwidth", rest_val)

    def download(self, pathname):
        """
        Downloads the specified built-in file and returns a binary buffer with its content.
        
        @param pathname : name of the new file to load
        
        @return a binary buffer with the file content
        
        On failure, throws an exception or returns an empty content.
        """
        return self._download(pathname)
        

    def get_icon2d(self ):
        """
        Returns the icon of the module. The icon is a PNG image and does not
        exceeds 1536 bytes.
        
        @return a binary buffer with module icon, in png format.
        """
        return self._download("icon2d.png")
        

    def get_lastLogs(self ):
        """
        Returns a string with last logs of the module. This method return only
        logs that are still in the module.
        
        @return a string with last logs of the module.
        """
        
        content = self._download("logs.txt")
        return content
        


    def nextModule(self):
        """
        Continues the module enumeration started using yFirstModule().
        
        @return a pointer to a YModule object, corresponding to
                the next module found, or a None pointer
                if there are no more modules to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YModule.FindModule(hwidRef.value)

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

#--- (end of generated code: YModule implementation)


    def get_friendlyName(self):
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        fname   =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        snum    =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid  =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff =  ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc =ctypes.c_int()
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if not YAPI.YISERR(res) and not YAPI.YISERR(YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, fname, None, errbuff)):
            dname   =  ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
            moddescr = YAPI.yapiGetFunction("Module",YByte2String(snum.value),errmsgRef)
            if not YAPI.YISERR(moddescr) and not YAPI.YISERR(YAPI._yapiGetFunctionInfo(moddescr, ctypes.byref(devdesc), None, None, dname, None, errbuff)):
                if YByte2String(dname.value) != "":
                    return "%s" %(YByte2String(dname.value))
            return "%s" %(YByte2String(snum.value))
        self._throw(YAPI.DEVICE_NOT_FOUND, errmsgRef.value)
        return self.FRIENDLYNAME_INVALID

    def setImmutableAttributes(self,infosRef):
        self._serialNumber = YByte2String(infosRef.serial)
        self._productName = YByte2String(infosRef.productname)
        self._productId = int(infosRef.deviceid)

    # Return the properties of the nth function of our device
    def _getFunction(self,idx, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef):
        functionsRef = YRefParam()
        devRef = YRefParam()
        devdescrRef = YRefParam()

        # retrieve device object
        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        # get reference to all functions from the device
        res = devRef.value.getFunctions(functionsRef, errmsgRef)
        if YAPI.YISERR(res):
            return res

        # get latest function info from yellow pages
        fundescr = int(functionsRef.value[idx])

        res = YAPI.yapiGetFunctionInfo(fundescr, devdescrRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            return res

        return YAPI.SUCCESS

    def functionCount(self):
        """
        Returns the number of functions (beside the "module" interface) available on the module.
        
        @return the number of functions on the module
        
        On failure, throws an exception or returns a negative error code.
        """
        functionsRef = YRefParam()
        devRef = YRefParam()
        errmsgRef = YRefParam()

        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res


        res = devRef.value.getFunctions(functionsRef, errmsgRef)
        if YAPI.YISERR(res):

            self._throw(res, errmsgRef.value)
            return res

        return len(functionsRef.value)

    def functionId(self,functionIndex):
        """
        Retrieves the hardware identifier of the <i>n</i>th function on the module.
        
        @param functionIndex : the index of the function for which the information is desired, starting at
        0 for the first function.
        
        @return a string corresponding to the unambiguous hardware identifier of the requested module function
        
        On failure, throws an exception or returns an empty string.
        """
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        errmsgRef = YRefParam()

        res = self._getFunction(functionIndex, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return  YAPI.INVALID_STRING

        return funcIdRef.value

    def functionName(self,functionIndex):
        """
        Retrieves the logical name of the <i>n</i>th function on the module.
        
        @param functionIndex : the index of the function for which the information is desired, starting at
        0 for the first function.
        
        @return a string corresponding to the logical name of the requested module function
        
        On failure, throws an exception or returns an empty string.
        """
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        errmsgRef = YRefParam()

        res = self._getFunction(functionIndex, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return  YAPI.INVALID_STRING

        return funcNameRef.value

    def functionValue(self,functionIndex):
        """
        Retrieves the advertised value of the <i>n</i>th function on the module.
        
        @param functionIndex : the index of the function for which the information is desired, starting at
        0 for the first function.
        
        @return a short string (up to 6 characters) corresponding to the advertised value of the requested
        module function
        
        On failure, throws an exception or returns an empty string.
        """
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        errmsgRef = YRefParam()

        res = self._getFunction(functionIndex, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return YAPI.INVALID_STRING

        return  funcValRef.value

    #--- (generated code: Module functions)

    @staticmethod 
    def FindModule(func):
        """
        Allows you to find a module from its serial number or from its logical name.
        
        This function does not require that the module is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YModule.isOnline() to test if the module is
        indeed online at a given time. In case of ambiguity when looking for
        a module by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string containing either the serial number or
                the logical name of the desired module
        
        @return a YModule object allowing you to drive the module
                or get additional information on the module.
        """
        if func in YModule._ModuleCache:
            return YModule._ModuleCache[func]
        res =YModule(func)
        YModule._ModuleCache[func] =  res
        return res

    @staticmethod 
    def  FirstModule():
        """
        Starts the enumeration of modules currently accessible.
        Use the method YModule.nextModule() to iterate on the
        next modules.
        
        @return a pointer to a YModule object, corresponding to
                the first module currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Module", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YModule.FindModule(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _ModuleCleanup():
        pass

  #--- (end of generated code: Module functions)

