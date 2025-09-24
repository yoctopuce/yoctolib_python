# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Implements yFindRfidReader(), the high-level API for RfidReader functions
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

def yInternalEventCallback(obj, value):
    obj._internalEventHandler(value)

#--- (generated code: YRfidTagInfo class start)
#noinspection PyProtectedMember
class YRfidTagInfo(object):
    """
    YRfidTagInfo objects are used to describe RFID tag attributes,
    such as the tag type and its storage size. These objects are returned by
    method get_tagInfo() of class YRfidReader.

    """
    #--- (end of generated code: YRfidTagInfo class start)
    #--- (generated code: YRfidTagInfo return codes)
    #--- (end of generated code: YRfidTagInfo return codes)
    #--- (generated code: YRfidTagInfo dlldef)
    #--- (end of generated code: YRfidTagInfo dlldef)
    #--- (generated code: YRfidTagInfo yapiwrapper)
    #--- (end of generated code: YRfidTagInfo yapiwrapper)
    #--- (generated code: YRfidTagInfo definitions)
    IEC_15693 = 1
    IEC_14443 = 2
    IEC_14443_MIFARE_ULTRALIGHT = 3
    IEC_14443_MIFARE_CLASSIC1K = 4
    IEC_14443_MIFARE_CLASSIC4K = 5
    IEC_14443_MIFARE_DESFIRE = 6
    IEC_14443_NTAG_213 = 7
    IEC_14443_NTAG_215 = 8
    IEC_14443_NTAG_216 = 9
    IEC_14443_NTAG_424_DNA = 10
    #--- (end of generated code: YRfidTagInfo definitions)

    def __init__(self):
        super(YRfidTagInfo, self).__init__()
        self._className = 'RfidTagInfo'
        #--- (generated code: YRfidTagInfo attributes)
        self._tagId = ''
        self._tagType = 0
        self._typeStr = ''
        self._size = 0
        self._usable = 0
        self._blksize = 0
        self._fblk = 0
        self._lblk = 0
        #--- (end of generated code: YRfidTagInfo attributes)

    #--- (generated code: YRfidTagInfo implementation)
    def get_tagId(self):
        """
        Returns the RFID tag identifier.

        @return a string with the RFID tag identifier.
        """
        return self._tagId

    def get_tagType(self):
        """
        Returns the type of the RFID tag, as a numeric constant.
        (IEC_14443_MIFARE_CLASSIC1K, ...).

        @return an integer corresponding to the RFID tag type
        """
        return self._tagType

    def get_tagTypeStr(self):
        """
        Returns the type of the RFID tag, as a string.

        @return a string corresponding to the RFID tag type
        """
        return self._typeStr

    def get_tagMemorySize(self):
        """
        Returns the total memory size of the RFID tag, in bytes.

        @return the total memory size of the RFID tag
        """
        return self._size

    def get_tagUsableSize(self):
        """
        Returns the usable storage size of the RFID tag, in bytes.

        @return the usable storage size of the RFID tag
        """
        return self._usable

    def get_tagBlockSize(self):
        """
        Returns the block size of the RFID tag, in bytes.

        @return the block size of the RFID tag
        """
        return self._blksize

    def get_tagFirstBlock(self):
        """
        Returns the index of the block available for data storage on the RFID tag.
        Some tags have special block used to configure the tag behavior, these
        blocks must be handled with precaution. However, the  block return by
        get_tagFirstBlock() can be locked, use get_tagLockState()
        to find out  which block are locked.

        @return the index of the first usable storage block on the RFID tag
        """
        return self._fblk

    def get_tagLastBlock(self):
        """
        Returns the index of the last last black available for data storage on the RFID tag,
        However, this block can be locked, use get_tagLockState() to find out
        which block are locked.

        @return the index of the last usable storage block on the RFID tag
        """
        return self._lblk

    def imm_init(self, tagId, tagType, size, usable, blksize, fblk, lblk):
        # typeStr
        typeStr = "unknown"
        if tagType == YRfidTagInfo.IEC_15693:
            typeStr = "IEC 15693"
        if tagType == YRfidTagInfo.IEC_14443:
            typeStr = "IEC 14443"
        if tagType == YRfidTagInfo.IEC_14443_MIFARE_ULTRALIGHT:
            typeStr = "MIFARE Ultralight"
        if tagType == YRfidTagInfo.IEC_14443_MIFARE_CLASSIC1K:
            typeStr = "MIFARE Classic 1K"
        if tagType == YRfidTagInfo.IEC_14443_MIFARE_CLASSIC4K:
            typeStr = "MIFARE Classic 4K"
        if tagType == YRfidTagInfo.IEC_14443_MIFARE_DESFIRE:
            typeStr = "MIFARE DESFire"
        if tagType == YRfidTagInfo.IEC_14443_NTAG_213:
            typeStr = "NTAG 213"
        if tagType == YRfidTagInfo.IEC_14443_NTAG_215:
            typeStr = "NTAG 215"
        if tagType == YRfidTagInfo.IEC_14443_NTAG_216:
            typeStr = "NTAG 216"
        if tagType == YRfidTagInfo.IEC_14443_NTAG_424_DNA:
            typeStr = "NTAG 424 DNA"
        self._tagId = tagId
        self._tagType = tagType
        self._typeStr = typeStr
        self._size = size
        self._usable = usable
        self._blksize = blksize
        self._fblk = fblk
        self._lblk = lblk

#--- (end of generated code: YRfidTagInfo implementation)

#--- (generated code: YRfidTagInfo functions)
#--- (end of generated code: YRfidTagInfo functions)

