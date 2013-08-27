#*********************************************************************
#*
#* $Id: yocto_files.py 12326 2013-08-13 15:52:20Z mvuilleu $
#*
#* Implements yFindFiles(), the high-level API for Files functions
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


class YFileRecord:
    """
    
    """

    #--- (generated code: YFileRecord definitions)



    _FileRecordCache ={}

    #--- (end of generated code: YFileRecord definitions)



    def __init__(self,json):
        self._name = ""
        self._crc  = -1
        self._size = -1
        for member in json.members:
            if member.name == "name":
                self._name = member.svalue
            elif member.name == "crc":
                self._crc = member.ivalue
            elif member.name == "size":
                self._size = member.ivalue


    #--- (generated code: YFileRecord implementation)

    def get_name(self ):
        return self._name

    def get_size(self ):
        return self._size

    def get_crc(self ):
        return self._crc

    def name(self ):
        return self._name

    def size(self ):
        return self._size

    def crc(self ):
        return self._crc

#--- (end of generated code: YFileRecord implementation)

#--- (FileRecord generated code: functions)


#--- (end of FileRecord generated code: functions)




class YFiles(YFunction):
    """
    The filesystem interface makes it possible to store files
    on some devices, for instance to design a custom web UI
    (for networked devices) or to add fonts (on display
    devices).
    
    """
    #--- (generated code: globals)


    #--- (end of generated code: globals)

    #--- (generated code: definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    FILESCOUNT_INVALID              = YAPI.INVALID_LONG
    FREESPACE_INVALID               = YAPI.INVALID_LONG



    _FilesCache ={}

    #--- (end of generated code: definitions)

    #--- (generated code: YFiles implementation)

    def __init__(self,func):
        super(YFiles,self).__init__("Files", func)
        self._callback = None
        self._logicalName = YFiles.LOGICALNAME_INVALID
        self._advertisedValue = YFiles.ADVERTISEDVALUE_INVALID
        self._filesCount = YFiles.FILESCOUNT_INVALID
        self._freeSpace = YFiles.FREESPACE_INVALID

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "filesCount":
                self._filesCount = member.ivalue
            elif member.name == "freeSpace":
                self._freeSpace = member.ivalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the filesystem.
        
        @return a string corresponding to the logical name of the filesystem
        
        On failure, throws an exception or returns YFiles.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YFiles.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the filesystem. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the filesystem
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the filesystem (no more than 6 characters).
        
        @return a string corresponding to the current value of the filesystem (no more than 6 characters)
        
        On failure, throws an exception or returns YFiles.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YFiles.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_filesCount(self):
        """
        Returns the number of files currently loaded in the filesystem.
        
        @return an integer corresponding to the number of files currently loaded in the filesystem
        
        On failure, throws an exception or returns YFiles.FILESCOUNT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YFiles.FILESCOUNT_INVALID
        return self._filesCount

    def get_freeSpace(self):
        """
        Returns the free space for uploading new files to the filesystem, in bytes.
        
        @return an integer corresponding to the free space for uploading new files to the filesystem, in bytes
        
        On failure, throws an exception or returns YFiles.FREESPACE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YFiles.FREESPACE_INVALID
        return self._freeSpace
    def sendCommand(self, command):
        
        url =  "files.json?a="+command
        return self._download(url)
        

    def format_fs(self ):
        """
        Reinitializes the filesystem to its clean, unfragmented, empty state.
        All files previously uploaded are permanently lost.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        
        json = self.sendCommand("format")
        res  = self._json_get_key(json, "res")
        if not (res == "ok") : self._throw( YAPI.IO_ERROR,  "format failed")
        return YAPI.SUCCESS

    def get_list(self, pattern):
        """
        Returns a list of YFileRecord objects that describe files currently loaded
        in the filesystem.
        
        @param pattern : an optional filter pattern, using star and question marks
                as wildcards. When an empty pattern is provided, all file records
                are returned.
        
        @return a list of YFileRecord objects, containing the file path
                and name, byte size and 32-bit CRC of the file content.
        
        On failure, throws an exception or returns an empty list.
        """
        
        list = []
        res = []
        json = self.sendCommand("dir&f="+pattern)
        list = self._json_get_array(json)
        for y in list : res.append( YFileRecord(y))
        return res

    def download(self, pathname):
        """
        Downloads the requested file and returns a binary buffer with its content.
        
        @param pathname : path and name of the new file to load
        
        @return a binary buffer with the file content
        
        On failure, throws an exception or returns an empty content.
        """
        return self._download(pathname)
        

    def upload(self, pathname, content):
        """
        Uploads a file to the filesystem, to the specified full path name.
        If a file already exists with the same path name, its content is overwritten.
        
        @param pathname : path and name of the new file to create
        @param content : binary buffer with the content to set
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        return self._upload(pathname,content)
        

    def remove(self, pathname):
        """
        Deletes a file, given by its full path name, from the filesystem.
        Because of filesystem fragmentation, deleting a file may not always
        free up the whole space used by the file. However, rewriting a file
        with the same path name will always reuse any space not freed previously.
        If you need to ensure that no space is taken by previously deleted files,
        you can use format_fs to fully reinitialize the filesystem.
        
        @param pathname : path and name of the file to remove.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        
        
        json = self.sendCommand("del&f="+pathname)
        res  = self._json_get_key(json, "res")
        if not (res == "ok") : self._throw( YAPI.IO_ERROR,  "unable to remove file")
        return YAPI.SUCCESS


    def nextFiles(self):
        """
        Continues the enumeration of filesystems started using yFirstFiles().
        
        @return a pointer to a YFiles object, corresponding to
                a filesystem currently online, or a None pointer
                if there are no more filesystems to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YFiles.FindFiles(hwidRef.value)

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

#--- (end of generated code: YFiles implementation)

#--- (generated code: Files functions)

    @staticmethod 
    def FindFiles(func):
        """
        Retrieves a filesystem for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the filesystem is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YFiles.isOnline() to test if the filesystem is
        indeed online at a given time. In case of ambiguity when looking for
        a filesystem by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the filesystem
        
        @return a YFiles object allowing you to drive the filesystem.
        """
        if func in YFiles._FilesCache:
            return YFiles._FilesCache[func]
        res =YFiles(func)
        YFiles._FilesCache[func] =  res
        return res

    @staticmethod 
    def  FirstFiles():
        """
        Starts the enumeration of filesystems currently accessible.
        Use the method YFiles.nextFiles() to iterate on
        next filesystems.
        
        @return a pointer to a YFiles object, corresponding to
                the first filesystem currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Files", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YFiles.FindFiles(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _FilesCleanup():
        pass

  #--- (end of generated code: Files functions)

