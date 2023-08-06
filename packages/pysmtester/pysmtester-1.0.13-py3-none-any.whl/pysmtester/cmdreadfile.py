import ctypes
# from ctypes import *

from enum import IntEnum
from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME
from spv1.spv1 import RESPONSE_BASE, Def_SPSCERR
#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


class ENUM_READ_FILE_ACTION(IntEnum):
    BEGIN_FILE = 0,
    READ_BUFFER = 1,
    END_FILE = 2


class RESPONSE_READ_FILE(ctypes.Structure):
    def __init__(self):
        self.lfs_err = 0
        self.file_size = 0
        self.datalength = 0
        self.binary_file_data_buffer = (ctypes.c_uint8 * 250)()
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        """
        super().__init__(lfs_err = self.lfs_err,
                         datalength = self.datalength,
                         binary_file_data_buffer = self.binary_file_data_buffer,
                         responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f
                         )
        """

    _fields_ = [("lfs_err", ctypes.c_int8),
                ("file_size", ctypes.c_uint32),
                ("datalength", ctypes.c_uint16),
                ("binary_file_data_buffer", ctypes.c_uint8 * 250),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]



class CmdReadFile(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdreadfile)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdreadfile
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdReadFile.PARAMS_READ_FILE)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdreadfile
        self.spv1_get_response_api.restype = RESPONSE_READ_FILE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_READ_FILE()


    class PARAMS_READ_FILE(ctypes.Structure):
        def __init__(self):
            self.file_action = ENUM_READ_FILE_ACTION.BEGIN_FILE
            self.percantage = 0
            self.read_buffer_size = 0
            self.c_file_name = "".encode() #  "".encode('utf-8')) if configured as (ctypes.c_char * 128)
            self.file_name =""


            #super().__init__(keys=self.keys)

        _fields_ = [("file_action", ctypes.c_uint8),
                    ("percantage", ctypes.c_uint8),
                    ("read_buffer_size", ctypes.c_uint16),
                    ("c_file_name", ctypes.c_char * 128)
                    ]


    def build(self, commandParams:PARAMS_READ_FILE, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        if (commandParams.file_action == ENUM_READ_FILE_ACTION.BEGIN_FILE):
            # Bind given filename to databuffer
            commandParams.c_file_name = commandParams.file_name.encode('ascii')
            # ba = bytearray(commandParams.file_name.encode('ascii'))
            # for i in range(len(ba)):
            #    commandParams.data_buffer[i] = ba[i]

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_READ_FILE:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response