#--- (generated code: YRfidStatus class start)
#noinspection PyProtectedMember
class YRfidStatus(object):
    """
    YRfidStatus objects provide additional information about
    operations on RFID tags, including the range of blocks affected
    by read/write operations and possible errors when communicating
    with RFID tags.
    This makes it possible, for example, to distinguish communication
    errors that can be recovered by an additional attempt, from
    security or other errors on the tag.
    Combined with the EnableDryRun option in RfidOptions,
    this structure can be used to predict which blocks will be affected
    by a write operation.

    """
    #--- (end of generated code: YRfidStatus class start)
    #--- (generated code: YRfidStatus return codes)
    #--- (end of generated code: YRfidStatus return codes)
    #--- (generated code: YRfidStatus dlldef)
    #--- (end of generated code: YRfidStatus dlldef)
    #--- (generated code: YRfidStatus yapiwrapper)
    #--- (end of generated code: YRfidStatus yapiwrapper)
    #--- (generated code: YRfidStatus definitions)
    SUCCESS = 0
    COMMAND_NOT_SUPPORTED = 1
    COMMAND_NOT_RECOGNIZED = 2
    COMMAND_OPTION_NOT_RECOGNIZED = 3
    COMMAND_CANNOT_BE_PROCESSED_IN_TIME = 4
    UNDOCUMENTED_ERROR = 15
    BLOCK_NOT_AVAILABLE = 16
    BLOCK_ALREADY_LOCKED = 17
    BLOCK_LOCKED = 18
    BLOCK_NOT_SUCESSFULLY_PROGRAMMED = 19
    BLOCK_NOT_SUCESSFULLY_LOCKED = 20
    BLOCK_IS_PROTECTED = 21
    CRYPTOGRAPHIC_ERROR = 64
    READER_BUSY = 1000
    TAG_NOTFOUND = 1001
    TAG_LEFT = 1002
    TAG_JUSTLEFT = 1003
    TAG_COMMUNICATION_ERROR = 1004
    TAG_NOT_RESPONDING = 1005
    TIMEOUT_ERROR = 1006
    COLLISION_DETECTED = 1007
    INVALID_CMD_ARGUMENTS = -66
    UNKNOWN_CAPABILITIES = -67
    MEMORY_NOT_SUPPORTED = -68
    INVALID_BLOCK_INDEX = -69
    MEM_SPACE_UNVERRUN_ATTEMPT = -70
    BROWNOUT_DETECTED = -71
    BUFFER_OVERFLOW = -72
    CRC_ERROR = -73
    COMMAND_RECEIVE_TIMEOUT = -75
    DID_NOT_SLEEP = -76
    ERROR_DECIMAL_EXPECTED = -77
    HARDWARE_FAILURE = -78
    ERROR_HEX_EXPECTED = -79
    FIFO_LENGTH_ERROR = -80
    FRAMING_ERROR = -81
    NOT_IN_CNR_MODE = -82
    NUMBER_OU_OF_RANGE = -83
    NOT_SUPPORTED = -84
    NO_RF_FIELD_ACTIVE = -85
    READ_DATA_LENGTH_ERROR = -86
    WATCHDOG_RESET = -87
    UNKNOW_COMMAND = -91
    UNKNOW_ERROR = -92
    UNKNOW_PARAMETER = -93
    UART_RECEIVE_ERROR = -94
    WRONG_DATA_LENGTH = -95
    WRONG_MODE = -96
    UNKNOWN_DWARFxx_ERROR_CODE = -97
    RESPONSE_SHORT = -98
    UNEXPECTED_TAG_ID_IN_RESPONSE = -99
    UNEXPECTED_TAG_INDEX = -100
    READ_EOF = -101
    READ_OK_SOFAR = -102
    WRITE_DATA_MISSING = -103
    WRITE_TOO_MUCH_DATA = -104
    TRANSFER_CLOSED = -105
    COULD_NOT_BUILD_REQUEST = -106
    INVALID_OPTIONS = -107
    UNEXPECTED_RESPONSE = -108
    AFI_NOT_AVAILABLE = -109
    DSFID_NOT_AVAILABLE = -110
    TAG_RESPONSE_TOO_SHORT = -111
    DEC_EXPECTED = -112
    HEX_EXPECTED = -113
    NOT_SAME_SECOR = -114
    MIFARE_AUTHENTICATED = -115
    NO_DATABLOCK = -116
    KEYB_IS_READABLE = -117
    OPERATION_NOT_EXECUTED = -118
    BLOK_MODE_ERROR = -119
    BLOCK_NOT_WRITABLE = -120
    BLOCK_ACCESS_ERROR = -121
    BLOCK_NOT_AUTHENTICATED = -122
    ACCESS_KEY_BIT_NOT_WRITABLE = -123
    USE_KEYA_FOR_AUTH = -124
    USE_KEYB_FOR_AUTH = -125
    KEY_NOT_CHANGEABLE = -126
    BLOCK_TOO_HIGH = -127
    AUTH_ERR = -128
    NOKEY_SELECT = -129
    CARD_NOT_SELECTED = -130
    BLOCK_TO_READ_NONE = -131
    NO_TAG = -132
    TOO_MUCH_DATA = -133
    CON_NOT_SATISFIED = -134
    BLOCK_IS_SPECIAL = -135
    READ_BEYOND_ANNOUNCED_SIZE = -136
    BLOCK_ZERO_IS_RESERVED = -137
    VALUE_BLOCK_BAD_FORMAT = -138
    ISO15693_ONLY_FEATURE = -139
    ISO14443_ONLY_FEATURE = -140
    MIFARE_CLASSIC_ONLY_FEATURE = -141
    BLOCK_MIGHT_BE_PROTECTED = -142
    NO_SUCH_BLOCK = -143
    COUNT_TOO_BIG = -144
    UNKNOWN_MEM_SIZE = -145
    MORE_THAN_2BLOCKS_MIGHT_NOT_WORK = -146
    READWRITE_NOT_SUPPORTED = -147
    UNEXPECTED_VICC_ID_IN_RESPONSE = -148
    LOCKBLOCK_NOT_SUPPORTED = -150
    INTERNAL_ERROR_SHOULD_NEVER_HAPPEN = -151
    INVLD_BLOCK_MODE_COMBINATION = -152
    INVLD_ACCESS_MODE_COMBINATION = -153
    INVALID_SIZE = -154
    BAD_PASSWORD_FORMAT = -155
    RADIO_IS_OFF = -156
    #--- (end of generated code: YRfidStatus definitions)

    def __init__(self):
        super(YRfidStatus, self).__init__()
        self._className = 'RfidStatus'
        #--- (generated code: YRfidStatus attributes)
        self._tagId = ''
        self._errCode = 0
        self._errBlk = 0
        self._errMsg = ''
        self._yapierr = 0
        self._fab = 0
        self._lab = 0
        #--- (end of generated code: YRfidStatus attributes)

    #--- (generated code: YRfidStatus implementation)
    def get_tagId(self):
        """
        Returns RFID tag identifier related to the status.

        @return a string with the RFID tag identifier.
        """
        return self._tagId

    def get_errorCode(self):
        """
        Returns the detailled error code, or 0 if no error happened.

        @return a numeric error code
        """
        return self._errCode

    def get_errorBlock(self):
        """
        Returns the RFID tag memory block number where the error was encountered, or -1 if the
        error is not specific to a memory block.

        @return an RFID tag block number
        """
        return self._errBlk

    def get_errorMessage(self):
        """
        Returns a string describing precisely the RFID commande result.

        @return an error message string
        """
        return self._errMsg

    def get_yapiError(self):
        return self._yapierr

    def get_firstAffectedBlock(self):
        """
        Returns the block number of the first RFID tag memory block affected
        by the operation. Depending on the type of operation and on the tag
        memory granularity, this number may be smaller than the requested
        memory block index.

        @return an RFID tag block number
        """
        return self._fab

    def get_lastAffectedBlock(self):
        """
        Returns the block number of the last RFID tag memory block affected
        by the operation. Depending on the type of operation and on the tag
        memory granularity, this number may be bigger than the requested
        memory block index.

        @return an RFID tag block number
        """
        return self._lab

    def imm_init(self, tagId, errCode, errBlk, fab, lab):
        # errMsg
        if errCode == 0:
            self._yapierr = YAPI.SUCCESS
            errMsg = "Success (no error)"
        else:
            if errCode < 0:
                if errCode > -50:
                    self._yapierr = errCode
                    errMsg = "YoctoLib error " + str(int(errCode))
                else:
                    self._yapierr = YAPI.RFID_HARD_ERROR
                    errMsg = "Non-recoverable RFID error " + str(int(errCode))
            else:
                if errCode > 1000:
                    self._yapierr = YAPI.RFID_SOFT_ERROR
                    errMsg = "Recoverable RFID error " + str(int(errCode))
                else:
                    self._yapierr = YAPI.RFID_HARD_ERROR
                    errMsg = "Non-recoverable RFID error " + str(int(errCode))
            if errCode == YRfidStatus.TAG_NOTFOUND:
                errMsg = "Tag not found"
            if errCode == YRfidStatus.TAG_JUSTLEFT:
                errMsg = "Tag left during operation"
            if errCode == YRfidStatus.TAG_LEFT:
                errMsg = "Tag not here anymore"
            if errCode == YRfidStatus.READER_BUSY:
                errMsg = "Reader is busy"
            if errCode == YRfidStatus.INVALID_CMD_ARGUMENTS:
                errMsg = "Invalid command arguments"
            if errCode == YRfidStatus.UNKNOWN_CAPABILITIES:
                errMsg = "Unknown capabilities"
            if errCode == YRfidStatus.MEMORY_NOT_SUPPORTED:
                errMsg = "Memory no present"
            if errCode == YRfidStatus.INVALID_BLOCK_INDEX:
                errMsg = "Invalid block index"
            if errCode == YRfidStatus.MEM_SPACE_UNVERRUN_ATTEMPT:
                errMsg = "Tag memory space overrun attempt"
            if errCode == YRfidStatus.COMMAND_NOT_SUPPORTED:
                errMsg = "The command is not supported"
            if errCode == YRfidStatus.COMMAND_NOT_RECOGNIZED:
                errMsg = "The command is not recognized"
            if errCode == YRfidStatus.COMMAND_OPTION_NOT_RECOGNIZED:
                errMsg = "The command option is not supported."
            if errCode == YRfidStatus.COMMAND_CANNOT_BE_PROCESSED_IN_TIME:
                errMsg = "The command cannot be processed in time"
            if errCode == YRfidStatus.UNDOCUMENTED_ERROR:
                errMsg = "Error with no information given"
            if errCode == YRfidStatus.BLOCK_NOT_AVAILABLE:
                errMsg = "Block is not available"
            if errCode == YRfidStatus.BLOCK_ALREADY_LOCKED:
                errMsg = "Block / byte is already locked and thus cannot be locked again."
            if errCode == YRfidStatus.BLOCK_LOCKED:
                errMsg = "Block / byte is locked and its content cannot be changed"
            if errCode == YRfidStatus.BLOCK_NOT_SUCESSFULLY_PROGRAMMED:
                errMsg = "Block was not successfully programmed"
            if errCode == YRfidStatus.BLOCK_NOT_SUCESSFULLY_LOCKED:
                errMsg = "Block was not successfully locked"
            if errCode == YRfidStatus.BLOCK_IS_PROTECTED:
                errMsg = "Block is protected"
            if errCode == YRfidStatus.CRYPTOGRAPHIC_ERROR:
                errMsg = "Generic cryptographic error"
            if errCode == YRfidStatus.BROWNOUT_DETECTED:
                errMsg = "BrownOut detected (BOD)"
            if errCode == YRfidStatus.BUFFER_OVERFLOW:
                errMsg = "Buffer Overflow (BOF)"
            if errCode == YRfidStatus.CRC_ERROR:
                errMsg = "Communication CRC Error (CCE)"
            if errCode == YRfidStatus.COLLISION_DETECTED:
                errMsg = "Collision Detected (CLD/CDT)"
            if errCode == YRfidStatus.COMMAND_RECEIVE_TIMEOUT:
                errMsg = "Command Receive Timeout (CRT)"
            if errCode == YRfidStatus.DID_NOT_SLEEP:
                errMsg = "Did Not Sleep (DNS)"
            if errCode == YRfidStatus.ERROR_DECIMAL_EXPECTED:
                errMsg = "Error Decimal Expected (EDX)"
            if errCode == YRfidStatus.HARDWARE_FAILURE:
                errMsg = "Error Hardware Failure (EHF)"
            if errCode == YRfidStatus.ERROR_HEX_EXPECTED:
                errMsg = "Error Hex Expected (EHX)"
            if errCode == YRfidStatus.FIFO_LENGTH_ERROR:
                errMsg = "FIFO length error (FLE)"
            if errCode == YRfidStatus.FRAMING_ERROR:
                errMsg = "Framing error (FER)"
            if errCode == YRfidStatus.NOT_IN_CNR_MODE:
                errMsg = "Not in CNR Mode (NCM)"
            if errCode == YRfidStatus.NUMBER_OU_OF_RANGE:
                errMsg = "Number Out of Range (NOR)"
            if errCode == YRfidStatus.NOT_SUPPORTED:
                errMsg = "Not Supported (NOS)"
            if errCode == YRfidStatus.NO_RF_FIELD_ACTIVE:
                errMsg = "No RF field active (NRF)"
            if errCode == YRfidStatus.READ_DATA_LENGTH_ERROR:
                errMsg = "Read data length error (RDL)"
            if errCode == YRfidStatus.WATCHDOG_RESET:
                errMsg = "Watchdog reset (SRT)"
            if errCode == YRfidStatus.TAG_COMMUNICATION_ERROR:
                errMsg = "Tag Communication Error (TCE)"
            if errCode == YRfidStatus.TAG_NOT_RESPONDING:
                errMsg = "Tag Not Responding (TNR)"
            if errCode == YRfidStatus.TIMEOUT_ERROR:
                errMsg = "TimeOut Error (TOE)"
            if errCode == YRfidStatus.UNKNOW_COMMAND:
                errMsg = "Unknown Command (UCO)"
            if errCode == YRfidStatus.UNKNOW_ERROR:
                errMsg = "Unknown error (UER)"
            if errCode == YRfidStatus.UNKNOW_PARAMETER:
                errMsg = "Unknown Parameter (UPA)"
            if errCode == YRfidStatus.UART_RECEIVE_ERROR:
                errMsg = "UART Receive Error (URE)"
            if errCode == YRfidStatus.WRONG_DATA_LENGTH:
                errMsg = "Wrong Data Length (WDL)"
            if errCode == YRfidStatus.WRONG_MODE:
                errMsg = "Wrong Mode (WMO)"
            if errCode == YRfidStatus.UNKNOWN_DWARFxx_ERROR_CODE:
                errMsg = "Unknown DWARF15 error code"
            if errCode == YRfidStatus.UNEXPECTED_TAG_ID_IN_RESPONSE:
                errMsg = "Unexpected Tag id in response"
            if errCode == YRfidStatus.UNEXPECTED_TAG_INDEX:
                errMsg = "internal error : unexpected TAG index"
            if errCode == YRfidStatus.TRANSFER_CLOSED:
                errMsg = "transfer closed"
            if errCode == YRfidStatus.WRITE_DATA_MISSING:
                errMsg = "Missing write data"
            if errCode == YRfidStatus.WRITE_TOO_MUCH_DATA:
                errMsg = "Attempt to write too much data"
            if errCode == YRfidStatus.COULD_NOT_BUILD_REQUEST:
                errMsg = "Could not not request"
            if errCode == YRfidStatus.INVALID_OPTIONS:
                errMsg = "Invalid transfer options"
            if errCode == YRfidStatus.UNEXPECTED_RESPONSE:
                errMsg = "Unexpected Tag response"
            if errCode == YRfidStatus.AFI_NOT_AVAILABLE:
                errMsg = "AFI not available"
            if errCode == YRfidStatus.DSFID_NOT_AVAILABLE:
                errMsg = "DSFID not available"
            if errCode == YRfidStatus.TAG_RESPONSE_TOO_SHORT:
                errMsg = "Tag's response too short"
            if errCode == YRfidStatus.DEC_EXPECTED:
                errMsg = "Error Decimal value Expected, or is missing"
            if errCode == YRfidStatus.HEX_EXPECTED:
                errMsg = "Error Hexadecimal value Expected, or is missing"
            if errCode == YRfidStatus.NOT_SAME_SECOR:
                errMsg = "Input and Output block are not in the same Sector"
            if errCode == YRfidStatus.MIFARE_AUTHENTICATED:
                errMsg = "No chip with MIFARE Classic technology Authenticated"
            if errCode == YRfidStatus.NO_DATABLOCK:
                errMsg = "No Data Block"
            if errCode == YRfidStatus.KEYB_IS_READABLE:
                errMsg = "Key B is Readable"
            if errCode == YRfidStatus.OPERATION_NOT_EXECUTED:
                errMsg = "Operation Not Executed, would have caused an overflow"
            if errCode == YRfidStatus.BLOK_MODE_ERROR:
                errMsg = "Block has not been initialized as a 'value block'"
            if errCode == YRfidStatus.BLOCK_NOT_WRITABLE:
                errMsg = "Block Not Writable"
            if errCode == YRfidStatus.BLOCK_ACCESS_ERROR:
                errMsg = "Block Access Error"
            if errCode == YRfidStatus.BLOCK_NOT_AUTHENTICATED:
                errMsg = "Block Not Authenticated"
            if errCode == YRfidStatus.ACCESS_KEY_BIT_NOT_WRITABLE:
                errMsg = "Access bits or Keys not Writable"
            if errCode == YRfidStatus.USE_KEYA_FOR_AUTH:
                errMsg = "Use Key B for authentication"
            if errCode == YRfidStatus.USE_KEYB_FOR_AUTH:
                errMsg = "Use Key A for authentication"
            if errCode == YRfidStatus.KEY_NOT_CHANGEABLE:
                errMsg = "Key(s) not changeable"
            if errCode == YRfidStatus.BLOCK_TOO_HIGH:
                errMsg = "Block index is too high"
            if errCode == YRfidStatus.AUTH_ERR:
                errMsg = "Authentication Error (i.e. wrong key)"
            if errCode == YRfidStatus.NOKEY_SELECT:
                errMsg = "No Key Select, select a temporary or a static key"
            if errCode == YRfidStatus.CARD_NOT_SELECTED:
                errMsg = " Card is Not Selected"
            if errCode == YRfidStatus.BLOCK_TO_READ_NONE:
                errMsg = "Number of Blocks to Read is 0"
            if errCode == YRfidStatus.NO_TAG:
                errMsg = "No Tag detected"
            if errCode == YRfidStatus.TOO_MUCH_DATA:
                errMsg = "Too Much Data (i.e. Uart input buffer overflow)"
            if errCode == YRfidStatus.CON_NOT_SATISFIED:
                errMsg = "Conditions Not Satisfied"
            if errCode == YRfidStatus.BLOCK_IS_SPECIAL:
                errMsg = "Bad parameter: block is a special block"
            if errCode == YRfidStatus.READ_BEYOND_ANNOUNCED_SIZE:
                errMsg = "Attempt to read more than announced size."
            if errCode == YRfidStatus.BLOCK_ZERO_IS_RESERVED:
                errMsg = "Block 0 is reserved and cannot be used"
            if errCode == YRfidStatus.VALUE_BLOCK_BAD_FORMAT:
                errMsg = "One value block is not properly initialized"
            if errCode == YRfidStatus.ISO15693_ONLY_FEATURE:
                errMsg = "Feature available on ISO 15693 only"
            if errCode == YRfidStatus.ISO14443_ONLY_FEATURE:
                errMsg = "Feature available on ISO 14443 only"
            if errCode == YRfidStatus.MIFARE_CLASSIC_ONLY_FEATURE:
                errMsg = "Feature available on ISO 14443 MIFARE Classic only"
            if errCode == YRfidStatus.BLOCK_MIGHT_BE_PROTECTED:
                errMsg = "Block might be protected"
            if errCode == YRfidStatus.NO_SUCH_BLOCK:
                errMsg = "No such block"
            if errCode == YRfidStatus.COUNT_TOO_BIG:
                errMsg = "Count parameter is too large"
            if errCode == YRfidStatus.UNKNOWN_MEM_SIZE:
                errMsg = "Tag memory size is unknown"
            if errCode == YRfidStatus.MORE_THAN_2BLOCKS_MIGHT_NOT_WORK:
                errMsg = "Writing more than two blocks at once might not be supported by this tag"
            if errCode == YRfidStatus.READWRITE_NOT_SUPPORTED:
                errMsg = "Read/write operation not supported for this tag"
            if errCode == YRfidStatus.UNEXPECTED_VICC_ID_IN_RESPONSE:
                errMsg = "Unexpected VICC ID in response"
            if errCode == YRfidStatus.LOCKBLOCK_NOT_SUPPORTED:
                errMsg = "This tag does not support the Lock block function"
            if errCode == YRfidStatus.INTERNAL_ERROR_SHOULD_NEVER_HAPPEN:
                errMsg = "Yoctopuce RFID code ran into an unexpected state, please contact support"
            if errCode == YRfidStatus.INVLD_BLOCK_MODE_COMBINATION:
                errMsg = "Invalid combination of block mode options"
            if errCode == YRfidStatus.INVLD_ACCESS_MODE_COMBINATION:
                errMsg = "Invalid combination of access mode options"
            if errCode == YRfidStatus.INVALID_SIZE:
                errMsg = "Invalid data size parameter"
            if errCode == YRfidStatus.BAD_PASSWORD_FORMAT:
                errMsg = "Bad password format or type"
            if errCode == YRfidStatus.RADIO_IS_OFF:
                errMsg = "Radio is OFF (refreshRate=0)."
            if errBlk >= 0:
                errMsg = "" + errMsg + " (block " + str(int(errBlk)) + ")"
        self._tagId = tagId
        self._errCode = errCode
        self._errBlk = errBlk
        self._errMsg = errMsg
        self._fab = fab
        self._lab = lab

