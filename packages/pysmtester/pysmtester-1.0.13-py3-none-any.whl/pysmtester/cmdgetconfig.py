import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR
from spv1.spv1 import RESPONSE_BASE
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

class RESPONSE_SMTESTER_CONFIG(ctypes.Structure):
    def __init__(self):
        self.smester_device_id = 0;
        self.baudrateID = 0
        self.rsv1 = 0
        self.rsv2 = 0
        self.rsv3 = 0
        self.keys = (0x00000000, 0x00000000, 0x00000000, 0x00000000)
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        super().__init__(smester_device_id = self.smester_device_id,
                         baudrateID = self.baudrateID,
                         rsv1 = self.rsv1,
                         rsv2 = self.rsv2,
                         rsv3 = self.rsv3,
                         keys=self.keys,
                         responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f
                         )

    _fields_ = [("smester_device_id", ctypes.c_uint32),
                ("baudrateID", ctypes.c_ubyte),
                ("rsv1", ctypes.c_ubyte),
                ("rsv2", ctypes.c_ubyte),
                ("rsv3", ctypes.c_ubyte),
                ("keys", ctypes.c_uint32 * 4),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]


class CmdGetConfig(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdgetconfig)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdgetconfig
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong,)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdgetconfig
        self.spv1_get_response_api.restype = RESPONSE_SMTESTER_CONFIG
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_SMTESTER_CONFIG()


    def build(self, nodeAddress=0) -> STRUCT_SPV1FRAME:

        txframe = self.spv1_command_build_api(self.command_instance,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_SMTESTER_CONFIG:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
