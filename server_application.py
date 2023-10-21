from server_settings.server import *
from server_settings.encryption_context import *
from server_settings.socket_context import *

if __name__ == '__main__':
    socket = SocketContext(encryption_context=EncryptionContext())
    server = Server(socket)
    server.run()