#--- (end of generated code: YRfidStatus implementation)

#--- (generated code: YRfidStatus functions)
#--- (end of generated code: YRfidStatus functions)

#--- (generated code: YRfidOptions class start)
#noinspection PyProtectedMember
class YRfidOptions(object):
    """
    The YRfidOptions objects are used to specify additional
    optional parameters to RFID commands that interact with tags,
    including security keys. When instantiated,the parameters of
    this object are pre-initialized to a value  which corresponds
    to the most common usage.

    """
    #--- (end of generated code: YRfidOptions class start)
    #--- (generated code: YRfidOptions return codes)
    #--- (end of generated code: YRfidOptions return codes)
    #--- (generated code: YRfidOptions dlldef)
    #--- (end of generated code: YRfidOptions dlldef)
    #--- (generated code: YRfidOptions yapiwrapper)
    #--- (end of generated code: YRfidOptions yapiwrapper)
    #--- (generated code: YRfidOptions definitions)
    NO_RFID_KEY = 0
    MIFARE_KEY_A = 1
    MIFARE_KEY_B = 2
    #--- (end of generated code: YRfidOptions definitions)

    def __init__(self):
        #--- (generated code: YRfidOptions attributes)
        """
        Type of security key to be used to access the RFID tag.
        For MIFARE Classic tags, allowed values are
        Y_MIFARE_KEY_A or Y_MIFARE_KEY_B.
        The default value is Y_NO_RFID_KEY, in that case
        the reader will use the most common default key for the
        tag type.
        When a security key is required, it must be provided
        using property HexKey.
        """
        self.KeyType = 0
        """
        Security key to be used to access the RFID tag, as an
        hexadecimal string. The key will only be used if you
        also specify which type of key it is, using property
        KeyType.
        """
        self.HexKey = ''
        """
        Forces the use of single-block commands to access RFID tag memory blocks.
        By default, the Yoctopuce library uses the most efficient access strategy
        generally available for each tag type, but you can force the use of
        single-block commands if the RFID tags you are using do not support
        multi-block commands. If operation speed is not a priority, choose
        single-block mode as it will work with any mode.
        """
        self.ForceSingleBlockAccess = 0
        """
        Forces the use of multi-block commands to access RFID tag memory blocks.
        By default, the Yoctopuce library uses the most efficient access strategy
        generally available for each tag type, but you can force the use of
        multi-block commands if you know for sure that the RFID tags you are using
        do support multi-block commands. Be  aware that even if a tag allows multi-block
        operations, the maximum number of blocks that can be written or read at the same
        time can be (very) limited. If the tag does not support multi-block mode
        for the wanted operation, the option will be ignored.
        """
        self.ForceMultiBlockAccess = 0
        """
        Enables direct access to RFID tag control blocks.
        By default, Yoctopuce library read and write functions only work
        on data blocks and automatically skip special blocks, as specific functions are provided
        to configure security parameters found in control blocks.
        If you need to access control blocks in your own way using
        read/write functions, enable this option.  Use this option wisely,
        as overwriting a special block migth very well irreversibly alter your
        tag behavior.
        """
        self.EnableRawAccess = 0
        """
        Disables the tag memory overflow test. By default, the Yoctopuce
        library's read/write functions detect overruns and do not run
        commands that are likely to fail. If you nevertheless wish to
        try to access more memory than the tag announces, you can try to use
        this option.
        """
        self.DisableBoundaryChecks = 0
        """
        Enables simulation mode to check the affected block range as well
        as access rights. When this option is active, the operation is
        not fully applied to the RFID tag but the affected block range
        is determined and the optional access key is tested on these blocks.
        The access key rights are not tested though. This option applies to
        write / configure operations only, it is ignored for read operations.
        """
        self.EnableDryRun = 0
        #--- (end of generated code: YRfidOptions attributes)

    #--- (generated code: YRfidOptions implementation)
    def imm_getParams(self):
        # opt
        # res
        if self.ForceSingleBlockAccess:
            opt = 1
        else:
            opt = 0
        if self.ForceMultiBlockAccess:
            opt = (opt | 2)
        if self.EnableRawAccess:
            opt = (opt | 4)
        if self.DisableBoundaryChecks:
            opt = (opt | 8)
        if self.EnableDryRun:
            opt = (opt | 16)
        res = "&o=" + str(int(opt))
        if self.KeyType != 0:
            res = "" + res + "&k=" + ("%02x" % self.KeyType) + ":" + self.HexKey
        return res

