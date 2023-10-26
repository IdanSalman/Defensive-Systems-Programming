import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
from uuid import uuid4

from constants import ClientRequest
from utils import generate_key, read_port_file, connect_to_db

connected = set()


async def handleClient_alpha(websocket, path):
    print("A client just connected")
    user_data = websocket.remote_address
    host_ip = user_data[
        0
    ]  # The client who sent the socket's ip (Will give 127.0.0.1 if it's the same ip as the server's)
    host_port = user_data[1]  # Port used to connect to the server

    # Store a copy of the connected client
    connected.add(websocket)
    # Handle incoming messages
    try:
        async for message in websocket:
            print(f"Received message from client {host_ip}: " + message)
            # Send a response to all connected clients except sender
            for conn in connected:
                if conn != websocket:
                    await conn.send("Someone said: " + message)
    # Handle disconnecting clients
    except ConnectionClosed as e:
        print(f"{host_ip} just disconnected")
    finally:
        connected.remove(websocket)


class Server:
    def __init__(self) -> None:
        self.client_list = set()

    def start(self) -> bool:
        server_port = read_port_file()
        # db_connection = connect_to_db()
        # db_data = db_connection.load_data()
        # self.client_list += db_data.items()

        start_server = websockets.serve(
            self.handleClient_beta, "localhost", server_port
        )
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handleClient_beta(self, websocket, path):
        user_data = websocket.remote_address
        host_ip = user_data[
            0
        ]  # The client who sent the socket's ip (Will give 127.0.0.1 if it's the same ip as the server's)
        host_port = user_data[1]  # Port used to connect to the server
        if host_ip in self.client_list:
            return "Client already exists"
        else:
            client_id = uuid4()
            try:
                async for message in websocket:
                    print(f"Received message from client {host_ip}: " + message)
                    request = self.identify_request(message)
                    self.handleRequest(request)

            # Handle disconnecting clients
            except ConnectionClosed as e:
                print(f"{host_ip} just disconnected")

    def identify_request(self, message: str) -> str:
        pass

    def handleRequest(self, request: "ClientRequest") -> None:
        pass


if __name__ == "__main__":
    server_instance = Server()
    server_instance.start()
