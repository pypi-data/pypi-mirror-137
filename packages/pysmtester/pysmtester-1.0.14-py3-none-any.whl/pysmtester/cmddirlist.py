import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR

#from pysmtester.smtesterdef import PARAMS_RELAY_ON_OFF
from pysmtester import  smtesterdef


from pysmtester.globalvar import spv1handler
from pysmtester.smtesterdef import ENUM_WRITE_FILE_ACTION
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare


"""
struct RESPONSE_DIR_LIST{

	int8_t result;
	uint8_t type;
	uint32_t size;
	const char* name;	//Name of the directory or file

	// Followings will only keep reference/copy of the actual values found inside command object. 
	// The following members will be only initialized when caller request the response.
	unsigned char responseErrorcode; //
	const char* responseMessage;
	STRUCT_SPV1FRAME f;

};

"""
class RESPONSE_DIR_LIST(ctypes.Structure):
    def __init__(self):
        self.result = 0
        self.type = 0
        self.size = 0
        self.name = b''
        self.responseErrorcode = Def_SPSCERR.RESPONSE_NOT_AVAILABLE
        self.responseMessage = b''
        self.f = STRUCT_SPV1FRAME()

        super().__init__(result = self.result,
                         type = self.type,
                         size = self.size,
                         name = self.name,
                         responseErrorcode=self.responseErrorcode,
                         responseMessage=self.responseMessage,
                         f=self.f
                         )

    _fields_ = [("result", ctypes.c_int8),
                ("type", ctypes.c_ubyte),
                ("size", ctypes.c_uint32),
                ("name", ctypes.c_char_p),
                ("responseErrorcode", ctypes.c_ubyte),
                ("responseMessage", ctypes.c_char_p),
                ("f", STRUCT_SPV1FRAME)]




class CmdDirList(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmddirlist)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmddirlist
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdDirList.PARAMS_DIR_LIST)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmddirlist
        self.spv1_get_response_api.restype = RESPONSE_DIR_LIST
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_DIR_LIST()

    class PARAMS_DIR_LIST(ctypes.Structure):
        def __init__(self):
            self.data_buffer = (ctypes.c_uint8 * 128)()  # char* path will be converted to data_buffer array
            self.path = ""

            #super().__init__(keys=self.keys)

        _fields_ = [("data_buffer", ctypes.c_uint8 * 128) #("data_buffer", ctypes.c_char * 128),
                    ]


    def build(self, commandParams:PARAMS_DIR_LIST, nodeAddress=0) -> STRUCT_SPV1FRAME:

        # Here we can check parameter integritiy.
        # Convert string to ctype buffer
        # Bind given filename to databuffer
        ba = bytearray(commandParams.path.encode('ascii'))
        for i in range(len(ba)):
            commandParams.data_buffer[i] = ba[i]

        txframe = self.spv1_command_build_api(self.command_instance,commandParams,nodeAddress)
        return txframe

    def get_response(self) -> RESPONSE_DIR_LIST:

        self.response = self.spv1_get_response_api(self.command_instance)

        #str_response = self.spv1_get_response_api(self.command_instance)
        #Parse structure response(c type) to Python Response (python class)
        #self.response.responseErrorcode = str_response.responseErrorcode
        #self.response.responseMessage = str_response.responseMessage
        #self.response.f = str_response.f

        return self.response
