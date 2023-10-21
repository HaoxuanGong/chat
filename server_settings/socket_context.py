import socket
import configparser

config = configparser.ConfigParser()

config.read('configs/config.ini')

# Extract values
SERVER_HOST = config['SERVER']['host']
SERVER_PORT = int(config['SERVER']['port'])
BACK_LOG = int(config['SERVER']['backlog'])


class SocketContext:

    def __init__(self, encryption_context):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((SERVER_HOST, SERVER_PORT))
        self._socket.listen(5)
        self._socket = encryption_context.wrap_socket(self.socket, server_side=True)

    @property
    def socket(self):
        return self._socket

    @socket.setter
    def socket(self, value):
        self._socket = value

    @staticmethod
    def server_host():
        return SERVER_HOST

    @staticmethod
    def server_port():
        return SERVER_PORT
