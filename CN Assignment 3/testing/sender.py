# sender.py
from goback_n import Sender

def main():
    # Create sender entity
    sender = Sender(
        host="localhost", 
        port=5000,
        peer_host="localhost", 
        peer_port=5001,
        T1=0.1,  # Min packet generation interval
        T2=0.3,  # Max packet generation interval
        T3=0.5,  # Min transmission delay
        T4=0.15,  # Max transmission delay
        drop_prob=0.01  # 1% packet drop probability
    )
    
    print("Sender starting...")
    try:
        sender.start(num_packets=30)  # can test with 100 packets for testing
    except KeyboardInterrupt:
        print("\nSender stopped by user")
    except Exception as e:
        print(f"Sender error: {e}")

if __name__ == "__main__":
    main()