#--- (end of generated code: YRfidOptions implementation)

#--- (generated code: YRfidOptions functions)
#--- (end of generated code: YRfidOptions functions)


#--- (generated code: YRfidReader class start)
#noinspection PyProtectedMember
class YRfidReader(YFunction):
    """
    The YRfidReader class allows you to detect RFID tags, as well as
    read and write on these tags if the security settings allow it.

    Short reminder:

    - A tag's memory is generally organized in fixed-size blocks.
    - At tag level, each block must be read and written in its entirety.
    - Some blocks are special configuration blocks, and may alter the tag's behavior
    if they are rewritten with arbitrary data.
    - Data blocks can be set to read-only mode, but on many tags, this operation is irreversible.


    By default, the RfidReader class automatically manages these blocks so that
    arbitrary size data  can be manipulated of  without risk and without knowledge of
    tag architecture.

    """
    #--- (end of generated code: YRfidReader class start)
    #--- (generated code: YRfidReader return codes)
    #--- (end of generated code: YRfidReader return codes)
    #--- (generated code: YRfidReader dlldef)
    #--- (end of generated code: YRfidReader dlldef)
    #--- (generated code: YRfidReader yapiwrapper)
    #--- (end of generated code: YRfidReader yapiwrapper)
    #--- (generated code: YRfidReader definitions)
    NTAGS_INVALID = YAPI.INVALID_UINT
    REFRESHRATE_INVALID = YAPI.INVALID_UINT
    #--- (end of generated code: YRfidReader definitions)

    def __init__(self, func):
        super(YRfidReader, self).__init__(func)
        self._className = 'RfidReader'
        #--- (generated code: YRfidReader attributes)
        self._callback = None
        self._nTags = YRfidReader.NTAGS_INVALID
        self._refreshRate = YRfidReader.REFRESHRATE_INVALID
        self._eventCallback = None
        self._isFirstCb = 0
        self._prevCbPos = 0
        self._eventPos = 0
        self._eventStamp = 0
        #--- (end of generated code: YRfidReader attributes)

    #--- (generated code: YRfidReader implementation)
    def _parseAttr(self, json_val):
        if json_val.has("nTags"):
            self._nTags = json_val.getInt("nTags")
        if json_val.has("refreshRate"):
            self._refreshRate = json_val.getInt("refreshRate")
        super(YRfidReader, self)._parseAttr(json_val)

    def get_nTags(self):
        """
        Returns the number of RFID tags currently detected.

        @return an integer corresponding to the number of RFID tags currently detected

        On failure, throws an exception or returns YRfidReader.NTAGS_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YRfidReader.NTAGS_INVALID
        res = self._nTags
        return res

    def get_refreshRate(self):
        """
        Returns the tag list refresh rate, measured in Hz.

        @return an integer corresponding to the tag list refresh rate, measured in Hz

        On failure, throws an exception or returns YRfidReader.REFRESHRATE_INVALID.
        """
        # res
        if self._cacheExpiration <= YAPI.GetTickCount():
            if self.load(YAPI._yapiContext.GetCacheValidity()) != YAPI.SUCCESS:
                return YRfidReader.REFRESHRATE_INVALID
        res = self._refreshRate
        return res

    def set_refreshRate(self, newval):
        """
        Changes the present tag list refresh rate, measured in Hz. The reader will do
        its best to respect it. Note that the reader cannot detect tag arrival or removal
        while it is  communicating with a tag.  Maximum frequency is limited to 100Hz,
        but in real life it will be difficult to do better than 50Hz.  A zero value
        will power off the device radio.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.

        @param newval : an integer corresponding to the present tag list refresh rate, measured in Hz

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return self._setAttr("refreshRate", rest_val)

    @staticmethod
    def FindRfidReader(func):
        """
        Retrieves a RFID reader for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the RFID reader is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRfidReader.isOnline() to test if the RFID reader is
        indeed online at a given time. In case of ambiguity when looking for
        a RFID reader by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the RFID reader, for instance
                MyDevice.rfidReader.

        @return a YRfidReader object allowing you to drive the RFID reader.
        """
        # obj
        obj = YFunction._FindFromCache("RfidReader", func)
        if obj is None:
            obj = YRfidReader(func)
            YFunction._AddToCache("RfidReader", func, obj)
        return obj

    def _chkerror(self, tagId, json, status):
        # jsonStr
        # errCode
        # errBlk
        # fab
        # lab
        # retcode

        if len(json) == 0:
            errCode = self.get_errorType()
            errBlk = -1
            fab = -1
            lab = -1
        else:
            jsonStr = json.decode(YAPI.DefaultEncoding)
            errCode = YAPI._atoi(self._json_get_key(json, "err"))
            errBlk = YAPI._atoi(self._json_get_key(json, "errBlk"))-1
            if jsonStr.find("\"fab\":") >= 0:
                fab = YAPI._atoi(self._json_get_key(json, "fab"))-1
                lab = YAPI._atoi(self._json_get_key(json, "lab"))-1
            else:
                fab = -1
                lab = -1
        status.imm_init(tagId, errCode, errBlk, fab, lab)
        retcode = status.get_yapiError()
        if not (retcode == YAPI.SUCCESS):
            self._throw(retcode, status.get_errorMessage())
            return retcode
        return YAPI.SUCCESS

    def reset(self):
        # json
        # status
        status = YRfidStatus()

        json = self._download("rfid.json?a=reset")
        return self._chkerror("", json, status)

    def get_tagIdList(self):
        """
        Returns the list of RFID tags currently detected by the reader.

        @return a list of strings, corresponding to each tag identifier (UID).

        On failure, throws an exception or returns an empty list.
        """
        # json
        jsonList = []
        taglist = []

        json = self._download("rfid.json?a=list")
        del taglist[:]
        if len(json) > 3:
            jsonList = self._json_get_array(json)
            for ii_0 in jsonList:
                taglist.append(self._json_get_string(ii_0))
        return taglist

    def get_tagInfo(self, tagId, status):
        """
        Returns a description of the properties of an existing RFID tag.
        This function can cause communications with the tag.

        @param tagId : identifier of the tag to check
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return a YRfidTagInfo object.

        On failure, throws an exception or returns an empty YRfidTagInfo objact.
        When it happens, you can get more information from the status object.
        """
        # url
        # json
        # tagType
        # size
        # usable
        # blksize
        # fblk
        # lblk
        # res
        url = "rfid.json?a=info&t=" + tagId

        json = self._download(url)
        self._chkerror(tagId, json, status)
        tagType = YAPI._atoi(self._json_get_key(json, "type"))
        size = YAPI._atoi(self._json_get_key(json, "size"))
        usable = YAPI._atoi(self._json_get_key(json, "usable"))
        blksize = YAPI._atoi(self._json_get_key(json, "blksize"))
        fblk = YAPI._atoi(self._json_get_key(json, "fblk"))
        lblk = YAPI._atoi(self._json_get_key(json, "lblk"))
        res = YRfidTagInfo()
        res.imm_init(tagId, tagType, size, usable, blksize, fblk, lblk)
        return res

    def tagLockBlocks(self, tagId, firstBlock, nBlocks, options, status):
        """
        Changes an RFID tag configuration to prevents any further write to
        the selected blocks. This operation is definitive and irreversible.
        Depending on the tag type and block index, adjascent blocks may become
        read-only as well, based on the locking granularity.

        @param tagId : identifier of the tag to use
        @param firstBlock : first block to lock
        @param nBlocks : number of blocks to lock
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        optstr = options.imm_getParams()
        url = "rfid.json?a=lock&t=" + tagId + "&b=" + str(int(firstBlock)) + "&n=" + str(int(nBlocks)) + "" + optstr

        json = self._download(url)
        return self._chkerror(tagId, json, status)

    def get_tagLockState(self, tagId, firstBlock, nBlocks, options, status):
        """
        Reads the locked state for RFID tag memory data blocks.
        FirstBlock cannot be a special block, and any special
        block encountered in the middle of the read operation will be
        skipped automatically.

        @param tagId : identifier of the tag to use
        @param firstBlock : number of the first block to check
        @param nBlocks : number of blocks to check
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return a list of booleans with the lock state of selected blocks

        On failure, throws an exception or returns an empty list. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        # binRes
        res = []
        # idx
        # val
        # isLocked
        optstr = options.imm_getParams()
        url = "rfid.json?a=chkl&t=" + tagId + "&b=" + str(int(firstBlock)) + "&n=" + str(int(nBlocks)) + "" + optstr

        json = self._download(url)
        self._chkerror(tagId, json, status)
        if status.get_yapiError() != YAPI.SUCCESS:
            return res

        binRes = YAPI._hexStrToBin(self._json_get_key(json, "bitmap"))
        idx = 0
        while idx < nBlocks:
            val = binRes[(idx >> 3)]
            isLocked = (((val) & ((1 << ((idx) & (7))))) != 0)
            res.append(isLocked)
            idx = idx + 1

        return res

    def get_tagSpecialBlocks(self, tagId, firstBlock, nBlocks, options, status):
        """
        Tells which block of a RFID tag memory are special and cannot be used
        to store user data. Mistakely writing a special block can lead to
        an irreversible alteration of the tag.

        @param tagId : identifier of the tag to use
        @param firstBlock : number of the first block to check
        @param nBlocks : number of blocks to check
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return a list of booleans with the lock state of selected blocks

        On failure, throws an exception or returns an empty list. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        # binRes
        res = []
        # idx
        # val
        # isLocked
        optstr = options.imm_getParams()
        url = "rfid.json?a=chks&t=" + tagId + "&b=" + str(int(firstBlock)) + "&n=" + str(int(nBlocks)) + "" + optstr

        json = self._download(url)
        self._chkerror(tagId, json, status)
        if status.get_yapiError() != YAPI.SUCCESS:
            return res

        binRes = YAPI._hexStrToBin(self._json_get_key(json, "bitmap"))
        idx = 0
        while idx < nBlocks:
            val = binRes[(idx >> 3)]
            isLocked = (((val) & ((1 << ((idx) & (7))))) != 0)
            res.append(isLocked)
            idx = idx + 1

        return res

    def tagReadHex(self, tagId, firstBlock, nBytes, options, status):
        """
        Reads data from an RFID tag memory, as an hexadecimal string.
        The read operation may span accross multiple blocks if the requested
        number of bytes is larger than the RFID tag block size. By default
        firstBlock cannot be a special block, and any special block encountered
        in the middle of the read operation will be skipped automatically.
        If you rather want to read special blocks, use the EnableRawAccess
        field from the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where read should start
        @param nBytes : total number of bytes to read
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return an hexadecimal string if the call succeeds.

        On failure, throws an exception or returns an empty binary buffer. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        # hexbuf
        optstr = options.imm_getParams()
        url = "rfid.json?a=read&t=" + tagId + "&b=" + str(int(firstBlock)) + "&n=" + str(int(nBytes)) + "" + optstr

        json = self._download(url)
        self._chkerror(tagId, json, status)
        if status.get_yapiError() == YAPI.SUCCESS:
            hexbuf = self._json_get_key(json, "res")
        else:
            hexbuf = ""
        return hexbuf

    def tagReadBin(self, tagId, firstBlock, nBytes, options, status):
        """
        Reads data from an RFID tag memory, as a binary buffer. The read operation
        may span accross multiple blocks if the requested number of bytes
        is larger than the RFID tag block size.  By default
        firstBlock cannot be a special block, and any special block encountered
        in the middle of the read operation will be skipped automatically.
        If you rather want to read special blocks, use the EnableRawAccess
        field frrm the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where read should start
        @param nBytes : total number of bytes to read
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return a binary object with the data read if the call succeeds.

        On failure, throws an exception or returns an empty binary buffer. When it
        happens, you can get more information from the status object.
        """
        return YAPI._hexStrToBin(self.tagReadHex(tagId, firstBlock, nBytes, options, status))

    def tagReadArray(self, tagId, firstBlock, nBytes, options, status):
        """
        Reads data from an RFID tag memory, as a byte list. The read operation
        may span accross multiple blocks if the requested number of bytes
        is larger than the RFID tag block size.  By default
        firstBlock cannot be a special block, and any special block encountered
        in the middle of the read operation will be skipped automatically.
        If you rather want to read special blocks, use the EnableRawAccess
        field from the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where read should start
        @param nBytes : total number of bytes to read
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return a byte list with the data read if the call succeeds.

        On failure, throws an exception or returns an empty list. When it
        happens, you can get more information from the status object.
        """
        # blk
        # idx
        # endidx
        res = []
        blk = self.tagReadBin(tagId, firstBlock, nBytes, options, status)
        endidx = len(blk)

        idx = 0
        while idx < endidx:
            res.append(blk[idx])
            idx = idx + 1

        return res

    def tagReadStr(self, tagId, firstBlock, nChars, options, status):
        """
        Reads data from an RFID tag memory, as a text string. The read operation
        may span accross multiple blocks if the requested number of bytes
        is larger than the RFID tag block size.  By default
        firstBlock cannot be a special block, and any special block encountered
        in the middle of the read operation will be skipped automatically.
        If you rather want to read special blocks, use the EnableRawAccess
        field from the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where read should start
        @param nChars : total number of characters to read
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return a text string with the data read if the call succeeds.

        On failure, throws an exception or returns an empty string. When it
        happens, you can get more information from the status object.
        """
        return self.tagReadBin(tagId, firstBlock, nChars, options, status).decode(YAPI.DefaultEncoding)

    def tagWriteBin(self, tagId, firstBlock, buff, options, status):
        """
        Writes data provided as a binary buffer to an RFID tag memory.
        The write operation may span accross multiple blocks if the
        number of bytes to write is larger than the RFID tag block size.
        By default firstBlock cannot be a special block, and any special block
        encountered in the middle of the write operation will be skipped
        automatically. The last data block affected by the operation will
        be automatically padded with zeros if neccessary.  If you rather want
        to rewrite special blocks as well,
        use the EnableRawAccess field from the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where write should start
        @param buff : the binary buffer to write
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # hexstr
        # buflen
        # fname
        # json
        buflen = len(buff)
        if buflen <= 16:
            # // short data, use an URL-based command
            hexstr = YAPI._bytesToHexStr(buff)
            return self.tagWriteHex(tagId, firstBlock, hexstr, options, status)
        else:
            # // long data, use an upload command
            optstr = options.imm_getParams()
            fname = "Rfid:t=" + tagId + "&b=" + str(int(firstBlock)) + "&n=" + str(int(buflen)) + "" + optstr
            json = self._uploadEx(fname, buff)
            return self._chkerror(tagId, json, status)

    def tagWriteArray(self, tagId, firstBlock, byteList, options, status):
        """
        Writes data provided as a list of bytes to an RFID tag memory.
        The write operation may span accross multiple blocks if the
        number of bytes to write is larger than the RFID tag block size.
        By default firstBlock cannot be a special block, and any special block
        encountered in the middle of the write operation will be skipped
        automatically. The last data block affected by the operation will
        be automatically padded with zeros if neccessary.
        If you rather want to rewrite special blocks as well,
        use the EnableRawAccess field from the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where write should start
        @param byteList : a list of byte to write
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # bufflen
        # buff
        # idx
        # hexb
        bufflen = len(byteList)
        buff = bytearray(bufflen)
        idx = 0
        while idx < bufflen:
            hexb = byteList[idx]
            buff[idx] = hexb
            idx = idx + 1

        return self.tagWriteBin(tagId, firstBlock, buff, options, status)

    def tagWriteHex(self, tagId, firstBlock, hexString, options, status):
        """
        Writes data provided as an hexadecimal string to an RFID tag memory.
        The write operation may span accross multiple blocks if the
        number of bytes to write is larger than the RFID tag block size.
        By default firstBlock cannot be a special block, and any special block
        encountered in the middle of the write operation will be skipped
        automatically. The last data block affected by the operation will
        be automatically padded with zeros if neccessary.
        If you rather want to rewrite special blocks as well,
        use the EnableRawAccess field from the options parameter.

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where write should start
        @param hexString : a string of hexadecimal byte codes to write
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # bufflen
        # optstr
        # url
        # json
        # buff
        # idx
        # hexb
        bufflen = len(hexString)
        bufflen = (bufflen >> 1)
        if bufflen <= 16:
            # // short data, use an URL-based command
            optstr = options.imm_getParams()
            url = "rfid.json?a=writ&t=" + tagId + "&b=" + str(int(firstBlock)) + "&w=" + hexString + "" + optstr
            json = self._download(url)
            return self._chkerror(tagId, json, status)
        else:
            # // long data, use an upload command
            buff = bytearray(bufflen)
            idx = 0
            while idx < bufflen:
                hexb = int((hexString)[2 * idx: 2 * idx + 2], 16)
                buff[idx] = hexb
                idx = idx + 1
            return self.tagWriteBin(tagId, firstBlock, buff, options, status)

    def tagWriteStr(self, tagId, firstBlock, text, options, status):
        """
        Writes data provided as an ASCII string to an RFID tag memory.
        The write operation may span accross multiple blocks if the
        number of bytes to write is larger than the RFID tag block size.
        Note that only the characters present in the provided string
        will be written, there is no notion of string length. If your
        string data have variable length, you'll have to encode the
        string length yourself, with a terminal zero for instannce.

        This function only works with ISO-latin characters, if you wish to
        write strings encoded with alternate character sets, you'll have to
        use tagWriteBin() function.

        By default firstBlock cannot be a special block, and any special block
        encountered in the middle of the write operation will be skipped
        automatically. The last data block affected by the operation will
        be automatically padded with zeros if neccessary.
        If you rather want to rewrite special blocks as well,
        use the EnableRawAccess field from the options parameter
        (definitely not recommanded).

        @param tagId : identifier of the tag to use
        @param firstBlock : block number where write should start
        @param text : the text string to write
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # buff
        buff = bytearray(text, YAPI.DefaultEncoding)

        return self.tagWriteBin(tagId, firstBlock, buff, options, status)

    def tagGetAFI(self, tagId, options, status):
        """
        Reads an RFID tag AFI byte (ISO 15693 only).

        @param tagId : identifier of the tag to use
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return the AFI value (0...255)

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        # res
        optstr = options.imm_getParams()
        url = "rfid.json?a=rdsf&t=" + tagId + "&b=0" + optstr

        json = self._download(url)
        self._chkerror(tagId, json, status)
        if status.get_yapiError() == YAPI.SUCCESS:
            res = YAPI._atoi(self._json_get_key(json, "res"))
        else:
            res = status.get_yapiError()
        return res

    def tagSetAFI(self, tagId, afi, options, status):
        """
        Changes an RFID tag AFI byte (ISO 15693 only).

        @param tagId : identifier of the tag to use
        @param afi : the AFI value to write (0...255)
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        optstr = options.imm_getParams()
        url = "rfid.json?a=wrsf&t=" + tagId + "&b=0&v=" + str(int(afi)) + "" + optstr

        json = self._download(url)
        return self._chkerror(tagId, json, status)

    def tagLockAFI(self, tagId, options, status):
        """
        Locks the RFID tag AFI byte (ISO 15693 only).
        This operation is definitive and irreversible.

        @param tagId : identifier of the tag to use
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        optstr = options.imm_getParams()
        url = "rfid.json?a=lksf&t=" + tagId + "&b=0" + optstr

        json = self._download(url)
        return self._chkerror(tagId, json, status)

    def tagGetDSFID(self, tagId, options, status):
        """
        Reads an RFID tag DSFID byte (ISO 15693 only).

        @param tagId : identifier of the tag to use
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return the DSFID value (0...255)

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        # res
        optstr = options.imm_getParams()
        url = "rfid.json?a=rdsf&t=" + tagId + "&b=1" + optstr

        json = self._download(url)
        self._chkerror(tagId, json, status)
        if status.get_yapiError() == YAPI.SUCCESS:
            res = YAPI._atoi(self._json_get_key(json, "res"))
        else:
            res = status.get_yapiError()
        return res

    def tagSetDSFID(self, tagId, dsfid, options, status):
        """
        Changes an RFID tag DSFID byte (ISO 15693 only).

        @param tagId : identifier of the tag to use
        @param dsfid : the DSFID value to write (0...255)
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        optstr = options.imm_getParams()
        url = "rfid.json?a=wrsf&t=" + tagId + "&b=1&v=" + str(int(dsfid)) + "" + optstr

        json = self._download(url)
        return self._chkerror(tagId, json, status)

    def tagLockDSFID(self, tagId, options, status):
        """
        Locks the RFID tag DSFID byte (ISO 15693 only).
        This operation is definitive and irreversible.

        @param tagId : identifier of the tag to use
        @param options : an YRfidOptions object with the optional
                command execution parameters, such as security key
                if required
        @param status : an RfidStatus object that will contain
                the detailled status of the operation

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code. When it
        happens, you can get more information from the status object.
        """
        # optstr
        # url
        # json
        optstr = options.imm_getParams()
        url = "rfid.json?a=lksf&t=" + tagId + "&b=1" + optstr

        json = self._download(url)
        return self._chkerror(tagId, json, status)

    def get_lastEvents(self):
        """
        Returns a string with last tag arrival/removal events observed.
        This method return only events that are still buffered in the device memory.

        @return a string with last events observed (one per line).

        On failure, throws an exception or returns  YAPI.INVALID_STRING.
        """
        # content

        content = self._download("events.txt?pos=0")
        return content.decode(YAPI.DefaultEncoding)

    def registerEventCallback(self, callback):
        """
        Registers a callback function to be called each time that an RFID tag appears or
        disappears. The callback is invoked only during the execution of
        ySleep or yHandleEvents. This provides control over the time when
        the callback is triggered. For good responsiveness, remember to call one of these
        two functions periodically. To unregister a callback, pass a None pointer as argument.

        @param callback : the callback function to call, or a None pointer.
                The callback function should take four arguments:
                the YRfidReader object that emitted the event, the
                UTC timestamp of the event, a character string describing
                the type of event ("+" or "-") and a character string with the
                RFID tag identifier.
                On failure, throws an exception or returns a negative error code.
        """
        self._eventCallback = callback
        self._isFirstCb = True
        if callback is not None:
            self.registerValueCallback(yInternalEventCallback)
        else:
            self.registerValueCallback(None)
        return 0

    def _internalEventHandler(self, cbVal):
        # cbPos
        # cbDPos
        # url
        # content
        # contentStr
        eventArr = []
        # arrLen
        # lenStr
        # arrPos
        # eventStr
        # eventLen
        # hexStamp
        # typePos
        # dataPos
        # intStamp
        # binMStamp
        # msStamp
        # evtStamp
        # evtType
        # evtData
        # // detect possible power cycle of the reader to clear event pointer
        cbPos = YAPI._atoi(cbVal)
        cbPos = int(cbPos / 1000)
        cbDPos = ((cbPos - self._prevCbPos) & (0x7ffff))
        self._prevCbPos = cbPos
        if cbDPos > 16384:
            self._eventPos = 0
        if not (self._eventCallback is not None):
            return YAPI.SUCCESS
        if self._isFirstCb:
            # // first emulated value callback caused by registerValueCallback:
            # // retrieve arrivals of all tags currently present to emulate arrival
            self._isFirstCb = False
            self._eventStamp = 0
            content = self._download("events.txt")
            contentStr = content.decode(YAPI.DefaultEncoding)
            eventArr = (contentStr).split('\n')
            arrLen = len(eventArr)
            if not (arrLen > 0):
                self._throw(YAPI.IO_ERROR, "fail to download events")
                return YAPI.IO_ERROR
            # // first element of array is the new position preceeded by '@'
            arrPos = 1
            lenStr = eventArr[0]
            lenStr = (lenStr)[1: 1 + len(lenStr)-1]
            # // update processed event position pointer
            self._eventPos = YAPI._atoi(lenStr)
        else:
            # // load all events since previous call
            url = "events.txt?pos=" + str(int(self._eventPos))
            content = self._download(url)
            contentStr = content.decode(YAPI.DefaultEncoding)
            eventArr = (contentStr).split('\n')
            arrLen = len(eventArr)
            if not (arrLen > 0):
                self._throw(YAPI.IO_ERROR, "fail to download events")
                return YAPI.IO_ERROR
            # // last element of array is the new position preceeded by '@'
            arrPos = 0
            arrLen = arrLen - 1
            lenStr = eventArr[arrLen]
            lenStr = (lenStr)[1: 1 + len(lenStr)-1]
            # // update processed event position pointer
            self._eventPos = YAPI._atoi(lenStr)
        # // now generate callbacks for each real event
        while arrPos < arrLen:
            eventStr = eventArr[arrPos]
            eventLen = len(eventStr)
            typePos = eventStr.find(":")+1
            if (eventLen >= 14) and (typePos > 10):
                hexStamp = (eventStr)[0: 0 + 8]
                intStamp = int(hexStamp, 16)
                if intStamp >= self._eventStamp:
                    self._eventStamp = intStamp
                    binMStamp = bytearray((eventStr)[8: 8 + 2], YAPI.DefaultEncoding)
                    msStamp = (binMStamp[0]-64) * 32 + binMStamp[1]
                    evtStamp = intStamp + (0.001 * msStamp)
                    dataPos = eventStr.find("=")+1
                    evtType = (eventStr)[typePos: typePos + 1]
                    evtData = ""
                    if dataPos > 10:
                        evtData = (eventStr)[dataPos: dataPos + eventLen-dataPos]
                    if self._eventCallback is not None:
                        self._eventCallback(self, evtStamp, evtType, evtData)
            arrPos = arrPos + 1
        return YAPI.SUCCESS

    def nextRfidReader(self):
        """
        Continues the enumeration of RFID readers started using yFirstRfidReader().
        Caution: You can't make any assumption about the returned RFID readers order.
        If you want to find a specific a RFID reader, use RfidReader.findRfidReader()
        and a hardwareID or a logical name.

        @return a pointer to a YRfidReader object, corresponding to
                a RFID reader currently online, or a None pointer
                if there are no more RFID readers to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YRfidReader.FindRfidReader(hwidRef.value)

#--- (end of generated code: YRfidReader implementation)

#--- (generated code: YRfidReader functions)

    @staticmethod
    def FirstRfidReader():
        """
        Starts the enumeration of RFID readers currently accessible.
        Use the method YRfidReader.nextRfidReader() to iterate on
        next RFID readers.

        @return a pointer to a YRfidReader object, corresponding to
                the first RFID reader currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("RfidReader", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YRfidReader.FindRfidReader(serialRef.value + "." + funcIdRef.value)

#--- (end of generated code: YRfidReader functions)
