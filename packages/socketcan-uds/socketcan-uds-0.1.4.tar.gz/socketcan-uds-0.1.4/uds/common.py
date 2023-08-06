""" module:: uds.common
    :platform: Posix
    :synopsis: An abstraction of ISO 14229 UDS protocol
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import struct
from enum import IntEnum

import logging
from typing import Optional, List

LOGGER = logging.getLogger(__name__)


class DiagnosticSession(IntEnum):
    """
    Diagnostic session enum
    """
    DefaultSession = 1
    ProgrammingSession = 2
    ExtendedDiagnosticSession = 3
    SafetySystemDiagnosticSession = 4


class ResetType(IntEnum):
    """
    Reset type enum
    """
    HardReset = 1
    KeyOffOnReset = 2
    SoftReset = 3
    EnableRapidPowerShutdown = 4
    DisableRapidPowerShutdown = 5


class ComCtrlType(IntEnum):
    """
    Control types used in Communication Control service.
    """
    EnableRxTx = 0
    EnableRxDisableTx = 1
    DisableRxEnableTx = 2
    DisableRxTx = 3
    EnableRxDisableTxEnhancedAddressInfo = 4
    EnableRxTxEnhancedAddressInfo = 5


class DtcSettingType(IntEnum):
    """
    Type used in uds service control dtc settings.
    """
    On = 1
    Off = 2


class DtcReportType(IntEnum):
    """
    Type used in uds service read dtc information
    """
    ReportNumberOfDtcByStatusMask = 1
    ReportDtcByStatusMask = 2
    ReportDtcSnapshotIdentification = 3
    ReportDtcSnapshotByDtcNumber = 4
    ReportDtcStoredDataByRecordNumber = 5
    ReportDtcExtDataRecordByDtcNumber = 6
    ReportNumberOfDtcBySeverityMaskRecord = 7
    ReportDtcBySeverityMaskRecord = 8
    ReportSeverityInformationOfDtc = 9
    ReportSupportedDtc = 0xA
    ReportFirstTestFailedDtc = 0xB
    ReportFirstConfirmedDtc = 0xC
    ReportMostRecentTestFailedDtc = 0xD
    ReportMostRecentConfirmedDtc = 0xE
    ReportDtcFaultDetectionCounter = 0x14
    ReportDtcWithPermanentStatus = 0x15
    ReportDtcExtDataRecordByRecordNumber = 0x16
    ReportUserDefMemoryDtcByStatusMask = 0x17
    ReportUserDefMemoryDtcSnapshotRecordByDtcNumber = 0x18
    ReportUserDefMemoryDtcExtDataRecordByDtcNumber = 0x19
    ReportSupportedDtcExtDataRecord = 0x1A
    ReportWwhobdDtcByMaskRecord = 0x42
    ReportWwhobdDtcWithPermanentStatus = 0x55
    ReportDtcInformationByDtcReadinessGroupIdentifier = 0x56


class CompressionMethod(IntEnum):
    NO_COMPRESSION = 0
    LZMA = 0xA


class EncryptionMethod(IntEnum):
    NO_ENCRYPTION = 0
    AES128CBC = 0xA


class ServiceId(IntEnum):
    """
    Service id enum
    """
    # Diagnostic and Communication Management
    DiagnosticSessionControl = 0x10
    EcuReset = 0x11
    SecurityAccess = 0x27
    CommunicationControl = 0x28
    TesterPresent = 0x3E
    AccessTimingParameter = 0x83
    SecuredDataTransmission = 0x84
    ControlDtcSettings = 0x85
    ResponseOnEvent = 0x86
    LinkControl = 0x87

    # Data Transmission
    ReadDataByIdentifier = 0x22
    ReadMemoryByAddress = 0x23
    ReadScalingDataByIdentifier = 0x24
    ReadDataByPeriodicIdentifier = 0x2A
    DynamicallyDefineDataIdentifier = 0x2C
    WriteDataByIdentifier = 0x2E
    WriteMemoryByAddress = 0x3D

    # Stored Data Transmission
    ClearDiagnosticInformation = 0x14
    ReadDtcInformation = 0x19

    # Input / Output Control
    InputOutputByIdentifier = 0x2F

    # Remote Activation of Routine
    RoutineControl = 0x31

    # Upload / Download
    RequestDownload = 0x34
    RequestUpload = 0x35
    TransferData = 0x36
    RequestTransferExit = 0x37


class ResponseCode(IntEnum):
    """
    UDS Negative Response Codes

    Some Explanation, when ISO14229 (UDS) was made,
    it had to be compatible with the preceding ISO14230 (KWP2000)
    so everything up to the 0x40 range is nearly identical.
    BTW: See how BOSCH managed to fake the ISO numbering?
    There are some unofficial ranges for different topics
    0x10-0x1F, 0x20-0x2F and so on.
    """
    # tester side error
    GeneralReject = 0x10
    ServiceNotSupported = 0x11
    SubFunctionNotSupported = 0x12
    IncorrectMessageLengthOrInvalidFormat = 0x13
    ResponseTooLong = 0x14

    # device side error
    BusyRepeatRequest = 0x21
    ConditionsNotCorrect = 0x22
    RequestSequenceError = 0x24
    NoResponseFromSubnetComponent = 0x25
    FaultPreventsExecutionOfRequestedAction = 0x26

    # function side error
    RequestOutOfRange = 0x31
    SecurityAccessDenied = 0x33
    InvalidKey = 0x35
    ExceededNumberOfAttempts = 0x36
    RequiredTimeDelayNotExpired = 0x37

    # 0x38-0x4F Reserved by Extended Data Link Security Document

    UploadDownloadNotAccepted = 0x70
    TransferDataSuspended = 0x71
    GeneralProgrammingFailure = 0x72
    WrongBlockSequenceCounter = 0x73

    RequestCorrectlyReceivedButResponsePending = 0x78
    # This is essentially not an Error, it is just a delay information.
    # This Response Code is due to the fact that standard autosar modules do not necessarily run on the same time disc
    # and no IPC method has every been defined for Autosar.

    SubFunctionNotSupportedInActiveSession = 0x7E
    ServiceNotSupportedInActiveSession = 0x7F


class RoutineControlType(IntEnum):
    """
    The first byte of Routine Control Request
    that determines what should be done with the routine.
    """
    StartRoutine = 1
    StopRoutine = 2
    RequestRoutineResults = 3


# helper functions

def int_to_dtc_mask(num: int,
                    ) -> bytes:
    """
    A helper to cast an integer into a 3 byte big endian representation.
    :param num: The number.
    :return: The number as 3 bytes.
    """
    assert 0 <= num < 0x1000000
    return struct.pack(">I", num)[1:]


def dtc_mask_to_int(mask: bytes,
                    ) -> int:
    """
    A helper to cast a 3 byte big endian number to integer
    :param mask: The 3 bytes big endian value.
    :return: The number as integer.
    """
    assert len(mask) == 3
    return struct.unpack(">I", mask.rjust(4, b"\x00"))[0]


# parser and concat functions for services

def concat_diagnostic_session_control_request(session: DiagnosticSession) -> bytes:
    """
    Concat diagnostic session control request.
    :param session: The requested diagnostic session.
    :return: The request as bytes.
    """
    assert session in DiagnosticSession
    return struct.pack("BB", ServiceId.DiagnosticSessionControl, session)


def parse_diagnostic_session_control_response(resp: bytes) -> dict:
    """
    Parse diagnostic session control response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack(">BBHH", resp))
    # scale both values to seconds
    values[1] = DiagnosticSession(values[1])
    values[2] = values[2] / 1000
    values[3] = values[3] / 100
    return dict(zip(["response_sid", "session", "p2_server_max", "p2*_server_max"], values))


