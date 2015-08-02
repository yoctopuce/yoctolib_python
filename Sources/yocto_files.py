#*********************************************************************
#*
#* $Id: yocto_files.py 19610 2015-03-05 10:39:47Z seb $
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


#--- (generated code: YFileRecord class start)
#noinspection PyProtectedMember
class YFileRecord(object):
#--- (end of generated code: YFileRecord class start)
    #--- (generated code: YFileRecord definitions)
    #--- (end of generated code: YFileRecord definitions)

    def __init__(self, json):
    #--- (generated code: YFileRecord attributes)
        self._name = ''
        self._size = 0
        self._crc = 0
        #--- (end of generated code: YFileRecord attributes)
        self._crc = -1
        self._size = -1
        j = YAPI.TJsonParser(json, False)
        node = j.GetRootNode()
        for member in node.members:
            if member.name == "name":
                self._name = member.svalue
            elif member.name == "crc":
                self._crc = member.ivalue
            elif member.name == "size":
                self._size = member.ivalue

    #--- (generated code: YFileRecord implementation)
    def get_name(self):
        return self._name

    def get_size(self):
        return self._size

    def get_crc(self):
        return self._crc

#--- (end of generated code: YFileRecord implementation)

#--- (FileRecord generated code: functions)

#--- (end of FileRecord generated code: functions)


#--- (generated code: YFiles class start)
#noinspection PyProtectedMember
class YFiles(YFunction):
    """
    The filesystem interface makes it possible to store files
    on some devices, for instance to design a custom web UI
    (for networked devices) or to add fonts (on display
    devices).

    """
#--- (end of generated code: YFiles class start)
    #--- (generated code: YFiles definitions)
    FILESCOUNT_INVALID = YAPI.INVALID_UINT
    FREESPACE_INVALID = YAPI.INVALID_UINT
    #--- (end of generated code: YFiles definitions)

    def __init__(self, func):
        super(YFiles, self).__init__(func)
        self._className = "Files"
        #--- (generated code: YFiles attributes)
        self._callback = None
        self._filesCount = YFiles.FILESCOUNT_INVALID
        self._freeSpace = YFiles.FREESPACE_INVALID
        #--- (end of generated code: YFiles attributes)

    #--- (generated code: YFiles implementation)
    def _parseAttr(self, member):
        if member.name == "filesCount":
            self._filesCount = member.ivalue
            return 1
        if member.name == "freeSpace":
            self._freeSpace = member.ivalue
            return 1
        super(YFiles, self)._parseAttr(member)

    def get_filesCount(self):
        """
        Returns the number of files currently loaded in the filesystem.

        @return an integer corresponding to the number of files currently loaded in the filesystem

        On failure, throws an exception or returns YFiles.FILESCOUNT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YFiles.FILESCOUNT_INVALID
        return self._filesCount

    def get_freeSpace(self):
        """
        Returns the free space for uploading new files to the filesystem, in bytes.

        @return an integer corresponding to the free space for uploading new files to the filesystem, in bytes

        On failure, throws an exception or returns YFiles.FREESPACE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YFiles.FREESPACE_INVALID
        return self._freeSpace

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
        # obj
        obj = YFunction._FindFromCache("Files", func)
        if obj is None:
            obj = YFiles(func)
            YFunction._AddToCache("Files", func, obj)
        return obj

    def sendCommand(self, command):
        # url
        url = "files.json?a=" + command
        # // may throw an exception
        return self._download(url)

    def format_fs(self):
        """
        Reinitialize the filesystem to its clean, unfragmented, empty state.
        All files previously uploaded are permanently lost.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # json
        # res
        json = self.sendCommand("format")
        res = self._json_get_key(json, "res")
        if not (res == "ok"):
            self._throw(YAPI.IO_ERROR, "format failed")
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
        # json
        filelist = []
        res = []
        json = self.sendCommand("dir&f=" + pattern)
        filelist = self._json_get_array(json)
        del res[:]
        for y in filelist:
            res.append(YFileRecord(y))
        return res

    def download(self, pathname):
        """
        Downloads the requested file and returns a binary buffer with its content.

        @param pathname : path and name of the file to download

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
        return self._upload(pathname, content)

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
        # json
        # res
        json = self.sendCommand("del&f=" + pathname)
        res  = self._json_get_key(json, "res")
        if not (res == "ok"):
            self._throw(YAPI.IO_ERROR, "unable to remove file")
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

#--- (end of generated code: YFiles implementation)

#--- (generated code: Files functions)

    @staticmethod
    def FirstFiles():
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
        p = (ctypes.c_int * 1)()
        err = YAPI.apiGetFunctionsByClass("Files", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YFiles.FindFiles(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: Files functions)

