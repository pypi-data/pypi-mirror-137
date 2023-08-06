import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR

#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
#from pysmtester.smtesterdef import ENUM_WRITE_FILE_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

from enum import IntEnum

"""
#define ERR_UART_BRIDGE_SUCCESS												0x00
#define ERR_UART_BRIDGE_INVALID_CH										0x10
#define ERR_UART_BRIDGE_TIMEOUT												0x12
#define ERR_UART_BRIDGE_HAL_ERROR											0x14

"""

class ENUM_ERR_UART_BRIDGE_RESPONSE(IntEnum):
    ERR_UART_BRIDGE_SUCCESS = 0x00,
    ERR_UART_BRIDGE_INVALID_CH = 0x10,
    ERR_UART_BRIDGE_TIMEOUT = 0x12,
    ERR_UART_BRIDGE_HAL_ERROR = 0x14,



class EnumUartBridgeChannel(IntEnum):
    UART_CH2_UART3 = 2, # UART for Target
    UART_CH3_UART4 = 3  # UART for external control (i.e. MotorControl)



class RESPONSE_UART_BRIDGE(ctypes.Structure):
    def __init__(self):
        self.target_response_frame = bytearray(0) # will be filled (binded) at get response - helper variable
        self.uart_bridge_status = ENUM_ERR_UART_BRIDGE_RESPONSE.ERR_UART_BRIDGE_HAL_ERROR.value
        self.rxDataLength = 0
        #self.rxBuffer = (ctypes.c_uint8 * 255)()
        self.prxBuffer =()
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        super().__init__(rxDataLength = self.rxDataLength,
                         # rxBuffer = self.rxBuffer,
                         prxBuffer = self.prxBuffer,
                         responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f
                         )

    _fields_ = [("uart_bridge_status", ctypes.c_uint8),
                ("rxDataLength", ctypes.c_uint8),
                #("rxBuffer", ctypes.c_uint8 * 255),
                ("prxBuffer", ctypes.POINTER(ctypes.c_uint8)),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]


class CmdUartBridge(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmduartbridge)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmduartbridge
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdUartBridge.PARAMS_UART_BRIDGE)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmduartbridge
        self.spv1_get_response_api.restype = RESPONSE_UART_BRIDGE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_UART_BRIDGE() #CmdAuthenticate.Response()

    class PARAMS_UART_BRIDGE(ctypes.Structure):
        def __init__(self):
            self.uart_channel = EnumUartBridgeChannel.UART_CH2_UART3
            self.wait_response = 1 # True
            self.receiveTimeout = 500
            self.packageTimeout = 50
            self.txLength = 0
            self.txBuffer = (ctypes.c_uint8 * 250)()  #("".encode('utf-8')) if configured as ("data_buffer", ctypes.c_char * 128)

            #super().__init__(keys=self.keys)

        _fields_ = [("uart_channel", ctypes.c_uint8),
                    ("wait_response", ctypes.c_uint8),
                    ("receiveTimeout", ctypes.c_uint16),
                    ("packageTimeout", ctypes.c_uint16),
                    ("txLength", ctypes.c_uint8),
                    ("txBuffer", ctypes.c_uint8 * 250) #("data_buffer", ctypes.c_char * 128),
                    ]

    def build(self, commandParams:PARAMS_UART_BRIDGE, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_UART_BRIDGE:

        self.response = self.spv1_get_response_api(self.command_instance)

        # Wrapper
        # Bind target_response in to bytearray (helper variable for target response)
        if self.response.responseErrorcode == Def_SPSCERR.SUCCESS:
            self.response.target_response_frame = bytearray(self.response.rxDataLength)
            for i in range(self.response.rxDataLength):
                self.response.target_response_frame[i] = self.response.prxBuffer[i]
                #print(" ".join("0x{:02x}".format(element) for element in self.response.target_response_frame[:]))
        else:
            self.response.target_response_frame = bytearray(0)


        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
