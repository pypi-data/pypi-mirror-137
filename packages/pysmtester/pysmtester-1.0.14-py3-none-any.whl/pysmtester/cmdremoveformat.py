import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR
# from spv1.spv1 import RESPONSE_BASE
#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from pysmtester.smtesterdef import ENUM_REMOVE_FORMAT_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare



class RESPONSE_REMOVE_FORMAT(ctypes.Structure):
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



class CmdRemoveFormat(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdremoveformat)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdremoveformat
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdRemoveFormat.PARAMS_REMOVEFORMAT)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdremoveformat
        self.spv1_get_response_api.restype = RESPONSE_REMOVE_FORMAT
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_REMOVE_FORMAT()

    class PARAMS_REMOVEFORMAT(ctypes.Structure):
        def __init__(self):
            self.remove_format_action = ENUM_REMOVE_FORMAT_ACTION.REMOVE_DIR_FILE
            self.data_buffer = (ctypes.c_uint8 * 128)()
            self.file_name = ""

            #super().__init__(keys=self.keys)

        _fields_ = [("remove_format_action", ctypes.c_uint8),
                    ("data_buffer", ctypes.c_uint8 * 128) #("data_buffer", ctypes.c_char * 128),
                    ]


    def build(self, commandParams:PARAMS_REMOVEFORMAT, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        if (commandParams.remove_format_action == ENUM_REMOVE_FORMAT_ACTION.REMOVE_DIR_FILE):
            # Bind given filename to databuffer
            ba = bytearray(commandParams.file_name.encode('ascii'))
            for i in range(len(ba)):
                commandParams.data_buffer[i] = ba[i]

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_REMOVE_FORMAT:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
