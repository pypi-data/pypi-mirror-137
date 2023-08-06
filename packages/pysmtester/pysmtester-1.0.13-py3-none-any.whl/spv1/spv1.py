import ctypes
from ctypes import *
from spv1.spsc import STR_LOG
from spv1.spsc import Def_SPSCERR


class STRUCT_SPV1FRAME(ctypes.Structure):
    def __init__(self):
        self.dataLength = 0
        self.dataBufferIndex = 0
        self.frameBufferLength = 0
        self.command = 0
        self.checksum = 0
        self.nodeAddress = 0
        self.frameBuffer =()
        self.dataBuffer =()

        super().__init__(spv1IsDataLength16Bit=False,
                         dataLength=self.dataLength,
                         dataBufferIndex=self.dataBufferIndex,
                         frameBufferLength=self.frameBufferLength,
                         command=self.command,
                         nodeAddress=self.nodeAddress,
                         frameBuffer=self.frameBuffer,
                         dataBuffer=self.dataBuffer)

    def print_frame(self):
        print(" ".join("0x{:02x}".format(element) for element in self.frameBuffer[0:self.frameBufferLength]))
        #print(", ".join("0x{:02x}".format(element) for element in self.frameBuffer[0:self.frameBufferLength]))

    _fields_ = [("spv1IsDataLength16Bit",c_bool),
                ("dataLength",c_uint),
                ("dataBufferIndex", c_uint),
                ("frameBufferLength", c_uint),
                ("command",c_ubyte),
                ("checksum",c_ubyte),
                ("nodeAddress",c_ubyte),
                ("frameBuffer",POINTER(c_ubyte)),
                ("dataBuffer",POINTER(c_ubyte))]

class STRUCT_SPV1CONSTRUCTOR(ctypes.Structure):
    _fields_ = [("callbacklog", ctypes.CFUNCTYPE(None, c_int, STR_LOG)),
                ("callbackcheckconnectionstate", ctypes.CFUNCTYPE(c_bool, c_int)),
                ("callbackwritebuffer", ctypes.CFUNCTYPE(c_bool, c_int, POINTER(ctypes.c_ubyte),c_int)),
                ("callbackwaitforresponse", ctypes.CFUNCTYPE(c_bool, c_int)),
                ("callbackAsyncReceiveTimerStart",ctypes.CFUNCTYPE(None, c_int)),
                ("callbackAsyncReceiveTimerStop",ctypes.CFUNCTYPE(None, c_int)),
                ("callbackAsyncRxProtocol", ctypes.CFUNCTYPE(None, c_int, STRUCT_SPV1FRAME)),
                ("logtypesendcommand", c_int),
                ("logtypereceiveresponse", c_int),
                ("logtypereceiveokresponsefail", c_int),
                ("logtypeasyncincoming", c_int),
                ("instanceID", c_int)]


class RESPONSE_BASE(ctypes.Structure):
    def __init__(self):
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        super().__init__(responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f)

    _fields_ = [("responseErrorcode", c_ubyte),
                ("responseMessage", c_char_p),
                ("f", STRUCT_SPV1FRAME)]


#class ParameterlessResponse():
#    def __init__(self):
#        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
#        self.responseMessage = ''
#        self.f = STR_SPV1FRAME()


#array = (ctypes.c_ubyte * 4)(0x31, 0x32, 0x33, 0x34)
#txframe = STR_SPV1FRAME(frameBufferLength=4, frameBuffer=array)
