from enum import Enum
from dataclasses import dataclass

"""
?: boolean
h: short
l: long
i: int
f: float
q: long long int
"""


@dataclass
class ClientRequest:
    client_id: str
    version: int
    code: "RequestCodes"
    payload_size: int
    payload: bytes


class RequestCodes(Enum):
    REGISTER = 1025
    SENT_PUBLIC_KEY = 1026
    RECONNECTION = 1027
    SENT_FILE = 1028
    VALID_CRC = 1029
    INVALID_CRC = 1030
    INVALID_CRC_LAST = 1031


class ResponseCodes(Enum):
    REGISTER_SUCCESSFUL = 2100
    REGISTER_FAILED = 2101
    RECEIVED_PUBLIC_KEY = 2102
    FILE_ACCEPTED_VALID_CRC = 2103
    RECEIVED_MESSAGE = 2104
    RECONNECTION_SUCCESSFUL = 2105
    RECONNECTION_FAILED = 2106
    UNKNOWN_FAIL = 2107
