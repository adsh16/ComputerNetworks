import socket
import threading
import time
import random
import queue

class DataLinkEntity:
    def __init__(self, my_port, peer_port):
        # Configuration
        self.T1, self.T2 = 0.5, 1.5
        self.T3, self.T4 = 0.1, 0.3
        self.P = 0.1
        self.WINDOW_SIZE = 7
        self.SEQ_MODULO = 8
        self.PACKET_COUNT = 10
        
        # Socket setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', my_port))
        self.peer_address = ('localhost', peer_port)
        
        # Buffers and state
        self.outgoing_queue = queue.Queue()
        self.expected_seq_num = 0
        self.base = 0
        self.next_seq_num = 0   
        
        # Performance metrics
        self.start_time = time.time()
        self.sent_times = []
        self.received_times = []

        self.running = True
        self.successfully_transmitted = 0

    def packet_generator(self):
        for i in range(self.PACKET_COUNT):
            time.sleep(random.uniform(self.T1, self.T2))
            packet = f"Packet_{i}".encode()
            self.outgoing_queue.put(packet)
            self.sent_times.append(time.time() - self.start_time)

    def transmitter(self):
        sent_frames = {}
        while self.running and self.successfully_transmitted < self.PACKET_COUNT:
            while self.next_seq_num < self.base + self.WINDOW_SIZE and self.next_seq_num < self.PACKET_COUNT:
                if not self.outgoing_queue.empty():
                    packet = self.outgoing_queue.get()
                    seq_num = self.next_seq_num % self.SEQ_MODULO
                    frame = f"{seq_num}:{packet.decode()}".encode()
                    
                    time.sleep(random.uniform(self.T3, self.T4))
                    
                    if random.random() > self.P:
                        self.socket.sendto(frame, self.peer_address)
                        sent_frames[seq_num] = time.time()
                        print(f"Sent frame {seq_num}")
                    else:
                        print(f"Frame {seq_num} dropped during transmission")
                    
                    self.next_seq_num += 1

            try:
                self.socket.settimeout(1.0)
                ack, _ = self.socket.recvfrom(1024)
                ack_num = int(ack.decode())
                print(f"Received ACK {ack_num}")
                
                if ack_num >= self.base % self.SEQ_MODULO:
                    self.base = ack_num + 1
                    self.successfully_transmitted += 1
                    self.received_times.append(time.time() - self.start_time)
                    
                    if self.successfully_transmitted >= self.PACKET_COUNT:
                        self.running = False
                        break
                        
            except socket.timeout:
                print("Timeout occurred, resending window")
                self.next_seq_num = self.base

    def receiver(self):
        while self.running:
            try:
                self.socket.settimeout(1.0)
                frame, addr = self.socket.recvfrom(1024)
                time.sleep(random.uniform(self.T3, self.T4))
                
                if random.random() < self.P:
                    print("Frame dropped at receiver")
                    continue
                
                seq_num = int(frame.decode().split(':')[0])
                print(f"Received frame {seq_num}")
                
                if seq_num == self.expected_seq_num:
                    print(f"Frame {seq_num} in sequence")
                    ack = str(seq_num).encode()
                    self.socket.sendto(ack, addr)
                    self.expected_seq_num = (self.expected_seq_num + 1) % self.SEQ_MODULO
                else:
                    print(f"Out of sequence: expected {self.expected_seq_num}, got {seq_num}")
                    last_ack = str((self.expected_seq_num - 1) % self.SEQ_MODULO).encode()
                    self.socket.sendto(last_ack, addr)
                    
            except socket.timeout:
                if not self.running:
                    break
                continue
            except Exception as e:
                print(f"Receiver error: {e}")
                if not self.running:
                    break

    def start(self):
        threads = [
            threading.Thread(target=self.packet_generator),
            threading.Thread(target=self.transmitter),
            threading.Thread(target=self.receiver)
        ]
        
        for thread in threads:
            thread.daemon = True
            thread.start()
        
        # Wait for transmission completion
        while self.successfully_transmitted < self.PACKET_COUNT:
            time.sleep(0.1)
        
        self.running = False
        print(f"Transmission complete. {self.successfully_transmitted} packets sent successfully.")
