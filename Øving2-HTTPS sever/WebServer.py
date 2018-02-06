# Import socket module
import base64
from socket import *

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket

# Assign a port number
serverPort = 1994

# Bind the socket to server address and server port
serverSocket.bind(('',1994)) # '' finner ip.adressen automatisk

# Listen to at most 1 connection at a time (max. number of threads in the connection queue)
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')

    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()

    try:
		# Receives the request message from the client
        message = connectionSocket.recv(1024)
        outputdata=""

		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
        filepath = message.split()[1]
        # Read the file "f" and store the entire content of the requested file in a temporary buffer
        if b'png' in filepath:
            data_uri = base64.b64encode(open(filepath[1:], 'rb').read()).decode('utf-8').replace('\n', '')
            outputdata = '<img src="data:image/png;base64,{0}">'.format(data_uri)

        else:
		# Because the extracted path of the HTTP request includes
		# a character '\', we read the path from the second character
            f = open(filepath[1:])
            lines = f.readlines()
            for line in lines:
                outputdata += line

		# Send the HTTP response header line to the connection socket
		# Format: "HTTP/1.1 *code-for-successful-request*\r\n\r\n"
        connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")##

		# Send the content of the requested file to the connection socket
        response = outputdata + "\r\n"
        connectionSocket.send(response.encode()) #Python 3

		# Close the client connection socket
        connectionSocket.close()

    except (IOError, IndexError):
        # Send HTTP response message for file not found
        # Same format as above, but with code for "Not Found" (see outputdata variable)
        # FILL IN START
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")##
        # FILL IN END
        connectionSocket.send(b"<!DOCTYPE html><html><body><h1>404 NOT FOUND</h1></body></html>\r\n")

        # Close the client connection socket
        connectionSocket.close()


serverSocket.close()
