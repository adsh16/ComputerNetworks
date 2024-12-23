# Computer Networks Assignments

This repository contains the implementations and reports for three assignments from the Computer Networks course. Each assignment explores fundamental networking concepts through hands-on coding and simulation exercises.

## Table of Contents
1. [UDP Ping and Heartbeat Systems](#udp-ping-and-heartbeat-systems)
2. [Go-Back-N Protocol Implementation](#go-back-n-protocol-implementation)
3. [Network Simulation using NS-3](#network-simulation-using-ns-3)

---

### UDP Ping and Heartbeat Systems

**Objective:**  
This assignment focuses on implementing two UDP-based applications: a Ping system and a Heartbeat system, demonstrating basic principles of network programming and handling unreliable connections.

**Key Features:**
- **Ping System:** Simulates packet loss (30%), measures Round Trip Time (RTT), and calculates packet loss statistics.
- **Heartbeat System:** Monitors server availability through periodic UDP messages, detecting downtime after consecutive missed responses.

**Highlights:**
- Simulated real-world network conditions with a 30% packet loss rate.
- Developed client-server programs for both Ping and Heartbeat systems.
- Provided detailed statistics, including RTT and packet loss rate.

---

### Go-Back-N Protocol Implementation

**Objective:**  
The goal was to implement the Go-Back-N ARQ protocol for reliable data transmission over an unreliable network.

**Key Features:**
- Reliable retransmission of lost or corrupted packets.
- Sliding window mechanism to optimize throughput.
- Robust error handling to ensure data integrity.

**Highlights:**
- Simulated sender and receiver interactions using the protocol.
- Demonstrated sequence number management and acknowledgment mechanisms.

---

### Network Simulation using NS-3

**Objective:**  
This assignment involved simulating a computer network using the NS-3 simulator to evaluate network performance under various traffic conditions.

**Key Features:**
- **Topology:** Modeled a network with 4 routers and 5 workstations.
- **Traffic Simulation:** Used Poisson-distributed traffic patterns.
- **Performance Metrics:** Analyzed delay, packet drops, and queue statistics.

**Highlights:**
- Simulated realistic network scenarios with RED (Random Early Detection) queue management.
- Measured the impact of traffic on end-to-end delays and packet loss.
- Gained insights into congestion management techniques.

---

## Conclusion

These assignments provided hands-on experience with critical networking concepts, including UDP-based communication, ARQ protocols, and network simulation tools like NS-3. Each project offered practical insights into network behavior and performance optimization.
