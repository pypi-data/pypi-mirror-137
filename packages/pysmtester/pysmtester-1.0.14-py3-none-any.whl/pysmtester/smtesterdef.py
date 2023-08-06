import ctypes
from ctypes import *
#from pip._vendor.six import class_types

from enum import IntEnum

"""
import ctypes

from enum import IntEnum

from pyspv1.spv1dll import Spv1Dll # This is necessary to add path for pyspv1 project even we dont use it here.import
from pyspv1.spv1 import STRUCT_SPV1FRAME
from pyspv1.spsc  import Def_SPSCERR
"""

CONST_BAUDRATE_LIST = ['2400', '4800', '9600', '19200', '38400', '57600', '115200']

class ENUM_BAUDRATES(IntEnum):
    BR9600 = 0,
    BR19200 = 1,
    BR38400 = 2,
    BR57600 = 3,
    BR115200 = 4,
    BR1200 = 5,
    BR2400 = 6,
    BR4800 = 7


def get_baudrate_id(baudrate):

    baudrate = int(baudrate)
    if baudrate == 1200:
        return True, ENUM_BAUDRATES.BR1200
    elif baudrate == 2400:
        return True, ENUM_BAUDRATES.BR2400
    elif baudrate == 4800:
        return True, ENUM_BAUDRATES.BR4800
    elif baudrate == 9600:
        return True, ENUM_BAUDRATES.BR9600
    elif baudrate == 19200:
        return True, ENUM_BAUDRATES.BR19200
    elif baudrate == 38400:
        return True, ENUM_BAUDRATES.BR38400
    elif baudrate == 57600:
        return True, ENUM_BAUDRATES.BR57600
    elif baudrate == 115200:
        return True, ENUM_BAUDRATES.BR115200
    else:
        return False,ENUM_BAUDRATES.BR19200




class Def_SMTESTER_COMMANDS:
    SET_TARGET_POWER = 0x01
    RELAY_ANTENNA = 0x02
    CHIP_PROGRAM = 0xC0
    GET_CONFIG = 0xD0
    SET_CONFIG_BAUDRATE = 0xD1
    SET_CONFIG_DEVICE_KEYS = 0xD5
    FILE = 0xE0
    DIR_LIST = 0xE1
    REMOVE_FORMAT = 0xE2


class ENUM_WRITE_FILE_ACTION(IntEnum):
    BEGIN_FILE = 0,
    WRITE_BUFFER = 1,
    END_FILE = 2





class ENUM_REMOVE_FORMAT_ACTION(IntEnum):
    REMOVE_DIR_FILE = 0x01,
    FORMAT_MEM = 0x33,


class PARAMS_RELAY_ON_OFF(ctypes.Structure):
    def __init__(self):
        self.relayStatus = 0;
        super().__init__(relayStatus=self.relayStatus)

    _fields_ = [("relayStatus", c_ubyte)]