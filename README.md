# Python Chat Program

This program facilitates secure one-to-one chat 
communication between a server and clients 
using the power of Python. It leverages Python's 
socket programming capabilities and `select` module 
to achieve non-blocking IO operations. 
The communication is encrypted using `SSL/TLS` for 
added security

## How To Run

- Open Command Prompt and Navigate to the Root Directory
- Start the Server by:

    ``python server_application.py``

- Start the Client by:

    ``python client_application.py``

## Address and Port Configuration

- Open the configs folder under the root directory
- Locate the config.ini configuration file
- `host address`, `port`, and `backlog` are freely to be 
customized
- If the default port number 12719 is taken up, feel free to 
change the port number in the configuration file
