

from client_settings.client import ChatClient
from client_settings.encryption_context import EncryptionContext
from client_settings.socket_context import SocketContext

if __name__ == "__main__":
    client_name = input("Please enter your name: ")
    socket = SocketContext(encryption_context=EncryptionContext())
    client = ChatClient(name=client_name, socket_context=socket)
    client.run()
