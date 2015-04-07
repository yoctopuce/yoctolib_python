#*********************************************************************
#*
#* $Id: yocto_motor.py 19610 2015-03-05 10:39:47Z seb $
#*
#* Implements yFindMotor(), the high-level API for Motor functions
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


#--- (YMotor class start)
#noinspection PyProtectedMember
class YMotor(YFunction):
    """
    Yoctopuce application programming interface allows you to drive the
    power sent to the motor to make it turn both ways, but also to drive accelerations
    and decelerations. The motor will then accelerate automatically: you will not
    have to monitor it. The API also allows to slow down the motor by shortening
    its terminals: the motor will then act as an electromagnetic brake.

    """
#--- (end of YMotor class start)
    #--- (YMotor return codes)
    #--- (end of YMotor return codes)
    #--- (YMotor dlldef)
    #--- (end of YMotor dlldef)
    #--- (YMotor definitions)
    DRIVINGFORCE_INVALID = YAPI.INVALID_DOUBLE
    BRAKINGFORCE_INVALID = YAPI.INVALID_DOUBLE
    CUTOFFVOLTAGE_INVALID = YAPI.INVALID_DOUBLE
    OVERCURRENTLIMIT_INVALID = YAPI.INVALID_INT
    FREQUENCY_INVALID = YAPI.INVALID_DOUBLE
    STARTERTIME_INVALID = YAPI.INVALID_INT
    FAILSAFETIMEOUT_INVALID = YAPI.INVALID_UINT
    COMMAND_INVALID = YAPI.INVALID_STRING
    MOTORSTATUS_IDLE = 0
    MOTORSTATUS_BRAKE = 1
    MOTORSTATUS_FORWD = 2
    MOTORSTATUS_BACKWD = 3
    MOTORSTATUS_LOVOLT = 4
    MOTORSTATUS_HICURR = 5
    MOTORSTATUS_HIHEAT = 6
    MOTORSTATUS_FAILSF = 7
    MOTORSTATUS_INVALID = -1
    #--- (end of YMotor definitions)

    def __init__(self, func):
        super(YMotor, self).__init__(func)
        self._className = 'Motor'
        #--- (YMotor attributes)
        self._callback = None
        self._motorStatus = YMotor.MOTORSTATUS_INVALID
        self._drivingForce = YMotor.DRIVINGFORCE_INVALID
        self._brakingForce = YMotor.BRAKINGFORCE_INVALID
        self._cutOffVoltage = YMotor.CUTOFFVOLTAGE_INVALID
        self._overCurrentLimit = YMotor.OVERCURRENTLIMIT_INVALID
        self._frequency = YMotor.FREQUENCY_INVALID
        self._starterTime = YMotor.STARTERTIME_INVALID
        self._failSafeTimeout = YMotor.FAILSAFETIMEOUT_INVALID
        self._command = YMotor.COMMAND_INVALID
        #--- (end of YMotor attributes)

    #--- (YMotor implementation)
    def _parseAttr(self, member):
        if member.name == "motorStatus":
            self._motorStatus = member.ivalue
            return 1
        if member.name == "drivingForce":
            self._drivingForce = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "brakingForce":
            self._brakingForce = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "cutOffVoltage":
            self._cutOffVoltage = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "overCurrentLimit":
            self._overCurrentLimit = member.ivalue
            return 1
        if member.name == "frequency":
            self._frequency = round(member.ivalue * 1000.0 / 65536.0) / 1000.0
            return 1
        if member.name == "starterTime":
            self._starterTime = member.ivalue
            return 1
        if member.name == "failSafeTimeout":
            self._failSafeTimeout = member.ivalue
            return 1
        if member.name == "command":
            self._command = member.svalue
            return 1
        super(YMotor, self)._parseAttr(member)

    def get_motorStatus(self):
        """
        Return the controller state. Possible states are:
        IDLE   when the motor is stopped/in free wheel, ready to start;
        FORWD  when the controller is driving the motor forward;
        BACKWD when the controller is driving the motor backward;
        BRAKE  when the controller is braking;
        LOVOLT when the controller has detected a low voltage condition;
        HICURR when the controller has detected an overcurrent condition;
        HIHEAT when the controller has detected an overheat condition;
        FAILSF when the controller switched on the failsafe security.

        When an error condition occurred (LOVOLT, HICURR, HIHEAT, FAILSF), the controller
        status must be explicitly reset using the resetStatus function.

        @return a value among YMotor.MOTORSTATUS_IDLE, YMotor.MOTORSTATUS_BRAKE, YMotor.MOTORSTATUS_FORWD,
        YMotor.MOTORSTATUS_BACKWD, YMotor.MOTORSTATUS_LOVOLT, YMotor.MOTORSTATUS_HICURR,
        YMotor.MOTORSTATUS_HIHEAT and YMotor.MOTORSTATUS_FAILSF

        On failure, throws an exception or returns YMotor.MOTORSTATUS_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.MOTORSTATUS_INVALID
        return self._motorStatus

    def set_motorStatus(self, newval):
        rest_val = str(newval)
        return self._setAttr("motorStatus", rest_val)

    def set_drivingForce(self, newval):
        """
        Changes immediately the power sent to the motor. The value is a percentage between -100%
        to 100%. If you want go easy on your mechanics and avoid excessive current consumption,
        try to avoid brutal power changes. For example, immediate transition from forward full power
        to reverse full power is a very bad idea. Each time the driving power is modified, the
        braking power is set to zero.

        @param newval : a floating point number corresponding to immediately the power sent to the motor

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("drivingForce", rest_val)

    def get_drivingForce(self):
        """
        Returns the power sent to the motor, as a percentage between -100% and +100%.

        @return a floating point number corresponding to the power sent to the motor, as a percentage
        between -100% and +100%

        On failure, throws an exception or returns YMotor.DRIVINGFORCE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.DRIVINGFORCE_INVALID
        return self._drivingForce

    def set_brakingForce(self, newval):
        """
        Changes immediately the braking force applied to the motor (in percents).
        The value 0 corresponds to no braking (free wheel). When the braking force
        is changed, the driving power is set to zero. The value is a percentage.

        @param newval : a floating point number corresponding to immediately the braking force applied to
        the motor (in percents)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("brakingForce", rest_val)

    def get_brakingForce(self):
        """
        Returns the braking force applied to the motor, as a percentage.
        The value 0 corresponds to no braking (free wheel).

        @return a floating point number corresponding to the braking force applied to the motor, as a percentage

        On failure, throws an exception or returns YMotor.BRAKINGFORCE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.BRAKINGFORCE_INVALID
        return self._brakingForce

    def set_cutOffVoltage(self, newval):
        """
        Changes the threshold voltage under which the controller automatically switches to error state
        and prevents further current draw. This setting prevent damage to a battery that can
        occur when drawing current from an "empty" battery.
        Note that whatever the cutoff threshold, the controller switches to undervoltage
        error state if the power supply goes under 3V, even for a very brief time.

        @param newval : a floating point number corresponding to the threshold voltage under which the
        controller automatically switches to error state
                and prevents further current draw

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("cutOffVoltage", rest_val)

    def get_cutOffVoltage(self):
        """
        Returns the threshold voltage under which the controller automatically switches to error state
        and prevents further current draw. This setting prevents damage to a battery that can
        occur when drawing current from an "empty" battery.

        @return a floating point number corresponding to the threshold voltage under which the controller
        automatically switches to error state
                and prevents further current draw

        On failure, throws an exception or returns YMotor.CUTOFFVOLTAGE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.CUTOFFVOLTAGE_INVALID
        return self._cutOffVoltage

    def get_overCurrentLimit(self):
        """
        Returns the current threshold (in mA) above which the controller automatically
        switches to error state. A zero value means that there is no limit.

        @return an integer corresponding to the current threshold (in mA) above which the controller automatically
                switches to error state

        On failure, throws an exception or returns YMotor.OVERCURRENTLIMIT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.OVERCURRENTLIMIT_INVALID
        return self._overCurrentLimit

    def set_overCurrentLimit(self, newval):
        """
        Changes the current threshold (in mA) above which the controller automatically
        switches to error state. A zero value means that there is no limit. Note that whatever the
        current limit is, the controller switches to OVERCURRENT status if the current
        goes above 32A, even for a very brief time.

        @param newval : an integer corresponding to the current threshold (in mA) above which the
        controller automatically
                switches to error state

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("overCurrentLimit", rest_val)

    def set_frequency(self, newval):
        """
        Changes the PWM frequency used to control the motor. Low frequency is usually
        more efficient and may help the motor to start, but an audible noise might be
        generated. A higher frequency reduces the noise, but more energy is converted
        into heat.

        @param newval : a floating point number corresponding to the PWM frequency used to control the motor

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return self._setAttr("frequency", rest_val)

    def get_frequency(self):
        """
        Returns the PWM frequency used to control the motor.

        @return a floating point number corresponding to the PWM frequency used to control the motor

        On failure, throws an exception or returns YMotor.FREQUENCY_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.FREQUENCY_INVALID
        return self._frequency

    def get_starterTime(self):
        """
        Returns the duration (in ms) during which the motor is driven at low frequency to help
        it start up.

        @return an integer corresponding to the duration (in ms) during which the motor is driven at low
        frequency to help
                it start up

        On failure, throws an exception or returns YMotor.STARTERTIME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.STARTERTIME_INVALID
        return self._starterTime

    def set_starterTime(self, newval):
        """
        Changes the duration (in ms) during which the motor is driven at low frequency to help
        it start up.

        @param newval : an integer corresponding to the duration (in ms) during which the motor is driven
        at low frequency to help
                it start up

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("starterTime", rest_val)

    def get_failSafeTimeout(self):
        """
        Returns the delay in milliseconds allowed for the controller to run autonomously without
        receiving any instruction from the control process. When this delay has elapsed,
        the controller automatically stops the motor and switches to FAILSAFE error.
        Failsafe security is disabled when the value is zero.

        @return an integer corresponding to the delay in milliseconds allowed for the controller to run
        autonomously without
                receiving any instruction from the control process

        On failure, throws an exception or returns YMotor.FAILSAFETIMEOUT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.FAILSAFETIMEOUT_INVALID
        return self._failSafeTimeout

    def set_failSafeTimeout(self, newval):
        """
        Changes the delay in milliseconds allowed for the controller to run autonomously without
        receiving any instruction from the control process. When this delay has elapsed,
        the controller automatically stops the motor and switches to FAILSAFE error.
        Failsafe security is disabled when the value is zero.

        @param newval : an integer corresponding to the delay in milliseconds allowed for the controller to
        run autonomously without
                receiving any instruction from the control process

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("failSafeTimeout", rest_val)

    def get_command(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI.DefaultCacheValidity) != YAPI.SUCCESS:
                return YMotor.COMMAND_INVALID
        return self._command

    def set_command(self, newval):
        rest_val = newval
        return self._setAttr("command", rest_val)

    @staticmethod
    def FindMotor(func):
        """
        Retrieves a motor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>

        This function does not require that the motor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YMotor.isOnline() to test if the motor is
        indeed online at a given time. In case of ambiguity when looking for
        a motor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param func : a string that uniquely characterizes the motor

        @return a YMotor object allowing you to drive the motor.
        """
        # obj
        obj = YFunction._FindFromCache("Motor", func)
        if obj is None:
            obj = YMotor(func)
            YFunction._AddToCache("Motor", func, obj)
        return obj

    def keepALive(self):
        """
        Rearms the controller failsafe timer. When the motor is running and the failsafe feature
        is active, this function should be called periodically to prove that the control process
        is running properly. Otherwise, the motor is automatically stopped after the specified
        timeout. Calling a motor <i>set</i> function implicitely rearms the failsafe timer.
        """
        # // may throw an exception
        return self.set_command("K")

    def resetStatus(self):
        """
        Reset the controller state to IDLE. This function must be invoked explicitely
        after any error condition is signaled.
        """
        # // may throw an exception
        return self.set_motorStatus(YMotor.MOTORSTATUS_IDLE)

    def drivingForceMove(self, targetPower, delay):
        """
        Changes progressively the power sent to the moteur for a specific duration.

        @param targetPower : desired motor power, in percents (between -100% and +100%)
        @param delay : duration (in ms) of the transition

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("P" + str(int(round(targetPower*10))) + "," + str(int(delay)))

    def brakingForceMove(self, targetPower, delay):
        """
        Changes progressively the braking force applied to the motor for a specific duration.

        @param targetPower : desired braking force, in percents
        @param delay : duration (in ms) of the transition

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return self.set_command("B" + str(int(round(targetPower*10))) + "," + str(int(delay)))

    def nextMotor(self):
        """
        Continues the enumeration of motors started using yFirstMotor().

        @return a pointer to a YMotor object, corresponding to
                a motor currently online, or a None pointer
                if there are no more motors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YMotor.FindMotor(hwidRef.value)

#--- (end of YMotor implementation)

#--- (Motor functions)

    @staticmethod
    def FirstMotor():
        """
        Starts the enumeration of motors currently accessible.
        Use the method YMotor.nextMotor() to iterate on
        next motors.

        @return a pointer to a YMotor object, corresponding to
                the first motor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Motor", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YMotor.FindMotor(serialRef.value + "." + funcIdRef.value)

#--- (end of Motor functions)
