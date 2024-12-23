"""
Probability of hear 3 consecutive misseed responses is 0.3^3 = 0.027 = 2.7%
"""


import socket
import time  # Import time library

consecutive_misses = 0  # Track consecutive missing responses
max_misses = 3  # Maximum allowed consecutive misses

while True:
    start_key_press = input("\nPress any key to start...")

    print("-------------------------")
    print("Starting Heartbeat")
    print("-------------------------\n")

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket for the client
    server_address = ('127.0.0.1', 12000)  # Set IP Address and Port Number of Socket
    mysocket.settimeout(1)  # Sets a timeout value 1 seconds
    rtt = []  # Create an empty list to store round trip time
    try:  # Infinite loop to continuously send messages to the server
        for i in range(1000):  # Adjust the range as needed
            start = time.time()  # Start time send message to server
            message = f"{i} {start}"
            try:
                sent = mysocket.sendto(message.encode("utf-8"), server_address)
                print("Sent " + message)
                data, server = mysocket.recvfrom(4096)  # Maximum data received 4096 bytes i.e buffer size
                print("Received " + str(data))
                end = time.time()
                elapsed = end - start
                print("Time: " + str(elapsed * 1000) + " Milliseconds\n")
                rtt.append(elapsed)
                consecutive_misses = 0  # Reset consecutive misses on successful response
            except socket.timeout:
                print("#" + str(i) + " Requested Timed out\n")
                consecutive_misses += 1
                if consecutive_misses >= max_misses:
                    print("Server is assumed to be down after 3 consecutive misses.")
                    break
    finally:
        print("Finish heartbeat, closing socket")
        print("-------------------------")
        print("Statistics")
        if rtt:
            print("Average RTT: " + str(sum(rtt) / len(rtt) * 1000) + " Milliseconds")
            print("Max RTT: " + str(max(rtt) * 1000) + " Milliseconds")
            print("Min RTT: " + str(min(rtt) * 1000) + " Milliseconds")
        print("Packet Loss: " + str((1000 - len(rtt)) * 100 / 1000) + "%")
        print("-------------------------")
        mysocket.close()