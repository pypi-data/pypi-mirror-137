import ctypes
from enum import IntEnum

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR
# from spv1.spv1 import RESPONSE_BASE
#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from pysmtester.smtesterdef import ENUM_REMOVE_FORMAT_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

"""
namespace ReadChecksumTargetDevice
{
	enum ReadChecksumTargetDevices
	{
		CY8C27443_ISSP = 1,
		CY8C4124_SWD = 2,
		STM32 = 3
	};
}
"""
class ENUM_READ_CHECKSUM_TARGET_DEVICES(IntEnum):
    NONE = 0,
    CY8C27443_ISSP = 1,
    CY8C4124_SWD = 2,
    STM32 = 3,
    SM125M1_ISSP = 4


class RESPONSE_READ_CHECKSUM(ctypes.Structure):
    def __init__(self):
        self.programming_error_code = 0
        self.targetDeviceChecksum = 0
        self.targetDeviceSerialNumber = 0
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

    _fields_ = [("programming_error_code", ctypes.c_int8),
                ("targetDeviceChecksum", ctypes.c_uint32),
                ("targetDeviceSerialNumber", ctypes.c_uint32),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]



class CmdReadChecksum(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdreadchecksum)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdreadchecksum
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdReadChecksum.PARAMS_READ_CHECKSUM)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdreadchecksum
        self.spv1_get_response_api.restype = RESPONSE_READ_CHECKSUM
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_READ_CHECKSUM()

    class PARAMS_READ_CHECKSUM(ctypes.Structure):
        def __init__(self):
            self.target_device = 0

            #super().__init__(keys=self.keys)

        _fields_ = [("target_device", ctypes.c_uint8)]



    def build(self, commandParams:PARAMS_READ_CHECKSUM, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        # Bind given filename to databuffer

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_READ_CHECKSUM:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
