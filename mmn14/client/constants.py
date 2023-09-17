from enum import Enum

# Max size allowed of certain fields.
MAX_NAME_LEN = 0xFFFF  # Max name_len field size (2 Bytes).
MAX_PACKET_SIZE = 0xFFFFFFFF  # Max size field size (4 Bytes).
MAX_CLIENT_VER = 0xFF  # Max version field size (1 Byte).
SERVER_INFO = "server.info"
BACKUP_INFO = "backup.info"


class EStatus(Enum):  # Response Codes
    SUCCESS_RESTORE = 210  # File was found and restored. all fields are valid.
    SUCCESS_DIR = 211  # Files listing returned successfully. all fields are valid.
    SUCCESS_BACKUP_REMOVE = (
        212  # File was successfully backed up or deleted. size, payload are invalid.
    )
    ERROR_NOT_EXIST = 1001  # File doesn't exist. size, payload are invalid.
    ERROR_NO_FILES = 1002  # Client has no files. Only status & version are valid.
    ERROR_GENERIC = 1003  # Generic server error. Only status & version are valid.


class EOp(Enum):  # Request codes
    FILE_BACKUP = 100  # Save file backup. All fields should be valid.
    FILE_RESTORE = 200  # Restore a file. size, payload unused.
    FILE_DELETE = 201  # Delete a file. size, payload unused.
    FILE_DIR = 202  # List all client's files. name_len, filename, size, payload unused.
