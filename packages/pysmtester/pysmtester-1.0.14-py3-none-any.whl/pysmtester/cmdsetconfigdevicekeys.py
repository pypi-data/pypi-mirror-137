import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME
from spv1.spv1 import RESPONSE_BASE
#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare



class CmdSetConfigDeviceKeys(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdsetconfigdevicekeys)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdsetconfigdevicekeys
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdSetConfigDeviceKeys.PARAMS_DEVICE_KEYS_AND_ID)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdsetconfigdevicekeys
        self.spv1_get_response_api.restype = RESPONSE_BASE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_BASE() #CmdAuthenticate.Response()

    class PARAMS_DEVICE_KEYS_AND_ID(ctypes.Structure):
        def __init__(self):
            self.smtester_device_id = 0
            self.keys =  (0xA0A1A2A3, 0xB0B1B2B3, 0xC0C1C2C3, 0xD0D1D2D3)
            super().__init__(keys=self.keys)

        _fields_ = [("smtester_device_id", ctypes.c_uint32),
                    ("keys", ctypes.c_uint32 * 4)]


    def build(self, commandParams:PARAMS_DEVICE_KEYS_AND_ID, nodeAddress=0) -> STRUCT_SPV1FRAME:

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
