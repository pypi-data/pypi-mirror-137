import os,sys,platform

from spv1.serialcommspv1 import SerialCommSpv1
from spv1.spsc import EnumLogFilter
from pysmtester.globalvar import spv1handler
from pysmtester.smtesterasynchandler import SmTesterAsyncHandler
from pysmtester import smtesterdef

modulepath = os.path.dirname(smtesterdef.__file__)
sys.path.insert(0, modulepath)

def create_smtester_serial_comm(DefaultSerialTimeOut = 0.5,AsyncReceive=True,async_callback = None,auto_log=True, vertical_log = False,log_filter = EnumLogFilter.ALL,external_dll_path=None):
    """ Create and returns SerialSpv1 object and initialize system including dll """
    """ Example platform.platform() outputs:

    Windows 10:
    Windows-10-10.0.14393-SP0

    Raspberry Pi:
    Linux-4.4.38-v7+-armv71-with-debian-8.0

    Debian 64 bit ( Virtual Box)
    Linux-3.16.0-4-amd64-x86_64-with-debian-8.3

    Ubuntu 16.04 (Crea PC)
    Linux-4.4.0-66-generic-i686-with-Ubuntu-16.04-xenial
    """

    # Check armv first; as Raspberry and Debian both have Debian string.
    if external_dll_path == None:
        _platform_string = platform.platform().lower()
        _architecture_string = platform.architecture()[0]
        # !!! Attention comparision msut be lower case!!
        if "win".lower() in _platform_string:
            # Tested on 64 bit windows 10,(python installed version is 32 bit)
            # Windows-10-10.0.14393-SP0
            spv1handler.initialize(path=modulepath + "\\spv1smtester_win.dll",log_filter=log_filter,vertical_log=vertical_log)
        elif "armv7".lower() in _platform_string:
            # Tested with Raspberry Pi 3
            # Linux-4.4.38-v7+-armv71-with-debian-8.0
            # Beaglebone may work too as well. Not tested
            spv1handler.initialize(path=modulepath + "//spv1smtester_armv7.dll",log_filter=log_filter,vertical_log=vertical_log)
        elif "ubuntu".lower() in _platform_string:
            if "32" in _architecture_string:
                # Tested with ubuntu 16.04 32 bit machine.
                # Linux-4.4.0-66-generic-i686-with-Ubuntu-16.04-xenial
                spv1handler.initialize(path=modulepath + "//spv1smtester_ubuntu_32.dll",log_filter=log_filter,vertical_log=vertical_log)
            elif "64" in _architecture_string:
                # This dll is not available.
                print("64 bit ubuntu dll is not available yet with this package. Please contact to request")
                #spv1handler.initialize(path=modulepath + "//spv1mifare_ubuntu_64.dll",log_filter=log_filter,vertical_log=vertical_log)
                # try using 32bit version
                # Linux-4.4.0-66-generic-i686-with-Ubuntu-16.04-xenial
                spv1handler.initialize(path=modulepath + "//spv1smtester_ubuntu_32.dll",log_filter=log_filter,vertical_log=vertical_log)
        elif "debian".lower() in _platform_string:
            if "32" in _architecture_string:
                # Not available. Not tested
                # Try using 64 bit debian
                # Linux-3.16.0-4-amd64-x86_64-with-debian-8.3
                print("32 bit debian dll is not available yet with this package. Please contact to request")
                #spv1handler.initialize(path=modulepath + "\\spv1mifare_deb32.dll",log_filter=log_filter,vertical_log=vertical_log)
                spv1handler.initialize(path=modulepath + "//spv1smtester_deb64.dll",log_filter=log_filter,vertical_log=vertical_log)
            elif "64" in _architecture_string:
                # Tested with debian 64 bit.
                # Linux-3.16.0-4-amd64-x86_64-with-debian-8.3
                spv1handler.initialize(path=modulepath + "//spvsmtester_deb64.dll",log_filter=log_filter,vertical_log=vertical_log)
        elif "x86_64-with-glibc".lower() in _platform_string:
            spv1handler.initialize(path=modulepath + "//spv1smtester_glibc.so", log_filter=log_filter,
                                   vertical_log=vertical_log)
        else:
            spv1handler.initialize(path=modulepath + "//spv1smtester.so", log_filter=log_filter,
                                   vertical_log=vertical_log)
            #spv1handler.initialize(path=external_dll_path,log_filter=log_filter,vertical_log=vertical_log)

    smtester_async_handler = SmTesterAsyncHandler(spv1handler, async_callback=async_callback, auto_log=auto_log)
    smtester_serial_comm = SerialCommSpv1(spv1handler, smtester_async_handler, DefaultSerialTimeOut, AsyncReceive)
    return smtester_serial_comm
