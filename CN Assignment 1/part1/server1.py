import random  # Import random library
from socket import *  # Import socket library

serverSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket for the server
serverSocket.bind(('127.0.0.1', 12000))  # Set IP Address and Port Number of Socket
print("Started UDP Server IP Address: 127.0.0.1 and Port: 12000")  # Print string on screen
while True:  # Run program forever
    rand = random.randint(1, 10)  # Probability 100%
    message, address = serverSocket.recvfrom(1024)
    message = message.upper()  # Convert client message to uppercase letter
    if rand < 4:  # < 30% without reply message
        continue
    serverSocket.sendto(message, address)  # Send the uppercase message back to the client
