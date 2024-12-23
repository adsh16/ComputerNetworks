import socket
import threading
import time
import random
import queue

class DLEntity1:
    def __init__(self):
        self.T1, self.T2 = 0.5, 1.5
        self.T3, self.T4 = 0.1, 0.3
        self.P = 0.1
        self.WINDOW_SIZE = 7
        self.SEQ_MODULO = 8
        self.PACKET_COUNT = 10
        
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver_address = ('localhost', 8080)
        self.packet_queue = queue.Queue()
        self.start_time = time.time()
        self.sent_times = []
        self.received_times = []
        
    def packet_generator(self):
        for i in range(self.PACKET_COUNT):
            time.sleep(random.uniform(self.T1, self.T2))
            packet = f"DL1_Packet_{i}".encode()
            self.packet_queue.put(packet)
            self.sent_times.append(time.time() - self.start_time)
            
    def transmit(self):
        base = 0
        next_seq_num = 0
        sent_frames = {}
        acked_frames = 0
        
        while acked_frames < self.PACKET_COUNT:
            while next_seq_num < base + self.WINDOW_SIZE and next_seq_num < self.PACKET_COUNT:
                if not self.packet_queue.empty():
                    packet = self.packet_queue.get()
                    seq_num = next_seq_num % self.SEQ_MODULO
                    frame = (seq_num, packet)
                    
                    time.sleep(random.uniform(self.T3, self.T4))
                    
                    if random.random() > self.P:
                        self.sender_socket.sendto(str(frame).encode(), self.receiver_address)
                        sent_frames[seq_num] = time.time()
                        print(f"DL1: Sent frame {seq_num}")
                    else:
                        print(f"DL1: Frame {seq_num} dropped")
                    
                    next_seq_num += 1
            
            try:
                self.sender_socket.settimeout(1.0)
                ack, _ = self.sender_socket.recvfrom(1024)
                ack_num = int(ack.decode())
                print(f"DL1: Received ACK {ack_num}")
                
                if ack_num >= base % self.SEQ_MODULO:
                    base = ack_num + 1
                    acked_frames += 1
                    self.received_times.append(time.time() - self.start_time)
            except socket.timeout:
                print("DL1: Timeout, resending window")
                next_seq_num = base
                
    def start(self):
        generator_thread = threading.Thread(target=self.packet_generator)
        transmit_thread = threading.Thread(target=self.transmit)
        
        generator_thread.start()
        transmit_thread.start()
        
        generator_thread.join()
        transmit_thread.join()
