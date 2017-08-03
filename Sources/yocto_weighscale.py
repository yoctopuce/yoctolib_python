# -*- coding: utf-8 -*-
#*********************************************************************
#*
#* $Id: yocto_weighscale.py 28231 2017-07-31 16:37:33Z mvuilleu $
#*
#* Implements yFindWeighScale(), the high-level API for WeighScale functions
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


#--- (YWeighScale class start)
#noinspection PyProtectedMember
class YWeighScale(YSensor):
    """
    The YWeighScale class provides a weight measurement from a ratiometric load cell
    sensor. It can be used to control the bridge excitation parameters, in order to avoid
    measure shifts caused by temperature variation in the electronics, and can also
    automatically apply an additional correction factor based on temperature to
    compensate for offsets in the load cell itself.

    """
#--- (end of YWeighScale class start)
    #--- (YWeighScale return codes)
    #--- (end of YWeighScale return codes)
    #--- (YWeighScale dlldef)
    #--- (end of YWeighScale dlldef)
    #--- (YWeighScale definitions)
    ADAPTRATIO_INVALID = YAPI.INVALID_DOUBLE
    COMPTEMPERATURE_INVALID = YAPI.INVALID_DOUBLE
    COMPENSATION_INVALID = YAPI.INVALID_DOUBLE
    ZEROTRACKING_INVALID = YAPI.INVALID_DOUBLE
    COMMAND_INVALID = YAPI.INVALID_STRING
    EXCITATION_OFF = 0
    EXCITATION_DC = 1
    EXCITATION_AC = 2
    EXCITATION_INVALID = -1
    #--- (end of YWeighScale definitions)

    def __init__(self, func):
        super(YWeighScale, self).__init__(func)
        self._className = 'WeighScale'
        #--- (YWeighScale attributes)
        self._callback = None
        self._excitation = YWeighScale.EXCITATION_INVALID
        self._adaptRatio = YWeighScale.ADAPTRATIO_INVALID
        self._compTemperature = YWeighScale.COMPTEMPERATURE_INVALID
        self._compensation = YWeighScale.COMPENSATION_INVALID
        self._zeroTracking = YWeighScale.ZEROTRACKING_INVALID
        self._command = YWeighScale.COMMAND_INVALID
        #--- (end of YWeighScale attributes)

    #--- (YWeighScale implementation)
    def _parseAttr(self, json_val):
        if json_val.has("excitation"):
            self._excitation = json_val.getInt("excitation")
        if json_val.has("adaptRatio"):
            self._adaptRatio = round(json_val.getDouble("adaptRatio") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("compTemperature"):
            self._compTemperature = round(json_val.getDouble("compTemperature") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("compensation"):
            self._compensation = round(json_val.getDouble("compensation") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("zeroTracking"):
            self._zeroTracking = round(json_val.getDouble("zeroTracking") * 1000.0 / 65536.0) / 1000.0
        if json_val.has("command"):
            self._command = json_val.getString("command")
        super(YWeighScale, self)._parseAttr(json_val)

    def get_excitation(self):
        """
        Returns the current load cell bridge excitation method.

        @return a value among YWeighScale.EXCITATION_OFF, YWeighScale.EXCITATION_DC and
        YWeighScale.EXCITATION_AC corresponding to the current load cell bridge excitation method

        On failure, throws an exception or returns YWeighScale.EXCITATION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YWeighScale.EXCITATION_INVALID
        res = self._excitation
        return res

    def set_excitation(self, newval):
        """
        Changes the current load cell bridge excitation method.

        @param newval : a value among YWeighScale.EXCITATION_OFF, YWeighScale.EXCITATION_DC and
        YWeighScale.EXCITATION_AC corresponding to the current load cell bridge excitation method

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("excitation", rest_val)

    def set_adaptRatio(self, newval):
        """
        Changes the compensation temperature update rate, in percents.

        @param newval : a floating point number corresponding to the compensation temperature update rate, in percents

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("adaptRatio", rest_val)

    def get_adaptRatio(self):
        """
        Returns the compensation temperature update rate, in percents.
        the maximal value is 65 percents.

        @return a floating point number corresponding to the compensation temperature update rate, in percents

        On failure, throws an exception or returns YWeighScale.ADAPTRATIO_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YWeighScale.ADAPTRATIO_INVALID
        res = self._adaptRatio
        return res

    def get_compTemperature(self):
        """
        Returns the current compensation temperature.

        @return a floating point number corresponding to the current compensation temperature

        On failure, throws an exception or returns YWeighScale.COMPTEMPERATURE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YWeighScale.COMPTEMPERATURE_INVALID
        res = self._compTemperature
        return res

    def get_compensation(self):
        """
        Returns the current current thermal compensation value.

        @return a floating point number corresponding to the current current thermal compensation value

        On failure, throws an exception or returns YWeighScale.COMPENSATION_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YWeighScale.COMPENSATION_INVALID
        res = self._compensation
        return res

    def set_zeroTracking(self, newval):
        """
        Changes the compensation temperature update rate, in percents.

        @param newval : a floating point number corresponding to the compensation temperature update rate, in percents

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("zeroTracking", rest_val)

    def get_zeroTracking(self):
        """
        Returns the zero tracking threshold value. When this threshold is larger than
        zero, any measure under the threshold will automatically be ignored and the
        zero compensation will be updated.

        @return a floating point number corresponding to the zero tracking threshold value

        On failure, throws an exception or returns YWeighScale.ZEROTRACKING_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YWeighScale.ZEROTRACKING_INVALID
        res = self._zeroTracking
        return res

    def get_command(self):
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YWeighScale.COMMAND_INVALID
        res = self._command
        return res

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindWeighScale(func):
        """
        Retrieves a weighing scale sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the weighing scale sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWeighScale.isOnline() to test if the weighing scale sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a weighing scale sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the weighing scale sensor

        @return a YWeighScale object allowing you to drive the weighing scale sensor.
        """
        # obj
        obj = YFunction._FindFromCache("WeighScale", func)
        if obj is None:
            obj = YWeighScale(func)
            YFunction._AddToCache("WeighScale", func, obj)
        return obj

    def tare(self):
        """
        Adapts the load cell signal bias (stored in the corresponding genericSensor)
        so that the current signal corresponds to a zero weight.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("T")

    def setupSpan(self, currWeight, maxWeight):
        """
        Configures the load cell span parameters (stored in the corresponding genericSensor)
        so that the current signal corresponds to the specified reference weight.

        @param currWeight : reference weight presently on the load cell.
        @param maxWeight : maximum weight to be expectect on the load cell.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("S" + str(int(round(1000*currWeight))) + ":" + str(int(round(1000*maxWeight))))

    def set_offsetCompensationTable(self, tempValues, compValues):
        """
        Records a weight offset thermal compensation table, in order to automatically correct the
        measured weight based on the compensation temperature.
        The weight correction will be applied by linear interpolation between specified points.

        @param tempValues : array of floating point numbers, corresponding to all
                temperatures for which an offset correction is specified.
        @param compValues : array of floating point numbers, corresponding to the offset correction
                to apply for each of the temperature included in the first
                argument, index by index.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # siz
        # res
        # idx
        # found
        # prev
        # curr
        # currComp
        # idxTemp
        siz = len(tempValues)
        if not (siz != 1):
            self._throw(YAPI.INVALID_ARGUMENT, "thermal compensation table must have at least two points")
        if not (siz == len(compValues)):
            self._throw(YAPI.INVALID_ARGUMENT, "table sizes mismatch")

        res = self.set_command("2Z")
        if not (res==YAPI.SUCCESS):
            self._throw(YAPI.IO_ERROR, "unable to reset thermal compensation table")
        # // add records in growing temperature value
        found = 1
        prev = -999999.0
        while found > 0:
            found = 0
            curr = 99999999.0
            currComp = -999999.0
            idx = 0
            while idx < siz:
                idxTemp = tempValues[idx]
                if (idxTemp > prev) and (idxTemp < curr):
                    curr = idxTemp
                    currComp = compValues[idx]
                    found = 1
                idx = idx + 1
            if found > 0:
                res = self.set_command("2m" + str(int(round(1000*curr))) + ":" + str(int(round(1000*currComp))))
                if not (res==YAPI.SUCCESS):
                    self._throw(YAPI.IO_ERROR, "unable to set thermal compensation table")
                prev = curr
        return YAPI.SUCCESS

    def loadOffsetCompensationTable(self, tempValues, compValues):
        """
        Retrieves the weight offset thermal compensation table previously configured using the
        set_offsetCompensationTable function.
        The weight correction is applied by linear interpolation between specified points.

        @param tempValues : array of floating point numbers, that is filled by the function
                with all temperatures for which an offset correction is specified.
        @param compValues : array of floating point numbers, that is filled by the function
                with the offset correction applied for each of the temperature
                included in the first argument, index by index.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # id
        # bin_json
        paramlist = []
        # siz
        # idx
        # temp
        # comp

        id = self.get_functionId()
        id = (id)[11: 11 + len(id) - 11]
        bin_json = self._download("extra.json?page=2")
        paramlist = self._json_get_array(bin_json)
        # // convert all values to float and append records
        siz = ((len(paramlist)) >> (1))
        del tempValues[:]
        del compValues[:]
        idx = 0
        while idx < siz:
            temp = float(paramlist[2*idx])/1000.0
            comp = float(paramlist[2*idx+1])/1000.0
            tempValues.append(temp)
            compValues.append(comp)
            idx = idx + 1


        return YAPI.SUCCESS

    def set_spanCompensationTable(self, tempValues, compValues):
        """
        Records a weight span thermal compensation table, in order to automatically correct the
        measured weight based on the compensation temperature.
        The weight correction will be applied by linear interpolation between specified points.

        @param tempValues : array of floating point numbers, corresponding to all
                temperatures for which a span correction is specified.
        @param compValues : array of floating point numbers, corresponding to the span correction
                (in percents) to apply for each of the temperature included in the first
                argument, index by index.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # siz
        # res
        # idx
        # found
        # prev
        # curr
        # currComp
        # idxTemp
        siz = len(tempValues)
        if not (siz != 1):
            self._throw(YAPI.INVALID_ARGUMENT, "thermal compensation table must have at least two points")
        if not (siz == len(compValues)):
            self._throw(YAPI.INVALID_ARGUMENT, "table sizes mismatch")

        res = self.set_command("3Z")
        if not (res==YAPI.SUCCESS):
            self._throw(YAPI.IO_ERROR, "unable to reset thermal compensation table")
        # // add records in growing temperature value
        found = 1
        prev = -999999.0
        while found > 0:
            found = 0
            curr = 99999999.0
            currComp = -999999.0
            idx = 0
            while idx < siz:
                idxTemp = tempValues[idx]
                if (idxTemp > prev) and (idxTemp < curr):
                    curr = idxTemp
                    currComp = compValues[idx]
                    found = 1
                idx = idx + 1
            if found > 0:
                res = self.set_command("3m" + str(int(round(1000*curr))) + ":" + str(int(round(1000*currComp))))
                if not (res==YAPI.SUCCESS):
                    self._throw(YAPI.IO_ERROR, "unable to set thermal compensation table")
                prev = curr
        return YAPI.SUCCESS

    def loadSpanCompensationTable(self, tempValues, compValues):
        """
        Retrieves the weight span thermal compensation table previously configured using the
        set_spanCompensationTable function.
        The weight correction is applied by linear interpolation between specified points.

        @param tempValues : array of floating point numbers, that is filled by the function
                with all temperatures for which an span correction is specified.
        @param compValues : array of floating point numbers, that is filled by the function
                with the span correction applied for each of the temperature
                included in the first argument, index by index.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        # id
        # bin_json
        paramlist = []
        # siz
        # idx
        # temp
        # comp

        id = self.get_functionId()
        id = (id)[11: 11 + len(id) - 11]
        bin_json = self._download("extra.json?page=3")
        paramlist = self._json_get_array(bin_json)
        # // convert all values to float and append records
        siz = ((len(paramlist)) >> (1))
        del tempValues[:]
        del compValues[:]
        idx = 0
        while idx < siz:
            temp = float(paramlist[2*idx])/1000.0
            comp = float(paramlist[2*idx+1])/1000.0
            tempValues.append(temp)
            compValues.append(comp)
            idx = idx + 1


        return YAPI.SUCCESS

    def nextWeighScale(self):
        """
        Continues the enumeration of weighing scale sensors started using yFirstWeighScale().

        @return a pointer to a YWeighScale object, corresponding to
                a weighing scale sensor currently online, or a None pointer
                if there are no more weighing scale sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YWeighScale.FindWeighScale(hwidRef.value)

#--- (end of YWeighScale implementation)

#--- (WeighScale functions)

    @staticmethod
    def FirstWeighScale():
        """
        Starts the enumeration of weighing scale sensors currently accessible.
        Use the method YWeighScale.nextWeighScale() to iterate on
        next weighing scale sensors.

        @return a pointer to a YWeighScale object, corresponding to
                the first weighing scale sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("WeighScale", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YWeighScale.FindWeighScale(serialRef.value + "." + funcIdRef.value)

#--- (end of WeighScale functions)
