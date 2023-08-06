import ctypes
from ctypes import *
from enum import IntEnum

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR
#from spv1.spv1 import RESPONSE_BASE
#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from pysmtester.smtesterdef import ENUM_WRITE_FILE_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


class STRUCT_DEVICE_ID(ctypes.Structure):
    def __init__(self):
        self.manufacturerID = 0
        self.serialNumber = 0
        self.deviceFamily = 0

    _fields_ = [("manufacturerID",c_uint32),
                ("serialNumber",c_uint32),
                ("deviceFamily", c_uint32)]


class STRUCT_FIRMWARE_INFO(ctypes.Structure):
    def __init__(self):
        self.caption = (ctypes.c_uint8 * 24)() # (ctypes.c_uint8 * 250)()  #("".encode('utf-8')) if configured as ("data_buffer", ctypes.c_char * 128)
        self.version = 0
        self.revision = 0
        self.build = 0
        self.releaseType = 0
        self.dateYear = 0
        self.dateMonth = 0
        self.dateDay = 0


    _fields_ = [("caption", ctypes.c_uint8 * 24),
                ("version",c_uint8),
                ("revision",c_uint8),
                ("build",c_uint8),
                ("releaseType",c_uint8),
                ("dateYear", c_uint16),
                ("dateMonth",c_uint8),
                ("dateDay",c_uint8)]


class STRUCT_DEVICE_INFO(ctypes.Structure):
    def __init__(self):
        self.deviceID = STRUCT_DEVICE_ID()
        self.userCodeStartAddress = 0
        self.flashChecksum = 0
        self.calculatedChecksum = 0
        self.checksumSectors = (ctypes.c_uint32 * 16)()
        self.checksumControl = 0
        self.firmwareInfo = STRUCT_FIRMWARE_INFO()
        self.bootFirmwareInfo = STRUCT_FIRMWARE_INFO()

    _fields_ = [("deviceID", STRUCT_DEVICE_ID),
                ("userCodeStartAddress",c_uint32),
                ("flashChecksum",c_uint32),
                ("calculatedChecksum",c_uint32),
                ("checksumSectors",c_uint32 * 16),
                ("checksumControl",c_uint32),
                ("firmwareInfo", STRUCT_FIRMWARE_INFO),
                ("bootFirmwareInfo",STRUCT_FIRMWARE_INFO)]



class RESPONSE_BOOT_TRYCONNECT(ctypes.Structure):
    def __init__(self):
        self.deviceInfo = STRUCT_DEVICE_INFO()

        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()


    _fields_ = [("deviceInfo", STRUCT_DEVICE_INFO),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]


class CmdBootTryConnect(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdboottryconnect)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdboottryconnect
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdBootTryConnect.PARAMS_BOOT_TRYCONNECT)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdboottryconnect
        self.spv1_get_response_api.restype = RESPONSE_BOOT_TRYCONNECT
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_BOOT_TRYCONNECT() #CmdAuthenticate.Response()

    class PARAMS_BOOT_TRYCONNECT(ctypes.Structure):
        def __init__(self):
            self.baudrateID = 0

            #super().__init__(keys=self.keys)

        _fields_ = [("baudrateID", ctypes.c_uint8)]


    def build(self, commandParams:PARAMS_BOOT_TRYCONNECT, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy and bind wrapper objects to ctypes fields.
        # Bind given filename to databuffer

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_BOOT_TRYCONNECT:

        self.response = self.spv1_get_response_api(self.command_instance)

        # print("get_response self.response.responseMessage",self.response.responseMessage)

        #Parse structure response(c type) to Python Response (python class)
        """
        str_response = self.spv1_get_response_api(self.command_instance)
        self.response.chip_program_action = str_response.chip_program_action
        self.response.error_type = str_response.error_type
        self.response.programming_error_code = str_response.programming_error_code
        self.response.programming_info = str_response.programming_info
        self.response.file_result = str_response.file_result

        self.response.responseErrorcode = str_response.responseErrorcode
        self.response.responseMessage = str_response.responseMessage
        self.response.f = str_response.f
        """

        return self.response
