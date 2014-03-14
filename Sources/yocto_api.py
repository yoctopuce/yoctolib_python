#*********************************************************************
#*
#* $Id: yocto_api.py 14799 2014-01-31 14:59:44Z seb $
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
import datetime
import ctypes
import platform
#import abc  (not supported in 2.5.x)
import random
import sys
import os
import time
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


def YGetBytePython2x(binBuffer, idx):
    return ord(binBuffer[idx])


def YAddBytePython2x(binBuffer, b):
    return binBuffer + chr(b)


def YByte2StringPython3x(binBuffer):
    return binBuffer.decode("latin-1")


def YString2BytePython3x(strBuffer):
    return strBuffer.encode("latin-1")


def YGetBytePython3x(binBuffer, l):
    return binBuffer[l]


def YAddBytePython3x(binBuffer, b):
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
yLogFct = None
yArrivalFct = None
yRemovalFct = None
yChangeFct = None
yHubDiscoveryCallback = None


# This class is used to mimic "ByReference" parameter in function calls
class YRefParam:
    def __init__(self, initialValue=None):
        self.value = initialValue

    def __str__(self):
        return str(self.value)


#noinspection PyClassHasNoInit,PyProtectedMember
# noinspection PyUnresolvedReferences
class YAPI:
    #noinspection PyUnresolvedReferences
    class YPCHAR(ctypes.Structure):
        _fields_ = [("buffer", ctypes.c_char_p)]

    class JsonError(Exception):
        def __init__(self, msg):
            self.msg = msg
            Exception.__init__(self)

    #noinspection PyClassHasNoInit
    class TJSONRECORDTYPE:
        JSON_NONE, JSON_STRING, JSON_INTEGER, JSON_BOOLEAN, JSON_STRUCT, JSON_ARRAY = range(6)

    class TJSONRECORD:
        def __init__(self, name, datatype):
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

        #noinspection PyClassHasNoInit
        class Tjstate:
            JSTART, JWAITFORNAME, JWAITFORENDOFNAME, JWAITFORCOLON, JWAITFORDATA, JWAITFORNEXTSTRUCTMEMBER, \
                JWAITFORNEXTARRAYITEM, JSCOMPLETED, JWAITFORSTRINGVALUE, JWAITFORINTVALUE, JWAITFORBOOLVALUE = range(11)

        def __init__(self, jsonData, withHttpHeader=True):
            self.httpcode = 0
            self.data = None
            if withHttpHeader:
                httpheader = "HTTP/1.1 "
                okHeader = "OK\r\n"
                CR = "\r\n"
                if jsonData[0: len(okHeader)] == okHeader:
                    self.httpcode = 200
                else:
                    if jsonData[0: len(httpheader)] != httpheader:
                        errmsgRef = ("data should start with " + httpheader)
                        raise YAPI.JsonError(errmsgRef)

                    p1 = jsonData.find(" ", len(httpheader) - 1)
                    p2 = jsonData.find(" ", p1 + 1)

                    self.httpcode = int(jsonData[p1: p2])

                    if self.httpcode != 200:
                        return
                        #json data is a structure
                p1 = jsonData.find(CR + CR + "{")
                if p1 < 0:
                    p1 = jsonData.find(CR + CR + "[")  # json data is an array
                if p1 < 0:
                    errmsgRef = "data  does not contain JSON data"
                    raise YAPI.JsonError(errmsgRef)
                p1 += 4
                jsonData = jsonData[p1: len(jsonData)]
            else:
                start_struct = jsonData.find("{")   # json data is a structure
                start_array = jsonData.find("[")    # json data is an array
                if start_array < 0 and start_struct < 0:
                    errmsgRef = "data  does not contain JSON data"
                    raise YAPI.JsonError(errmsgRef)
            self.data = self._Parse(jsonData)

        def convertToString(self, p, showNamePrefix):
            if p is None:
                p = self.data
            if p.name != "" and showNamePrefix:
                outbuffer = '"' + p.name + "\":"
            else:
                outbuffer = ""
            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRING:
                outbuffer = outbuffer + '"' + p.svalue + '"'
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_INTEGER:
                outbuffer += p.ivalue
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_BOOLEAN:
                if p.bvalue:
                    outbuffer += "TRUE"
                else:
                    outbuffer += "FALSE"
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                outbuffer += '{'
                for i in range(len(p.members)):
                    if i > 0:
                        outbuffer += ','
                    outbuffer += self.convertToString(p.members[i], True)
                outbuffer += '}'
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                outbuffer += '['
                for i in range(len(p.items)):
                    if i > 0:
                        outbuffer += ','
                    outbuffer += self.convertToString(p.items[i], False)
                outbuffer += ']'
            return outbuffer

        def __del__(self):
            self._freestructure()

        def GetRootNode(self):
            return self.data

        class refidx:
            def __init__(self):
                self.i = 0

        def _Parse(self, st):
            idx = self.refidx()
            st = "\"root\" : " + st + " "
            return self._ParseEx(self.Tjstate.JWAITFORNAME, "", st, idx)

        @staticmethod
        def _ParseError(st, i, errmsgRef):
            ststart = i - 10
            stend = i + 10
            if ststart < 0:
                ststart = 0
            if stend > len(st):
                stend = len(st) - 1
            errmsgRef = errmsgRef + " near " + st[ststart:i] + "*" + st[i: stend]
            raise YAPI.JsonError(errmsgRef)

        @staticmethod
        def _createStructRecord(name):
            return YAPI.TJSONRECORD(name, YAPI.TJSONRECORDTYPE.JSON_STRUCT)

        @staticmethod
        def _createArrayRecord(name):
            return YAPI.TJSONRECORD(name, YAPI.TJSONRECORDTYPE.JSON_ARRAY)

        @staticmethod
        def _createStrRecord(name, value):
            res = YAPI.TJSONRECORD(name, YAPI.TJSONRECORDTYPE.JSON_STRING)
            res.svalue = value
            return res

        @staticmethod
        def _createIntRecord(name, value):
            res = YAPI.TJSONRECORD(name, YAPI.TJSONRECORDTYPE.JSON_INTEGER)
            res.ivalue = value
            return res

        @staticmethod
        def _createBoolRecord(name, value):
            res = YAPI.TJSONRECORD(name, YAPI.TJSONRECORDTYPE.JSON_BOOLEAN)
            res.bvalue = value
            return res

        @staticmethod
        def _add2StructRecord(container, element):
            if container.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                raise YAPI.JsonError("container is not a struct type")
            container.members.append(element)

        @staticmethod
        def _add2ArrayRecord(container, element):
            if container.recordtype != YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                raise YAPI.JsonError("container is not a struct type")
            container.items.append(element)

        @staticmethod
        def _Skipgarbage(st, idx):
            sti = st[idx.i]
            while idx.i < len(st) and (sti == '\n' or sti == '\r' or sti == ' '):
                idx.i += 1
                if idx.i < len(st):
                    sti = st[idx.i]
            return sti

        def _ParseEx(self, initialstate, defaultname, st, idx):

            res = YAPI.TJSONRECORD("", YAPI.TJSONRECORDTYPE.JSON_NONE)
            svalue = ""
            name = defaultname
            state = initialstate
            isign = 1
            ivalue = 0

            while idx.i < len(st):
                sti = st[idx.i]
                if state == self.Tjstate.JWAITFORNAME:
                    if sti == "\"":
                        state = self.Tjstate.JWAITFORENDOFNAME
                    elif sti != " " and sti != "\n":
                        self._ParseError(st, idx.i, "invalid char: was expecting \"")

                elif state == self.Tjstate.JWAITFORENDOFNAME:
                    if sti == "\"":
                        state = self.Tjstate.JWAITFORCOLON
                    elif ord(sti) >= 32:
                        name = name + sti
                    else:
                        self._ParseError(st, idx.i, "invalid char: was expecting an identifier compliant char")

                elif state == self.Tjstate.JWAITFORCOLON:
                    if sti == ":":
                        state = self.Tjstate.JWAITFORDATA
                    elif sti != " " and sti != "\n":
                        self._ParseError(st, idx.i, "invalid char: was expecting \"")

                elif state == self.Tjstate.JWAITFORDATA:
                    if sti == "{":
                        res = self._createStructRecord(name)
                        state = self.Tjstate.JWAITFORNEXTSTRUCTMEMBER
                    elif sti == "[":
                        res = self._createArrayRecord(name)
                        state = self.Tjstate.JWAITFORNEXTARRAYITEM
                    elif sti == "\"":
                        svalue = ""
                        state = self.Tjstate.JWAITFORSTRINGVALUE
                    elif "0" <= sti <= "9":
                        state = self.Tjstate.JWAITFORINTVALUE
                        ivalue = ord(sti) - 48
                        isign = 1
                    elif sti == "-":
                        state = self.Tjstate.JWAITFORINTVALUE
                        ivalue = 0
                        isign = -1
                    elif sti == "t" or sti == "f" or sti == "T" or sti == "F":
                        svalue = sti.upper()
                        state = self.Tjstate.JWAITFORBOOLVALUE
                    elif sti != " " and sti != "\n":
                        self._ParseError(st, idx.i, "invalid char: was expecting  \",0..9,t or f")

                elif state == self.Tjstate.JWAITFORSTRINGVALUE:
                    if sti == "\"":
                        state = self.Tjstate.JSCOMPLETED
                        res = self._createStrRecord(name, svalue)
                    elif ord(sti) < 32:
                        self._ParseError(st, idx.i, "invalid char: was expecting string value")
                    else:
                        svalue = svalue + sti

                elif state == self.Tjstate.JWAITFORINTVALUE:
                    if "0" <= sti <= "9":
                        ivalue = (ivalue * 10) + ord(sti) - 48
                    else:
                        res = self._createIntRecord(name, isign * ivalue)
                        state = self.Tjstate.JSCOMPLETED
                        idx.i -= 1

                elif state == self.Tjstate.JWAITFORBOOLVALUE:
                    if sti < "A" or sti > "Z":
                        if svalue != "TRUE" and svalue != "FALSE":
                            self._ParseError(st, idx.i, "unexpected value, was expecting \"true\" or \"false\"")
                        if svalue == "TRUE":
                            res = self._createBoolRecord(name, True)
                        else:
                            res = self._createBoolRecord(name, False)
                        state = self.Tjstate.JSCOMPLETED
                        idx.i -= 1
                    else:
                        svalue = svalue + sti.upper()

                elif state == self.Tjstate.JWAITFORNEXTSTRUCTMEMBER:
                    sti = self._Skipgarbage(st, idx)
                    if idx.i < len(st):
                        if sti == "}":
                            idx.i += 1
                            return res
                        else:
                            value = self._ParseEx(self.Tjstate.JWAITFORNAME, "", st, idx)
                            self._add2StructRecord(res, value)
                            sti = self._Skipgarbage(st, idx)
                            if idx.i < len(st):
                                if sti == "}" and idx.i < len(st):
                                    idx.i -= 1
                                elif sti != " " and sti != "\n" and sti != ",":
                                    self._ParseError(st, idx.i, "invalid char: vas expecting , or }")

                elif state == self.Tjstate.JWAITFORNEXTARRAYITEM:
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
                                    idx.i -= 1
                                elif sti != " " and sti != "\n" and sti != ",":
                                    self._ParseError(st, idx.i, "invalid char: vas expecting , or ]")

                elif state == self.Tjstate.JSCOMPLETED:
                    return res

                idx.i += 1

            self._ParseError(st, idx.i, "unexpected end of data")
            return None

        def _DumpStructureRec(self, p, deep):
            indent = ""
            for i in range(0, deep * 2):
                indent += " "
            line = indent + p.name + ":"
            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRING:
                line = line + " str  = " + p.svalue
                print(line)
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_INTEGER:
                line = line + " int  = " + str(p.ivalue)
                print(line)
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_BOOLEAN:
                if p.bvalue:
                    line += " bool = TRUE"
                else:
                    line += " bool = FALSE"
                print(line)
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                print (line + " struct")
                for i in range(0, len(p.members)):
                    self._DumpStructureRec(p.members[i], deep + 1)
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                print(line + " array")
                for i in range(0, len(p.items)):
                    self._DumpStructureRec(p.items[i], deep + 1)

        def _freestructure(self):
            pass

        def DumpStructure(self):
            self._DumpStructureRec(self.data, 0)

        @staticmethod
        def GetNbChild(parent):
            return len(parent.items)

        def GetAllChilds(self, parent):
            res = []
            p = parent
            if p is None:
                p = self.data
            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                for i in range(0, len(p.members)):
                    res.append(self.convertToString(p.members[i], False))
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                for i in range(0, len(p.items)):
                    res.append(self.convertToString(p.items[i], False))
            return res

        def GetChildNode(self, parent, nodename):
            p = parent
            if p is None:
                p = self.data

            if p.recordtype == YAPI.TJSONRECORDTYPE.JSON_STRUCT:
                for i in range(0, len(p.members)):
                    if p.members[i].name == nodename:
                        return p.members[i]
            elif p.recordtype == YAPI.TJSONRECORDTYPE.JSON_ARRAY:
                index = int(nodename)
                if index >= len(p.items):
                    raise YAPI.JsonError("index out of bounds " + nodename + ">=" + str(p.Value.itemcount))
                return p.items[index]

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
    INVALID_UINT = -1
    INVALID_LONG = -9223372036854775807

    # yInitAPI argument
    Y_DETECT_NONE = 0
    Y_DETECT_USB = 1
    Y_DETECT_NET = 2

    Y_DETECT_ALL = Y_DETECT_USB | Y_DETECT_NET

    YOCTO_API_VERSION_STR = "1.10"
    YOCTO_API_VERSION_BCD = 0x0110

    YOCTO_API_BUILD_NO = "14801"
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

    _yApiCLibFile = ""
    _yApiCLibFileFallback = ""
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
        if libpath == '':
            libpath = '.'
        if system == 'Windows':
            if arch == '32bit':
                YAPI._yApiCLibFile = libpath + "\\cdll\\yapi.dll"
            elif arch == '64bit':
                YAPI._yApiCLibFile = libpath + "\\cdll\\yapi64.dll"
            else:
                raise NotImplementedError(
                    "unsupported windows architecture (" + arch + "), contact support@yoctopuce.com.")
        #
        #  LINUX (INTEL + ARM)
        #
        elif system == 'Linux':
            if arch == "armhf":
                YAPI._yApiCLibFile = libpath + "/cdll/libyapi-armhf.so"
            elif arch == "armel":
                YAPI._yApiCLibFile = libpath + "/cdll/libyapi-armel.so"
            elif arch == 'i386':
                YAPI._yApiCLibFile = libpath + "/cdll/libyapi-i386.so"
            elif arch == 'x86_64':
                YAPI._yApiCLibFile = libpath + "/cdll/libyapi-amd64.so"
            else:
                raise NotImplementedError(
                    "unsupported linux architecture (" + arch + "), contact support@yoctopuce.com.")
        #
        #  Mac OS X
        #
        elif system == 'Darwin':
            if arch == 'x86_64':
                YAPI._yApiCLibFile = libpath + "/cdll/libyapi.dylib"
            else:
                raise NotImplementedError(
                    "unsupported Mac OS architecture (" + arch + "), contact support@yoctopuce.com.")
        #
        #  UNKNOWN, contact Yoctopuce support :-)
        #
        else:
            raise NotImplementedError("unsupported platform " + system + ", contact support@yoctopuce.com.")

    @staticmethod
    def yloadYapiCDLL():
        if YAPI._yApiCLibFile == "":
            libpath = os.path.dirname(__file__)
            system = platform.system()
            arch = platform.architecture()[0]
            machine = platform.machine()
            if libpath == '':
                libpath = '.'
                #
            #  WINDOWS
            #
            if system == 'Windows':
                if arch == '32bit':
                    YAPI._yApiCLibFile = libpath + "\\cdll\\yapi.dll"
                elif arch == '64bit':
                    YAPI._yApiCLibFile = libpath + "\\cdll\\yapi64.dll"
                else:
                    raise NotImplementedError(
                        "unsupported windows architecture (" + arch + "), contact support@yoctopuce.com.")
            #
            #  LINUX (INTEL + ARM)
            #
            elif platform.system() == 'Linux':
                if machine.find("arm") >= 0:
                    YAPI._yApiCLibFile = libpath + "/cdll/libyapi-armhf.so"
                    YAPI._yApiCLibFileFallback = libpath + "/cdll/libyapi-armel.so"
                elif machine == 'x86_32' or (machine[0] == 'i' and machine[-2:] == '86'):
                    YAPI._yApiCLibFile = libpath + "/cdll/libyapi-i386.so"
                    YAPI._yApiCLibFileFallback = libpath + "/cdll/libyapi-amd64.so"  # just in case
                elif machine == 'x86_64':
                    YAPI._yApiCLibFile = libpath + "/cdll/libyapi-amd64.so"
                    YAPI._yApiCLibFileFallback = libpath + "/cdll/libyapi-i386.so"  # just in case
                else:
                    raise NotImplementedError(
                        "unsupported linux machine (" + machine + "), contact support@yoctopuce.com.")
            #
            #  Mac OS X
            #
            elif platform.system() == 'Darwin':
                if sys.maxsize > 2 ** 32:
                    YAPI._yApiCLibFile = libpath + "/cdll/libyapi.dylib"
                else:
                    raise NotImplementedError("Only Intel 64 bits installation are supported for Mac OS X.")
            #
            #  UNKNOWN, contact Yoctopuce support :-)
            #
            else:
                raise NotImplementedError("unsupported platform " + system +
                                          ", contact support@yoctopuce.com.")

        if not os.path.exists(YAPI._yApiCLibFile):
            raise ImportError(
                "YAPI shared library is missing (" + YAPI._yApiCLibFile +
                "), make sure it is available and accessible.")

        # try to load main librray
        libloaded = False
        #noinspection PyBroadException
        try:
            YAPI._yApiCLib = ctypes.CDLL(YAPI._yApiCLibFile)
            libloaded = True
        except Exception:
            pass

        # try to load fallback library
        if not libloaded and YAPI._yApiCLibFileFallback != '':
            #noinspection PyBroadException
            try:
                YAPI._yApiCLib = ctypes.CDLL(YAPI._yApiCLibFileFallback)
                libloaded = True
            except Exception:
                ImportError(
                    "Cannot load " + YAPI._yApiCLibFileFallback + " nor " + YAPI._yApiCLibFile +
                    "  make sure it is available and accessible.")

        if not libloaded:
            raise ImportError(
                "Unable to import YAPI shared library (" + YAPI._yApiCLibFile +
                "), make sure it is available and accessible.")

        #  private extern static int _yapiInitAPI(int mode, StringBuilder errmsgRef);
        YAPI._yapiInitAPI = YAPI._yApiCLib.yapiInitAPI
        YAPI._yapiInitAPI.restypes = ctypes.c_int
        YAPI._yapiInitAPI.argtypes = [ctypes.c_int, ctypes.c_char_p]

        #  private extern static void _yapiFreeAPI();
        YAPI._yapiFreeAPI = YAPI._yApiCLib.yapiFreeAPI
        YAPI._yapiFreeAPI.restypes = ctypes.c_int
        YAPI._yapiFreeAPI.argtypes = []

        YAPI._yapiSetTraceFile = YAPI._yApiCLib.yapiSetTraceFile
        YAPI._yapiSetTraceFile.restypes = ctypes.c_int
        YAPI._yapiSetTraceFile.argtypes = [ctypes.c_char_p]

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

        #  private extern static void _yapiRegisterTimedReportCallback(IntPtr fct);
        YAPI._yapiRegisterTimedReportCallback = YAPI._yApiCLib.yapiRegisterTimedReportCallback
        YAPI._yapiRegisterTimedReportCallback.restypes = ctypes.c_int
        YAPI._yapiRegisterTimedReportCallback.argtypes = [ctypes.c_void_p]

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
        YAPI._yapiRegisterHub.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

        #  private extern static int _yapiPreregisterHub(StringBuilder rootUrl, StringBuilder errmsgRef);
        YAPI._yapiPreregisterHub = YAPI._yApiCLib.yapiPreregisterHub
        YAPI._yapiPreregisterHub.restypes = ctypes.c_int
        YAPI._yapiPreregisterHub.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

        #  private extern static void _yapiUnregisterHub(StringBuilder rootUrl);
        YAPI._yapiUnregisterHub = YAPI._yApiCLib.yapiUnregisterHub
        YAPI._yapiUnregisterHub.restypes = ctypes.c_int
        YAPI._yapiUnregisterHub.argtypes = [ctypes.c_char_p]

        #  private extern static int _yapiUpdateDeviceList(uint force, StringBuilder errmsgRef);
        YAPI._yapiUpdateDeviceList = YAPI._yApiCLib.yapiUpdateDeviceList
        YAPI._yapiUpdateDeviceList.restypes = ctypes.c_int
        YAPI._yapiUpdateDeviceList.argtypes = [ctypes.c_uint, ctypes.c_char_p]

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
        YAPI._yapiGetAPIVersion.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

        #  private extern static YDEV_DESCR _yapiGetDevice(StringBuilder device_str, StringBuilder errmsgRef);
        YAPI._yapiGetDevice = YAPI._yApiCLib.yapiGetDevice
        YAPI._yapiGetDevice.restypes = ctypes.c_int
        YAPI._yapiGetDevice.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

        #  private extern static int _yapiGetAllDevices(IntPtr buffer,
        #                                               int maxsize, ref int neededsize,
        #                                               StringBuilder errmsgRef);
        YAPI._yapiGetAllDevices = YAPI._yApiCLib.yapiGetAllDevices
        YAPI._yapiGetAllDevices.restypes = ctypes.c_int
        YAPI._yapiGetAllDevices.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiGetDeviceInfo(YDEV_DESCR d, ref yDeviceSt infos, StringBuilder errmsgRef);
        YAPI._yapiGetDeviceInfo = YAPI._yApiCLib.yapiGetDeviceInfo
        YAPI._yapiGetDeviceInfo.restypes = ctypes.c_int
        YAPI._yapiGetDeviceInfo.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static YFUN_DESCR _yapiGetFunction(StringBuilder class_str,
        #                                                    StringBuilder function_str,
        #                                                    StringBuilder errmsgRef);
        YAPI._yapiGetFunction = YAPI._yApiCLib.yapiGetFunction
        YAPI._yapiGetFunction.restypes = ctypes.c_int
        YAPI._yapiGetFunction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

        #  private extern static int _yapiGetFunctionsByClass(StringBuilder class_str,
        #                                                     YFUN_DESCR precFuncDesc,
        #                                                     IntPtr buffer,
        #                                                     int maxsize,
        #                                                     ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetFunctionsByClass = YAPI._yApiCLib.yapiGetFunctionsByClass
        YAPI._yapiGetFunctionsByClass.restypes = ctypes.c_int
        YAPI._yapiGetFunctionsByClass.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int,
                                                  ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiGetFunctionsByDevice(YDEV_DESCR device, YFUN_DESCR precFuncDesc,
        # IntPtr buffer, int maxsize, ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetFunctionsByDevice = YAPI._yApiCLib.yapiGetFunctionsByDevice
        YAPI._yapiGetFunctionsByDevice.restypes = ctypes.c_int
        YAPI._yapiGetFunctionsByDevice.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int,
                                                   ctypes.c_void_p, ctypes.c_char_p]

        #  internal extern static int _yapiGetFunctionInfo(YFUN_DESCR fundesc, ref YDEV_DESCR devdesc,
        # StringBuilder serial, StringBuilder funcId, StringBuilder funcName, StringBuilder funcVal,
        # StringBuilder errmsgRef);
        YAPI._yapiGetFunctionInfo = YAPI._yApiCLib.yapiGetFunctionInfo
        YAPI._yapiGetFunctionInfo.restypes = ctypes.c_int
        YAPI._yapiGetFunctionInfo.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p,
                                              ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

        #  private extern static int _yapiGetErrorString(int errorcode, StringBuilder buffer,
        # int maxsize, StringBuilder errmsgRef);
        #YAPI._yapiGetErrorString = YAPI._yApiCLib.yapiGetErrorString
        #YAPI._yapiGetErrorString.restypes = ctypes.c_int
        #YAPI._yapiGetErrorString.argtypes = [ctypes.c_int , ctypes.c_char_p , ctypes.c_int , ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestSyncStart(YIOHDL *iohdl, const char *device,
        # const char *request, char **reply, int *replysize, char *errmsg);
        YAPI._yapiHTTPRequestSyncStart = YAPI._yApiCLib.yapiHTTPRequestSyncStart
        YAPI._yapiHTTPRequestSyncStart.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestSyncStart.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p,
                                                   POINTER(POINTER(ctypes.c_ubyte)), ctypes.c_void_p, ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestSyncStartEx(YIOHDL *iohdl, const char *device,
        # const char *request, int requestsize, char **reply, int *replysize, char *errmsg);
        YAPI._yapiHTTPRequestSyncStartEx = YAPI._yApiCLib.yapiHTTPRequestSyncStartEx
        YAPI._yapiHTTPRequestSyncStartEx.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestSyncStartEx.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
                                                     POINTER(POINTER(ctypes.c_ubyte)), ctypes.c_void_p, ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestSyncDone(YIOHDL *iohdl, char *errmsg);
        YAPI._yapiHTTPRequestSyncDone = YAPI._yApiCLib.yapiHTTPRequestSyncDone
        YAPI._yapiHTTPRequestSyncDone.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestSyncDone.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        #YRETCODE YAPI_FUNCTION_EXPORT yapiHTTPRequestAsync(const char *device, const char *request,
        # yapiRequestAsyncCallback callback, void *context, char *errmsg);
        YAPI._yapiHTTPRequestAsync = YAPI._yApiCLib.yapiHTTPRequestAsync
        YAPI._yapiHTTPRequestAsync.restypes = ctypes.c_int
        YAPI._yapiHTTPRequestAsync.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p,
                                               ctypes.c_char_p]

        #  private extern static int _yapiHTTPRequest(StringBuilder device, StringBuilder url,
        # StringBuilder buffer, int buffsize, ref int fullsize, StringBuilder errmsgRef);
        YAPI._yapiHTTPRequest = YAPI._yApiCLib.yapiHTTPRequest
        YAPI._yapiHTTPRequest.restypes = ctypes.c_int
        YAPI._yapiHTTPRequest.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
                                          ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiGetBootloadersDevs(StringBuilder serials, u32 maxNbSerial,
        # ref u32 totalBootladers, StringBuilder errmsgRef);
        YAPI._yapiGetBootloadersDevs = YAPI._yApiCLib.yapiGetBootloadersDevs
        YAPI._yapiGetBootloadersDevs.restypes = ctypes.c_int
        YAPI._yapiGetBootloadersDevs.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiFlashDevice(ref yFlashArg args, StringBuilder errmsgRef);
        YAPI._yapiFlashDevice = YAPI._yApiCLib.yapiFlashDevice
        YAPI._yapiFlashDevice.restypes = ctypes.c_int
        YAPI._yapiFlashDevice.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiVerifyDevice(ref yFlashArg args, StringBuilder errmsgRef);
        YAPI._yapiVerifyDevice = YAPI._yApiCLib.yapiVerifyDevice
        YAPI._yapiVerifyDevice.restypes = ctypes.c_int
        YAPI._yapiVerifyDevice.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiGetDevicePath(int devdesc, StringBuilder rootdevice, StringBuilder path,
        # int pathsize, ref int neededsize, StringBuilder errmsgRef);
        YAPI._yapiGetDevicePath = YAPI._yApiCLib.yapiGetDevicePath
        YAPI._yapiGetDevicePath.restypes = ctypes.c_int
        YAPI._yapiGetDevicePath.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
                                            ctypes.c_void_p, ctypes.c_char_p]

        #  private extern static int _yapiSleep(int duration_ms, StringBuilder errmsgRef);
        YAPI._yapiSleep = YAPI._yApiCLib.yapiSleep
        YAPI._yapiSleep.restypes = ctypes.c_int
        YAPI._yapiSleep.argtypes = [ctypes.c_int, ctypes.c_char_p]
        YAPI._ydllLoaded = True

        YAPI._yapiRegisterHubDiscoveryCallback = YAPI._yApiCLib.yapiRegisterHubDiscoveryCallback
        YAPI._yapiRegisterHubDiscoveryCallback.restypes = ctypes.c_int
        YAPI._yapiRegisterHubDiscoveryCallback.argtypes = [ctypes.c_void_p]

        YAPI._yapiTriggerHubDiscovery = YAPI._yApiCLib.yapiTriggerHubDiscovery
        YAPI._yapiTriggerHubDiscovery.restypes = ctypes.c_int
        YAPI._yapiTriggerHubDiscovery.argtypes = [ctypes.c_char_p]
        YAPI._ydllLoaded = True

    #noinspection PyUnresolvedReferences
    class yDeviceSt(ctypes.Structure):
        _pack_ = 1
        #noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,
        # PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker,PyTypeChecker
        _fields_ = [("vendorid", ctypes.c_uint16),
                    ("deviceid", ctypes.c_uint16),
                    ("devrelease", ctypes.c_uint16),
                    ("nbinbterfaces", ctypes.c_uint16),
                    ("manufacturer", ctypes.c_char * 20),   # YAPI.YOCTO_MANUFACTURER_LEN),
                    ("productname", ctypes.c_char * 28),    # YAPI.YOCTO_PRODUCTNAME_LEN),
                    ("serial", ctypes.c_char * 20),         # YAPI.YAPI.YOCTO_SERIAL_LEN),
                    ("logicalname", ctypes.c_char * 20),    # YAPI.YOCTO_LOGICAL_LEN),
                    ("firmware", ctypes.c_char * 22),       # YAPI.YOCTO_FIRMWARE_LEN),
                    ("beacon", ctypes.c_int8)]

    #noinspection PyUnresolvedReferences
    class YIOHDL(ctypes.Structure):
        _pack_ = 1
        _fields_ = [("raw", ctypes.c_byte)]

    #noinspection PyClassHasNoInit
    class yDEVICE_PROP:
        PROP_VENDORID, PROP_DEVICEID, PROP_DEVRELEASE, PROP_FIRMWARELEVEL, PROP_MANUFACTURER, PROP_PRODUCTNAME, \
            PROP_SERIAL, PROP_LOGICALNAME, PROP_URL = range(9)

    #noinspection PyClassHasNoInit
    class yFACE_STATUS:
        YFACE_EMPTY, YFACE_RUNNING, YFACE_ERROR = range(3)

    class _Event:
        ARRIVAL, REMOVAL, CHANGE, FUN_VALUE, FUN_TIMEDREPORT, \
            HUB_DISCOVERY, YAPI_NOP = range(7)

        def __init__(self):
            self.ev = self.YAPI_NOP
            self.module = None
            self.fun_descr = 0
            self.value = ""
            self.timestamp = 0.0
            self.report = None
            self.serial = None
            self.url = None

        def setArrival(self, module):
            self.ev = self.ARRIVAL
            self.module = module

        def setRemoval(self, module):
            self.ev = self.REMOVAL
            self.module = module

        def setChange(self, module):
            self.ev = self.CHANGE
            self.module = module

        def setFunVal(self, fun_descr, value):
            self.ev = self.FUN_VALUE
            self.fun_descr = fun_descr
            self.value = value

        def setTimedReport(self, fun_descr, timestamp, report):
            self.ev = self.FUN_TIMEDREPORT
            self.fun_descr = fun_descr
            self.timestamp = timestamp
            self.report = report

        def setHubDiscovery(self, serial, url):
            self.ev = self.HUB_DISCOVERY
            self.serial = serial
            self.url = url

        def invokePlug(self):
            global yArrivalFct
            global yRemovalFct
            global yChangeFct
            global yHubDiscoveryCallback
            if self.ev == self.ARRIVAL:
                if yArrivalFct is not None:
                #noinspection PyCallingNonCallable
                    yArrivalFct(self.module)
            elif self.ev == self.REMOVAL:
                if yRemovalFct is not None:
                    #noinspection PyCallingNonCallable
                    yRemovalFct(self.module)
            elif self.ev == self.CHANGE:
                if yChangeFct is not None:
                    #noinspection PyCallingNonCallable
                    yChangeFct(self.module)
            elif self.ev == self.HUB_DISCOVERY:
                if yHubDiscoveryCallback is not None:
                    yHubDiscoveryCallback(self.serial, self.url)

        # noinspection PyProtectedMember
        def invokeData(self):
            if self.ev == self.FUN_VALUE:
                for i in range(len(YFunction._FunctionCallbacks)):
                    if YFunction._FunctionCallbacks[i].get_functionDescriptor() == self.fun_descr:
                        YFunction._FunctionCallbacks[i]._invokeValueCallback(self.value)
            elif self.ev == self.FUN_TIMEDREPORT:
                for i in range(len(YFunction._TimedReportCallbackList)):
                    if YFunction._TimedReportCallbackList[i].get_functionDescriptor() == self.fun_descr:
                        sensor = YFunction._TimedReportCallbackList[i]
                        sensor._invokeTimedReportCallback(sensor._decodeTimedReport(self.timestamp, self.report))

    ##--- (generated code: YFunction return codes)
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

    #--- (end of generated code: YFunction return codes)

    class YAPI_Exception(Exception):
        pass

    YDevice_devCache = []

    # - Types used for internal yapi callbacks
    _yapiLogFunc = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int)

    _yapiDeviceUpdateFunc = ctypes.CFUNCTYPE(None, ctypes.c_int)

    _yapiFunctionUpdateFunc = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p)

    _yapiTimedReportFunc = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_double, POINTER(c_ubyte), ctypes.c_int)

    _yapiHubDiscoveryCallback = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_char_p)

    @staticmethod
    def YISERR(retcode):
        if retcode < 0:
            return True
        return False

    #noinspection PyClassHasNoInit
    class blockingCallbackCtx:
        res = 0
        response = ""
        errmsgRef = ""

    #noinspection PyUnusedLocal
    @staticmethod
    def YblockingCallback(device, context, returnval, result, errmsgRef):
        context.res = returnval
        context.response = result
        context.errmsgRef = errmsgRef

    @staticmethod
    def GetTickCount():
        """
        Returns the current value of a monotone millisecond-based time counter.
        This counter can be used to compute delays in relation with
        Yoctopuce devices, which also uses the millisecond as timebase.
        
        @return a long integer corresponding to the millisecond counter.
        """
        #### for python, since some implementations don't support 64bits integers
        #### GetTickCount returns a datetime object instead of a u64
        #noinspection PyUnresolvedReferences
        return datetime.datetime.today()

    @staticmethod
    def SetTraceFile(filename):
        fname = ctypes.create_string_buffer(filename.encode("ASCII"))
        #noinspection PyUnresolvedReferences
        YAPI._yapiSetTraceFile(fname)

    #noinspection PyUnresolvedReferences
    @staticmethod
    def Sleep(ms_duration, errmsgRef=None):
        """
        Pauses the execution flow for a specified duration.
        This function implements a passive waiting loop, meaning that it does not
        consume CPU cycles significantly. The processor is left available for
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
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        if type(ms_duration) == type(int()):
            ms_duration = datetime.timedelta(milliseconds=ms_duration)
        timeout = YAPI.GetTickCount() + ms_duration
        res = YAPI.SUCCESS

        ok = True
        while ok:
            res = YAPI.HandleEvents(errmsgRef)
            if YAPI.YISERR(res):
                return res

            if YAPI.GetTickCount() < timeout:
                #noinspection PyUnresolvedReferences
                res = YAPI._yapiSleep(1, errBuffer)
                if YAPI.YISERR(res):
                    if not errmsgRef is None:
                        errmsgRef.value = YByte2String(errBuffer.value)
                    return res
            ok = YAPI.GetTickCount() < timeout
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errBuffer.value)
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
    def yapiLockFunctionCallBack(errmsgRef=None):
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiLockFunctionCallBack(errBuffer)
        if errmsgRef is not None:
            #noinspection PyAttributeOutsideInit
            errmsgRef.value = YByte2String(errBuffer.value)
        return res

    @staticmethod
    def yapiUnlockFunctionCallBack(errmsgRef=None):
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUnlockFunctionCallBack(errBuffer)
        if not errmsgRef is None:
            #noinspection PyAttributeOutsideInit
            errmsgRef.value = YByte2String(errBuffer.value)
        return res

    @staticmethod
    def _getCalibrationHandler(calType):
        key = str(calType)
        if key in YAPI._CalibHandlers:
            return YAPI._CalibHandlers[key]
        return None

    @staticmethod
    def _setArrayLength(a, length):
        if len(a) > length:
            del a[length:]
        while len(a) < length:
            a.append(0)

    decExp = [1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1, 1.0, 1.0e1, 1.0e2, 1.0e3, 1.0e4, 1.0e5, 1.0e6, 1.0e7,
              1.0e8, 1.0e9]

    # Convert Yoctopuce 16-bit decimal floats to standard double-precision floats

    @staticmethod
    def _decimalToDouble(val):
        negate = False
        if not val:
            return 0.0
        if val > 32767:
            negate = True
            val = 65536 - val
        elif val < 0:
            negate = True
            val = -val
        exp = val >> 11
        res = (val & 2047) * YAPI.decExp[exp]
        if negate:
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
            decpow += 1
        mant = val / YAPI.decExp[decpow]
        if decpow == 15 and mant > 2047.0:
            res = (15 << 11) + 2047  # overflow
        else:
            res = (decpow << 11) + round(mant)
        if negate:
            return -res
        else:
            return res

    @staticmethod
    def _decodeWords(sdat):
        p = 0
        udat = []
        while p < len(sdat):
            c = sdat[p]
            p += 1
            if c == '*':
                val = 0
            elif c == 'X':
                val = 0xffff
            elif c == 'Y':
                val = 0x7fff
            elif c >= 'a':
                srcpos = int(len(udat) - 1 - (ord(c) - ord('a')))
                if srcpos < 0:
                    val = 0
                else:
                    val = udat[srcpos]
            else:
                if p + 2 > len(sdat):
                    return udat
                val = (ord(c) - ord('0'))
                c = sdat[p]
                p += 1
                val += (ord(c) - ord('0')) << 5
                c = sdat[p]
                p += 1
                if c == 'z':
                    c = "\\"
                val += (ord(c) - ord('0')) << 10
            udat.append(val)
        return udat

    #noinspection PyUnresolvedReferences
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
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)

        #noinspection PyUnresolvedReferences
        res = YAPI._yapiHandleEvents(errBuffer)
        if YAPI.YISERR(res):
            if errmsgRef is not None:
                #noinspection PyAttributeOutsideInit
                errmsgRef.value = YByte2String(errBuffer.value)
            return res

        while len(YAPI._DataEvents) > 0:
            YAPI.yapiLockFunctionCallBack(errmsgRef)
            if not (len(YAPI._DataEvents)):
                YAPI.yapiUnlockFunctionCallBack(errmsgRef)
                break

            ev = YAPI._DataEvents.pop(0)
            YAPI.yapiUnlockFunctionCallBack(errmsgRef)
            ev.invokeData()
        return YAPI.SUCCESS

    @staticmethod
    def yapiUpdateDeviceList(force, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUpdateDeviceList(force, errmsg_buffer)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def apiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer, maxsize, neededsizeRef, errmsgRef):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        neededsize = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer,
                                             maxsize, ctypes.byref(neededsize), errmsg_buffer)
        neededsizeRef.value = neededsize.value
        if not errmsgRef is None:
            errmsgRef.value = YByte2String(errmsg_buffer.value)
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
    def native_yLogFunction(log, loglen):

        global yLogFct
        if yLogFct is not None:
            #noinspection PyCallingNonCallable
            yLogFct(YByte2String(log))
        return 0

    @staticmethod
    def RegisterLogFunction(logfun):
        """
        Registers a log callback function. This callback will be called each time
        the API have something to say. Quite useful to debug the API.
        
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
        infos.logicalname = "".encode("ASCII")
        infos.firmware = "".encode("ASCII")
        infos.beacon = 0
        return infos

    @staticmethod
    def yapiGetDeviceInfo(d, infos, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetDeviceInfo(d, ctypes.byref(infos), errmsg_buffer)
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def native_yDeviceArrivalCallback(d):
        infos = YAPI.emptyDeviceSt()
        errmsgRef = YRefParam()
        if YAPI.yapiGetDeviceInfo(d, infos, errmsgRef) != YAPI.SUCCESS:
            return
        modul = YModule.FindModule(YByte2String(infos.serial) + ".module")
        modul.setImmutableAttributes(infos)
        ev = YAPI._Event()
        ev.setArrival(modul)
        if yArrivalFct is not None:
            YAPI._PlugEvents.append(ev)

    @staticmethod
    def native_HubDiscoveryCallback(serial_ptr, url_ptr):
        serial = YByte2String(serial_ptr)
        url = YByte2String(url_ptr)
        ev = YAPI._Event()
        ev.setHubDiscovery(serial, url)
        YAPI._PlugEvents.append(ev)

    @staticmethod
    def yapiLockDeviceCallBack(errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiLockDeviceCallBack(errmsg_buffer)
        if errmsgRef is not None:
            #noinspection PyAttributeOutsideInit
            errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def yapiUnlockDeviceCallBack(errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUnlockDeviceCallBack(errmsg_buffer)
        if errmsgRef is not None:
            #noinspection PyAttributeOutsideInit
            errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def RegisterDeviceArrivalCallback(arrivalCallback):
        """
        Register a callback function, to be called each time
        a device is plugged. This callback will be invoked while yUpdateDeviceList
        is running. You will have to call this function on a regular basis.
        
        @param arrivalCallback : a procedure taking a YModule parameter, or None
                to unregister a previously registered  callback.
        """
        global yArrivalFct
        yArrivalFct = arrivalCallback
        if arrivalCallback is not None:
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
    def RegisterDeviceRemovalCallback(removalCallback):
        """
        Register a callback function, to be called each time
        a device is unplugged. This callback will be invoked while yUpdateDeviceList
        is running. You will have to call this function on a regular basis.
        
        @param removalCallback : a procedure taking a YModule parameter, or None
                to unregister a previously registered  callback.
        """
        global yRemovalFct
        yRemovalFct = removalCallback

    @staticmethod
    def RegisterHubDiscoveryCallback(hubDiscoveryCallback):
        """
        Register a callback function, to be called each time an Network Hub send
        an SSDP message. The callback has two string parameter, the first one
        contain the serial number of the hub and the second contain the URL of the
        network hub (this URL can be passed to RegisterHub). This callback will be invoked
        while yUpdateDeviceList is running. You will have to call this function on a regular basis.
        
        @param hubDiscoveryCallback : a procedure taking two string parameter, or None
                to unregister a previously registered  callback.
        """
        global yHubDiscoveryCallback
        yHubDiscoveryCallback = hubDiscoveryCallback
        errmsgRef = YRefParam()
        YAPI.TriggerHubDiscovery(errmsgRef)
        return 0

    #noinspection PyUnresolvedReferences
    @staticmethod
    def native_yDeviceChangeCallback(d):
        global yChangeFct
        infos = YAPI.emptyDeviceSt()
        errmsgRef = YRefParam()
        if yChangeFct is None:
            return
        if YAPI.yapiGetDeviceInfo(d, infos, errmsgRef) != YAPI.SUCCESS:
            return
        modul = YModule.FindModule(YByte2String(infos.serial) + ".module")
        ev = YAPI._Event()
        ev.setChange(modul)
        YAPI._PlugEvents.append(ev)
        return 0

    @staticmethod
    def RegisterDeviceChangeCallback(callback):
        global yChangeFct
        yChangeFct = callback

    @staticmethod
    def queuesCleanUp():
        del YAPI._PlugEvents[:]
        del YAPI._DataEvents[:]

    @staticmethod
    def native_yFunctionUpdateCallback(f, data):
        if data is None:
            return
        ev = YAPI._Event()
        ev.setFunVal(f, YByte2String(data))
        YAPI._DataEvents.append(ev)
        return 0

    @staticmethod
    def native_yTimedReportCallback(f, timestamp, data, dataLen):
        report = YString2Byte("")
        for i in range(dataLen):
            report = YAddByte(report, data[i])
        ev = YAPI._Event()
        ev.setTimedReport(f, timestamp, report)
        YAPI._DataEvents.append(ev)
        return 0

    @staticmethod
    def RegisterCalibrationHandler(calibType, callback):
        key = str(calibType)
        YAPI._CalibHandlers[key] = callback

    #noinspection PyUnusedLocal
    @staticmethod
    def LinearCalibrationHandler(rawValue, calibType, params, rawValues, refValues):
        npt = calibType % 10
        x = rawValues[0]
        adj = refValues[0] - x
        i = 0
        if npt > len(rawValues) + 1:
            npt = len(rawValues) + 1
        if npt > len(refValues) + 1:
            npt = len(refValues) + 1
        while rawValue > rawValues[i] and i + 1 < npt:
            i += 1
            x2 = x
            adj2 = adj
            x = rawValues[i]
            adj = refValues[i] - x
            if rawValue < x and x > x2:
                adj = adj2 + (adj - adj2) * (rawValue - x2) / (x - x2)
        return rawValue + adj

    #noinspection PyUnresolvedReferences
    @staticmethod
    def native_yDeviceRemovalCallback(d):
        global yRemovalFct
        infos = YAPI.emptyDeviceSt()
        errmsgRef = YRefParam()
        if yRemovalFct is None:
            return
        infos.deviceid = 0
        if YAPI.yapiGetDeviceInfo(d, infos, errmsgRef) != YAPI.SUCCESS:
            return
        modul = YModule.FindModule(YByte2String(infos.serial) + ".module")
        ev = YAPI._Event()
        ev.setRemoval(modul)
        YAPI._PlugEvents.append(ev)
        return 0

    @staticmethod
    def apiGetAPIVersion(versionRef, dateRef):
        pversion = YAPI.YPCHAR()
        pdate = YAPI.YPCHAR()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetAPIVersion(ctypes.byref(pversion), ctypes.byref(pdate))
        #noinspection PyAttributeOutsideInit
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
        if not YAPI._ydllLoaded:
            YAPI.yloadYapiCDLL()
        YAPI.apiGetAPIVersion(version, date)
        #noinspection PyTypeChecker
        return YAPI.YOCTO_API_VERSION_STR + "." + YAPI.YOCTO_API_BUILD_NO + " (" + version.value + ")"

    @staticmethod
    def InitAPI(mode, errmsg=None):
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
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        if YAPI._apiInitialized:
            return YAPI.SUCCESS
            #load yapi functions form dynamic library
        if not YAPI._ydllLoaded:
            YAPI.yloadYapiCDLL()
        version = YRefParam()
        date = YRefParam()
        if YAPI.apiGetAPIVersion(version, date) != YAPI.YOCTO_API_VERSION_BCD:
            if errmsg is not None:
                errmsg.value \
                    = YAPI._yApiCLibFile + " does does not match the version of the Libary (Libary=" + \
                    YAPI.YOCTO_API_VERSION_STR + "." + YAPI.YOCTO_API_BUILD_NO
                #noinspection PyTypeChecker
                errmsg.value += " yapi.dll=" + version.value + ")"
                return YAPI.VERSION_MISMATCH

        YAPI.pymodule_initialization()

        #noinspection PyUnresolvedReferences
        res = YAPI._yapiInitAPI(mode, errmsg_buffer)
        if errmsg is not None:
            errmsg.value = YByte2String(errmsg_buffer.value)
        if YAPI.YISERR(res):
            return res

        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterDeviceArrivalCallback(native_yDeviceArrivalAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterDeviceRemovalCallback(native_yDeviceRemovalAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterDeviceChangeCallback(native_yDeviceChangeAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterFunctionUpdateCallback(native_yFunctionUpdateAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterTimedReportCallback(native_yTimedReportAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterLogFunction(native_yLogFunctionAnchor)
        #noinspection PyUnresolvedReferences
        YAPI._yapiRegisterHubDiscoveryCallback(native_yHubDiscoveryAnchor)

        for i in range(21):
            YAPI.RegisterCalibrationHandler(i, YAPI.LinearCalibrationHandler)
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
            YFunction._ClearCache()
            YAPI._apiInitialized = False

    @staticmethod
    def RegisterHub(url, errmsg=None):
        """
        Setup the Yoctopuce library to use modules connected on a given machine. The
        parameter will determine how the API will work. Use the following values:
        
        <b>usb</b>: When the usb keyword is used, the API will work with
        devices connected directly to the USB bus. Some programming languages such a Javascript,
        PHP, and Java don't provide direct access to USB hardware, so usb will
        not work with these. In this case, use a VirtualHub or a networked YoctoHub (see below).
        
        <b><i>x.x.x.x</i></b> or <b><i>hostname</i></b>: The API will use the devices connected to the
        host with the given IP address or hostname. That host can be a regular computer
        running a VirtualHub, or a networked YoctoHub such as YoctoHub-Ethernet or
        YoctoHub-Wireless. If you want to use the VirtualHub running on you local
        computer, use the IP address 127.0.0.1.
        
        <b>callback</b>: that keyword make the API run in "<i>HTTP Callback</i>" mode.
        This a special mode allowing to take control of Yoctopuce devices
        through a NAT filter when using a VirtualHub or a networked YoctoHub. You only
        need to configure your hub to call your server script on a regular basis.
        This mode is currently available for PHP and Node.JS only.
        
        Be aware that only one application can use direct USB access at a
        given time on a machine. Multiple access would cause conflicts
        while trying to access the USB modules. In particular, this means
        that you must stop the VirtualHub software before starting
        an application that uses direct USB access. The workaround
        for this limitation is to setup the library to use the VirtualHub
        rather than direct USB access.
        
        If access control has been activated on the hub, virtual or not, you want to
        reach, the URL parameter should look like:
        
        http://username:password@adresse:port
        
        You can call <i>RegisterHub</i> several times to connect to several machines.
        
        @param url : a string containing either "usb","callback" or the
                root URL of the hub to monitor
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN + 1)
        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsg)
            if YAPI.YISERR(res):
                return res
        p = ctypes.create_string_buffer(url.encode("ASCII"))
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiRegisterHub(p, errmsg_buffer)
        if YAPI.YISERR(res):
            if errmsg is not None:
                errmsg.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def PreregisterHub(url, errmsgRef=None):
        """
        Fault-tolerant alternative to RegisterHub(). This function has the same
        purpose and same arguments as RegisterHub(), but does not trigger
        an error when the selected hub is not available at the time of the function call.
        This makes it possible to register a network hub independently of the current
        connectivity, and to try to contact it only when a device is actively needed.
        
        @param url : a string containing either "usb","callback" or the
                root URL of the hub to monitor
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)

        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsgRef)
            if YAPI.YISERR(res):
                return res
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiPreregisterHub(ctypes.create_string_buffer(url.encode("ASCII")), errmsg_buffer)
        if YAPI.YISERR(res):
            if errmsgRef is not None:
                errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def UnregisterHub(url):
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
    def UpdateDeviceList(errmsg=None):
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
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsg)
            if YAPI.YISERR(res):
                return res
        res = YAPI.yapiUpdateDeviceList(0, errmsg)
        if YAPI.YISERR(res):
            return res
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiHandleEvents(errmsg_buffer)
        if YAPI.YISERR(res):
            if errmsg is not None:
                #noinspection PyAttributeOutsideInit
                errmsg.value = YByte2String(errmsg_buffer.value)
            return res
        while len(YAPI._PlugEvents) > 0:
            YAPI.yapiLockDeviceCallBack(errmsg)
            p = YAPI._PlugEvents.pop(0)
            YAPI.yapiUnlockDeviceCallBack(errmsg)
            p.invokePlug()
        return YAPI.SUCCESS

    @staticmethod
    def TriggerHubDiscovery(errmsg=None):
        """
        Force a hub discovery, if a callback as been registered with yRegisterDeviceRemovalCallback it
        will be called for each net work hub that will respond to the discovery
        
        @param errmsg : a string passed by reference to receive any error message.
        
        @return YAPI.SUCCESS when the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN + 1)
        if not YAPI._apiInitialized:
            res = YAPI.InitAPI(0, errmsg)
            if YAPI.YISERR(res):
                return res
        res = YAPI._yapiTriggerHubDiscovery(errmsg_buffer)
        if YAPI.YISERR(res):
            if errmsg is not None:
                errmsg.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def yapiGetFunctionInfo(fundesc, devdescRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef=None):
        serialBuffer = ctypes.create_string_buffer(YAPI.YOCTO_SERIAL_LEN)
        funcIdBuffer = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcNameBuffer = ctypes.create_string_buffer(YAPI.YOCTO_LOGICAL_LEN)
        funcValBuffer = ctypes.create_string_buffer(YAPI.YOCTO_PUBVAL_LEN)
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        p = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundesc, ctypes.byref(p), serialBuffer, funcIdBuffer, funcNameBuffer,
                                        funcValBuffer, errBuffer)
        devdescRef.value = p.value
        serialRef.value = YByte2String(serialBuffer.value)
        funcIdRef.value = YByte2String(funcIdBuffer.value)
        funcNameRef.value = YByte2String(funcNameBuffer.value)
        funcValRef.value = YByte2String(funcValBuffer.value)
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errBuffer.value)
        return res

    @staticmethod
    def yapiGetDeviceByFunction(fundesc, errmsgRef=None):
        errBuffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundesc, ctypes.byref(devdesc), None, None, None, None, errBuffer)
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errBuffer.value)
        if res < 0:
            return res
        return devdesc.value

    @staticmethod
    def yapiUpdateDeviceList(force, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiUpdateDeviceList(force, errmsg_buffer)
        if YAPI.YISERR(res):
            if errmsgRef is not None:
                errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def yapiGetDevice(device_str, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        p = ctypes.create_string_buffer(device_str.encode("ASCII"))
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetDevice(p, errmsg_buffer)
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def yapiGetFunction(class_str, function_str, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunction(ctypes.create_string_buffer(class_str.encode("ASCII")),
                                    ctypes.create_string_buffer(function_str.encode("ASCII")), errmsg_buffer)
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def apiGetFunctionsByClass(class_str, precFuncDesc, dbuffer, maxsize, neededsizeRef, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        cneededsize = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionsByClass(ctypes.create_string_buffer(class_str.encode("ASCII")), precFuncDesc,
                                            dbuffer, maxsize, ctypes.byref(cneededsize), errmsg_buffer)
        #noinspection PyUnresolvedReferences
        neededsizeRef.value = cneededsize.value
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errmsg_buffer.value)
        return res

    @staticmethod
    def apiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer, maxsize, neededsizeRef, errmsgRef=None):
        errmsg_buffer = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        cneededsize = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionsByDevice(devdesc, precFuncDesc, dbuffer, maxsize, ctypes.byref(cneededsize),
                                             errmsg_buffer)
        #noinspection PyUnresolvedReferences
        neededsizeRef.value = cneededsize.value
        if errmsgRef is not None:
            errmsgRef.value = YByte2String(errmsg_buffer.value)
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


#--- (generated code: YDataStream class start)
#noinspection PyProtectedMember
class YDataStream(object):
    """
    YDataStream objects represent bare recorded measure sequences,
    exactly as found within the data logger present on Yoctopuce
    sensors.
    
    In most cases, it is not necessary to use YDataStream objects
    directly, as the YDataSet objects (returned by the
    get_recordedData() method from sensors and the
    get_dataSets() method from the data logger) provide
    a more convenient interface.
    
    """
#--- (end of generated code: YDataStream class start)
    #--- (generated code: YDataStream definitions)
    #--- (end of generated code: YDataStream definitions)

    DATA_INVALID = YAPI.INVALID_DOUBLE
    DURATION_INVALID = -1

    def __init__(self, parent, dataset=None, encoded=None):
        #--- (generated code: YDataStream attributes)
        self._parent = None
        self._runNo = 0
        self._utcStamp = 0
        self._nCols = 0
        self._nRows = 0
        self._duration = 0
        self._columnNames = []
        self._functionId = ''
        self._isClosed = 0
        self._isAvg = 0
        self._isScal = 0
        self._decimals = 0
        self._offset = 0
        self._scale = 0
        self._samplesPerHour = 0
        self._minVal = 0
        self._avgVal = 0
        self._maxVal = 0
        self._decexp = 0
        self._caltyp = 0
        self._calpar = []
        self._calraw = []
        self._calref = []
        self._values = []
        #--- (end of generated code: YDataStream attributes)
        self._calhdl = None
        self._parent = parent
        if dataset is not None:
            self._initFromDataSet(dataset, encoded)

    #--- (generated code: YDataStream implementation)
    def _initFromDataSet(self, dataset, encoded):
        # val
        # i
        # iRaw
        # iRef
        # fRaw
        # fRef
        # duration_float
        iCalib = []
        
        # // decode sequence header to extract data
        self._runNo = encoded[0] + (((encoded[1]) << (16)))
        self._utcStamp = encoded[2] + (((encoded[3]) << (16)))
        val = encoded[4]
        self._isAvg = (((val) & (0x100)) == 0)
        self._samplesPerHour = ((val) & (0xff))
        if ((val) & (0x100)) != 0:
            self._samplesPerHour = self._samplesPerHour * 3600
        else:
            if ((val) & (0x200)) != 0:
                self._samplesPerHour = self._samplesPerHour * 60
        
        val = encoded[5]
        if val > 32767:
            val = val - 65536
        self._decimals = val
        self._offset = val
        self._scale = encoded[6]
        self._isScal = (self._scale != 0)
        
        val = encoded[7]
        self._isClosed = (val != 0xffff)
        if val == 0xffff:
            val = 0
        self._nRows = val
        duration_float = self._nRows * 3600 / self._samplesPerHour
        self._duration = round(duration_float)
        # // precompute decoding parameters
        self._decexp = 1.0
        if self._scale == 0:
            i = 0
            while i < self._decimals:
                self._decexp = self._decexp * 10.0
                i = i + 1
        iCalib = dataset.get_calibration()
        self._caltyp = iCalib[0]
        if self._caltyp != 0:
            self._calhdl = YAPI._getCalibrationHandler(self._caltyp)
            del self._calpar[:]
            del self._calraw[:]
            del self._calref[:]
            i = 1
            while i + 1 < len(iCalib):
                iRaw = iCalib[i]
                iRef = iCalib[i + 1]
                self._calpar.append(iRaw)
                self._calpar.append(iRef)
                if self._isScal:
                    fRaw = iRaw
                    fRaw = (fRaw - self._offset) / self._scale
                    fRef = iRef
                    fRef = (fRef - self._offset) / self._scale
                    self._calraw.append(fRaw)
                    self._calref.append(fRef)
                else:
                    self._calraw.append(YAPI._decimalToDouble(iRaw))
                    self._calref.append(YAPI._decimalToDouble(iRef))
                i = i + 2
        # // preload column names for backward-compatibility
        self._functionId = dataset.get_functionId()
        if self._isAvg:
            del self._columnNames[:]
            self._columnNames.append("" + self._functionId + "_min")
            self._columnNames.append("" + self._functionId + "_avg")
            self._columnNames.append("" + self._functionId + "_max")
            self._nCols = 3
        else:
            del self._columnNames[:]
            self._columnNames.append(self._functionId)
            self._nCols = 1
        # // decode min/avg/max values for the sequence
        if self._nRows > 0:
            self._minVal = self._decodeVal(encoded[8])
            self._maxVal = self._decodeVal(encoded[9])
            self._avgVal = self._decodeAvg(encoded[10] + (((encoded[11]) << (16))), self._nRows)
        return 0

    def parse(self, sdata):
        # idx
        udat = []
        dat = []
        # // may throw an exception
        udat = YAPI._decodeWords(self._parent._json_get_string(sdata))
        del self._values[:]
        idx = 0
        if self._isAvg:
            while idx + 3 < len(udat):
                del dat[:]
                dat.append(self._decodeVal(udat[idx]))
                dat.append(self._decodeAvg(udat[idx + 2] + (((udat[idx + 3]) << (16))), 1))
                dat.append(self._decodeVal(udat[idx + 1]))
                self._values.append(dat[:])
                idx = idx + 4
        else:
            if self._isScal:
                while idx < len(udat):
                    del dat[:]
                    dat.append(self._decodeVal(udat[idx]))
                    self._values.append(dat[:])
                    idx = idx + 1
            else:
                while idx + 1 < len(udat):
                    del dat[:]
                    dat.append(self._decodeAvg(udat[idx] + (((udat[idx + 1]) << (16))), 1))
                    self._values.append(dat[:])
                    idx = idx + 2
        
        self._nRows = len(self._values)
        return YAPI.SUCCESS

    def get_url(self):
        # url
        url = "logger.json?id=" + self._functionId + "&run=" + str(int(self._runNo)) + "&utc=" + str(int(self._utcStamp))
        return url

    def loadStream(self):
        # // may throw an exception
        return self.parse(self._parent._download(self.get_url()))

    def _decodeVal(self, w):
        # val
        val = w
        if self._isScal:
            val = (val - self._offset) / self._scale
        else:
            val = YAPI._decimalToDouble(w)
        if self._caltyp != 0:
            val = self._calhdl(val, self._caltyp, self._calpar, self._calraw, self._calref)
        return val

    def _decodeAvg(self, dw, count):
        # val
        val = dw
        if self._isScal:
            val = (val / (100 * count) - self._offset) / self._scale
        else:
            val = val / (count * self._decexp)
        if self._caltyp != 0:
            val = self._calhdl(val, self._caltyp, self._calpar, self._calraw, self._calref)
        return val

    def isClosed(self):
        return self._isClosed

    def get_runIndex(self):
        """
        Returns the run index of the data stream. A run can be made of
        multiple datastreams, for different time intervals.
        
        @return an unsigned number corresponding to the run index.
        """
        return self._runNo

    def get_startTime(self):
        """
        Returns the relative start time of the data stream, measured in seconds.
        For recent firmwares, the value is relative to the present time,
        which means the value is always negative.
        If the device uses a firmware older than version 13000, value is
        relative to the start of the time the device was powered on, and
        is always positive.
        If you need an absolute UTC timestamp, use get_startTimeUTC().
        
        @return an unsigned number corresponding to the number of seconds
                between the start of the run and the beginning of this data
                stream.
        """
        return self._utcStamp - int(time.time())

    def get_startTimeUTC(self):
        """
        Returns the start time of the data stream, relative to the Jan 1, 1970.
        If the UTC time was not set in the datalogger at the time of the recording
        of this data stream, this method returns 0.
        
        @return an unsigned number corresponding to the number of seconds
                between the Jan 1, 1970 and the beginning of this data
                stream (i.e. Unix time representation of the absolute time).
        """
        return self._utcStamp

    def get_dataSamplesIntervalMs(self):
        """
        Returns the number of milliseconds between two consecutive
        rows of this data stream. By default, the data logger records one row
        per second, but the recording frequency can be changed for
        each device function
        
        @return an unsigned number corresponding to a number of milliseconds.
        """
        return ((3600000) / (self._samplesPerHour))

    def get_dataSamplesInterval(self):
        return 3600.0 / self._samplesPerHour

    def get_rowCount(self):
        """
        Returns the number of data rows present in this stream.
        
        If the device uses a firmware older than version 13000,
        this method fetches the whole data stream from the device
        if not yet done, which can cause a little delay.
        
        @return an unsigned number corresponding to the number of rows.
        
        On failure, throws an exception or returns zero.
        """
        if (self._nRows != 0) and self._isClosed:
            return self._nRows
        self.loadStream()
        return self._nRows

    def get_columnCount(self):
        """
        Returns the number of data columns present in this stream.
        The meaning of the values present in each column can be obtained
        using the method get_columnNames().
        
        If the device uses a firmware older than version 13000,
        this method fetches the whole data stream from the device
        if not yet done, which can cause a little delay.
        
        @return an unsigned number corresponding to the number of columns.
        
        On failure, throws an exception or returns zero.
        """
        if self._nCols != 0:
            return self._nCols
        self.loadStream()
        return self._nCols

    def get_columnNames(self):
        """
        Returns the title (or meaning) of each data column present in this stream.
        In most case, the title of the data column is the hardware identifier
        of the sensor that produced the data. For streams recorded at a lower
        recording rate, the dataLogger stores the min, average and max value
        during each measure interval into three columns with suffixes _min,
        _avg and _max respectively.
        
        If the device uses a firmware older than version 13000,
        this method fetches the whole data stream from the device
        if not yet done, which can cause a little delay.
        
        @return a list containing as many strings as there are columns in the
                data stream.
        
        On failure, throws an exception or returns an empty array.
        """
        if len(self._columnNames) != 0:
            return self._columnNames
        self.loadStream()
        return self._columnNames

    def get_minValue(self):
        """
        Returns the smallest measure observed within this stream.
        If the device uses a firmware older than version 13000,
        this method will always return YDataStream.DATA_INVALID.
        
        @return a floating-point number corresponding to the smallest value,
                or YDataStream.DATA_INVALID if the stream is not yet complete (still recording).
        
        On failure, throws an exception or returns YDataStream.DATA_INVALID.
        """
        return self._minVal

    def get_averageValue(self):
        """
        Returns the average of all measures observed within this stream.
        If the device uses a firmware older than version 13000,
        this method will always return YDataStream.DATA_INVALID.
        
        @return a floating-point number corresponding to the average value,
                or YDataStream.DATA_INVALID if the stream is not yet complete (still recording).
        
        On failure, throws an exception or returns YDataStream.DATA_INVALID.
        """
        return self._avgVal

    def get_maxValue(self):
        """
        Returns the largest measure observed within this stream.
        If the device uses a firmware older than version 13000,
        this method will always return YDataStream.DATA_INVALID.
        
        @return a floating-point number corresponding to the largest value,
                or YDataStream.DATA_INVALID if the stream is not yet complete (still recording).
        
        On failure, throws an exception or returns YDataStream.DATA_INVALID.
        """
        return self._maxVal

    def get_duration(self):
        """
        Returns the approximate duration of this stream, in seconds.
        
        @return the number of seconds covered by this stream.
        
        On failure, throws an exception or returns YDataStream.DURATION_INVALID.
        """
        if self._isClosed:
            return self._duration
        return int(time.time()) - self._utcStamp

    def get_dataRows(self):
        """
        Returns the whole data set contained in the stream, as a bidimensional
        table of numbers.
        The meaning of the values present in each column can be obtained
        using the method get_columnNames().
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @return a list containing as many elements as there are rows in the
                data stream. Each row itself is a list of floating-point
                numbers.
        
        On failure, throws an exception or returns an empty array.
        """
        if (len(self._values) == 0) or not (self._isClosed):
            self.loadStream()
        return self._values

    def get_data(self, row, col):
        """
        Returns a single measure from the data stream, specified by its
        row and column index.
        The meaning of the values present in each column can be obtained
        using the method get_columnNames().
        
        This method fetches the whole data stream from the device,
        if not yet done.
        
        @param row : row index
        @param col : column index
        
        @return a floating-point number
        
        On failure, throws an exception or returns YDataStream.DATA_INVALID.
        """
        if (len(self._values) == 0) or not (self._isClosed):
            self.loadStream()
        if row >= len(self._values):
            return YDataStream.DATA_INVALID
        if col >= len(self._values[row]):
            return YDataStream.DATA_INVALID
        return self._values[row][col]

#--- (end of generated code: YDataStream implementation)
#--- (generated code: DataStream functions)
#--- (end of generated code: DataStream functions)


#--- (generated code: YMeasure class start)
#noinspection PyProtectedMember
class YMeasure(object):
    """
    YMeasure objects are used within the API to represent
    a value measured at a specified time. These objects are
    used in particular in conjunction with the YDataSet class.
    
    """
#--- (end of generated code: YMeasure class start)
    #--- (generated code: YMeasure definitions)
    #--- (end of generated code: YMeasure definitions)

    def __init__(self, start, end, minVal, avgVal, maxVal):
        #--- (generated code: YMeasure attributes)
        self._start = 0
        self._end = 0
        self._minVal = 0
        self._avgVal = 0
        self._maxVal = 0
        #--- (end of generated code: YMeasure attributes)
        self._start = start
        self._end = end
        self._minVal = minVal
        self._avgVal = avgVal
        self._maxVal = maxVal
        rounded = int(start * 10 + 0.5)
        self._start_datetime = datetime.datetime.fromtimestamp(rounded / 10.0)
        rounded = int(end * 10 + 0.5)
        self._end_datetime = datetime.datetime.fromtimestamp(rounded / 10.0)

    def get_startTimeUTC_asDatetime(self):
        """
        """
        return self._start_datetime

    def get_endTimeUTC_asDatetime(self):
        """
        """
        return self._end_datetime

    #--- (generated code: YMeasure implementation)
    def get_startTimeUTC(self):
        """
        Returns the start time of the measure, relative to the Jan 1, 1970 UTC
        (Unix timestamp). When the recording rate is higher then 1 sample
        per second, the timestamp may have a fractional part.
        
        @return an floating point number corresponding to the number of seconds
                between the Jan 1, 1970 UTC and the beginning of this measure.
        """
        return self._start

    def get_endTimeUTC(self):
        """
        Returns the end time of the measure, relative to the Jan 1, 1970 UTC
        (Unix timestamp). When the recording rate is higher then 1 sample
        per second, the timestamp may have a fractional part.
        
        @return an floating point number corresponding to the number of seconds
                between the Jan 1, 1970 UTC and the end of this measure.
        """
        return self._end

    def get_minValue(self):
        """
        Returns the smallest value observed during the time interval
        covered by this measure.
        
        @return a floating-point number corresponding to the smallest value observed.
        """
        return self._minVal

    def get_averageValue(self):
        """
        Returns the average value observed during the time interval
        covered by this measure.
        
        @return a floating-point number corresponding to the average value observed.
        """
        return self._avgVal

    def get_maxValue(self):
        """
        Returns the largest value observed during the time interval
        covered by this measure.
        
        @return a floating-point number corresponding to the largest value observed.
        """
        return self._maxVal

#--- (end of generated code: YMeasure implementation)

#--- (generated code: Measure functions)
#--- (end of generated code: Measure functions)


#--- (generated code: YDataSet class start)
#noinspection PyProtectedMember
class YDataSet(object):
    """
    YDataSet objects make it possible to retrieve a set of recorded measures
    for a given sensor and a specified time interval. They can be used
    to load data points with a progress report. When the YDataSet object is
    instanciated by the get_recordedData()  function, no data is
    yet loaded from the module. It is only when the loadMore()
    method is called over and over than data will be effectively loaded
    from the dataLogger.
    
    A preview of available measures is available using the function
    get_preview() as soon as loadMore() has been called
    once. Measures themselves are available using function get_measures()
    when loaded by subsequent calls to loadMore().
    
    This class can only be used on devices that use a recent firmware,
    as YDataSet objects are not supported by firmwares older than version 13000.
    
    """
#--- (end of generated code: YDataSet class start)
    #--- (generated code: YDataSet definitions)
    #--- (end of generated code: YDataSet definitions)

    def __init__(self, parent, functionId, unit=None, starttime=None, endTime=None):
        #--- (generated code: YDataSet attributes)
        self._parent = None
        self._hardwareId = ''
        self._functionId = ''
        self._unit = ''
        self._startTime = 0
        self._endTime = 0
        self._progress = 0
        self._calib = []
        self._streams = []
        self._summary = None
        self._preview = []
        self._measures = []
        #--- (end of generated code: YDataSet attributes)
        self._summary = YMeasure(0, 0, 0, 0, 0)
        if unit is None:
            self._initFromJson(parent, functionId)
        else:
            self._initFromParams(parent, functionId, unit, starttime, endTime)

    def _initFromParams(self, parent, functionId, unit, startTime, endTime):
        self._parent = parent
        self._functionId = functionId
        self._unit = unit
        self._startTime = startTime
        self._endTime = endTime
        self._progress = -1
        
    def _initFromJson(self, parent, json):
        self._parent = parent
        self._startTime = 0
        self._endTime = 0
        self._parse(json)

    def _parse(self, json):
        try:
            j = YAPI.TJsonParser(json, False)
        except YAPI.JsonError:
            #( exception handling working in both  in 2.x and 3.x)
            return

        summaryMinVal = float('inf')
        summaryMaxVal = float('-inf')
        summaryTotalTime = 0
        summaryTotalAvg = 0
        node = j.GetRootNode()

        if node.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT:
            return
        for member in node.members:
            if member.name == "id":
                self._functionId = member.svalue
            elif member.name == "unit":
                self._unit = member.svalue
            elif member.name == "cal":
                self._calib = YAPI._decodeWords(member.svalue)
            elif member.name == "streams":
                self._streams = []
                self._preview = []
                self._measures = []
                streams_node = j.GetChildNode(node, "streams")
                for streams_json in streams_node.items:
                    stream = self._parent._findDataStream(self, streams_json.svalue)
                    if self._startTime > 0 and stream.get_startTimeUTC() + stream.get_duration() <= self._startTime:
                        # this stream is too early, drop it
                        pass
                    elif 0 < self._endTime < stream.get_startTimeUTC():
                        # this stream is too late, drop it
                        pass
                    else:
                        self._streams.append(stream)
                        if(stream.isClosed() and stream.get_startTimeUTC() >= self._startTime and
                           (self._endTime == 0 or stream.get_startTimeUTC() + stream.get_duration() <= self._endTime)):
                            if summaryMinVal > stream.get_minValue():
                                summaryMinVal = stream.get_minValue()
                            if summaryMaxVal < stream.get_maxValue():
                                summaryMaxVal = stream.get_maxValue()
                            summaryTotalAvg += stream.get_averageValue() * stream.get_duration()
                            summaryTotalTime += stream.get_duration()

                            rec = YMeasure(stream.get_startTimeUTC(),
                                           stream.get_startTimeUTC() + stream.get_duration(),
                                           stream.get_minValue(),
                                           stream.get_averageValue(),
                                           stream.get_maxValue())
                            self._preview.append(rec)
                if len(self._streams) > 0:
                    # update time boundaries with actual data
                    stream = self._streams[len(self._streams) - 1]
                    endtime = stream.get_startTimeUTC() + stream.get_duration()
                    startTime = self._streams[0].get_startTimeUTC() - stream.get_dataSamplesIntervalMs() / 1000
                    if self._startTime < startTime:
                        self._startTime = startTime
                    if self._endTime == 0 or self._endTime > endtime:
                        self._endTime = endtime
                    self._summary = YMeasure(self._startTime, self._endTime,
                                             summaryMinVal, summaryTotalAvg / summaryTotalTime, summaryMaxVal)
        self._progress = 0
        return self.get_progress()

    #--- (generated code: YDataSet implementation)
    def get_calibration(self):
        return self._calib

    def processMore(self, progress, data):
        # stream
        dataRows = []
        # strdata
        # tim
        # itv
        # nCols
        # minCol
        # avgCol
        # maxCol
        # // may throw an exception
        if progress != self._progress:
            return self._progress
        if self._progress < 0:
            strdata = YByte2String(data)
            if strdata == "{}":
                self._parent._throw(YAPI.VERSION_MISMATCH, "device firmware is too old")
                return YAPI.VERSION_MISMATCH
            return self._parse(strdata)
        stream = self._streams[self._progress]
        stream.parse(data)
        dataRows = stream.get_dataRows()
        self._progress = self._progress + 1
        if len(dataRows) == 0:
            return self.get_progress()
        tim = stream.get_startTimeUTC()
        itv = stream.get_dataSamplesInterval()
        nCols = len(dataRows[0])
        minCol = 0
        if nCols > 2:
            avgCol = 1
        else:
            avgCol = 0
        if nCols > 2:
            maxCol = 2
        else:
            maxCol = 0
        
        for y in dataRows:
            if (tim >= self._startTime) and ((self._endTime == 0) or (tim <= self._endTime)):
                self._measures.append(YMeasure(tim - itv, tim, y[minCol], y[avgCol], y[maxCol]))
                tim = tim + itv
        
        return self.get_progress()

    def get_privateDataStreams(self):
        return self._streams

    def get_hardwareId(self):
        """
        Returns the unique hardware identifier of the function who performed the measures,
        in the form SERIAL.FUNCTIONID. The unique hardware identifier is composed of the
        device serial number and of the hardware identifier of the function
        (for example THRMCPL1-123456.temperature1)
        
        @return a string that uniquely identifies the function (ex: THRMCPL1-123456.temperature1)
        
        On failure, throws an exception or returns  YDataSet.HARDWAREID_INVALID.
        """
        # mo
        if not (self._hardwareId == ""):
            return self._hardwareId
        mo = self._parent.get_module()
        self._hardwareId = "" + mo.get_serialNumber() + "." + self.get_functionId()
        return self._hardwareId

    def get_functionId(self):
        """
        Returns the hardware identifier of the function that performed the measure,
        without reference to the module. For example temperature1.
        
        @return a string that identifies the function (ex: temperature1)
        """
        return self._functionId

    def get_unit(self):
        """
        Returns the measuring unit for the measured value.
        
        @return a string that represents a physical unit.
        
        On failure, throws an exception or returns  YDataSet.UNIT_INVALID.
        """
        return self._unit

    def get_startTimeUTC(self):
        """
        Returns the start time of the dataset, relative to the Jan 1, 1970.
        When the YDataSet is created, the start time is the value passed
        in parameter to the get_dataSet() function. After the
        very first call to loadMore(), the start time is updated
        to reflect the timestamp of the first measure actually found in the
        dataLogger within the specified range.
        
        @return an unsigned number corresponding to the number of seconds
                between the Jan 1, 1970 and the beginning of this data
                set (i.e. Unix time representation of the absolute time).
        """
        return self._startTime

    def get_endTimeUTC(self):
        """
        Returns the end time of the dataset, relative to the Jan 1, 1970.
        When the YDataSet is created, the end time is the value passed
        in parameter to the get_dataSet() function. After the
        very first call to loadMore(), the end time is updated
        to reflect the timestamp of the last measure actually found in the
        dataLogger within the specified range.
        
        @return an unsigned number corresponding to the number of seconds
                between the Jan 1, 1970 and the end of this data
                set (i.e. Unix time representation of the absolute time).
        """
        return self._endTime

    def get_progress(self):
        """
        Returns the progress of the downloads of the measures from the data logger,
        on a scale from 0 to 100. When the object is instanciated by get_dataSet,
        the progress is zero. Each time loadMore() is invoked, the progress
        is updated, to reach the value 100 only once all measures have been loaded.
        
        @return an integer in the range 0 to 100 (percentage of completion).
        """
        if self._progress < 0:
            return 0
        # // index not yet loaded
        if self._progress >= len(self._streams):
            return 100
        return ((1 + (1 + self._progress) * 98) / ((1 + len(self._streams))))

    def loadMore(self):
        """
        Loads the the next block of measures from the dataLogger, and updates
        the progress indicator.
        
        @return an integer in the range 0 to 100 (percentage of completion),
                or a negative error code in case of failure.
        
        On failure, throws an exception or returns a negative error code.
        """
        # url
        # stream
        if self._progress < 0:
            url = "logger.json?id=" + self._functionId
        else:
            if self._progress >= len(self._streams):
                return 100
            else:
                stream = self._streams[self._progress]
                url = stream.get_url()
        return self.processMore(self._progress, self._parent._download(url))

    def get_summary(self):
        """
        Returns an YMeasure object which summarizes the whole
        DataSet. In includes the following information:
        - the start of a time interval
        - the end of a time interval
        - the minimal value observed during the time interval
        - the average value observed during the time interval
        - the maximal value observed during the time interval
        
        This summary is available as soon as loadMore() has
        been called for the first time.
        
        @return an YMeasure object
        """
        return self._summary

    def get_preview(self):
        """
        Returns a condensed version of the measures that can
        retrieved in this YDataSet, as a list of YMeasure
        objects. Each item includes:
        - the start of a time interval
        - the end of a time interval
        - the minimal value observed during the time interval
        - the average value observed during the time interval
        - the maximal value observed during the time interval
        
        This preview is available as soon as loadMore() has
        been called for the first time.
        
        @return a table of records, where each record depicts the
                measured values during a time interval
        
        On failure, throws an exception or returns an empty array.
        """
        return self._preview

    def get_measures(self):
        """
        Returns all measured values currently available for this DataSet,
        as a list of YMeasure objects. Each item includes:
        - the start of the measure time interval
        - the end of the measure time interval
        - the minimal value observed during the time interval
        - the average value observed during the time interval
        - the maximal value observed during the time interval
        
        Before calling this method, you should call loadMore()
        to load data from the device. You may have to call loadMore()
        several time until all rows are loaded, but you can start
        looking at available data rows before the load is complete.
        
        The oldest measures are always loaded first, and the most
        recent measures will be loaded last. As a result, timestamps
        are normally sorted in ascending order within the measure table,
        unless there was an unexpected adjustment of the datalogger UTC
        clock.
        
        @return a table of records, where each record depicts the
                measured value for a given time interval
        
        On failure, throws an exception or returns an empty array.
        """
        return self._measures

#--- (end of generated code: YDataSet implementation)

    #--- (generated code: DataSet functions)
#--- (end of generated code: DataSet functions)


## ------------------------------------------------------------------------------------
##
## YDevice
##
## ------------------------------------------------------------------------------------

#noinspection PyProtectedMember
class YDevice:
    def __init__(self, devdesc):
        self._devdescr = devdesc
        self._cacheStamp = datetime.datetime(year=1970, month=1, day=1)
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

    def _HTTPRequestPrepare(self, request):
        errbuf = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        root = ctypes.create_string_buffer(YAPI.YOCTO_SERIAL_LEN)

        if not self._subpathinit:
            neededsize = ctypes.c_int()
            #noinspection PyUnresolvedReferences
            res = YAPI._yapiGetDevicePath(self._devdescr, root, None, 0, ctypes.byref(neededsize), errbuf)
            if YAPI.YISERR(res):
                return res, YByte2String(errbuf.value)
                #noinspection PyUnresolvedReferences
            b = ctypes.create_string_buffer(neededsize.value)
            tmp = ctypes.c_int()
            #noinspection PyUnresolvedReferences
            res = YAPI._yapiGetDevicePath(self._devdescr, root, b, neededsize.value, ctypes.byref(tmp), errbuf)
            if YAPI.YISERR(res):
                return res, YByte2String(errbuf.value)
            self._rootdevice = YByte2String(root.value)
            self._subpath = YByte2String(b.value)
            self._subpathinit = True

        # request can be a purely binary buffer or a text string
        if not isinstance(request, bytes):
            request = YString2Byte(request)
            # first / is expected within very first characters of the query
        p = 0
        while p < 10 and YGetByte(request, p) != 47:  # chr(47) = '/'
            p += 1
        newrequest = request[0:p] + self._subpath.encode("ASCII") + request[p + 1:]
        return YAPI.SUCCESS, newrequest

    #noinspection PyUnresolvedReferences,PyUnusedLocal
    def HTTPRequestAsync(self, request, callback, context, errmsgRef=None):
        errbuf = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        #invalidate cache
        self._cacheStamp = YAPI.GetTickCount()
        (res, newrequest) = self._HTTPRequestPrepare(request)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = newrequest
            return res
        res = YAPI._yapiHTTPRequestAsync(ctypes.create_string_buffer(self._rootdevice.encode("ASCII")),
                                         ctypes.create_string_buffer(newrequest), None, None, errbuf)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = YByte2String(errbuf.value)
            return res
        return YAPI.SUCCESS

    #noinspection PyUnresolvedReferences,PyUnresolvedReferences
    def HTTPRequest(self, request, bufferRef, errmsgRef=None):
        (res, newrequest) = self._HTTPRequestPrepare(request)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = newrequest
            return res
        iohdl = ctypes.create_string_buffer(YAPI.YIOHDL_SIZE)
        errbuf = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        root_c = ctypes.create_string_buffer(self._rootdevice.encode("ASCII"))
        newrequest_c = ctypes.create_string_buffer(newrequest)
        reply_c = POINTER(ctypes.c_ubyte)()
        neededsize_c = ctypes.c_int(0)
        res = YAPI._yapiHTTPRequestSyncStartEx(iohdl, root_c, newrequest_c, len(newrequest), ctypes.byref(reply_c),
                                               ctypes.byref(neededsize_c), errbuf)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = YByte2String(errbuf.value)
            return res
        reply_size = neededsize_c.value
        bb = YString2Byte("")
        #(xrange not supported in 2.5.x)
        for i in range(reply_size):
            bb = YAddByte(bb, reply_c[i])
        bufferRef.value = bb
        res = YAPI._yapiHTTPRequestSyncDone(iohdl, errbuf)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = YByte2String(errbuf.value)
            return res
        return YAPI.SUCCESS

    def requestAPI(self, apiresRef, errmsgRef=None):

        suberrmsg = YRefParam()

        #Check if we have a valid cache value
        if self._cacheStamp > YAPI.GetTickCount():
            apiresRef.value = self._cacheJson
            return YAPI.SUCCESS

        res = self.HTTPRequest("GET /api.json \r\n\r\n", suberrmsg, errmsgRef)
        if YAPI.YISERR(res):
            # make sure a device scan does not solve the issue
            res = YAPI.yapiUpdateDeviceList(1, errmsgRef)
            if YAPI.YISERR(res):
                return res

            res = self.HTTPRequest("GET /api.json \r\n\r\n", suberrmsg, errmsgRef)
            if YAPI.YISERR(res):
                return res

        try:
            j = YAPI.TJsonParser(YByte2String(suberrmsg.value))
        except YAPI.JsonError:
            #( exception handling working in both  in 2.x and 3.x)
            e = sys.exc_info()[1]
            if not errmsgRef is None:
                errmsgRef.value = "unexpected JSON structure: " + e.msg
            return YAPI.IO_ERROR

        # store result in cache
        self._cacheJson = j
        apiresRef.value = j
        self._cacheStamp = YAPI.GetTickCount() + YAPI.DefaultCacheValidity

        return YAPI.SUCCESS

    #noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker
    def getFunctions(self, functionsRef, errmsgRef=None):

        neededsize = YRefParam()
        if not len(self._functions):
            res = YAPI.apiGetFunctionsByDevice(self._devdescr, 0, None, 64, neededsize, errmsgRef)
            if YAPI.YISERR(res):
                return res

            count = int(neededsize.value / YAPI.C_INTSIZE)
            #noinspection PyCallingNonCallable
            p = (ctypes.c_int * count)()

            res = YAPI.apiGetFunctionsByDevice(self._devdescr, 0, p, 64, neededsize, errmsgRef)
            if YAPI.YISERR(res):
                return res

            for i in range(count):
                self._functions.append(p[i])

        functionsRef.value = self._functions
        return YAPI.SUCCESS

## - keeps a reference to our callbacks, to  protect them from GC
## (may
#noinspection PyProtectedMember
native_yLogFunctionAnchor = YAPI._yapiLogFunc(YAPI.native_yLogFunction)
#noinspection PyProtectedMember
native_yFunctionUpdateAnchor = YAPI._yapiFunctionUpdateFunc(YAPI.native_yFunctionUpdateCallback)
#noinspection PyProtectedMember
native_yTimedReportAnchor = YAPI._yapiTimedReportFunc(YAPI.native_yTimedReportCallback)
#noinspection PyProtectedMember
native_yDeviceArrivalAnchor = YAPI._yapiDeviceUpdateFunc(YAPI.native_yDeviceArrivalCallback)
#noinspection PyProtectedMember
native_yDeviceRemovalAnchor = YAPI._yapiDeviceUpdateFunc(YAPI.native_yDeviceRemovalCallback)
#noinspection PyProtectedMember
native_yDeviceChangeAnchor = YAPI._yapiDeviceUpdateFunc(YAPI.native_yDeviceChangeCallback)
#noinspection PyProtectedMember
native_yHubDiscoveryAnchor = YAPI._yapiHubDiscoveryCallback(YAPI.native_HubDiscoveryCallback)


#--- (generated code: YFunction class start)
#noinspection PyProtectedMember
class YFunction(object):
    """
    This is the parent class for all public objects representing device functions documented in
    the high-level programming API. This abstract class does all the real job, but without
    knowledge of the specific function attributes.
    
    Instantiating a child class of YFunction does not cause any communication.
    The instance simply keeps track of its function identifier, and will dynamically bind
    to a matching device at the time it is really being used to read or set an attribute.
    In order to allow true hot-plug replacement of one device by another, the binding stay
    dynamic through the life of the object.
    
    The YFunction class implements a generic high-level cache for the attribute values of
    the specified function, pre-parsed from the REST API string.
    
    """
#--- (end of generated code: YFunction class start)
    _cache = {}
    _FunctionCallbacks = []
    _TimedReportCallbackList = []
    _CalibHandlers = {}

    FUNCTIONDESCRIPTOR_INVALID = -1
    HARDWAREID_INVALID = YAPI.INVALID_STRING
    FUNCTIONID_INVALID = YAPI.INVALID_STRING
    FRIENDLYNAME_INVALID = YAPI.INVALID_STRING
    #--- (generated code: YFunction definitions)
    LOGICALNAME_INVALID = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID = YAPI.INVALID_STRING
    #--- (end of generated code: YFunction definitions)

    def __init__(self, func):
        self._className = 'Function'
        self._func = func
        self._lastErrorType = YAPI.SUCCESS
        self._lastErrorMsg = ""
        self._fundescr = YFunction.FUNCTIONDESCRIPTOR_INVALID
        self._userData = None
        self._genCallback = None
        self._dataStreams = dict()
        #--- (generated code: YFunction attributes)
        self._callback = None
        self._logicalName = YFunction.LOGICALNAME_INVALID
        self._advertisedValue = YFunction.ADVERTISEDVALUE_INVALID
        self._valueCallbackFunction = None
        self._cacheExpiration = datetime.datetime.fromtimestamp(0)
        self._serial = ''
        self._funId = ''
        self._hwId = ''
        #--- (end of generated code: YFunction attributes)

    @staticmethod
    def _FindFromCache(class_name, func):
        key = class_name + "_" + func
        if key in YFunction._cache:
            return YFunction._cache[key]
        return None

    @staticmethod
    def _AddToCache(class_name, func, obj):
        YFunction._cache[class_name + "_" + func] = obj

    @staticmethod
    def _ClearCache():
        YFunction._cache.clear()

    @staticmethod
    def _UpdateValueCallbackList(func, add):
        if add:
            func.isOnline()
            if func not in YFunction._FunctionCallbacks:
                YFunction._FunctionCallbacks.append(func)
        else:
            if func in YFunction._FunctionCallbacks:
                index = YFunction._FunctionCallbacks.index(func)
                del YFunction._FunctionCallbacks[index]

    @staticmethod
    def _UpdateTimedReportCallbackList(func, add):
        if add:
            func.isOnline()
            if func not in YFunction._TimedReportCallbackList:
                YFunction._TimedReportCallbackList.append(func)
        else:
            if func in YFunction._TimedReportCallbackList:
                index = YFunction._TimedReportCallbackList.index(func)
                del YFunction._TimedReportCallbackList[index]

    def _throw(self, errType, errorMessage):
        self._lastErrorType = errType
        self._lastErrorMsg = errorMessage
        if not YAPI.ExceptionsDisabled:
            raise YAPI.YAPI_Exception(errType, "YoctoApi error : " + errorMessage)

    #  Method used to resolve our name to our unique function descriptor (may trigger a hub scan)
    def _getDescriptor(self, fundescrRef, errmsgRef=None):
        tmp_fundescr = YAPI.yapiGetFunction(self._className, self._func, errmsgRef)
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

    def _getDevice(self, devRef, errmsgRef=None):
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
        p = (ctypes.c_int * n_element)()

        res = YAPI.apiGetFunctionsByClass(self._className, fundescrRef.value, p, maxsize, neededsizeRef, errmsgRef)

        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return res

        #noinspection PyTypeChecker
        count = neededsizeRef.value / YAPI.C_INTSIZE
        if not count:
            hwidRef.value = ""
            return YAPI.SUCCESS

        res = YAPI.yapiGetFunctionInfo(p[0], devdescrRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return YAPI.SUCCESS

        hwidRef.value = serialRef.value + "." + funcIdRef.value
        return YAPI.SUCCESS

    def _buildSetRequest(self, changeattr, changeval, requestRef, errmsgRef=None):
        fundescRef = YRefParam()
        funcid = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if YAPI.YISERR(res):
            return res
        devdesc = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), None, funcid, None, None, errbuff)
        if YAPI.YISERR(res):
            if not errmsgRef is None:
                errmsgRef.value = YByte2String(errbuff.value)
            self._throw(res, errmsgRef.value)
            return res
        requestRef.value = "GET /api/" + YByte2String(funcid.value) + "/"
        uchangeval = ""

        if changeattr != "":
            requestRef.value += changeattr + "?" + changeattr + "="

        for c in changeval:
            if c <= ' ' or \
                    (c > 'z' and c != '~') or c == '"' or c == '%' or c == '&' or c == '+' or \
                    c == '<' or c == '=' or c == '>' or c == '\\' or c == '^' or c == '`':
                uchangeval += "%" + ('%02X' % ord(c))
            else:
                uchangeval += c

        requestRef.value += uchangeval + " \r\n\r\n"
        return YAPI.SUCCESS

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT:
            return -1
        for member in j.members:
            self._parseAttr(member)
        self._parserHelper()
        return 0

    # Set an attribute in the function, and parse the resulting new function state
    def _setAttr(self, attrname, newvalue):
        errmsgRef = YRefParam()
        requestRef = YRefParam()
        devRef = YRefParam()

        #  Execute http request
        res = self._buildSetRequest(attrname, newvalue, requestRef, errmsgRef)
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
            res = YAPI.yapiUpdateDeviceList(1, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res

            res = devRef.value.HTTPRequestAsync(requestRef.value, None, None, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return res

        if self._cacheExpiration != datetime.datetime.fromtimestamp(0):
            self._cacheExpiration = YAPI.GetTickCount()

        return YAPI.SUCCESS

    def _request(self, request):
        errmsgRef = YRefParam()
        httpbuffer = YRefParam()
        devRef = YRefParam()
        # Get device Object
        res = self._getDevice(devRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, request)
            return b""
        res = devRef.value.HTTPRequest(request, httpbuffer, errmsgRef)
        if YAPI.YISERR(res):
            # make sure a device scan does not solve the issue
            res = YAPI.yapiUpdateDeviceList(1, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return b""
            res = devRef.value.HTTPRequest(request, httpbuffer, errmsgRef)
            if YAPI.YISERR(res):
                self._throw(res, errmsgRef.value)
                return b""
        if len(httpbuffer.value) >= 4:
            check = httpbuffer.value[0:4].decode("latin1")
            if check == "OK\r\n":
                return httpbuffer.value
            if len(httpbuffer.value) >= 17:
                check = httpbuffer.value[0:17].decode("latin1")
                if check == "HTTP/1.1 200 OK\r\n":
                    return httpbuffer.value
        self._throw(YAPI.IO_ERROR, "http request failed")
        return b""

    def _upload(self, path, content):
        body = "Content-Disposition: form-data; name=\"" + path + "\"; filename=\"api\"\r\n"
        body += "Content-Type: application/octet-stream\r\n"
        body += "Content-Transfer-Encoding: binary\r\n\r\n"
        if not isinstance(content, bytes):
            if isinstance(content, array.array):
                content = content.tostring()
            else:
                content = content.encode("latin1")
        body = body.encode("ASCII") + content
        boundary = "Zz%06xzZ" % (random.randint(0, 0xffffff))
        request = "POST /upload.html HTTP/1.1\r\n"
        request += "Content-Type: multipart/form-data, boundary=" + boundary + "\r\n"
        request += "\r\n--" + boundary + "\r\n"
        request = request.encode("ASCII") + body + str("\r\n--" + boundary + "--\r\n").encode("ASCII")
        tmpbuffer = self._request(request)
        if len(tmpbuffer) == 0:
            self._throw(YAPI.IO_ERROR, "http request failed")
            return YAPI.IO_ERROR
        return YAPI.SUCCESS

    def _download(self, url):
        request = "GET /" + url + " HTTP/1.1\r\n\r\n"
        result_buffer = self._request(request)
        found = 0
        while found <= len(result_buffer) - 4:
            if YGetByte(result_buffer, found) == 13 \
                    and YGetByte(result_buffer, found + 1) == 10 \
                    and YGetByte(result_buffer, found + 2) == 13 \
                    and YGetByte(result_buffer, found + 3) == 10:
                break
            found += 1
        if found > len(result_buffer) - 4:
            self._throw(YAPI.IO_ERROR, "http request failed")
            return YAPI.INVALID_STRING
        return result_buffer[found + 4:]

    def _json_get_key(self, json, key):
        try:
            json_str = YByte2String(json)
            j = YAPI.TJsonParser(json_str, False)
        except YAPI.JsonError:
            #( exception handling working in both  in 2.x and 3.x
            e = sys.exc_info()[1]
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: " + e.msg)
            return YAPI.IO_ERROR
        node = j.GetChildNode(None, key)
        return node.svalue

    def _json_get_array(self, json):
        try:
            json_str = YByte2String(json)
            j = YAPI.TJsonParser(json_str, False)
        except YAPI.JsonError:
            #( exception handling working in both  in 2.x and 3.x
            e = sys.exc_info()[1]
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: " + e.msg)
            return YAPI.IO_ERROR
        return j.GetAllChilds(None)

    def _json_get_string(self, json):
        try:
            json_str = YByte2String(json)
            j = YAPI.TJsonParser('[' + json_str + ']', False)
        except YAPI.JsonError:
            #( exception handling working in both  in 2.x and 3.x
            e = sys.exc_info()[1]
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: " + e.msg)
            return YAPI.IO_ERROR
        node = j.GetRootNode()
        return node.items[0].svalue

    # Method used to cache DataStream objects (new DataLogger)
    def _findDataStream(self, dataset, definition):
        key = dataset.get_functionId() + ":" + definition
        if key in self._dataStreams:
            return self._dataStreams[definition]
        newDataStream = YDataStream(self, dataset, YAPI._decodeWords(definition))
        self._dataStreams[key] = newDataStream
        return newDataStream

#--- (generated code: YFunction implementation)
    def _parseAttr(self, member):
        if member.name == "logicalName":
            self._logicalName = member.svalue
            return 1
        if member.name == "advertisedValue":
            self._advertisedValue = member.svalue
            return 1
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the function.
        
        @return a string corresponding to the logical name of the function
        
        On failure, throws an exception or returns YFunction.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YFunction.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the function. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the function
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)

    def get_advertisedValue(self):
        """
        Returns the current value of the function (no more than 6 characters).
        
        @return a string corresponding to the current value of the function (no more than 6 characters)
        
        On failure, throws an exception or returns YFunction.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YFunction.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    @staticmethod
    def FindFunction(func):
        """
        Retrieves a function for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the function is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YFunction.isOnline() to test if the function is
        indeed online at a given time. In case of ambiguity when looking for
        a function by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the function
        
        @return a YFunction object allowing you to drive the function.
        """
        # obj
        obj = YFunction._FindFromCache("Function", func)
        if obj is None:
            obj = YFunction(func)
            YFunction._AddToCache("Function", func, obj)
        return obj

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
        # val
        if callback is not None:
            YFunction._UpdateValueCallbackList(self, True)
        else:
            YFunction._UpdateValueCallbackList(self, False)
        self._valueCallbackFunction = callback
        # // Immediately invoke value callback with current value
        if callback is not None and self.isOnline():
            val = self._advertisedValue
            if not (val == ""):
                self._invokeValueCallback(val)
        return 0

    def _invokeValueCallback(self, value):
        if self._valueCallbackFunction is not None:
            self._valueCallbackFunction(self, value)
        return 0

    def _parserHelper(self):
        # // By default, nothing to do
        return 0

    def nextFunction(self):
        """
        comment from .yc definition
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YFunction.FindFunction(hwidRef.value)

#--- (end of generated code: YFunction implementation)

    def get_hardwareId(self):
        """
        Returns the unique hardware identifier of the function in the form SERIAL.FUNCTIONID.
        The unique hardware identifier is composed of the device serial
        number and of the hardware identifier of the function. (for example RELAYLO1-123456.relay1)
        
        @return a string that uniquely identifies the function (ex: RELAYLO1-123456.relay1)
        
        On failure, throws an exception or returns  YFunction.HARDWAREID_INVALID.
        """
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        snum = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.HARDWAREID_INVALID
        devdesc = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, None, None, errbuff)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.HARDWAREID_INVALID
        return YByte2String(snum.value) + "." + YByte2String(funcid.value)

    def get_functionId(self):
        """
        Returns the hardware identifier of the function, without reference to the module. For example
        relay1
        
        @return a string that identifies the function (ex: relay1)
        
        On failure, throws an exception or returns  YFunction.FUNCTIONID_INVALID.
        """
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        funcid = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.FUNCTIONID_INVALID
        devdesc = ctypes.c_int()
        #noinspection PyUnresolvedReferences
        res = YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), None, funcid, None, None, errbuff)
        if YAPI.YISERR(res):
            self._throw(res, errmsgRef.value)
            return self.FUNCTIONID_INVALID
        return YByte2String(funcid.value)

    #noinspection PyUnresolvedReferences,PyUnresolvedReferences
    def get_friendlyName(self):
        """
        Returns a global identifier of the function in the format MODULE_NAME&#46;FUNCTION_NAME.
        The returned string uses the logical names of the module and of the function if they are defined,
        otherwise the serial number of the module and the hardware identifier of the function
        (for exemple: MyCustomName.relay1)
        
        @return a string that uniquely identifies the function using logical names
                (ex: MyCustomName.relay1)
        
        On failure, throws an exception or returns  YFunction.FRIENDLYNAME_INVALID.
        """
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        fname = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        snum = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc = ctypes.c_int()
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        if not YAPI.YISERR(res) and not YAPI.YISERR(
                YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, fname, None, errbuff)):
            if YByte2String(fname.value) != "":
                funcid = fname
            dname = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
            moddescr = YAPI.yapiGetFunction("Module", YByte2String(snum.value), errmsgRef)
            if not YAPI.YISERR(moddescr) and not YAPI.YISERR(
                    YAPI._yapiGetFunctionInfo(moddescr, ctypes.byref(devdesc), None, None, dname, None, errbuff)):
                if YByte2String(dname.value) != "":
                    return "%s.%s" % (YByte2String(dname.value), YByte2String(funcid.value))
            return "%s.%s" % (YByte2String(snum.value), YByte2String(funcid.value))
        self._throw(YAPI.DEVICE_NOT_FOUND, errmsgRef.value)
        return self.FRIENDLYNAME_INVALID

    def describe(self):
        """
        Returns a short text that describes the function in the form TYPE(NAME)=SERIAL&#46;FUNCTIONID.
        More precisely,
        TYPE       is the type of the function,
        NAME       it the name used for the first access to the function,
        SERIAL     is the serial number of the module if the module is connected or "unresolved", and
        FUNCTIONID is  the hardware identifier of the function if the module is connected.
        For example, this method returns Relay(MyCustomName.relay1)=RELAYLO1-123456.relay1 if the
        module is already connected or Relay(BadCustomeName.relay1)=unresolved if the module has
        not yet been connected. This method does not trigger any USB or TCP transaction and can therefore be used in
        a debugger.
        
        @return a string that describes the function
                (ex: Relay(MyCustomName.relay1)=RELAYLO1-123456.relay1)
        """
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        snum = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc = ctypes.c_int()
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        #noinspection PyUnresolvedReferences
        if not YAPI.YISERR(res) and not YAPI.YISERR(
                YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, None, None, errbuff)):
            return self._className + "(" + self._func + ")=" + YByte2String(snum.value) + "." + YByte2String(
                funcid.value)
        return self._className + "(" + self._func + ")=unresolved"

    def __str__(self):
        return self.describe()

    def get_errorType(self):
        """
        Returns the numerical error code of the latest error with the function.
        This method is mostly useful when using the Yoctopuce library with
        exceptions disabled.
        
        @return a number corresponding to the code of the latest error that occured while
                using the function object
        """
        return self._lastErrorType

    def errorType(self):
        return self._lastErrorType

    def errType(self):
        return self._lastErrorType

    def get_errorMessage(self):
        """
        Returns the error message of the latest error with the function.
        This method is mostly useful when using the Yoctopuce library with
        exceptions disabled.
        
        @return a string corresponding to the latest error message that occured while
                using the function object
        """
        return self._lastErrorMsg

    def errorMessage(self):
        return self._lastErrorMsg

    def errMessage(self):
        return self._lastErrorMsg

    def isOnline(self):
        """
        Checks if the function is currently reachable, without raising any error.
        If there is a cached value for the function in cache, that has not yet
        expired, the device is considered reachable.
        No exception is raised if there is an error while trying to contact the
        device hosting the function.
        
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

        self.load(YAPI.DefaultCacheValidity)
        return True

    def load(self, msValidity):
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
        if type(msValidity) == type(int()):
            msValidity = datetime.timedelta(milliseconds=msValidity)
        self._cacheExpiration = YAPI.GetTickCount() + msValidity
        self._serial = str(serialRef.value)
        self._funId = str(funcIdRef.value)
        self._hwId = self._serial + '.' + self._funId

        node = apiresRef.value.GetChildNode(None, funcIdRef.value)
        if node is None:
            self._throw(YAPI.IO_ERROR, "unexpected JSON structure: missing function " + str(funcIdRef.value))
            return YAPI.IO_ERROR

        self._parse(node)
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
        if not YAPI.YISERR(fundescr):
            if not YAPI.YISERR(
                    YAPI.yapiGetFunctionInfo(fundescr, devdescrRef, serialRef, funcIdRef, funcNameRef, funcValueRef,
                                             errmsgRef)):
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

    def setUserData(self, data):
        self.set_userData(data)


#--- (generated code: YModule class start)
#noinspection PyProtectedMember
class YModule(YFunction):
    """
    This interface is identical for all Yoctopuce USB modules.
    It can be used to control the module global parameters, and
    to enumerate the functions provided by each module.
    
    """
#--- (end of generated code: YModule class start)
    #--- (generated code: YModule definitions)
    PRODUCTNAME_INVALID = YAPI.INVALID_STRING
    SERIALNUMBER_INVALID = YAPI.INVALID_STRING
    PRODUCTID_INVALID = YAPI.INVALID_UINT
    PRODUCTRELEASE_INVALID = YAPI.INVALID_UINT
    FIRMWARERELEASE_INVALID = YAPI.INVALID_STRING
    LUMINOSITY_INVALID = YAPI.INVALID_UINT
    UPTIME_INVALID = YAPI.INVALID_LONG
    USBCURRENT_INVALID = YAPI.INVALID_UINT
    REBOOTCOUNTDOWN_INVALID = YAPI.INVALID_INT
    PERSISTENTSETTINGS_LOADED = 0
    PERSISTENTSETTINGS_SAVED = 1
    PERSISTENTSETTINGS_MODIFIED = 2
    PERSISTENTSETTINGS_INVALID = -1
    BEACON_OFF = 0
    BEACON_ON = 1
    BEACON_INVALID = -1
    USBBANDWIDTH_SIMPLE = 0
    USBBANDWIDTH_DOUBLE = 1
    USBBANDWIDTH_INVALID = -1
    #--- (end of generated code: YModule definitions)
    
    def __init__(self, func):
        super(YModule, self).__init__(func)
        self._className = "Module"
        #--- (generated code: YModule attributes)
        self._callback = None
        self._productName = YModule.PRODUCTNAME_INVALID
        self._serialNumber = YModule.SERIALNUMBER_INVALID
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
        #--- (end of generated code: YModule attributes)

    #--- (generated code: YModule implementation)
    def _parseAttr(self, member):
        if member.name == "productName":
            self._productName = member.svalue
            return 1
        if member.name == "serialNumber":
            self._serialNumber = member.svalue
            return 1
        if member.name == "productId":
            self._productId = member.ivalue
            return 1
        if member.name == "productRelease":
            self._productRelease = member.ivalue
            return 1
        if member.name == "firmwareRelease":
            self._firmwareRelease = member.svalue
            return 1
        if member.name == "persistentSettings":
            self._persistentSettings = member.ivalue
            return 1
        if member.name == "luminosity":
            self._luminosity = member.ivalue
            return 1
        if member.name == "beacon":
            self._beacon = member.ivalue
            return 1
        if member.name == "upTime":
            self._upTime = member.ivalue
            return 1
        if member.name == "usbCurrent":
            self._usbCurrent = member.ivalue
            return 1
        if member.name == "rebootCountdown":
            self._rebootCountdown = member.ivalue
            return 1
        if member.name == "usbBandwidth":
            self._usbBandwidth = member.ivalue
            return 1
        super(YModule, self)._parseAttr(member)

    def get_productName(self):
        """
        Returns the commercial name of the module, as set by the factory.
        
        @return a string corresponding to the commercial name of the module, as set by the factory
        
        On failure, throws an exception or returns YModule.PRODUCTNAME_INVALID.
        """
        if self._cacheExpiration == datetime.datetime.fromtimestamp(0):
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.PRODUCTNAME_INVALID
        return self._productName

    def get_serialNumber(self):
        """
        Returns the serial number of the module, as set by the factory.
        
        @return a string corresponding to the serial number of the module, as set by the factory
        
        On failure, throws an exception or returns YModule.SERIALNUMBER_INVALID.
        """
        if self._cacheExpiration == datetime.datetime.fromtimestamp(0):
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.SERIALNUMBER_INVALID
        return self._serialNumber

    def get_productId(self):
        """
        Returns the USB device identifier of the module.
        
        @return an integer corresponding to the USB device identifier of the module
        
        On failure, throws an exception or returns YModule.PRODUCTID_INVALID.
        """
        if self._cacheExpiration == datetime.datetime.fromtimestamp(0):
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.PRODUCTID_INVALID
        return self._productId

    def get_productRelease(self):
        """
        Returns the hardware release version of the module.
        
        @return an integer corresponding to the hardware release version of the module
        
        On failure, throws an exception or returns YModule.PRODUCTRELEASE_INVALID.
        """
        if self._cacheExpiration == datetime.datetime.fromtimestamp(0):
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.PRODUCTRELEASE_INVALID
        return self._productRelease

    def get_firmwareRelease(self):
        """
        Returns the version of the firmware embedded in the module.
        
        @return a string corresponding to the version of the firmware embedded in the module
        
        On failure, throws an exception or returns YModule.FIRMWARERELEASE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
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
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.PERSISTENTSETTINGS_INVALID
        return self._persistentSettings

    def set_persistentSettings(self, newval):
        rest_val = str(newval)
        return self._setAttr("persistentSettings", rest_val)

    def get_luminosity(self):
        """
        Returns the luminosity of the  module informative leds (from 0 to 100).
        
        @return an integer corresponding to the luminosity of the  module informative leds (from 0 to 100)
        
        On failure, throws an exception or returns YModule.LUMINOSITY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
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
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.BEACON_INVALID
        return self._beacon

    def set_beacon(self, newval):
        """
        Turns on or off the module localization beacon.
        
        @param newval : either YModule.BEACON_OFF or YModule.BEACON_ON
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return self._setAttr("beacon", rest_val)

    def get_upTime(self):
        """
        Returns the number of milliseconds spent since the module was powered on.
        
        @return an integer corresponding to the number of milliseconds spent since the module was powered on
        
        On failure, throws an exception or returns YModule.UPTIME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.UPTIME_INVALID
        return self._upTime

    def get_usbCurrent(self):
        """
        Returns the current consumed by the module on the USB bus, in milli-amps.
        
        @return an integer corresponding to the current consumed by the module on the USB bus, in milli-amps
        
        On failure, throws an exception or returns YModule.USBCURRENT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
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
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YModule.REBOOTCOUNTDOWN_INVALID
        return self._rebootCountdown

    def set_rebootCountdown(self, newval):
        rest_val = str(newval)
        return self._setAttr("rebootCountdown", rest_val)

    def get_usbBandwidth(self):
        """
        Returns the number of USB interfaces used by the module.
        
        @return either YModule.USBBANDWIDTH_SIMPLE or YModule.USBBANDWIDTH_DOUBLE, according to the number
        of USB interfaces used by the module
        
        On failure, throws an exception or returns YModule.USBBANDWIDTH_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
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
        # obj
        obj = YFunction._FindFromCache("Module", func)
        if obj is None:
            obj = YModule(func)
            YFunction._AddToCache("Module", func, obj)
        return obj

    def saveToFlash(self):
        """
        Saves current settings in the nonvolatile memory of the module.
        Warning: the number of allowed save operations during a module life is
        limited (about 100000 cycles). Do not call this function within a loop.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_persistentSettings(YModule.PERSISTENTSETTINGS_SAVED)

    def revertFromFlash(self):
        """
        Reloads the settings stored in the nonvolatile memory, as
        when the module is powered on.
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_persistentSettings(YModule.PERSISTENTSETTINGS_LOADED)

    def reboot(self, secBeforeReboot):
        """
        Schedules a simple module reboot after the given number of seconds.
        
        @param secBeforeReboot : number of seconds before rebooting
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_rebootCountdown(secBeforeReboot)

    def triggerFirmwareUpdate(self, secBeforeReboot):
        """
        Schedules a module reboot into special firmware update mode.
        
        @param secBeforeReboot : number of seconds before rebooting
        
        @return YAPI.SUCCESS when the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self.set_rebootCountdown(-secBeforeReboot)

    def download(self, pathname):
        """
        Downloads the specified built-in file and returns a binary buffer with its content.
        
        @param pathname : name of the new file to load
        
        @return a binary buffer with the file content
        
        On failure, throws an exception or returns an empty content.
        """
        return self._download(pathname)

    def get_icon2d(self):
        """
        Returns the icon of the module. The icon is a PNG image and does not
        exceeds 1536 bytes.
        
        @return a binary buffer with module icon, in png format.
        """
        # // may throw an exception
        return self._download("icon2d.png")

    def get_lastLogs(self):
        """
        Returns a string with last logs of the module. This method return only
        logs that are still in the module.
        
        @return a string with last logs of the module.
        """
        # content
        # // may throw an exception
        content = self._download("logs.txt")
        return YByte2String(content)

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

#--- (end of generated code: YModule implementation)

    def get_friendlyName(self):
        errmsgRef = YRefParam()
        fundescRef = YRefParam()
        fname = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        snum = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        funcid = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
        errbuff = ctypes.create_string_buffer(YAPI.YOCTO_ERRMSG_LEN)
        devdesc = ctypes.c_int()
        # Resolve the function name
        res = self._getDescriptor(fundescRef, errmsgRef)
        #noinspection PyUnresolvedReferences
        if not YAPI.YISERR(res) and not YAPI.YISERR(
                YAPI._yapiGetFunctionInfo(fundescRef.value, ctypes.byref(devdesc), snum, funcid, fname, None, errbuff)):
            dname = ctypes.create_string_buffer(YAPI.YOCTO_FUNCTION_LEN)
            moddescr = YAPI.yapiGetFunction("Module", YByte2String(snum.value), errmsgRef)
            #noinspection PyUnresolvedReference,PyUnresolvedReferences
            if not YAPI.YISERR(moddescr) and not YAPI.YISERR(
                    YAPI._yapiGetFunctionInfo(moddescr, ctypes.byref(devdesc), None, None, dname, None, errbuff)):
                if YByte2String(dname.value) != "":
                    return "%s" % (YByte2String(dname.value))
            return "%s" % (YByte2String(snum.value))
        self._throw(YAPI.DEVICE_NOT_FOUND, errmsgRef.value)
        return self.FRIENDLYNAME_INVALID

    def setImmutableAttributes(self, infosRef):
        self._serialNumber = YByte2String(infosRef.serial)
        self._productName = YByte2String(infosRef.productname)
        self._productId = int(infosRef.deviceid)

    # Return the properties of the nth function of our device
    def _getFunction(self, idx, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef):
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

    def functionId(self, functionIndex):
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
            return YAPI.INVALID_STRING

        return funcIdRef.value

    def functionName(self, functionIndex):
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
            return YAPI.INVALID_STRING

        return funcNameRef.value

    def functionValue(self, functionIndex):
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

        return funcValRef.value

    #--- (generated code: Module functions)

    @staticmethod
    def FirstModule():
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
        p = (ctypes.c_int * 1)()
        err = YAPI.apiGetFunctionsByClass("Module", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YModule.FindModule(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: Module functions)


#--- (generated code: YSensor class start)
#noinspection PyProtectedMember
class YSensor(YFunction):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of generated code: YSensor class start)
    #--- (generated code: YSensor return codes)
    #--- (end of generated code: YSensor return codes)
    #--- (generated code: YSensor definitions)
    UNIT_INVALID = YAPI.INVALID_STRING
    CURRENTVALUE_INVALID = YAPI.INVALID_DOUBLE
    LOWESTVALUE_INVALID = YAPI.INVALID_DOUBLE
    HIGHESTVALUE_INVALID = YAPI.INVALID_DOUBLE
    CURRENTRAWVALUE_INVALID = YAPI.INVALID_DOUBLE
    LOGFREQUENCY_INVALID = YAPI.INVALID_STRING
    REPORTFREQUENCY_INVALID = YAPI.INVALID_STRING
    CALIBRATIONPARAM_INVALID = YAPI.INVALID_STRING
    RESOLUTION_INVALID = YAPI.INVALID_DOUBLE
    #--- (end of generated code: YSensor definitions)

    def __init__(self, func):
        super(YSensor, self).__init__(func)
        self._className = "Sensor"
        #--- (generated code: YSensor attributes)
        self._callback = None
        self._unit = YSensor.UNIT_INVALID
        self._currentValue = YSensor.CURRENTVALUE_INVALID
        self._lowestValue = YSensor.LOWESTVALUE_INVALID
        self._highestValue = YSensor.HIGHESTVALUE_INVALID
        self._currentRawValue = YSensor.CURRENTRAWVALUE_INVALID
        self._logFrequency = YSensor.LOGFREQUENCY_INVALID
        self._reportFrequency = YSensor.REPORTFREQUENCY_INVALID
        self._calibrationParam = YSensor.CALIBRATIONPARAM_INVALID
        self._resolution = YSensor.RESOLUTION_INVALID
        self._timedReportCallbackSensor = None
        self._prevTimedReport = 0
        self._iresol = 0
        self._offset = 0
        self._scale = 0
        self._decexp = 0
        self._isScal = 0
        self._caltyp = 0
        self._calpar = []
        self._calraw = []
        self._calref = []
        self._calhdl = None
        #--- (end of generated code: YSensor attributes)

    #--- (generated code: YSensor implementation)
    def _parseAttr(self, member):
        if member.name == "unit":
            self._unit = member.svalue
            return 1
        if member.name == "currentValue":
            self._currentValue = member.ivalue / 65536.0
            return 1
        if member.name == "lowestValue":
            self._lowestValue = member.ivalue / 65536.0
            return 1
        if member.name == "highestValue":
            self._highestValue = member.ivalue / 65536.0
            return 1
        if member.name == "currentRawValue":
            self._currentRawValue = member.ivalue / 65536.0
            return 1
        if member.name == "logFrequency":
            self._logFrequency = member.svalue
            return 1
        if member.name == "reportFrequency":
            self._reportFrequency = member.svalue
            return 1
        if member.name == "calibrationParam":
            self._calibrationParam = member.svalue
            return 1
        if member.name == "resolution":
            self._resolution = 1.0 / round(65536.0 / member.ivalue) if member.ivalue > 100 else 0.001 / round(67.0 / member.ivalue)
            return 1
        super(YSensor, self)._parseAttr(member)

    def get_unit(self):
        """
        Returns the measuring unit for the measure.
        
        @return a string corresponding to the measuring unit for the measure
        
        On failure, throws an exception or returns YSensor.UNIT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.UNIT_INVALID
        return self._unit

    def get_currentValue(self):
        """
        Returns the current value of the measure.
        
        @return a floating point number corresponding to the current value of the measure
        
        On failure, throws an exception or returns YSensor.CURRENTVALUE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.CURRENTVALUE_INVALID
        res = self._applyCalibration(self._currentRawValue)
        if res == YSensor.CURRENTVALUE_INVALID:
            res = self._currentValue
        res = res * self._iresol
        return round(res) / self._iresol

    def set_lowestValue(self, newval):
        """
        Changes the recorded minimal value observed.
        
        @param newval : a floating point number corresponding to the recorded minimal value observed
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval * 65536.0, 1))
        return self._setAttr("lowestValue", rest_val)

    def get_lowestValue(self):
        """
        Returns the minimal value observed for the measure since the device was started.
        
        @return a floating point number corresponding to the minimal value observed for the measure since
        the device was started
        
        On failure, throws an exception or returns YSensor.LOWESTVALUE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.LOWESTVALUE_INVALID
        res = self._lowestValue * self._iresol
        return round(res) / self._iresol

    def set_highestValue(self, newval):
        """
        Changes the recorded maximal value observed.
        
        @param newval : a floating point number corresponding to the recorded maximal value observed
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval * 65536.0, 1))
        return self._setAttr("highestValue", rest_val)

    def get_highestValue(self):
        """
        Returns the maximal value observed for the measure since the device was started.
        
        @return a floating point number corresponding to the maximal value observed for the measure since
        the device was started
        
        On failure, throws an exception or returns YSensor.HIGHESTVALUE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.HIGHESTVALUE_INVALID
        res = self._highestValue * self._iresol
        return round(res) / self._iresol

    def get_currentRawValue(self):
        """
        Returns the uncalibrated, unrounded raw value returned by the sensor.
        
        @return a floating point number corresponding to the uncalibrated, unrounded raw value returned by the sensor
        
        On failure, throws an exception or returns YSensor.CURRENTRAWVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.CURRENTRAWVALUE_INVALID
        return self._currentRawValue

    def get_logFrequency(self):
        """
        Returns the datalogger recording frequency for this function, or "OFF"
        when measures are not stored in the data logger flash memory.
        
        @return a string corresponding to the datalogger recording frequency for this function, or "OFF"
                when measures are not stored in the data logger flash memory
        
        On failure, throws an exception or returns YSensor.LOGFREQUENCY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.LOGFREQUENCY_INVALID
        return self._logFrequency

    def set_logFrequency(self, newval):
        """
        Changes the datalogger recording frequency for this function.
        The frequency can be specified as samples per second,
        as sample per minute (for instance "15/m") or in samples per
        hour (eg. "4/h"). To disable recording for this function, use
        the value "OFF".
        
        @param newval : a string corresponding to the datalogger recording frequency for this function
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logFrequency", rest_val)

    def get_reportFrequency(self):
        """
        Returns the timed value notification frequency, or "OFF" if timed
        value notifications are disabled for this function.
        
        @return a string corresponding to the timed value notification frequency, or "OFF" if timed
                value notifications are disabled for this function
        
        On failure, throws an exception or returns YSensor.REPORTFREQUENCY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.REPORTFREQUENCY_INVALID
        return self._reportFrequency

    def set_reportFrequency(self, newval):
        """
        Changes the timed value notification frequency for this function.
        The frequency can be specified as samples per second,
        as sample per minute (for instance "15/m") or in samples per
        hour (eg. "4/h"). To disable timed value notifications for this
        function, use the value "OFF".
        
        @param newval : a string corresponding to the timed value notification frequency for this function
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("reportFrequency", rest_val)

    def get_calibrationParam(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.CALIBRATIONPARAM_INVALID
        return self._calibrationParam

    def set_calibrationParam(self, newval):
        rest_val = newval
        return self._setAttr("calibrationParam", rest_val)

    def set_resolution(self, newval):
        """
        Changes the resolution of the measured physical values. The resolution corresponds to the numerical precision
        when displaying value. It does not change the precision of the measure itself.
        
        @param newval : a floating point number corresponding to the resolution of the measured physical values
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval * 65536.0, 1))
        return self._setAttr("resolution", rest_val)

    def get_resolution(self):
        """
        Returns the resolution of the measured values. The resolution corresponds to the numerical precision
        of the measures, which is not always the same as the actual precision of the sensor.
        
        @return a floating point number corresponding to the resolution of the measured values
        
        On failure, throws an exception or returns YSensor.RESOLUTION_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YSensor.RESOLUTION_INVALID
        return self._resolution

    @staticmethod
    def FindSensor(func):
        """
        Retrieves a sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSensor.isOnline() to test if the sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the sensor
        
        @return a YSensor object allowing you to drive the sensor.
        """
        # obj
        obj = YFunction._FindFromCache("Sensor", func)
        if obj is None:
            obj = YSensor(func)
            YFunction._AddToCache("Sensor", func, obj)
        return obj

    def _parserHelper(self):
        # position
        # maxpos
        iCalib = []
        # iRaw
        # iRef
        # fRaw
        # fRef
        # // Store inverted resolution, to provide better rounding
        if self._resolution > 0:
            self._iresol = round(1.0 / self._resolution)
        else:
            return 0
        
        self._scale = -1
        del self._calpar[:]
        del self._calraw[:]
        del self._calref[:]
        
        # // Old format: supported when there is no calibration
        if self._calibrationParam == "" or self._calibrationParam == "0":
            self._caltyp = 0
            return 0
        # // Old format: calibrated value will be provided by the device
        if self._calibrationParam.find(",") >= 0:
            self._caltyp = -1
            return 0
        # // New format, decode parameters
        iCalib = YAPI._decodeWords(self._calibrationParam)
        # // In case of unknown format, calibrated value will be provided by the device
        if len(iCalib) < 2:
            self._caltyp = -1
            return 0
        
        # // Save variable format (scale for scalar, or decimal exponent)
        self._isScal = (iCalib[1] > 0)
        if self._isScal:
            self._offset = iCalib[0]
            if self._offset > 32767:
                self._offset = self._offset - 65536
            self._scale = iCalib[1]
            self._decexp = 0
        else:
            self._offset = 0
            self._scale = 1
            self._decexp = 1.0
            position = iCalib[0]
            while position > 0:
                self._decexp = self._decexp * 10
                position = position - 1
        
        # // Shortcut when there is no calibration parameter
        if len(iCalib) == 2:
            self._caltyp = 0
            return 0
        
        self._caltyp = iCalib[2]
        self._calhdl = YAPI._getCalibrationHandler(self._caltyp)
        # // parse calibration points
        position = 3
        if self._caltyp <= 10:
            maxpos = self._caltyp
        else:
            if self._caltyp <= 20:
                maxpos = self._caltyp - 10
            else:
                maxpos = 5
        maxpos = 3 + 2 * maxpos
        if maxpos > len(iCalib):
            maxpos = len(iCalib)
        del self._calpar[:]
        del self._calraw[:]
        del self._calref[:]
        while position + 1 < maxpos:
            iRaw = iCalib[position]
            iRef = iCalib[position + 1]
            self._calpar.append(iRaw)
            self._calpar.append(iRef)
            if self._isScal:
                fRaw = iRaw
                fRaw = (fRaw - self._offset) / self._scale
                fRef = iRef
                fRef = (fRef - self._offset) / self._scale
                self._calraw.append(fRaw)
                self._calref.append(fRef)
            else:
                self._calraw.append(YAPI._decimalToDouble(iRaw))
                self._calref.append(YAPI._decimalToDouble(iRef))
            position = position + 2
        
        
        
        return 0

    def get_recordedData(self, startTime, endTime):
        """
        Retrieves a DataSet object holding historical data for this
        sensor, for a specified time interval. The measures will be
        retrieved from the data logger, which must have been turned
        on at the desired time. See the documentation of the DataSet
        class for information on how to get an overview of the
        recorded data, and how to load progressively a large set
        of measures from the data logger.
        
        This function only works if the device uses a recent firmware,
        as DataSet objects are not supported by firmwares older than
        version 13000.
        
        @param startTime : the start of the desired measure time interval,
                as a Unix timestamp, i.e. the number of seconds since
                January 1, 1970 UTC. The special value 0 can be used
                to include any meaasure, without initial limit.
        @param endTime : the end of the desired measure time interval,
                as a Unix timestamp, i.e. the number of seconds since
                January 1, 1970 UTC. The special value 0 can be used
                to include any meaasure, without ending limit.
        
        @return an instance of YDataSet, providing access to historical
                data. Past measures can be loaded progressively
                using methods from the YDataSet object.
        """
        # funcid
        # funit
        # // may throw an exception
        funcid = self.get_functionId()
        funit = self.get_unit()
        return YDataSet(self, funcid, funit, startTime, endTime)

    def registerTimedReportCallback(self, callback):
        """
        Registers the callback function that is invoked on every periodic timed notification.
        The callback is invoked only during the execution of ySleep or yHandleEvents.
        This provides control over the time when the callback is triggered. For good responsiveness, remember to call
        one of these two functions periodically. To unregister a callback, pass a None pointer as argument.
        
        @param callback : the callback function to call, or a None pointer. The callback function should take two
                arguments: the function object of which the value has changed, and an YMeasure object describing
                the new advertised value.
        @noreturn
        """
        if callback is not None:
            YFunction._UpdateTimedReportCallbackList(self, True)
        else:
            YFunction._UpdateTimedReportCallbackList(self, False)
        self._timedReportCallbackSensor = callback
        return 0

    def _invokeTimedReportCallback(self, value):
        if self._timedReportCallbackSensor is not None:
            self._timedReportCallbackSensor(self, value)
        return 0

    def calibrateFromPoints(self, rawValues, refValues):
        """
        Configures error correction data points, in particular to compensate for
        a possible perturbation of the measure caused by an enclosure. It is possible
        to configure up to five correction points. Correction points must be provided
        in ascending order, and be in the range of the sensor. The device will automatically
        perform a linear interpolation of the error correction between specified
        points. Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        For more information on advanced capabilities to refine the calibration of
        sensors, please contact support@yoctopuce.com.
        
        @param rawValues : array of floating point numbers, corresponding to the raw
                values returned by the sensor for the correction points.
        @param refValues : array of floating point numbers, corresponding to the corrected
                values for the correction points.
        """
        # rest_val
        # // may throw an exception
        rest_val = self._encodeCalibrationPoints(rawValues, refValues)
        return self._setAttr("calibrationParam", rest_val)

    def loadCalibrationPoints(self, rawValues, refValues):
        """
        Retrieves error correction data points previously entered using the method
        calibrateFromPoints.
        
        @param rawValues : array of floating point numbers, that will be filled by the
                function with the raw sensor values for the correction points.
        @param refValues : array of floating point numbers, that will be filled by the
                function with the desired values for the correction points.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        del rawValues[:]
        del refValues[:]
        
        # // Load function parameters if not yet loaded
        if self._scale == 0:
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAPI.DEVICE_NOT_FOUND
        
        if self._caltyp < 0:
            self._throw(YAPI.NOT_SUPPORTED, "Device does not support new calibration parameters. Please upgrade your firmware")
            return YAPI.NOT_SUPPORTED
        del rawValues[:]
        del refValues[:]
        for y in self._calraw:
            rawValues.append(y)
        for y in self._calref:
            refValues.append(y)
        return YAPI.SUCCESS

    def _encodeCalibrationPoints(self, rawValues, refValues):
        # res
        # npt
        # idx
        # iRaw
        # iRef
        
        npt = len(rawValues)
        if npt != len(refValues):
            self._throw(YAPI.INVALID_ARGUMENT, "Invalid calibration parameters (size mismatch)")
            return YAPI.INVALID_STRING
        
        # // Shortcut when building empty calibration parameters
        if npt == 0:
            return "0"
        
        # // Load function parameters if not yet loaded
        if self._scale == 0:
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YAPI.INVALID_STRING
        
        # // Detect old firmware
        if (self._caltyp < 0) or (self._scale < 0):
            self._throw(YAPI.NOT_SUPPORTED, "Device does not support new calibration parameters. Please upgrade your firmware")
            return "0"
        if self._isScal:
            #
            res = "" + str(int(npt))
            idx = 0
            while idx < npt:
                iRaw = round(rawValues[idx] * self._scale - self._offset)
                iRef = round(refValues[idx] * self._scale - self._offset)
                res = "" + res + "," + str(int(iRaw)) + "," + str(int(iRef))
                idx = idx + 1
        else:
            #
            res = "" + str(int(10 + npt))
            idx = 0
            while idx < npt:
                iRaw = YAPI._doubleToDecimal(rawValues[idx])
                iRef = YAPI._doubleToDecimal(refValues[idx])
                res = "" + res + "," + str(int(iRaw)) + "," + str(int(iRef))
                idx = idx + 1
        return res

    def _applyCalibration(self, rawValue):
        if rawValue == YSensor.CURRENTVALUE_INVALID:
            return YSensor.CURRENTVALUE_INVALID
        if self._caltyp == 0:
            return rawValue
        if self._caltyp < 0:
            return YSensor.CURRENTVALUE_INVALID
        if not (self._calhdl is not None):
            return YSensor.CURRENTVALUE_INVALID
        return self._calhdl(rawValue, self._caltyp, self._calpar, self._calraw, self._calref)

    def _decodeTimedReport(self, timestamp, report):
        # i
        # byteVal
        # poww
        # minRaw
        # avgRaw
        # maxRaw
        # startTime
        # endTime
        # minVal
        # avgVal
        # maxVal
        
        startTime = self._prevTimedReport
        endTime = timestamp
        self._prevTimedReport = endTime
        if startTime == 0:
            startTime = endTime
        if report[0] > 0:
            #
            minRaw = report[1] + 0x100 * report[2]
            maxRaw = report[3] + 0x100 * report[4]
            avgRaw = report[5] + 0x100 * report[6] + 0x10000 * report[7]
            byteVal = report[8]
            if ((byteVal) & (0x80)) == 0:
                avgRaw = avgRaw + 0x1000000 * byteVal
            else:
                avgRaw = avgRaw - 0x1000000 * (0x100 - byteVal)
            minVal = self._decodeVal(minRaw)
            avgVal = self._decodeAvg(avgRaw)
            maxVal = self._decodeVal(maxRaw)
        else:
            #
            poww = 1
            avgRaw = 0
            byteVal = 0
            i = 1
            while i < len(report):
                byteVal = report[i]
                avgRaw = avgRaw + poww * byteVal
                poww = poww * 0x100
                i = i + 1
            if self._isScal:
                avgVal = self._decodeVal(avgRaw)
            else:
                if ((byteVal) & (0x80)) != 0:
                    avgRaw = avgRaw - poww
                avgVal = self._decodeAvg(avgRaw)
            minVal = avgVal
            maxVal = avgVal
        
        return YMeasure(startTime, endTime, minVal, avgVal, maxVal)

    def _decodeVal(self, w):
        # val
        val = w
        if self._isScal:
            val = (val - self._offset) / self._scale
        else:
            val = YAPI._decimalToDouble(w)
        if self._caltyp != 0:
            val = self._calhdl(val, self._caltyp, self._calpar, self._calraw, self._calref)
        return val

    def _decodeAvg(self, dw):
        # val
        val = dw
        if self._isScal:
            val = (val / 100 - self._offset) / self._scale
        else:
            val = val / self._decexp
        if self._caltyp != 0:
            val = self._calhdl(val, self._caltyp, self._calpar, self._calraw, self._calref)
        return val

    def nextSensor(self):
        """
        Continues the enumeration of sensors started using yFirstSensor().
        
        @return a pointer to a YSensor object, corresponding to
                a sensor currently online, or a None pointer
                if there are no more sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YSensor.FindSensor(hwidRef.value)

#--- (end of generated code: YSensor implementation)

#--- (generated code: Sensor functions)

    @staticmethod
    def FirstSensor():
        """
        Starts the enumeration of sensors currently accessible.
        Use the method YSensor.nextSensor() to iterate on
        next sensors.
        
        @return a pointer to a YSensor object, corresponding to
                the first sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Sensor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YSensor.FindSensor(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: Sensor functions)
