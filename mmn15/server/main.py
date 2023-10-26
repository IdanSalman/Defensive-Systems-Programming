from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import random

from utils import read_port_file
from server import Server


def main():
    port = read_port_file()
    server = Server()
    print(port)


if __name__ == "__main__":
    main()
