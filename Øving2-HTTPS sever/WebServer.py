import base64
from socket import *

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a server socket. (AF_INET is used for IPv4 protocols)(SOCK_STREAM is used for TCP)

serverPort = 1994  # Assign a port number
serverSocket.bind(('',1994)) # Bind the socket to server address and server port. '' finds current IP.address


serverSocket.listen(1)  # max. number of threads in the connection queue

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Set up a new connection from the client

    try:
        message = connectionSocket.recv(1024)  # Receives the request message from the client
        outputdata=""
		# Extract the path of the requested object from the message. The path is the second part of HTTP header, identified by [1]
        filepath = message.split()[1]

        # Read the file and store the entire content of the requested file in a temporary buffer
        if b'png' in filepath:
            data_uri = base64.b64encode(open(filepath[1:], 'rb').read()).decode('utf-8').replace('\n', '')
            outputdata = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        else:
		    # Because the extracted path of the HTTP request includes a character '\', we read the path from the second character
            f = open(filepath[1:])
            lines = f.readlines()
            for line in lines:
                outputdata += line

        connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")  # Send the HTTP response header line to the connection socket
        response = outputdata + "\r\n"
        connectionSocket.send(response.encode())  # Send the content of the requested file to the connection socket
        connectionSocket.close()  # Close the client connection socket

    except (IOError, IndexError):
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")  # Send HTTP response message for file not found
        connectionSocket.send(b"<!DOCTYPE html><html><body><h1>404 NOT FOUND</h1></body></html>\r\n")

        connectionSocket.close()  # Close the client connection socket


serverSocket.close()
