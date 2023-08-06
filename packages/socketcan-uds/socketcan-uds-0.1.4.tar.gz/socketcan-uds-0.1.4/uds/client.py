""" module:: uds.client
    :platform: Posix
    :synopsis: A class file for Universal Diagnostic Service (UDS) client
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import datetime

from queue import Queue, Empty
from threading import Thread
from typing import Union, Callable

from socketcan import CanIsoTpSocket
from uds.common import *

import logging

LOGGER = logging.getLogger(__name__)


class UdsClient:
    """
    UDS Client class

    depends on socketcan
    therefore runs on linux only
    """

    def __init__(self,
                 socket: CanIsoTpSocket,
                 timeout: Union[str, int] = "auto",
                 ):
        """
        Constructor

        :param socket: A SocketCAN IsoTp socket.
        """
        self._s = socket
        if timeout == "auto" or (isinstance(timeout, int) and (0 < timeout < 100)):
            self.timeout = timeout
        else:
            raise ValueError("timeout {0} is not handled".format(timeout))
        # Todo: Add more parameters to initial set
        self.session_parameters = {"p2_server_max": 0.05,  # 50ms
                                   "p2*_server_max": 5,  # 5s
                                   }
        self.rx_queue = Queue()
        self.rx_handler = Thread(target=self._handle_rx)
        self.rx_handler.setDaemon(True)
        self.rx_handler.start()

    # basic functionality

    def _handle_rx(self) -> None:
        """
        Puts data from socket into a queue,
        where the requester (main thread) in self.recv()
        :return: Nothing.
        """
        while True:
            self.rx_queue.put(self._s.recv())

    def _send(self, data: bytes) -> int:
        """
        Sends data to the socket.
        :param data: The data to be sent.
        :return: The length of data that was sent.
        """
        return self._s.send(data=data)

    def _recv(self) -> Optional[bytes]:
        """
        Receives data from rx_queue in case it was filled by
        rx_handler.
        The underlying queue mechanism may raise an Empty Exception.
        :return: Data bytes.
        """
        timeout = self.timeout
        if timeout == "auto":
            timeout = self.session_parameters.get("p2*_server_max")
        assert 0 < timeout < 100
        return self.rx_queue.get(timeout=timeout)

    def _on_diagnostic_session_control_response(self,
                                                session_parameters: dict) -> None:
        session_parameters.pop("response_sid")
        LOGGER.debug("New Session Parameters {0}".format(session_parameters))
        self.session_parameters.update(session_parameters)

    def request(self, req: bytes, no_ack: bool = False) -> Optional[dict]:
        """
        Service request function
        It handles transmission, reception and check if a negative response error should be raised
        :param req: The request as bytes.
        :param no_ack: Don't wait for a response. Should be set when calling request. This is not automatically checked.
        :return: The response as bytes.
        :raises: Subtypes of NegativeResponse, UdsTimeoutError, etc.
        """
        if not self.rx_queue.empty():
            LOGGER.debug("flushing rx_queue before sending a new request")
            while not self.rx_queue.empty():
                resp_bytes = self.rx_queue.get_nowait()
                LOGGER.debug("dropping {0}".format(parse_response(resp_bytes)))

        bytes_sent = self._send(req)
        LOGGER.debug("Sent {0}".format(req))
        ts_request_sent = datetime.datetime.now()
        if bytes_sent != len(req):
            raise RuntimeError("bytes_sent != len(data)")
        if not no_ack:
            for cnt in range(2):
                try:
                    resp_bytes = self._recv()
                except Empty:
                    # break here, UdsTimeoutError is raised at the end of the function instead
                    break
                else:
                    time_for_response = datetime.datetime.now() - ts_request_sent
                    LOGGER.debug("Response received after timedelta {0}".format(time_for_response))
                    try:
                        resp_dict = parse_response(resp_bytes)
                        LOGGER.debug("Received {0}".format(resp_dict))
                    except RequestCorrectlyReceivedButResponsePending:
                        # wait for the real delayed response
                        continue
                    else:
                        if req[0] == ServiceId.DiagnosticSessionControl:
                            # we update the server's timing info
                            self._on_diagnostic_session_control_response(resp_dict.copy())
                        return resp_dict
            raise UdsTimeoutError

    # convenience functions for specific services

    def diagnostic_session_control(self,
                                   session: DiagnosticSession = DiagnosticSession.ExtendedDiagnosticSession) -> dict:
        """
        Basic uds service diagnostic session control.
        :param session: The requested diagnostic session.
        :return: The data that was returned.
        """
        return self.request(req=concat_diagnostic_session_control_request(session=session))

    def ecu_reset(self,
                  rtype: ResetType = ResetType.HardReset) -> dict:
        """
        Basic uds service ecu reset.
        :param rtype: The requested ResetType.
        :return: The data that was returned.
        """
        return self.request(req=concat_ecu_reset_request(rtype=rtype))

    def security_access(self,
                        slevel: int,
                        key: Optional[bytes] = None,
                        ) -> dict:
        """
        Basic uds service security access.
        The method is called SEED&KEY and was defined in KWP2000(ISO14230).
        The idea is to have a secret needed to compute a key from a given seed.
        In reality the seed/key is 4 bytes big endian and the seed2key function is a simple function,
        e.g. adding some value, rotating the seed, xor it with a mask value etc.

        Each security level is a tuple of an uneven number to request a seed
        and the next (even) number to post a key.
        :param slevel: The security level. Uneven=SeedRequest, Even=KeyPost
        :param key: The key bytes.
        :return: The data that was returned.
        """

        return self.request(req=concat_security_access_request(slevel=slevel,
                                                               key=key))

    def communication_control(self,
                              ctrl_type: ComCtrlType,
                              com_type: Optional[int] = None,
                              node_id: Optional[int] = None,
                              no_ack: bool = False) -> dict:
        """
        Basic uds service communication control.
        :param ctrl_type: The control type.
        :param com_type: The communication type.
        :param node_id: The Node identification number.
        :param no_ack: Suppress the the positive response.
        :return: The data that was returned.
        """
        return self.request(req=concat_communication_control_request(ctrl_type=ctrl_type,
                                                                     com_type=com_type,
                                                                     node_id=node_id,
                                                                     no_ack=no_ack))

    def tester_present(self,
                       no_ack: bool = False) -> dict:
        """
        Basic uds service tester present.
        :param no_ack: Suppress the the positive response.
        :return: The data that was returned. Actually nothing except for the response_sid.
        """
        return self.request(req=concat_tester_present_request(no_ack=no_ack))

    def control_dtc_setting(self,
                            stype: DtcSettingType,
                            dtcs: Optional[List[int]] = None,
                            no_ack: bool = False):
        """
        Basic uds service control dtc setting.
        :param stype: The DtcSettingType On or Off
        :param dtcs: A list of dtc numbers in range 0-0xFFFFFF
        :param no_ack: Suppress the the positive response.
        :return: The data that was returned.
        """
        return self.request(req=concat_control_dtc_setting_request(stype=stype, dtcs=dtcs, no_ack=no_ack))

    def read_data_by_id(self,
                        did: int) -> dict:
        """
        Basic uds service read data by id.
        :param did: The diagnostic identifier to be read.
        :return: The data that was returned.
        """
        return self.request(req=concat_read_data_by_id_request(did=did))

    def write_data_by_id(self,
                         did: int,
                         data: bytes) -> dict:
        """
        Basic uds service write data by id.
        :param did: The diagnostic identifier to be read.
        :param data: The data bytes to be written.
        :return: The data that was returned. Actually nothing except for the response_sid and the did for confirmation.
        """
        return self.request(req=concat_write_data_by_id_request(did=did,
                                                                data=data))

    def request_download(self,
                         addr: int,
                         size: int,
                         compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                         encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                         ) -> dict:
        """
        Basic uds service request download.
        :param addr: The address of the download. Hardcoded to 32bit for now.
        :param size: The size of the download. Hardcoded to 32bit for now.
        :param compression_method: The method of compression.
        :param encryption_method: The method of encryption.
        :return: The data that was returned.
        """
        return self.request(req=concat_request_download_request(addr=addr,
                                                                size=size,
                                                                compression_method=compression_method,
                                                                encryption_method=encryption_method))

    def request_upload(self,
                       addr: int,
                       size: int,
                       compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                       encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                       ) -> dict:
        """
        Basic uds service request upload.
        :param addr: The address of the upload. Hardcoded to 32bit for now.
        :param size: The size of the upload. Hardcoded to 32bit for now.
        :param compression_method: The method of compression.
        :param encryption_method: The method of encryption.
        :return: The data that was returned.
        """
        return self.request(req=concat_request_upload_request(addr=addr,
                                                              size=size,
                                                              compression_method=compression_method,
                                                              encryption_method=encryption_method))

    def transfer_data(self,
                      block_sequence_counter: int,
                      data: bytes,
                      ) -> dict:
        """
        Basic uds service transfer data.
        :param block_sequence_counter: The block counter for this transfer.
        :param data: The data to be transferred.
        :return: The data that was returned.
        """
        return self.request(req=concat_transfer_data_request(block_sequence_counter=block_sequence_counter,
                                                             data=data))

    def request_transfer_exit(self,
                              transfer_request_parameters: bytes = bytes(),
                              ) -> dict:
        """
        Basic uds service request transfer exit.
        :param transfer_request_parameters: A never used manufacturer specific value.
        :return: The data that was returned.
        """
        return self.request(
            req=concat_request_transfer_exit_request(transfer_request_parameters=transfer_request_parameters))

    def clear_diagnostic_information(self,
                                     dtc_mask: int,
                                     memory_select: Optional[int] = None,
                                     ) -> dict:
        """
        Basic uds service clear diagnostic information.
        :param dtc_mask: The Dtc Mask. A DTC Mask is a group of dtcs, e.g. 0xFFFF33 is emissions-related systems.
        :param memory_select: An optional byte to select a specific error memory, e.g. a secondary error memory mirror.
        :return: The data that was returned.
        """
        return self.request(
            req=concat_clear_diagnostic_information_request(dtc_mask=dtc_mask,
                                                            memory_select=memory_select))

    def routine_control(self,
                        routine_control_type: RoutineControlType,
                        routine_id: int,
                        data: Optional[bytes] = None
                        ) -> dict:
        """
        Basic uds service routine control.
        :param routine_control_type: The control type, e.g. Start/Stop/Poll.
        :param routine_id: The Routine Id.
        :param data: The (optional) data that the routine consumes.
        :return: The request as bytes.
        """
        return self.request(req=concat_routine_control_request(routine_control_type=routine_control_type,
                                                               routine_id=routine_id,
                                                               data=data))


