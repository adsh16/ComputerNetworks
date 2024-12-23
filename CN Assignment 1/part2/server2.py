import random  # Import random library
from socket import *  # Import socket library
import time  # Import time library

serverSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket for the server
serverSocket.bind(('127.0.0.1', 12000))  # Set IP Address and Port Number of Socket
print("Started UDP Server IP Address: 127.0.0.1 and Port: 12000")  # Print string on screen

while True:  # Run program forever
    rand = random.randint(1, 10)  # random number between 0 and 10
    message, address = serverSocket.recvfrom(1024)
    recv_time = time.time()  # Record the time the message was received
    if rand < 4:  # < 30% without reply message
        continue
    seq_num, timestamp = message.decode().split()
    timestamp = float(timestamp)
    time_diff = recv_time - timestamp
    response_message = f"{seq_num} {time_diff}"
    serverSocket.sendto(response_message.encode(), address)  # Send the time difference back to the client