import os
from spv1.spv1 import STRUCT_SPV1FRAME, Def_SPSCERR
from spv1.spsc import LogInfo
from pysmtester.smtesterdef import Def_SMTESTER_COMMANDS
from pysmtester.cmdchipprogram import CmdChipProgram, ENUM_CHIP_PROGRAM_RESPONSE_ERROR_TYPE, ENUM_CHIP_PROGRAM_RESPONSE_INFO, RESPONSE_CHIP_PROGRAM
#from mifaredef import Def_MIFARE_COMMANDS
#from cmdchangebaudrate import CmdChangeBaudrate
#from cmdactivateall import CmdActivateAll
#from cmdfirmware import CmdFirmware
from prompt_toolkit import print_formatted_text, HTML


def quit():
    os._exit(0)


class SmTesterAsyncHandler():
    def __init__(self,spv1handler,async_callback=None,auto_log=True):
        self.auto_log = auto_log
        self.async_callback = async_callback
        self.spv1handler = spv1handler
        self.programming_error_response = None
        self.programming_error_loginfo = None
        self.working = False
        self.reset_programming_async_result()

    def register_async_callback(self,callback):
        self.async_callback = callback

    def poll_programming_async_result(self) -> (bool,bool, RESPONSE_CHIP_PROGRAM, LogInfo):
        working = self.working
        # clear working state working state will be used to extend timeout at programing side.
        self.working = False
        return self.programming_is_ended, self.programming_has_error, self.programming_error_response, self.programming_error_loginfo, working

    def reset_programming_async_result(self):
        self.programming_is_ended = False
        self.programming_has_error = False

    def dll_callback_async_rx_protocol(self,instanceID, rx_spv1_frame: STRUCT_SPV1FRAME):
        #rx_spv1_frame.print_frame()
        if (rx_spv1_frame.command == Def_SMTESTER_COMMANDS.CHIP_PROGRAM):
            cmd_chip_program = CmdChipProgram()
            try:
                response, loginfo = self.spv1handler.response_builder_helper(cmd_chip_program,rx_spv1_frame, auto_log=self.auto_log)
                # print("response.responseErrorcode", response.responseErrorcode)
                if (response.responseErrorcode != Def_SPSCERR.SUCCESS):
                    self.programming_error_response = response
                    self.programming_error_loginfo = loginfo
                    self.programming_has_error = True
                    self.programming_is_ended = True
                elif (response.responseErrorcode == Def_SPSCERR.SUCCESS):
                    # info mesajlarda da SUCCESS geliyor, bu nedele error_type ile kontrolu sağlıyoruz.
                    if (response.error_type == ENUM_CHIP_PROGRAM_RESPONSE_ERROR_TYPE.PROGRAM_SUCCESS):
                        self.programming_has_error = False
                        self.programming_is_ended = True
                        print_formatted_text(HTML("<yellow>{}</yellow>").format("\r\nProgramming is finished successfully..."))
                    elif (response.error_type == ENUM_CHIP_PROGRAM_RESPONSE_ERROR_TYPE.UPGRADE_SUCCESS):
                        self.programming_has_error = False
                        self.programming_is_ended = True
                        print_formatted_text(HTML("<yellow>{}</yellow>").format("\r\nUpgrade is finished successfully..."))
                    elif (response.error_type == ENUM_CHIP_PROGRAM_RESPONSE_ERROR_TYPE.PROGRAM_INFO):
                        self.programming_is_ended = False
                        self.programming_has_error = False
                        if (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.START_PROGRAMMING):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Programming is started..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.PROGRAMMING_AND_VERIFYING):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Programming and Verifying..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.NO_PROTECTION):
                            print_formatted_text(HTML("<ansired>{}</ansired>").format("ATTENTION !!!CHIP IS NOT PROTECTED!!!..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.PROGRAMMING):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Programming..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.VERIFYING):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("\r\nVerifying..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.UPGRADING):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Upgrading..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.ERASING_MEMORY):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Erasing Memory..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.REMOVING_PROTECTION):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Removing Protection..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.PROTECTION_REMOVED):
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("Protection Removed..."))
                        elif (response.programming_info == ENUM_CHIP_PROGRAM_RESPONSE_INFO.WORKING):
                            self.working = True
                            print_formatted_text(HTML("<yellow>{}</yellow>").format("."),end="")


            except Exception as e:
                print("Sistem hatası (Exception) @dll_callback_async_rx_protocol", e)
                quit()
                #print(response.responseErrorcode)
                #print(response.responseMessage)
        else:
            print("ASYNC SPV1 RESPONSE InstanceID:", instanceID, " Command", hex(rx_spv1_frame.command))
            rx_spv1_frame.print_frame()

        # Call async callback
        """
        if (rx_spv1_frame.command == Def_MIFARE_COMMANDS.ACTIVATE_ALL) or \
                (rx_spv1_frame.command == Def_MIFARE_COMMANDS.SEEK_FOR_TAG):

            cmd_activate_all = CmdActivateAll()
            self.spv1handler.response_builder_helper(cmd_activate_all,rx_spv1_frame)

            if self.async_card_read_callback!=None:
                self.async_card_read_callback(cmd_activate_all)

        elif rx_spv1_frame.command == Def_MIFARE_COMMANDS.FIRMWARE:

            cmd_firmware = CmdFirmware()
            self.spv1handler.response_builder_helper(cmd_firmware,rx_spv1_frame)

        elif rx_spv1_frame.command == Def_MIFARE_COMMANDS.CHANGE_BAUD_RATE:

            cmd_change_baudrate = CmdChangeBaudrate()
            self.spv1handler.response_builder_helper(cmd_change_baudrate,rx_spv1_frame)

        else:
            print("UNKNOWN ASYNC COMMAND RESPONSE",hex(rx_spv1_frame.command))
            pass
            #custom handle rx protocol
        """