def concat_ecu_reset_request(rtype: ResetType) -> bytes:
    """
    Concat ecu reset request.
    :param rtype: The requested ResetType.
    :return: The request as bytes.
    """
    assert rtype in ResetType
    return struct.pack("BB", ServiceId.EcuReset, rtype)


def parse_ecu_reset_response(resp: bytes) -> dict:
    """
    Parse ecu reset response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "rtype", "power_down_time"], resp))


def concat_security_access_request(slevel: int,
                                   key: Optional[bytes]
                                   ) -> bytes:
    """
    Concat security access request.
    :param slevel: The security level. Uneven=SeedRequest, Even=KeyPost
    :param key: The key bytes.
    :return: The request as bytes.
    """
    if slevel not in range(0x100):
        raise ValueError("Value {0} is not in range 0-0xFF".format(slevel))

    if (slevel & 0x1) == 0:
        if key is None:
            raise ValueError("Security Access to an even slevel ({0}) must provide a key {1}".format(slevel, key))
        req = struct.pack("BB{0}s".format(len(key)), ServiceId.SecurityAccess, slevel, key)
    else:
        req = struct.pack("BB", ServiceId.SecurityAccess, slevel)
    return req


def parse_security_access_response(resp: bytes) -> dict:
    """
    Parse security access response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    if resp[1] & 0x1:
        # response to seed request, so extract seed, otherwise not
        fmt = "BB{0}s".format(len(resp) - 2)
    else:
        fmt = "BB"
    values = list(struct.unpack(fmt, resp))
    keys = ["response_sid", "slevel", "seed"]
    return dict(zip(keys, values))


