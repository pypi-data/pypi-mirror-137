import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME
from spv1.spv1 import RESPONSE_BASE

from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

from enum import IntEnum

class ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES(IntEnum):
    MAX4638_SWITCH_NO1 = 0,
    MAX4638_SWITCH_NO2 = 1,
    MAX4638_SWITCH_NO3 = 2,
    MAX4638_SWITCH_NO4 = 3,
    MAX4638_SWITCH_NO5 = 4,
    MAX4638_SWITCH_NO6 = 5,
    MAX4638_SWITCH_NO7 = 6,
    MAX4638_SWITCH_NO8 = 7


class ENUM_MEASUREMENT_EXTERNAL_MUX_4638_RENAMED_SWITCHES(IntEnum):
   TARGET_TA_OUT4_TB_TAGF = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO1,
   TARGET_OUT5_DE_DR = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO2,
   TARGET_TA_BUZZER_TB_OUT4 = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO3,
   TARGET_SREAD = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO4,
   TARGET_RESET = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO5,
   TARGET_IN2 = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO6,
   NONE_NO7 = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO7,
   NONE_NO8 = ENUM_MEASUREMENT_EXTERNAL_MUX_4638_SWITCHES.MAX4638_SWITCH_NO8




class CmdElectricalTestSetupExternalMux(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdelectricaltestsetupexternalmux)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdelectricaltestsetupexternalmux
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdElectricalTestSetupExternalMux.PARAMS_ELECTRICAL_TEST_SETUP_EXTERNAL_MUX)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdelectricaltestsetupexternalmux
        self.spv1_get_response_api.restype = RESPONSE_BASE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_BASE() #CmdAuthenticate.Response()


    class PARAMS_ELECTRICAL_TEST_SETUP_EXTERNAL_MUX(ctypes.Structure):
        def __init__(self):
            self.max4638_switch_address =  ENUM_MEASUREMENT_EXTERNAL_MUX_4638_RENAMED_SWITCHES.NONE_NO8
            super().__init__(max4638_switch_address=self.max4638_switch_address)

        _fields_ = [("max4638_switch_address", ctypes.c_uint8)]

    def build(self, commandParams:PARAMS_ELECTRICAL_TEST_SETUP_EXTERNAL_MUX, nodeAddress=0) -> STRUCT_SPV1FRAME:

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
