import os
import random
import socket
import struct

from typing import List, Tuple

from mmn14.client.constants import (
    EStatus,
    EOp,
    MAX_NAME_LEN,
    MAX_CLIENT_VER,
    MAX_PACKET_SIZE,
    SERVER_INFO,
    BACKUP_INFO,
)


class ClientConnection:
    def __init__(self, userId: int, serverIp: str, serverPort: int) -> None:
        self.userId = userId  # User ID
        self.serverIp = serverIp
        self.serverPort = serverPort

    def initializeSocket(self) -> socket.socket:
        """
        Initialize a TCP/IP Socket with parsed server parameters.
        Calling function is responsible for closing the socket.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.serverIp, self.serverPort))
            return s
        except Exception as e:
            stopClient(f"initializeSocket Exception: {e}!")

    def requestFilesList(self) -> None:
        """Prepare and send a request for file list from server"""
        try:
            request = CRequest.getRequest(self.userId, EOp.FILE_DIR)
            s = self.initializeSocket()
            socketSend(s, request.pack())
            response = CResponse(s.recv(MAX_PACKET_SIZE))
            if response.validate(EStatus.SUCCESS_DIR):
                bytesRead = len(response.payload.payload)
                buffer = response.payload.payload
                while bytesRead < response.payload.size:
                    buffer = buffer + s.recv(MAX_PACKET_SIZE)
                s.close()
                files = [
                    file.strip() for file in buffer.decode("utf-8").split("\n")
                ]  # \n seperates filenames..
                files.remove("")  # remove empty entries
                if files:
                    print(f"Received file list for status code {response.status}:")
                    for file in files:
                        print(f"\t{file}")
                else:
                    print(
                        f"Invalid response: status code {response.status} but file list is empty!"
                    )
        except Exception as e:
            print(f"requestFilesList Exception: {e}!")

    def requestFileBackup(self, fileName: str) -> None:
        """Request to backup a file to server. Large files supported."""
        try:
            request = CRequest.getRequest(self.userId, EOp.FILE_BACKUP, fileName)
            request.payload.size = os.path.getsize(fileName)
            file = open(fileName, "rb")
            request.payload.payload = file.read(
                MAX_PACKET_SIZE - request.sizeWithoutPayload()
            )
            s = self.initializeSocket()
            socketSend(s, request.pack())
            payload = file.read(MAX_PACKET_SIZE)
            while payload:
                socketSend(s, payload)
                payload = file.read(MAX_PACKET_SIZE)
            file.close()
            response = CResponse(s.recv(MAX_PACKET_SIZE))
            s.close()
            if response.validate(EStatus.SUCCESS_BACKUP_REMOVE):
                print(
                    f"File '{fileName}' successfully backed-up. status code {response.status}."
                )
        except Exception as e:
            print(f"backupFile Exception: {e}!")

    def requestFileRestore(self, fileName: str, restoreTo="") -> None:
        """request to restore a file from server"""
        try:
            request = CRequest.getRequest(self.userId, EOp.FILE_RESTORE, fileName)
            s = self.initializeSocket()
            socketSend(s, request.pack())
            response = CResponse(s.recv(MAX_PACKET_SIZE))
            if response.validate(EStatus.SUCCESS_RESTORE):
                if restoreTo is None:
                    restoreTo = response.filename
                if response.filename is None:
                    print(
                        f"Restore Error. Invalid filename. yet status code {response.status}."
                    )
                else:
                    file = open(restoreTo, "wb")
                    bytesRead = len(response.payload.payload)
                    file.write(response.payload.payload)
                    while bytesRead < response.payload.size:
                        data = s.recv(MAX_PACKET_SIZE)
                        dataLen = len(data)
                        if dataLen + bytesRead > response.payload.size:
                            dataLen = response.payload.size - bytesRead
                        file.write(data[:dataLen])
                        bytesRead += dataLen
                    file.close()
                    print(
                        f"File '{response.filename}' successfully restored within {restoreTo}. status code {response.status}."
                    )
                s.close()  # close socket at the end
        except Exception as e:
            print(f"requestFileRestore error! Exception: {e}")

    def requestFileRemoval(self, fileName: str) -> None:
        """request to remove a file from server"""
        try:
            request = CRequest.getRequest(self.userId, EOp.FILE_DELETE, fileName)
            s = self.initializeSocket()
            socketSend(s, request.pack())
            response = CResponse(s.recv(MAX_PACKET_SIZE))
            s.close()
            if response.validate(EStatus.SUCCESS_BACKUP_REMOVE):
                print(
                    f"File '{fileName}' successfully removed. status code {response.status}."
                )
        except Exception as e:
            print(f"requestFileRemoval error! Exception: {e}")


def stopClient(errString: str) -> None:
    print("\nFatal Error!", errString, "Script execution will stop.", sep="\n")
    exit(1)


def generateUniqueID() -> int:
    max_4byte = 0xFFFFFFFF  # Biggest 4 Bytes hex number.
    min_4byte = 0x00000001  # Smallest unsigned 4 Bytes hex number.
    return random.randint(min_4byte, max_4byte)


def socketSend(s: socket.socket, buffer: bytes) -> None:
    """Making sure that the socket being sent is sized MAX_PACKET_SIZE"""
    bytesSize = len(buffer)
    if bytesSize < MAX_PACKET_SIZE:
        buffer += bytearray(MAX_PACKET_SIZE - bytesSize)
    elif bytesSize > MAX_PACKET_SIZE:
        buffer = buffer[:MAX_PACKET_SIZE]
    s.send(buffer)


class CPayload:
    def __init__(self):
        self.size = 0  # payload size
        self.payload = b""


class CRequest:
    def __init__(self, userId: int):
        self.userId = userId  # User ID
        self.version = 1  # Client Version
        self.opId = 0  # Request Code
        self.nameLen = 0  # filename length
        self.fileName = b""  # filename
        self.payload = CPayload()

    def sizeWithoutPayload(self) -> int:
        return (
            12 + self.nameLen
        )  # userId(4), version(1), op(1) , nameLen(2), payload size(4), filename(..)

    def pack(self) -> bytes:
        """Little Endian pack the Request"""
        leftover = MAX_PACKET_SIZE - self.sizeWithoutPayload()
        if self.payload.size < leftover:
            leftover = self.payload.size
        return struct.pack(
            f"<IBBH{self.nameLen}sL{leftover}s",
            self.userId,
            self.version,
            self.opId,
            self.nameLen,
            self.fileName,
            self.payload.size,
            self.payload.payload[:leftover],
        )

    @staticmethod
    def getRequest(userId: int, opId: "EOp", filename: str = "") -> "CRequest":
        """Initialize a request with OP and filename"""
        request = CRequest(userId)
        request.opId = opId.value
        request.fileName = bytes(filename, "utf-8")
        request.nameLen = len(request.fileName)  # shouldn't exceed max filename length.
        if request.nameLen > MAX_NAME_LEN:
            stopClient(
                f"Filename exceeding length {MAX_NAME_LEN}! Filename: {filename}"
            )
        return request


class CResponse:
    def __init__(self, data: bytes):
        self.version = 0
        self.status = 0
        self.nameLen = 0
        self.filename = None  # filename
        self.payload = CPayload()

        try:  # [0] for unpacking tuples when required.
            self.version, self.status, self.nameLen = struct.unpack("<BHH", data[:5])
            offset = 5
            self.filename = struct.unpack(
                f"<{self.nameLen}s", data[offset : offset + self.nameLen]
            )
            self.filename = self.filename[0].decode("utf-8")
            offset += self.nameLen
            self.payload.size = struct.unpack("<I", data[offset : offset + 4])
            self.payload.size = self.payload.size[0]
            offset += 4
            leftover = MAX_PACKET_SIZE - offset
            if self.payload.size < leftover:
                leftover = self.payload.size
            self.payload.payload = struct.unpack(
                f"<{leftover}s", data[offset : offset + leftover]
            )
            self.payload.payload = self.payload.payload[0]
        except Exception as e:
            print(e)

    def validate(self, expectedStatus: "EStatus") -> bool:
        """Validate response status"""
        valid = False
        if self.status is None:
            print("Invalid response received!")
        elif self.status == EStatus.ERROR_GENERIC.value:
            print(f"Generic Error received! status code {self.status}.")
        elif self.status == EStatus.ERROR_NO_FILES.value:
            print(f"Client has no files! status code {self.status}.")
        elif self.status == EStatus.ERROR_NOT_EXIST.value:
            tmp_str = (
                ""
                if (self.filename is None or self.filename == "")
                else f"'{self.filename}'"
            )
            print(
                f"Requested File {tmp_str} doesn't exists! status code {self.status}."
            )
        elif expectedStatus.value != self.status:
            print(f"Unexpected server response {self.status}!")
        else:
            valid = True
        return valid


def parseServerInfo(serverInfo: str) -> Tuple[str, int]:
    """Parses server.info for server info. return IP String, port. Stop script if error occurred."""
    try:
        info = open(os.getcwd() + "/mmn14/client/" + serverInfo, "r")
        values = info.readline().strip().split(":")
        info.close()
        return values[0], int(values[1])
    except Exception as e:
        stopClient(f"parseServerInfo Exception: {e}!")


def parseFileList(backupInfo: str) -> List[str]:
    """Parses backup.info for files list to backup. Stop script on failure"""
    try:
        info = open(os.getcwd() + "/mmn14/client/" + backupInfo, "r")
        filesList = [line.strip() for line in info]
        for filename in filesList:
            if len(filename) > MAX_NAME_LEN:
                info.close()
                stopClient(
                    f"filename exceeding length {MAX_NAME_LEN} was found in {backupInfo}!"
                )
        if len(filesList) < 2:
            info.close()
            stopClient(
                f"Unfulfilled requirement to define at least two filenames in {backupInfo}!"
            )
        info.close()
        return filesList
    except Exception as e:
        stopClient(f"parseFileList Exception: {e}!")


def main():
    userId = generateUniqueID()  # (1).
    serverIp, serverPort = parseServerInfo(SERVER_INFO)  # (2).
    backupList = parseFileList(BACKUP_INFO)  # (3).

    # Connect a client
    clientUser = ClientConnection(userId, serverIp, serverPort)

    clientUser.requestFilesList()  # Request file list from server (4).
    clientUser.requestFileBackup(backupList[0])  # Backup first file (5).
    clientUser.requestFileBackup(backupList[1])  # Backup second file (6).
    clientUser.requestFilesList()  # Request file list from server after backing-up two first files (7).
    clientUser.requestFileRestore(
        backupList[0], "tmp"
    )  # Restore first file from server to 'tmp' (8).
    clientUser.requestFileRemoval(backupList[0])  # Remove first file from server (9)
    clientUser.requestFileRestore(
        backupList[0]
    )  # Restore 1st file from server. Expected error because file is removed (10).

    exit(1)  # Logout(user_id) (11).


if __name__ == "__main__":
    main()
