import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR

#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler

# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


class RESPONSE_TARGET_READ_MEASUREMENT(ctypes.Structure):
    def __init__(self):
        self.measuredVoltage = 0
        self.measuredCurrentma = 0
        self.measuredVoltageStr =  b''
        self.measuredCurrentmaStr =  b''
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()


    _fields_ = [("measuredVoltage", ctypes.c_float),
                ("measuredCurrentma", ctypes.c_float),
                ("measuredVoltageStr", ctypes.c_char_p),
                ("measuredCurrentmaStr", ctypes.c_char_p),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]


class CmdTargetReadMeasurement(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdtargetreadmeasurement)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdtargetreadmeasurement
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong,)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdtargetreadmeasurement
        self.spv1_get_response_api.restype = RESPONSE_TARGET_READ_MEASUREMENT
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_TARGET_READ_MEASUREMENT()


    def build(self, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.

        txframe = self.spv1_command_build_api(self.command_instance,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_TARGET_READ_MEASUREMENT:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
