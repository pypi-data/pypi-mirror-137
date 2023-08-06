import ctypes
# from ctypes import *

from spv1.commandbasespv1 import CommandBaseSpv1
from spv1.spv1 import STRUCT_SPV1FRAME
from spv1.spv1 import RESPONSE_BASE

from pysmtester.globalvar import spv1handler
# do not link to mifare.py here. It creates a circular dependency and we get ImportError
# mifare > MifareAsyncHandler > cmdActivateAll/(and some other async commands found in MifareAsyncHandler) > mifare

from enum import IntEnum

class ENUM_MUX_COM_SOURCE(IntEnum):
    MUX_COM_SOURCE_ADC = 0,
    MUX_COM_SOURCE_VIRTUAL_GND = 1



class ENUM_MEASUREMENT_MUX_14661_SWITCHES(IntEnum):
    NONE = 0,
    MAX14661_SW01 = 1 << 0,
    MAX14661_SW02 = 1 << 1,
    MAX14661_SW03 = 1 << 2,
    MAX14661_SW04 = 1 << 3,
    MAX14661_SW05 = 1 << 4,
    MAX14661_SW06 = 1 << 5,
    MAX14661_SW07 = 1 << 6,
    MAX14661_SW08 = 1 << 7,
    MAX14661_SW09 = 1 << 8,
    MAX14661_SW10 = 1 << 9,
    MAX14661_SW11 = 1 << 10,
    MAX14661_SW12 = 1 << 11,
    MAX14661_SW13 = 1 << 12,
    MAX14661_SW14 = 1 << 13,
    MAX14661_SW15 = 1 << 14,
    MAX14661_SW16 = 1 << 15,

class ENUM_MEASUREMENT_MUX_14661_RENAMED_SWITCHES(IntEnum):
    NONE = ENUM_MEASUREMENT_MUX_14661_SWITCHES.NONE,
    TARGET_VDD = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW01,
    TARGET_ANT1 = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW02,
    TARGET_ANT2 = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW03,
    TARGET_UTX = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW04,
    TARGET_URX = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW05,
    TARGET_I2C_SCL = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW06,
    TARGET_I2C_SDA = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW07,
    NC = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW08,
    EXT_MUX_INPUT = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW09,
    TARGET_TA_TAGF_TB_BUZZER = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW10,
    TARGET_IN1 = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW11,
    TARGET_SWDIO_BOOT0 = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW12,
    TARGET_SWDCLK = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW13,
    TARGET_OUT2_WDATA1 = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW14,
    TARGET_OUT1_WDATA0 = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW15,
    TARGET_GND = ENUM_MEASUREMENT_MUX_14661_SWITCHES.MAX14661_SW16

class CmdElectricalTestSetupPair(CommandBaseSpv1):
    def __init__(self): # logcallback = DefaultSpscLogger.print_log):
        super().__init__(spv1handler, spv1handler.dll.spv1_create_cmdelectricaltestsetuppair)

        self.spv1_command_build_api = spv1handler.dll.spv1_build_cmdelectricaltestsetuppair
        self.spv1_command_build_api.restype = STRUCT_SPV1FRAME
        self.spv1_command_build_api.argtypes = (ctypes.c_ulong, CmdElectricalTestSetupPair.PARAMS_ELECTRICAL_TEST_SETUP_PAIR)

        self.spv1_get_response_api = spv1handler.dll.spv1_get_response_cmdelectricaltestsetuppair
        self.spv1_get_response_api.restype = RESPONSE_BASE
        self.spv1_get_response_api.argtypes = (ctypes.c_ulong,)

        self.response = RESPONSE_BASE()


    class PARAMS_ELECTRICAL_TEST_SETUP_PAIR(ctypes.Structure):
        def __init__(self):
            self.comASwitch = ENUM_MEASUREMENT_MUX_14661_RENAMED_SWITCHES.NONE
            self.comBSwitch = ENUM_MEASUREMENT_MUX_14661_RENAMED_SWITCHES.NONE
            self.comASource = ENUM_MUX_COM_SOURCE.MUX_COM_SOURCE_ADC
            self.comBSource = ENUM_MUX_COM_SOURCE.MUX_COM_SOURCE_VIRTUAL_GND
            self.comAInitialADCVal = 0 # ADC value 8bit
            self.comBInitialADCVal = 0 # ADC value 8bit
            self.comAInitialADCVoltage = 0.00
            self.comBInitialADCVoltage = 0.00

            #super().__init__(ms_keep_reset_duration=self.ms_keep_reset_duration)

        _fields_ = [("comASwitch", ctypes.c_uint16),
                    ("comBSwitch", ctypes.c_uint16),
                    ("comASource", ctypes.c_uint8),
                    ("comBSource", ctypes.c_uint8),
                    ("comAInitialADCVal", ctypes.c_uint8),
                    ("comBInitialADCVal", ctypes.c_uint8),
                    ]

    def build(self, commandParams:PARAMS_ELECTRICAL_TEST_SETUP_PAIR, nodeAddress=0) -> STRUCT_SPV1FRAME:

        if (commandParams.comAInitialADCVoltage!=0):
            commandParams.comAInitialADCVal = int(commandParams.comAInitialADCVoltage / 0.0128)

        if (commandParams.comBInitialADCVoltage != 0):
            commandParams.comBInitialADCVal = int(commandParams.comBInitialADCVoltage / 0.0128)

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
