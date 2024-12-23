# goback_n.py
import socket
import threading
import queue
import time
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class Frame:
    seq_num: int
    data: str
    is_ack: bool = False
    ack_num: Optional[int] = None
    
    def __str__(self):
        if self.is_ack:
            return f"ACK:{self.ack_num}"
        return f"SEQ:{self.seq_num},DATA:{self.data}"

class Sender:
    def __init__(self, host: str, port: int, peer_host: str, peer_port: int,
                 T1: float, T2: float, T3: float, T4: float, drop_prob: float):
        # Configuration
        self.WINDOW_SIZE = 7
        self.MOD = 8  # Modulo-8 sequence numbering
        
        # Network parameters
        self.T1 = T1  # Min packet generation interval
        self.T2 = T2  # Max packet generation interval
        self.T3 = T3  # Min transmission delay
        self.T4 = T4  # Max transmission delay
        self.drop_prob = drop_prob
        
        # Socket setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.peer_addr = (peer_host, peer_port)
        
        # Protocol state
        self.send_base = 0
        self.next_seq_num = 0
        
        # Queues and buffers
        self.outgoing_queue = queue.Queue()
        self.window_frames = {}  # seq_num -> (frame, first_send_time)
        
        # Statistics
        self.packets_sent = 0
        self.retransmissions = 0
        self.delivery_times = []
        
        # adding more tracking parameters
        """
        a.  observe and record the times that correspond to the time when a frame was first sent, and 
            the time when the frame was first received without error and in order at the other end, 
                => tracking using delivery_times
        b.  compute: 
            I.   the average delay in delivering packets to the other end, and => 
            II.  average number of times a frame was sent => tracking using number of retransmissions
        """

        # Control flag
        self.running = True
        
    def generate_packets(self, num_packets: int):
        """Generate packets at random intervals"""
        for i in range(num_packets):
            delay = random.uniform(self.T1, self.T2)
            time.sleep(delay)
            self.outgoing_queue.put(f"Packet-{i}")
            print(f"Generated packet {i}")

    def send_frame(self, frame: Frame):
        """Send a frame with simulated delay and drop probability"""
        if random.random() >= self.drop_prob:  # Not dropped
            delay = random.uniform(self.T3, self.T4)
            time.sleep(delay)
            self.socket.sendto(str(frame).encode(), self.peer_addr)
            print(f"Sent {frame}")
        else:
            print(f"Dropped {frame}")

    def sender_thread(self):
        """Handle sending frames using Go-Back-N protocol"""
        while self.running:
            # Send new frames if window space available
            while (self.next_seq_num < self.send_base + self.WINDOW_SIZE and
                   not self.outgoing_queue.empty()):
                data = self.outgoing_queue.get()
                frame = Frame(seq_num=self.next_seq_num % self.MOD, data=data)
                self.window_frames[self.next_seq_num] = (frame, time.time())
                self.send_frame(frame)
                self.next_seq_num += 1
                self.packets_sent += 1

            # Check for timeout and retransmit if necessary
            current_time = time.time()
            timeout = 2.0  # Adjust as needed
            
            for seq_num in range(self.send_base, self.next_seq_num):
                if seq_num in self.window_frames:
                    frame, send_time = self.window_frames[seq_num]
                    if current_time - send_time > timeout:
                        print(f"Timeout for frame {frame}")
                        # Retransmit all frames in window
                        for resend_seq in range(self.send_base, self.next_seq_num):
                            if resend_seq in self.window_frames:
                                resend_frame, _ = self.window_frames[resend_seq]
                                self.send_frame(resend_frame)
                                self.retransmissions += 1
                        break

            time.sleep(0.1)  # Prevent busy waiting

    def receiver_thread(self):
        """Handle receiving acknowledgments"""
        while self.running:
            try:
                data, _ = self.socket.recvfrom(1024)
                ack_str = data.decode()
                
                if ack_str.startswith("ACK:"):
                    ack_num = int(ack_str.split(":")[1])
                    print(f"Received ACK for {ack_num}")
                    
                    if self.send_base <= ack_num < self.next_seq_num:
                        delivery_time = time.time() - self.window_frames[ack_num][1]
                        self.delivery_times.append(delivery_time)
                        # Slide window
                        self.send_base = ack_num + 1
                        # Clean up window_frames
                        for seq in list(self.window_frames.keys()):
                            if seq < self.send_base:
                                del self.window_frames[seq]
            except Exception as e:
                print(f"Error in receiver thread: {e}")

    def start(self, num_packets: int):
        """Start all threads and run the protocol"""
        threads = [
            threading.Thread(target=self.generate_packets, args=(num_packets,)),
            threading.Thread(target=self.sender_thread),
            threading.Thread(target=self.receiver_thread)
        ]
        
        for thread in threads:
            thread.daemon = True
            thread.start()
            
        # Wait for all packets to be sent and acknowledged
        while (self.packets_sent < num_packets or 
               self.send_base < self.next_seq_num):
            time.sleep(0.1)
            
        self.running = False
        
        # Print statistics
        if self.delivery_times:
            avg_delay = sum(self.delivery_times) / len(self.delivery_times)
            avg_retransmissions = self.retransmissions / num_packets
            
            print(f"\n---------------Statistics---------------")
            # printing the parameters used in this simulation
            print("Parameters used in this simulation:")
            print(f"Window size: {self.WINDOW_SIZE}")
            print(f"Packet generation interval (T1): {self.T1} seconds")
            print(f"Packet generation interval (T2): {self.T2} seconds")
            print(f"Min transmission delay (T3): {self.T3} seconds")
            print(f"Max transmission delay (T4): {self.T4} seconds")
            print(f"Packet drop probability: {self.drop_prob}")
            print("-------------------------------------------")

            print(f"Total packets sent: {self.packets_sent}")
            print(f"Total retransmissions: {self.retransmissions}")
            print(f"Average delivery delay: {avg_delay:.3f} seconds")
            print(f"Average retransmissions per packet: {avg_retransmissions:.2f}")

