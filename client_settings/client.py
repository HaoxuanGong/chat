import select
import sys
import threading
from client_settings.socket_context import SocketContext
from utils import *

stop_thread = False


def get_and_send(client):
    while not stop_thread:
        if not client.communicator_sent:
            send(client.socket, client.communicator)
            client.communicator_sent = True

        data = sys.stdin.readline().strip()
        if data:
            send(client.socket, data)


class ChatClient:
    """ A command line chat client using select """

    def __init__(self, name, socket_context, port=SocketContext.server_port(), host=SocketContext.server_host()):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.socket = socket_context.socket
        self.communicator_sent = False
        self.authenticated = False

        # Initial prompt
        self.prompt = f'[{name}@{socket.gethostname()}]> '

        # Connect to server at port
        try:
            self.socket.connect((host, port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True

            while not self.authenticated:
                task = input("Press R For Register / Press L For Log In: ")
                if task == "R":
                    self.register(self.name)
                elif task == "L":
                    password = input("Enter Your Password Here: ")
                    self.login(self.name, password)
                else:
                    print("Please Enter Either R or L")

            # Send my name...
            send(self.socket, 'NAME: ' + self.name)

            self.connected_clients()
            self.communicator = self.choose_communication()

            self.prompt = '[' + '@'.join((self.name, socket.gethostbyname(socket.gethostname()))) + ']> '

            threading.Thread(target=get_and_send, args=(self,)).start()

        except socket.error:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)

    def register(self, name):
        send(self.socket, 'REGISTER:' + name)
        response = receive(self.socket)
        if response.startswith('REGISTERED:'):
            password = response.split('REGISTERED:')[1]
            print(f"Registered successfully! Your password is {password}")
        else:
            print(response)

    def login(self, name, password):
        send(self.socket, f'LOGIN:{name},{password}')
        response = receive(self.socket)
        if response == 'LOGIN_SUCCESS':
            print("Logged in successfully!")
            self.authenticated = True
        else:
            print(response)

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        self.socket.close()

    def connected_clients(self):
        data = receive(self.socket)
        print(data)

    def choose_communication(self):
        try:
            client_number = input("Which Client Do You Want To Talk To? \nPress R To Refresh Or Type The Client "
                                  "Number Here: ")
            if client_number == "R":
                self.connected_clients()
                return self.choose_communication()

            return int(client_number)
        except ValueError:
            print("Please enter a valid client number!")
            return self.choose_communication()

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                readable, writeable, exceptional = select.select(
                    [self.socket], [], [])

                for sock in readable:
                    if sock == self.socket:
                        data = receive(self.socket)
                        if not data:
                            print('Client shutting down.')
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print(" Client interrupted. " "")
                self.cleanup()
                break
