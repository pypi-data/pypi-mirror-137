import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR

#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from pysmtester.smtesterdef import ENUM_WRITE_FILE_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


class RESPONSE_WRITE_FILE(ctypes.Structure):
    def __init__(self):
        self.lfs_error = 0
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        super().__init__(lfs_error = self.lfs_error,
                         responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f
                         )

    _fields_ = [("lfs_error", ctypes.c_int8),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]



class CmdWriteFile(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdwritefile)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdwritefile
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdWriteFile.PARAMS_WRITE_FILE)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdwritefile
        self.spv1_get_response_api.restype = RESPONSE_WRITE_FILE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_WRITE_FILE() #CmdAuthenticate.Response()

    class PARAMS_WRITE_FILE(ctypes.Structure):
        def __init__(self):
            self.file_action = ENUM_WRITE_FILE_ACTION.BEGIN_FILE
            self.percantage = 0
            self.write_buffer_size = 0
            self.data_buffer = (ctypes.c_uint8 * 250)()  #("".encode('utf-8')) if configured as ("data_buffer", ctypes.c_char * 128)
            self.file_name = ""

            #super().__init__(keys=self.keys)

        _fields_ = [("file_action", ctypes.c_uint8),
                    ("percantage", ctypes.c_uint8),
                    ("write_buffer_size", ctypes.c_uint16),
                    ("data_buffer", ctypes.c_uint8 * 250) #("data_buffer", ctypes.c_char * 128),
                    ]


    def build(self, commandParams:PARAMS_WRITE_FILE, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        if (commandParams.file_action == ENUM_WRITE_FILE_ACTION.BEGIN_FILE):
            # Bind given filename to databuffer
            ba = bytearray(commandParams.file_name.encode('ascii'))
            for i in range(len(ba)):
                commandParams.data_buffer[i] = ba[i]

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self):

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
