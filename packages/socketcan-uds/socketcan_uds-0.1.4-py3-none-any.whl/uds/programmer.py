""" module:: uds.programmer
    :platform: Posix
    :synopsis: A class file for a uds programmer
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from abc import ABC, abstractmethod

from uds.common import *

from uds.client import UdsClient

import logging
LOGGER = logging.getLogger(__name__)


class UdsProgrammerABC(ABC):
    """
    Abstract Base Class for an UDS Programmer class
    """

    def __init__(self,
                 client: UdsClient,
                 ):
        """
        Constructor

        :param client: A UdsClient for the uds services layer.
        """
        self._client = client

        self._programming_file = None
        self._current_state = None
        self._progress = None

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, val):
        self._progress = val

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, val):
        self._current_state = val

    @abstractmethod
    def prepare_programming(self) -> bool:
        """
        Check the programming preconditions.
        :return: True if met, False otherwise
        """

    @abstractmethod
    def switch_to_bootloader(self) -> bool:
        """
        Switch ecu to bootloader.
        :return: True if successful, False otherwise
        """

    @abstractmethod
    def is_device_in_bootloader(self) -> bool:
        """
        Check if the device is in bootloader.
        :return: True if successful, False otherwise
        """

    @abstractmethod
    def unlock_device(self) -> bool:
        """
        Unlock the device for programming.
        :return: True if successful, False otherwise
        """

    @abstractmethod
    def pre_block_download(self) -> bool:
        """
        Prepare a block before download.
        :return: True if successful, False otherwise
        """

    def download_block(self,
                       addr: int,
                       data: bytes,
                       compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                       encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                       transfer_request_parameters: bytes = bytes()) -> True:
        """
        Download a block.
        :param addr: The address of the upload. Hardcoded to 32bit for now.
        :param data: The data to be transferred.
        :param compression_method: The method of compression.
        :param encryption_method: The method of encryption.
        :param transfer_request_parameters: A never used manufacturer specific value.
        :return: Nothing.
        """
        size = len(data)
        LOGGER.debug("Download Block - Request Download Addr {0} Size {1}".format(addr, size))
        resp = self._client.request_download(addr=addr,
                                             size=size,
                                             compression_method=compression_method,
                                             encryption_method=encryption_method)
        block_size = resp.get("max_block_length")

        for chunk_idx, chunk_bytes in enumerate(
                [data[idx:idx + block_size] for idx in range(0, len(data), block_size)]):
            LOGGER.debug(
                "Download Block - Transfer Data Block {0} Size {1}".format(chunk_idx + 1, len(chunk_bytes)))
            self._client.transfer_data(block_sequence_counter=chunk_idx + 1,
                                       data=chunk_bytes)
        LOGGER.debug("Download Block - Request Transfer Exit")
        self._client.request_transfer_exit(transfer_request_parameters=transfer_request_parameters)
        LOGGER.debug("Download Block - Complete")

        success = True
        return success

    @abstractmethod
    def post_block_download(self) -> bool:
        """
        Check a block after download.
        :return: True if successful, False otherwise
        """

    @abstractmethod
    def finish_programming(self) -> bool:
        """
        Finish the programming, e.g. reset the device.
        :return: True if successful, False otherwise
        """

    @abstractmethod
    def load_programming_file(self, filepath: str) -> bool:
        """
        Load the file that is going to be programmed.
        :return: True if successful, False otherwise
        """

    # def program_ecu(self,
    #                 seca_level: int,
    #                 seed_key_function: Callable[[Union[int, bytes]], Union[int, bytes]],
    #                 blocks: dict) -> None:
    #     """
    #     Program an ecu by commonly used method.
    #     Note: This is intended as an example, basically to describe the basic
    #           steps how programming via UDS works. It will become obsolete when
    #           UDSFlasher class has been implemented.
    #     :param seca_level: The security access level to get programming access.
    #     :param seed_key_function: The function that calculates a key from a seed.
    #     :param blocks: The binary blocks that are to be transmitted.
    #     :return: Nothing.
    #     """
    #     # Example function - hardcode a typically programming process without exception handling here
    #     # 1. switch to programming session - this typically restarts the device to run in bootloader
    #     self._client.diagnostic_session_control(DiagnosticSession.ProgrammingSession)
    #     # 2. security access - to gain priviliges for other services that are needed during process
    #     seed = self._client.security_access(slevel=seca_level).get("seed")
    #     key = seed_key_function(seed)
    #     self._client.security_access(slevel=seca_level + 1, key=key)
    #     # 3. download each block
    #     for block_name, block_data in blocks.items():
    #         LOGGER.debug("Programming Block {0}".format(block_name))
    #         addr = block_data.get("addr")
    #         data = block_data.get("data")
    #         compression_method = block_data.get("compression_method")
    #         encryption_method = block_data.get("encryption_method")
    #         self._client.download_block(addr=addr,
    #                                     data=data,
    #                                     compression_method=compression_method,
    #                                     encryption_method=encryption_method)
    #     # 4. reset the ecu, so it jumps from bootloader to application or whatever is normally running on the device
    #     self._client.ecu_reset()


class ExampleUdsProgrammer(UdsProgrammerABC):
    def load_programming_file(self, filepath: str) -> bool:
        """
        Load the programming file. Save filepath to private variable
        for an easy example.
        :param filepath: The filepath.
        :return: True if successful.
        """
        self._programming_file = filepath
        return True

    def is_device_in_bootloader(self) -> bool:
        """
        Read a specific did and ask the device if it's in bootloader.
        :return: True if in bootloader.
        """
        check_bootloader_did = 0xFEED
        data = self._client.read_data_by_id(did=check_bootloader_did).get("data")
        status = data.decode().lower().startswith("bootloader")
        return status

    def finish_programming(self) -> bool:
        """
        Write the programming date for an easy example.
        :return: True if successful.
        """
        programming_date_did = 0x4242
        self._client.write_data_by_id(did=programming_date_did, data=bytes.fromhex("11 22 33 44"))
        success = True
        return success

    def unlock_device(self) -> bool:
        """
        Execute seed and key routine to unlock the device.
        :return: True if successful.
        """
        access_level = 1
        seed = self._client.security_access(slevel=access_level).get("seed")
        key = bytes.fromhex("11 22 33 45")
        self._client.security_access(slevel=access_level + 1, key=key)
        success = True
        return success

    def post_block_download(self) -> bool:
        """
        Execute a check routine in device.
        :return: True if successful.
        """
        self._client.routine_control(routine_control_type=RoutineControlType.StartRoutine,
                                     routine_id=0x1234,
                                     data=bytes.fromhex("11 22 33 44 55 66 77 88"))
        success = True
        return success

    def pre_block_download(self) -> bool:
        """
        Write the workshop name into the device for
        an easy example.
        :return: True if successful.
        """
        workshop_did = 0xCAFE
        self._client.write_data_by_id(did=workshop_did, data="1234".encode())
        success = True
        return success

    def switch_to_bootloader(self) -> bool:
        """
        Switch to programming session.
        This typically restarts a device into bootloader.
        :return: True if successful.
        """
        self._client.diagnostic_session_control(session=DiagnosticSession.ProgrammingSession)
        success = True
        return success

    def prepare_programming(self) -> bool:
        """
        Check if the logical preconditions for programming are fulfilled.
        You won't flash an engine ecu while the engine is running, would you?
        Well it can be done in some rare cases.
        :return: True if successful.
        """
        check_programming_did = 0xBEEF
        data = self._client.read_data_by_id(did=check_programming_did).get("data")
        status = bool.from_bytes(data, "big")
        return status