def concat_read_data_by_id_request(did: int) -> bytes:
    """
    Concat read data by id request.
    :param did: The diagnostic identifier to be read.
    :return: The request as bytes.
    """
    if did not in range(0x10000):
        raise ValueError("Value {0} is not in range 0-0xFFFF".format(did))
    return struct.pack(">BH", ServiceId.ReadDataByIdentifier, did)


def parse_read_data_by_id_response(resp: bytes) -> dict:
    """
    Parse read data by id response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "did", "data"], struct.unpack(">BH{0}s".format(len(resp) - 3), resp)))


def concat_communication_control_request(ctrl_type: ComCtrlType,
                                         com_type: Optional[int] = None,
                                         node_id: Optional[int] = None,
                                         no_ack: bool = False,
                                         ) -> bytes:
    """
    Concat communication control request.
    :param ctrl_type: The control type.
    :param com_type: The communication type.
    :param node_id: The Node identification number.
    :param no_ack: Suppress the the positive response.
    :return: The request as bytes.
    """
    assert ctrl_type in ComCtrlType
    if no_ack:
        ctrl_type_byte = ctrl_type | 0x80
    else:
        ctrl_type_byte = ctrl_type
    if com_type is not None and node_id is not None:
        # newer version
        return struct.pack(">BBBH", ServiceId.CommunicationControl, ctrl_type_byte, com_type, node_id)
    else:
        # old version
        return struct.pack("BB", ServiceId.CommunicationControl, ctrl_type_byte)


def parse_communication_control_response(resp: bytes) -> dict:
    """
    Parse communication control response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack("BB", resp))
    if values[1] & 0x80:
        raise ValueError("The suppress positive response bit is set, this is impossible")
    values[1] = ComCtrlType(values[1] & 0x7F)
    return dict(zip(["response_sid", "ctrl_type"], values))


# Todo: Authentication Request here - but its way to complicated for a beta, add when first non-beta release is out.


def concat_tester_present_request(no_ack: bool = False,
                                  ) -> bytes:
    """
    Concat tester present request.
    :param no_ack: Suppress the the positive response.
    :return: The request as bytes.
    """
    zerosubfunction = 0
    if no_ack:
        zerosubfunction = 0x80
    return struct.pack("BB", ServiceId.TesterPresent, zerosubfunction)


def parse_tester_present_response(resp: bytes) -> dict:
    """
    Parse tester present response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    # second byte zerosubfunction is always 0
    return dict(zip(["response_sid", "zerosubfunction"], resp))


def concat_control_dtc_setting_request(stype: DtcSettingType,
                                       dtcs: Optional[List[int]] = None,
                                       no_ack: bool = False):
    """
    Concat control dtc setting request.
    :param stype: The DtcSettingType On or Off
    :param dtcs: A list of dtc numbers in range 0-0xFFFFFF
    :param no_ack: Suppress the the positive response.
    :return: The request as bytes.
    """
    stype_byte = stype
    if no_ack:
        stype_byte = stype_byte | 0x80
    ret = bytearray(struct.pack("BB", ServiceId.ControlDtcSettings, stype_byte))
    if dtcs is not None:
        for dtc in dtcs:
            ret.extend(int_to_dtc_mask(dtc))
    return bytes(ret)


def parse_control_dtc_setting_response(resp: bytes) -> dict:
    """
    Parse control dtc setting response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    # second byte zerosubfunction is always 0
    values = list(resp)
    values[1] = DtcSettingType(values[1])
    return dict(zip(["response_sid", "stype"], values))


