import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME
from spv1.spv1 import RESPONSE_BASE

from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

from enum import IntEnum


class EnumPowerOption(IntEnum):
    POWER_NO_SOURCE = 0,
    POWER_SOURCE_3V3 = 1
    POWER_SOURCE_5V = 2,


class CmdSetTargetPower(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdsettargetpower)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdsettargetpower
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdSetTargetPower.PARAMS_SET_TARGET_POWER)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdsettargetpower
        self.spv1_get_response_api.restype = RESPONSE_BASE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_BASE() #CmdAuthenticate.Response()


    class PARAMS_SET_TARGET_POWER(ctypes.Structure):
        def __init__(self):
            self.powerOption =  EnumPowerOption.POWER_NO_SOURCE
            self.keep_reset_state = 0 # 0 -> Release reset after POR, 1-> keep reset after POR
            super().__init__(powerOption=self.powerOption)

        _fields_ = [("powerOption", ctypes.c_ubyte),
                    ("keep_reset_state", ctypes.c_ubyte)]

    def build(self, commandParams:PARAMS_SET_TARGET_POWER, nodeAddress=0) -> STRUCT_SPV1FRAME:

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
