import socket
import threading
import time
import random
import queue

class DLEntity2:
    def __init__(self):
        self.T3, self.T4 = 0.1, 0.3
        self.P = 0.1
        self.SEQ_MODULO = 8
        
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver_socket.bind(('localhost', 8080))
        self.expected_seq_num = 0
        self.received_packets = []
        
    def receive(self):
        while True:
            try:
                frame, sender_address = self.receiver_socket.recvfrom(1024)
                time.sleep(random.uniform(self.T3, self.T4))
                
                frame_data = eval(frame.decode())
                seq_num, packet = frame_data
                print(f"DL2: Received frame {seq_num}")
                
                if random.random() < self.P:
                    print(f"DL2: Frame {seq_num} dropped")
                    continue
                
                if seq_num == self.expected_seq_num:
                    print(f"DL2: Frame {seq_num} in order")
                    self.received_packets.append(packet)
                    ack = str(seq_num).encode()
                    self.receiver_socket.sendto(ack, sender_address)
                    self.expected_seq_num = (self.expected_seq_num + 1) % self.SEQ_MODULO
                else:
                    print(f"DL2: Expected {self.expected_seq_num}, got {seq_num}")
                    last_ack = str((self.expected_seq_num - 1) % self.SEQ_MODULO).encode()
                    self.receiver_socket.sendto(last_ack, sender_address)
                    
            except Exception as e:
                print(f"DL2: Error: {e}")
                break
    
    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        receive_thread.join()
