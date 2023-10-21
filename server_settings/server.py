import select
import sys

from server_settings.socket_context import *
from utils import *
import signal

CTRL_C = signal.SIGINT


class Server:
    def __init__(self, socket_context):
        self.outputs = []
        self.client_num = 0
        self.client_list = {}
        self.socket = socket_context.socket

        signal.signal(CTRL_C, self.exit_handler)
        print(f"Server is starting at {SocketContext.server_host()} listening to port {SocketContext.server_port()}")

    def exit_handler(self, signum, frame):
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.socket.close()

    def run(self):
        inputs = [self.socket]
        self.outputs = []
        running = True
        while running:

            """ Break If Exception Occurs """
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error:
                break

            for sock in readable:
                sys.stdout.flush()
                if sock == self.socket:
                    # handle the server socket
                    client, address = self.socket.accept()
                    # Compute client name and send back
                    self.client_num += 1

                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    client_name = receive(client).split('NAME: ')[1]
                    self.client_list[client] = (address, client_name)
                    # Send joining information to other clients
                    table_msg = self.get_clients_table()
                    self.outputs.append(client)
                    for output in self.outputs:
                        send(output, table_msg)

                    inputs.append(client)




                else:
                    # handle all other sockets
                    try:
                        communicator = receive(sock)
                        print(f'Communicator {communicator}')
                        data = receive(sock)
                        if data:
                            # Send as new client's message...
                            msg = f'\n#[{self.get_client_name(sock)}]>> {data}'

                            for index, output in enumerate(self.outputs):
                                if output != sock and index == communicator - 1:
                                    send(output, msg)
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            self.client_num -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            # Sending client leaving information to others
                            msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'

                            for output in self.outputs:
                                send(output, msg)
                    except socket.error:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)

        self.socket.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.client_list[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def get_clients_table(self):
        """Return a string that represents the currently connected clients in a table format."""
        header = "\nConnected Clients:\n"
        table_line = "---------------------------------\n"
        table_header = "| Client Number | Client Name   |\n"
        table_content = ""

        for idx, (client_socket, (address, name)) in enumerate(self.client_list.items(), start=1):
            table_content += f"| {idx:<14} | {name:<13} |\n"

        print(header + table_line + table_header + table_line + table_content + table_line)

        return header + table_line + table_header + table_line + table_content + table_line