class Receiver:
    def __init__(self, host: str, port: int, peer_host: str, peer_port: int,
                 T3: float, T4: float, drop_prob: float):
        # Configuration
        self.MOD = 8  # Modulo-8 sequence numbering
        
        # Network parameters
        self.T3 = T3  # Min transmission delay
        self.T4 = T4  # Max transmission delay
        self.drop_prob = drop_prob
        
        # Socket setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.peer_addr = (peer_host, peer_port)
        
        # Protocol state
        self.expected_seq_num = 0
        
        # Control flag
        self.running = True

    def send_ack(self, ack_num: int):
        """Send acknowledgment with simulated delay and drop probability"""
        if random.random() >= self.drop_prob:  # Not dropped
            delay = random.uniform(self.T3, self.T4)
            time.sleep(delay)
            ack_msg = f"ACK:{ack_num}"
            self.socket.sendto(ack_msg.encode(), self.peer_addr)
            print(f"Sent {ack_msg}")
        else:
            print(f"Dropped ACK {ack_num}")

    def receive_frames(self):
        """Main loop for receiving frames"""
        print("Receiver started, waiting for frames...")
        while self.running:
            try:
                data, _ = self.socket.recvfrom(1024)
                frame_str = data.decode()
                
                if frame_str.startswith("SEQ:"):
                    # Parse frame datac:\Users\adity\Downloads\go back n.pdf
                    seq_part, data_part = frame_str.split(",")
                    seq_num = int(seq_part.split(":")[1])
                    data = data_part.split(":")[1]
                    
                    print(f"Received frame {seq_num} with data: {data}")
                    
                    if seq_num == self.expected_seq_num % self.MOD:
                        print(f"Frame {seq_num} received in order")
                        self.send_ack(seq_num)
                        self.expected_seq_num += 1
                    else:
                        print(f"Frame {seq_num} out of order, expected {self.expected_seq_num % self.MOD}")
                        if self.expected_seq_num > 0:
                            self.send_ack(self.expected_seq_num - 1)
            except Exception as e:
                print(f"Error in receiver: {e}")

    def start(self):
        """Start the receiver"""
        self.receive_frames()