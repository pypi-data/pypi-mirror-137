import ctypes
from enum import IntEnum

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR
#from spv1.spv1 import RESPONSE_BASE
#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from pysmtester.smtesterdef import ENUM_WRITE_FILE_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


class ENUM_CHIP_PROGRAM_ACTION(IntEnum):
    NO_ACTION = 0,
    SWD_CY8C4124_432 = 1,
    STM32_SERIAL = 2,
    ISSP_CY8C27443 = 3,
    SERIAL_UPGRADE = 4,
    ISSP_SM125_M1 = 5

class ENUM_CHIP_PROGRAM_FLAG(IntEnum):
    NO_FLAG = 0,
    FIRST_TIME_UPGRADE = 1

class ENUM_CHIP_PROGRAM_RESPONSE_ERROR_TYPE(IntEnum):
    PROGRAM_SUCCESS = 0,
    PROGRAM_ERROR = 1,
    PROGRAM_FILE_ERROR = 2,
    PROGRAM_INFO = 3,
    UPGRADE_SUCCESS = 4

class ENUM_CHIP_PROGRAM_RESPONSE_INFO(IntEnum):
    NONE = 0,
    START_PROGRAMMING = 1,
    PROGRAMMING = 2,
    VERIFYING = 3,
    NO_PROTECTION = 4,
    UPGRADING = 5,
    ERASING_MEMORY = 6,
    PROGRAMMING_AND_VERIFYING = 7,
    REMOVING_PROTECTION = 8,
    PROTECTION_REMOVED = 9,
    WORKING = 10





class RESPONSE_CHIP_PROGRAM(ctypes.Structure):
    def __init__(self):
        self.chip_program_action = 0
        self.error_type = 0
        self.programming_error_code = 0
        self.file_result = 0
        self.programming_info = 0
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        super().__init__(chip_program_action = self.chip_program_action,
                         error_type = self.error_type,
                         programming_error_code = self.programming_error_code,
                         file_result = self.file_result,
                         programming_info = self.programming_info,
                         responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f
                         )

    _fields_ = [("chip_program_action", ctypes.c_uint8),
                ("error_type", ctypes.c_uint8),
                ("programming_error_code", ctypes.c_uint8),
                ("programming_info", ctypes.c_uint8),
                ("file_result", ctypes.c_int8),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]




class CmdChipProgram(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdchipprogram)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdchipprogram
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdChipProgram.PARAMS_CHIP_PROGRAM)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdchipprogram
        self.spv1_get_response_api.restype = RESPONSE_CHIP_PROGRAM
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_CHIP_PROGRAM() #CmdAuthenticate.Response()

    class PARAMS_CHIP_PROGRAM(ctypes.Structure):
        def __init__(self):
            self.chip_program_action = ENUM_CHIP_PROGRAM_ACTION.NO_ACTION
            self.flags = 0
            self.checksum = 0
            self.upgrade_first_time_force_serial_number = 0
            self.file_name_buffer = (ctypes.c_uint8 * 128)()  #("".encode('utf-8')) if configured as ("data_buffer", ctypes.c_char * 128)
            self.str_file_name = ""

            #super().__init__(keys=self.keys)

        _fields_ = [("chip_program_action", ctypes.c_uint8),
                    ("flags", ctypes.c_uint8),
                    ("checksum", ctypes.c_uint32),
                    ("upgrade_first_time_force_serial_number", ctypes.c_uint32),
                    ("file_name_buffer", ctypes.c_uint8 * 128)
                    ]


    def build(self, commandParams:PARAMS_CHIP_PROGRAM, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        # Bind given filename to databuffer
        ba = bytearray(commandParams.str_file_name.encode('ascii'))
        for i in range(len(ba)):
            commandParams.file_name_buffer[i] = ba[i]

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_CHIP_PROGRAM:

        self.response = self.spv1_get_response_api(self.command_instance)

        #Parse structure response(c type) to Python Response (python class)
        """
        str_response = self.spv1_get_response_api(self.command_instance)
        self.response.chip_program_action = str_response.chip_program_action
        self.response.error_type = str_response.error_type
        self.response.programming_error_code = str_response.programming_error_code
        self.response.programming_info = str_response.programming_info
        self.response.file_result = str_response.file_result

        self.response.responseErrorcode = str_response.responseErrorcode
        self.response.responseMessage = str_response.responseMessage
        self.response.f = str_response.f
        """

        return self.response
