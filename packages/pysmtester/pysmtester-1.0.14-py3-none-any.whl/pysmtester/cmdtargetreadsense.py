import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR

#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from enum import IntEnum


# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


class ENUM_TARGET_READ_SENSE_FLAGS(IntEnum):
    FLAG_GET_UART_RESPONSE = 0x01,
    FLAG_COUNT_ENABLE = 0x02,          # if this bit is 1 count will be disabled.
    FLAG_COUNT_SREAD = 0x04             # if this bit is 1 count SREAD, else count TAGF pin (If COUNT is enabled)


class RESPONSE_TARGET_READ_SENSE(ctypes.Structure):
    def __init__(self):
        self.read_status = 0
        self.flash_count = 0
        self.uart_bridge_status = 0
        self.uart_bridge_rx_length = 0
        self.read_rate_per_sec = 0
        self.target_uart_response = (ctypes.c_uint8 * 250)()
        self.readRatePerSecStr =  b''
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()


    _fields_ = [("read_status", ctypes.c_ubyte),
                ("flash_count", ctypes.c_ubyte),
                ("uart_bridge_status", ctypes.c_ubyte),
                ("uart_bridge_rx_length", ctypes.c_ubyte),
                ("read_rate_per_sec", ctypes.c_float),
                ("target_uart_response", ctypes.c_ubyte * 250),
                ("readRatePerSecStr", ctypes.c_char_p),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]


class CmdTargetReadSense(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdtargetreadsense)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdtargetreadsense
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdTargetReadSense.PARAMS_TARGET_READ_SENSE)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdtargetreadsense
        self.spv1_get_response_api.restype = RESPONSE_TARGET_READ_SENSE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_TARGET_READ_SENSE()

    class PARAMS_TARGET_READ_SENSE(ctypes.Structure):
        def __init__(self):
            self.flags = 0
            #self.targetBaudrateId = 1 # 1->BR19200 from sdk cpp (cmdgetconfig.h)
            #self.flags &= ~ENUM_TARGET_READ_SENSE_FLAGS.FLAG_GET_UART_RESPONSE

            #super().__init__(keys=self.keys)

        _fields_ = [("flags", ctypes.c_uint8)]


    def build(self, commandParams:PARAMS_TARGET_READ_SENSE, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_TARGET_READ_SENSE:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