def concat_write_data_by_id_request(did: int,
                                    data: bytes) -> bytes:
    """
    Concat write data by id request.
    :param did: The diagnostic identifier to be read.
    :param data: The data bytes to be written.
    :return: The request as bytes.
    """
    if did not in range(0x10000):
        raise ValueError("Value {0} is not in range 0-0xFFFF".format(did))
    if len(data) == 0:
        raise ValueError("Invalid length of data {0}".format(len(data)))
    return struct.pack(">BH{0}s".format(len(data)), ServiceId.WriteDataByIdentifier, did, data)


def parse_write_data_by_id_response(resp: bytes) -> dict:
    """
    Parse write data by id response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "did"], struct.unpack(">BH", resp)))


def concat_clear_diagnostic_information_request(dtc_mask: int,
                                                memory_select: Optional[int] = None) -> bytes:
    """
    Concat clear diagnostic information request.
    :param dtc_mask: The Dtc Mask. A DTC Mask is a group of dtcs, e.g. 0xFFFF33 is emissions-related systems.
    :param memory_select: An optional byte to select a specific error memory, e.g. a secondary error memory mirror.
    :return: The request as bytes.
    """
    if memory_select is not None:
        return struct.pack(">B3sB", ServiceId.ClearDiagnosticInformation, int_to_dtc_mask(dtc_mask), memory_select)
    else:
        return struct.pack(">B3s", ServiceId.ClearDiagnosticInformation, int_to_dtc_mask(dtc_mask))


def parse_clear_diagnostic_information_response(resp: bytes) -> dict:
    """
    Parse clear diagnostic information response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", ], struct.unpack("B", resp)))


def concat_request_download_or_upload_request(service_id: ServiceId,
                                              addr: int,
                                              size: int,
                                              compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                                              encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                                              ) -> bytes:
    """
    Concat request download/upload request. This method prevents double coding
    because the service and its response only differ by the service id.
    :param service_id: Select download/upload via service_id
    :param addr: The address of the download/upload.
    :param size: The size of the download/upload.
    :param compression_method: The method of compression.
    :param encryption_method: The method of encryption.
    :return: The request as bytes.
    """
    assert service_id in [ServiceId.RequestDownload, ServiceId.RequestUpload]
    assert 0 <= compression_method <= 0xF
    assert 0 <= encryption_method <= 0xF

    data_format_identifier = (compression_method << 4) | encryption_method

    addr_length = int(len("{0:02X}".format(addr)) / 2)
    size_length = int(len("{0:02X}".format(size)) / 2)
    LOGGER.debug("addr {0} len {1}, size {2} len {3}".format(addr, addr_length, size, size_length))

    address_and_length_format_identifier = (size_length << 4) | addr_length
    ret = bytearray((service_id, data_format_identifier, address_and_length_format_identifier))
    ret.extend(addr.to_bytes(length=addr_length, byteorder="big"))
    ret.extend(size.to_bytes(length=size_length, byteorder="big"))
    return bytes(ret)


def concat_request_download_request(addr: int,
                                    size: int,
                                    compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                                    encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                                    ) -> bytes:
    """
    Concat request download request.
    :param addr: The address of the download. Hardcoded to 32bit for now.
    :param size: The size of the download. Hardcoded to 32bit for now.
    :param compression_method: The method of compression.
    :param encryption_method: The method of encryption.
    :return: The request as bytes.
    """
    return concat_request_download_or_upload_request(service_id=ServiceId.RequestDownload,
                                                     addr=addr,
                                                     size=size,
                                                     compression_method=compression_method,
                                                     encryption_method=encryption_method
                                                     )


def concat_request_upload_request(addr: int,
                                  size: int,
                                  compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                                  encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                                  ) -> bytes:
    """
    Concat request download request.
    :param addr: The address of the download. Hardcoded to 32bit for now.
    :param size: The size of the download. Hardcoded to 32bit for now.
    :param compression_method: The method of compression.
    :param encryption_method: The method of encryption.
    :return: The request as bytes.
    """
    return concat_request_download_or_upload_request(service_id=ServiceId.RequestUpload,
                                                     addr=addr,
                                                     size=size,
                                                     compression_method=compression_method,
                                                     encryption_method=encryption_method
                                                     )


