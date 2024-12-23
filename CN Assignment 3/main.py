from data_link_entity import DataLinkEntity
import threading

if __name__ == "__main__":
    # Create two entities with different ports
    entity1 = DataLinkEntity(my_port=8080, peer_port=8081)
    entity2 = DataLinkEntity(my_port=8081, peer_port=8080)
    
    # Start both entities
    entity1_thread = threading.Thread(target=entity1.start)
    entity2_thread = threading.Thread(target=entity2.start)
    
    entity1_thread.start()
    entity2_thread.start()
    
    entity1_thread.join()
    entity2_thread.join()
