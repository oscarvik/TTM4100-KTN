# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

import time
from socket import *

# Get the server hostname and port as command line arguments                    
host = "127.0.0.1"
port = 12000
 
# Create UDP client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)  # Note the second parameter is NOT SOCK_STREAM but the corresponding to UDP

clientSocket.settimeout(1.0)  # Set socket timeout as 1 second

ptime = 0  # Sequence number of the ping message

while ptime < 10:  # Ping for 10 times
    ptime += 1
    data = "PING #"+str(ptime)+": "+str(time.asctime())+"\r"  # Format the message to be sent as in the Lab description
    
    try:
        sentTime = time.time()  # Record the "sent time"
        clientSocket.sendto(data.encode(), (host, port))  # Send the UDP packet with the ping message
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)  # Receive the server response
        recTime = time.time()  # Record the "received time"

        print("Modified message: "+modifiedMessage.decode('ascii'))  # Display the server response as an output

        RoundTripTime = ('% 12.6f' % (recTime-sentTime))  # Round trip time is the difference between sent and received time
        print("Round Trip Time:"+str(RoundTripTime))

    except timeout:  # Server does not response
        # Assume the packet is lost
        print("Request timed out.")
        continue

clientSocket.close()# Close the client socket
