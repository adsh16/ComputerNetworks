import threading
import time

class PerformanceMonitor:
    def __init__(self):
        self.delays = []
        self.retransmissions = 0
        self.total_packets = 0
        self.lock = threading.Lock()
        
    def record_delay(self, delay):
        with self.lock:
            self.delays.append(delay)
    
    def record_retransmission(self):
        with self.lock:
            self.retransmissions += 1
    
    def get_statistics(self):
        with self.lock:
            avg_delay = sum(self.delays) / len(self.delays) if self.delays else 0
            retransmission_rate = self.retransmissions / self.total_packets if self.total_packets else 0
            
            return {
                "average_delay": avg_delay,
                "retransmission_rate": retransmission_rate,
                "total_packets": self.total_packets,
                "total_retransmissions": self.retransmissions
            }
