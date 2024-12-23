## What the times chosen
1. Gap b/w two succuessive packets is normally distributed b/w T1 = 0.5 and T2 = 1.5
2. The delay time(to simulate queing and propogation delay) taken for a packet to be sent is normally distributed b/w T3 = 0.5 and T4 = 1.5

## “Go-back n” works well when error are infrequent
- Since several frames need to be re-transmitted if/when error occurs

## How will we do this
1. We will have Two DL_entity_1 and DL_entity_2
2. each will have a main thread:
   1. generate_thread : Generates packets in intervals normally distributed b/w T1 and T2 and puts them in a queue
   2. Sender_thread : Sends the packets from the queue to the receiver. It will have a delay to simulate the delay in transmission(propogation and queing delay) that is normally distributed b/w T3 and T4.
   3. Receiver_thread : Receives the packets from the sender and checks the sequence number. If the sequence number is correct, it acknowledges the packet. If the sequence number is incorrect, it retransmits the packet.
3. Both Threads will generated packets and send it two each other.


## How will we do this
1. We will have Two DL_entity_1(sender) and DL_entity_2(receiver)
2. **sender data entity** will have a main thread which will pop these threads:
   1. generate_thread : Generates packets in intervals normally distributed b/w T1 and T2 and puts them in a queue
   2. Sender_thread : Sends the packets from the queue to the receiver. It will have a delay to simulate the delay in transmission(propogation and queing delay) that is normally distributed b/w T3 and T4.
3. **receiver data entity** will Receives the packets from the sender and checks the sequence number. And sends an acknowledgement