def parse_request_download_or_upload_response(resp: bytes) -> dict:
    """
    Parse request download/upload response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    response_sid = resp[0]
    length_format_identifier = resp[1] >> 4
    if length_format_identifier != len(resp[2:]):
        raise ValueError(
            "Missmatch length_format_identifier {0} != buffer length {1}".format(length_format_identifier,
                                                                                 len(resp[2:])))
    max_block_length = int.from_bytes(resp[2:], byteorder="big")
    return dict(zip(["response_sid", "max_block_length"], [response_sid, max_block_length]))


def concat_transfer_data_request(block_sequence_counter: int,
                                 data: bytes,
                                 ) -> bytes:
    """
    Concat transfer data request.
    :param block_sequence_counter: The block counter for this transfer.
    :param data: The data to be transferred.
    :return: The request as bytes.
    """
    assert 0 < block_sequence_counter <= 255
    return struct.pack(">BB{0}s".format(len(data)), ServiceId.TransferData, block_sequence_counter, data)


def parse_transfer_data_response(resp: bytes) -> dict:
    """
    Parse transfer data response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = struct.unpack(">BB{0}s".format(len(resp) - 2), resp)
    return dict(zip(["response_sid", "block_sequence_counter", "data"], values))


def concat_request_transfer_exit_request(transfer_request_parameters: bytes = bytes()
                                         ) -> bytes:
    """
    Concat request transfer exit request.
    :param transfer_request_parameters: A never used manufacturer specific value.
    :return: The request as bytes.
    """
    return struct.pack(">B{0}s".format(len(transfer_request_parameters)), ServiceId.RequestTransferExit,
                       transfer_request_parameters)


def parse_request_transfer_exit_response(resp: bytes) -> dict:
    """
    Parse request transfer exit response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = struct.unpack(">B{0}s".format(len(resp) - 1), resp)
    return dict(zip(["response_sid", "transfer_request_parameters"], values))


def concat_routine_control_request(routine_control_type: RoutineControlType,
                                   routine_id: int,
                                   data: Optional[bytes] = None
                                   ):
    """
    Concat routine control request.
    :param routine_control_type: The control type, e.g. Start/Stop/Poll.
    :param routine_id: The Routine Id.
    :param data: The (optional) data that the routine consumes.
    :return: The request as bytes.
    """
    return struct.pack(">BBH{0}s".format(len(data)), ServiceId.RoutineControl, routine_control_type, routine_id, data)


def parse_routine_control_response(resp: bytes) -> dict:
    """
    Parse routine control response.
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack(">BBHB{0}s".format(len(resp) - 5), resp))
    values[1] = RoutineControlType(values[1])
    return dict(
        zip(["response_sid", "routine_control_type", "routine_id", "routine_info", "routine_status_record"], values))


SERVICE_TO_PARSER_MAPPING = {ServiceId.DiagnosticSessionControl: parse_diagnostic_session_control_response,
                             ServiceId.EcuReset: parse_ecu_reset_response,
                             ServiceId.ReadDataByIdentifier: parse_read_data_by_id_response,
                             ServiceId.SecurityAccess: parse_security_access_response,
                             ServiceId.CommunicationControl: parse_communication_control_response,
                             ServiceId.TesterPresent: parse_tester_present_response,
                             ServiceId.ControlDtcSettings: parse_control_dtc_setting_response,
                             ServiceId.WriteDataByIdentifier: parse_write_data_by_id_response,
                             ServiceId.RequestDownload: parse_request_download_or_upload_response,
                             ServiceId.RequestUpload: parse_request_download_or_upload_response,
                             ServiceId.TransferData: parse_transfer_data_response,
                             ServiceId.RequestTransferExit: parse_request_transfer_exit_response,
                             ServiceId.ClearDiagnosticInformation: parse_clear_diagnostic_information_response,
                             ServiceId.RoutineControl: parse_routine_control_response,
                             }


