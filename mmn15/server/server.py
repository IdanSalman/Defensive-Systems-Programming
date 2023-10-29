import struct
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
from typing import Optional

from constants import ClientRequest, RequestCodes
from utils import generate_key, read_port_file, connect_to_db


class Server:
    def __init__(self) -> None:
        self.client_list = (
            set()
        )  # Differentiated by IP Address, Should be swapped for hash(given_username)

    def start(self) -> bool:
        server_port = read_port_file()
        # db_connection = connect_to_db()
        # db_data = db_connection.load_data()
        # self.client_list += db_data.items()

        start_server = websockets.serve(self.handleClient, "localhost", server_port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handleClient(self, websocket, path) -> Optional[str]:
        user_data = websocket.remote_address
        host_ip = user_data[
            0
        ]  # The client who sent the socket's ip (Will give 127.0.0.1 if it's the same ip as the server's)
        host_port = user_data[1]  # Port used to connect to the server
        try:
            async for message in websocket:
                # print(f"Received message from client {host_ip}: " + message)
                request = self.configureRequest(message)
                self.handleRequest(request)

        # Handle disconnecting clients
        except ConnectionClosed as e:
            print(f"{host_ip} just disconnected")

    def configureRequest(self, message: bytes) -> "ClientRequest":
        CLIENT_ID_SIZE = 16
        HEADER_SIZE = 7  # Header size without clientID. (version, code, payload size).

        clientID = struct.unpack(f"<{CLIENT_ID_SIZE}s", message[:CLIENT_ID_SIZE])[0]
        header_data = message[CLIENT_ID_SIZE : CLIENT_ID_SIZE + HEADER_SIZE]
        version = header_data[0]
        code = int(header_data[1:3].hex(), base=16)
        payload_size = int(header_data[3:].hex(), base=16)
        payload = message[CLIENT_ID_SIZE + HEADER_SIZE :]

        if payload_size != len(payload):
            raise Exception(
                "Payload's length isn't corresponding to the expected payload size"
            )

        return ClientRequest(clientID, version, code, payload_size, payload)

    def handleRequest(self, request: "ClientRequest") -> None:
        requestOptions = {
            RequestCodes.REGISTER.value: self.handleRegisterRequest,
            RequestCodes.RECONNECTION.value: self.handleReconnectRequest,
            RequestCodes.SENT_PUBLIC_KEY.value: self.handlePKRequest,
            RequestCodes.SENT_FILE.value: self.handleFileRequest,
            RequestCodes.INVALID_CRC.value: self.handleInvalidCrcRequest,
            RequestCodes.VALID_CRC.value: self.handleValidCrcRequest,
        }
        requestOptions[request.code](request)  # Runs the appropriate handle function

    def handleRegisterRequest(self, request: "ClientRequest"):
        client_name = request.payload
        # A register request's payload should only include name (255 bytes)
        if len(client_name) != 255:
            raise Exception("Invalid payload length for a Register Request (Code 1025)")

        hashed_client_name = hash(client_name)
        if hashed_client_name in self.client_list:
            print("Client already registered")
            return -1
        else:
            self.client_list.add(hashed_client_name)

    def handleReconnectRequest(self, request: "ClientRequest"):
        raise NotImplementedError()

    def handlePKRequest(self, request: "ClientRequest"):
        raise NotImplementedError()

    def handleFileRequest(self, request: "ClientRequest"):
        raise NotImplementedError()

    def handleInvalidCrcRequest(self, request: "ClientRequest"):
        raise NotImplementedError()

    def handleValidCrcRequest(self, request: "ClientRequest"):
        raise NotImplementedError()


if __name__ == "__main__":
    server_instance = Server()
    server_instance.start()
