import ctypes

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME
from spv1.spv1 import RESPONSE_BASE

from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

from enum import IntEnum

class ENUM_TARGET_CONNECTION_TYPE(IntEnum):
    CONN_TYPE_NONE_DISCONNECT_ALL = 0,
    CONN_TYPE_SM125_M1_MODULE = 1,
    CONN_TYPE_SM125_M2_MODULE = 2,
    CONN_TYPE_TYPE_A_MODULE = 3,
    CONN_TYPE_TYPE_B_MODULE = 4,
    CONN_TYPE_SM125_IC = 5,
    CONN_TYPE_SM130_M2_WITH_SMD_TYPEA = 6,
    CONN_TYPE_SM130_M2_WITH_SMD_TYPEB = 7


class ENUM_TARGET_COMM_TYPE(IntEnum):
    CONN_COMM_TYPE_NONE_DISCONNECT = 0,
    CONN_COMM_TYPE_UART = 1,
    CONN_COMM_TYPE_RS232 = 2,
    CONN_COMM_TYPE_RS485 = 3


class CmdTargetConnectionSetup(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdtargetconnectionsetup)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdtargetconnectionsetup
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdTargetConnectionSetup.PARAMS_TARGET_CONNECTION_SETUP)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdtargetconnectionsetup
        self.spv1_get_response_api.restype = RESPONSE_BASE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_BASE()


    class PARAMS_TARGET_CONNECTION_SETUP(ctypes.Structure):
        def __init__(self):
            self.connType = ENUM_TARGET_CONNECTION_TYPE.CONN_TYPE_TYPE_A_MODULE
            self.serialCommType = ENUM_TARGET_COMM_TYPE.CONN_COMM_TYPE_UART
            self.targetBaudrateId = 1 # 1->BR19200 from sdk cpp (cmdgetconfig.h)

            #super().__init__(ms_keep_reset_duration=self.ms_keep_reset_duration)

        _fields_ = [("connType", ctypes.c_uint8),
                    ("serialCommType", ctypes.c_uint8),
                    ("targetBaudrateId", ctypes.c_uint8)]

    def build(self, commandParams:PARAMS_TARGET_CONNECTION_SETUP, nodeAddress=0) -> STRUCT_SPV1FRAME:

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_BASE:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
