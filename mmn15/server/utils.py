import os

from pathlib import Path
from Crypto.Cipher import AES


def read_port_file() -> str:
    file_directory = os.path.dirname(Path(__file__))
    file_path = file_directory + "/port.info"
    port = "1357"
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            port = str(f.read())
    else:
        print(
            f"WARNING: Port file not found in the following directory: {file_directory}"
        )
    return port


def generate_key(rsa_public_key: bytes):
    data = b"secret data"  # Can be as long as you want to <3

    encrypt_cipher = AES.new(rsa_public_key, AES.MODE_EAX)
    ciphertext, tag = encrypt_cipher.encrypt_and_digest(data)
    nonce = encrypt_cipher.nonce

    # Needs to return the nonce, tag (In order for the message decryption) and ciphertext (Encrypted data)

    decrypt_cipher = AES.new(rsa_public_key, AES.MODE_EAX, nonce)
    decrypted_data = decrypt_cipher.decrypt_and_verify(ciphertext, tag)
    print(decrypted_data)
    return ciphertext, encrypt_cipher


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


def connect_to_db():
    pass


if __name__ == "__main__":
    generate_key(b"abababababababab")
    read_port_file()