def parse_response(resp: bytes) -> dict:
    """
    A generic function to parse a service response.
    In case of negative response, it raises the appropriate protocol exceptions.
    Otherwise it calls a service specific parser and returns a dictionary with the contents.
    The UDS protocol was not designed properly, so the request is also needed to process the response.
    :param resp: The response bytes.
    :return: A dictionary with response specific values.
    """
    raise_for_exception(resp=resp)
    sid = ServiceId(resp[0] & 0xBF)
    parser_function = SERVICE_TO_PARSER_MAPPING.get(sid)
    ret = {"raw": resp}
    if parser_function is not None and callable(parser_function):
        ret.update(parser_function(resp))
    return ret


def raise_for_exception(resp: bytes) -> None:
    """
    In case of negative response, raise the appropriate protocol exceptions.
    :param resp: The response bytes.
    :return: Nothing.
    """

    if resp[0] == 0x7F:
        assert len(resp) >= 3
        assert resp[0] == 0x7F
        sid = ServiceId(resp[1])
        response_code = ResponseCode(resp[2])
        LOGGER.error("Service {0} Exception {1}".format(sid.name, response_code.name))
        raise RESPONSE_CODE_TO_EXCEPTION_MAPPING.get(response_code)


# Exceptions from client perspective

class UdsProtocolException(Exception):
    """
    The base exception for UDS
    """
    pass


class UdsTimeoutError(UdsProtocolException):
    """
    A (socket/message/protocol) timeout
    """
    pass


class NegativeResponse(UdsProtocolException):
    """
    The base negative response exception
    """
    pass


class GeneralReject(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ServiceNotSupported(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class SubfunctionNotSupported(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class IncorrectMessageLengthOrInvalidFormat(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ResponseTooLong(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class BusyRepeatRequest(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ConditionsNotCorrect(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequestSequenceError(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class NoResponseFromSubnetComponent(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class FaultPreventsExecutionOfRequestedAction(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequestOutOfRange(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class SecurityAccessDenied(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class InvalidKey(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ExceededNumberOfAttempts(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequiredTimeDelayNotExpired(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class UploadDownloadNotAccepted(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class TransferDataSuspended(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class GeneralProgrammingFailure(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class WrongBlockSequenceCounter(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequestCorrectlyReceivedButResponsePending(NegativeResponse):
    # This is actually not a Negative Response, see how we can handle this in program flow,
    # maybe base on Exception instead.
    """
    Protocol specific exception
    """
    pass


class SubFunctionNotSupportedInActiveSession(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ServiceNotSupportedInActiveSession(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


RESPONSE_CODE_TO_EXCEPTION_MAPPING = {
    ResponseCode.GeneralReject: GeneralReject,
    ResponseCode.ServiceNotSupported: ServiceNotSupported,
    ResponseCode.SubFunctionNotSupported: SubfunctionNotSupported,
    ResponseCode.IncorrectMessageLengthOrInvalidFormat: IncorrectMessageLengthOrInvalidFormat,
    ResponseCode.ResponseTooLong: ResponseTooLong,
    ResponseCode.BusyRepeatRequest: BusyRepeatRequest,
    ResponseCode.ConditionsNotCorrect: ConditionsNotCorrect,
    ResponseCode.RequestSequenceError: RequestSequenceError,
    ResponseCode.NoResponseFromSubnetComponent: NoResponseFromSubnetComponent,
    ResponseCode.FaultPreventsExecutionOfRequestedAction: FaultPreventsExecutionOfRequestedAction,
    ResponseCode.RequestOutOfRange: RequestOutOfRange,
    ResponseCode.SecurityAccessDenied: SecurityAccessDenied,
    ResponseCode.InvalidKey: InvalidKey,
    ResponseCode.ExceededNumberOfAttempts: ExceededNumberOfAttempts,
    ResponseCode.RequiredTimeDelayNotExpired: RequiredTimeDelayNotExpired,
    ResponseCode.UploadDownloadNotAccepted: UploadDownloadNotAccepted,
    ResponseCode.TransferDataSuspended: TransferDataSuspended,
    ResponseCode.GeneralProgrammingFailure: GeneralProgrammingFailure,
    ResponseCode.WrongBlockSequenceCounter: WrongBlockSequenceCounter,
    ResponseCode.RequestCorrectlyReceivedButResponsePending: RequestCorrectlyReceivedButResponsePending,
    ResponseCode.SubFunctionNotSupportedInActiveSession: SubFunctionNotSupportedInActiveSession,
    ResponseCode.ServiceNotSupportedInActiveSession: ServiceNotSupportedInActiveSession,
}
