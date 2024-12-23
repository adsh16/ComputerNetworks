# Go-Back-N Protocol Implementation Documentation

## Overview
This implementation simulates a Go-Back-N ARQ protocol between two data link entities using UDP sockets. The system consists of a Sender and Receiver that communicate using frames with modulo-8 sequence numbering.

## System Architecture

### Components
1. **Sender (DL_Entity_1)**
   - Window Size: 7 frames
   - Sequence Numbers: 0-7 (Modulo 8)
   - Key Components:
     - Packet Generator
     - Sender Thread
     - Receiver Thread (for ACKs)
     - Sliding Window Management

2. **Receiver (DL_Entity_2)**
   - Window Size: 1 frame
   - Handles in-order frame delivery
   - Sends cumulative acknowledgments

### Key Parameters
- T1, T2: Packet generation interval bounds (uniform distribution)
- T3, T4: Transmission delay bounds (uniform distribution)
- drop_prob: Probability of frame/ACK loss
- WINDOW_SIZE: 7 frames
- MOD: 8 (sequence number modulus)

## Protocol Operation

### Sender Operation
1. **Packet Generation**
   - Generates packets at random intervals between T1 and T2
   - Places packets in outgoing queue

2. **Frame Transmission**
   - Maintains sliding window of size 7
   - Sends frames within window limits
   - Handles timeouts and retransmissions
   - Tracks statistics (delays, retransmissions)

3. **ACK Processing**
   - Receives acknowledgments
   - Slides window based on cumulative ACKs
   - Updates delivery statistics

### Receiver Operation
1. **Frame Reception**
   - Checks sequence numbers
   - Accepts in-order frames
   - Buffers out-of-order frames

2. **ACK Transmission**
   - Sends cumulative acknowledgments
   - Simulates network delays and losses

## Statistics Collection
- Average packet delivery delay
- Number of retransmissions
- Total packets sent
- Average retransmissions per packet

## Network Simulation
- UDP sockets for communication
- Simulated propagation delays (T3-T4)
- Random packet drops (drop_prob)
- Timeout-based retransmission

## Usage
1. Start Receiver:
```bash
python receiver.py
```
2. Start Sender:
```bash
python sender.py
```
