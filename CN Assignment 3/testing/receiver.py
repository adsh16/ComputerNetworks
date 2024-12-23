# receiver.py
from goback_n import Receiver

def main():
    # Create receiver entity
    receiver = Receiver(
        host="localhost", 
        port=5001,
        peer_host="localhost", 
        peer_port=5000,
        T3=0.05,  # Min transmission delay
        T4=0.15,  # Max transmission delay
        drop_prob=0.1  # 10% packet drop probability
    )
    
    print("Receiver starting...")
    try:
        receiver.start()
    except KeyboardInterrupt:
        print("\nReceiver stopped by user")
    except Exception as e:
        print(f"Receiver error: {e}")

if __name__ == "__main__":
    main()