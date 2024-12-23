import socket
import time  # Import time library
while True:
    start_key_press = input("\nPress any key to start...\n")

    print("-------------------------")
    print("Starting Ping")
    print("-------------------------\n")
    # Abhay ip : 192.168.40.238
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket for the client
    server_address = ('127.0.0.1', 12000)  # Set IP Address and Port Number of Socket
    mysocket.settimeout(1)  # Sets a timeout value 1 seconds
    rtt = []  # Create an empty list to store round trip time
    try:  # Infinite loop to continuously send messages to the server
        for i in range(10):
            start = time.time()  # Start time send message to server
            message = 'Ping ' + str(i + 1) + " " + time.ctime(start)
            try:
                sent = mysocket.sendto(message.encode("utf-8"), server_address)
                print("Sent " + message)
                data, server = mysocket.recvfrom(4096)  # Maximum data received 4096 bytes i.e buffer size
                print("Received " + str(data))
                end = time.time()
                elapsed = end - start
                print("Time: " + str(elapsed * 1000) + " Milliseconds\n")
                rtt.append(elapsed)
            except socket.timeout:
                print("#" + str(i) + " Requested Timed out\n")
    finally:
        print("Finish ping, closing socket")
        print("-------------------------")
        try:
            print("Statistics")
            print("Average RTT: " + str(sum(rtt) / len(rtt) * 1000) + " Milliseconds")
            print("Max RTT: " + str(max(rtt) * 1000) + " Milliseconds")
            print("Min RTT: " + str(min(rtt) * 1000) + " Milliseconds")
            print("Packet Loss: " + str((10 - len(rtt)) * 10) + "%")
            print("-------------------------")
            mysocket.close()
        except:
            print("Server Is Down: No packets received")
            mysocket.close()
            continue