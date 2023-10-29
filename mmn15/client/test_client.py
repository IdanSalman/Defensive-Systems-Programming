import asyncio
import websockets


def dec_to_bytes(number: int, byte_amount: int) -> bytes:
    return hex_to_bytes(hex(number), byte_amount)


def hex_to_bytes(hex_string: str, byte_amount: int) -> bytes:
    hex_digits = byte_amount * 2
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]

    temp_len = hex_digits - len(hex_string)
    if temp_len < 0:
        raise Exception("Given hex string requires more bytes than the given amount")
    else:
        return bytes.fromhex(("0" * temp_len) + hex_string)


# The main function that will handle connection and communication
# with the server
async def listen():
    with open(
        "C:\\Users\\froga\\OneDrive\\Desktop\\Code_Scripts\\Defensive-Systems-Programming\\mmn15\\client\\transfer.info",
        "r",
    ) as f:
        server_url = f.readline().strip("\n")
    client_id = dec_to_bytes(123, 16)  # 16 bytes
    version = dec_to_bytes(1, 1)  # 1 byte
    code = dec_to_bytes(1025, 2)  # 2 bytes
    payload_size = dec_to_bytes(255, 4)  # 4 bytes
    payload = dec_to_bytes(15, 255)  # 1 byte
    url = f"ws://{server_url}"
    # Connect to the server
    async with websockets.connect(url) as ws:
        # Send a greeting message
        await ws.send(client_id + version + code + payload_size + payload)
        # Stay alive forever, listening to incoming msgs
        while True:
            msg = await ws.recv()
            print(msg)


if __name__ == "__main__":
    # Start the connection
    asyncio.get_event_loop().run_until_complete(listen())
