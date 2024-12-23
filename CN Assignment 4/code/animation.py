import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation

# Define the network topology
G = nx.Graph()  # Changed to an undirected graph
positions = {
    "A": (0, 0),
    "B": (1, 0),
    "C": (2, 0),
    "D": (3, 0),
    "E": (4, 0),
    "R1": (0.5, 1),
    "R2": (1.5, 1),
    "R3": (2.5, 1),
    "R4": (3.5, 1)
}
edges = [
    ("A", "R1"), ("B", "R1"),
    ("R1", "R2"), ("R2", "R3"),
    ("R3", "R4"), ("R4", "E"),
    ("R2", "C"), ("R3", "D")
]
G.add_edges_from(edges)

# Packet paths
paths = {
    "A": ["R1", "R2", "R3", "R4", "E"],
    "B": ["R1", "R2", "R3", "R4", "E"],
    "C": ["R2", "R3", "R4", "E"],
    "D": ["R3", "R4", "E"]
}

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', ax=ax)
plt.title("Packet Transfer Animation")

# Initialize packet positions
packets = [{"current": "A", "path": paths["A"], "color": "red"}]
for src in ["B", "C", "D"]:
    packets.append({"current": src, "path": paths[src], "color": "orange"})

# Function to update packet positions
def update(frame):
    ax.clear()
    nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', ax=ax)
    for packet in packets:
        if frame < len(packet["path"]):
            packet["current"] = packet["path"][frame]
        nx.draw_networkx_nodes(
            G, pos=positions, nodelist=[packet["current"]],
            node_color=packet["color"], node_size=300, ax=ax
        )
    
    ax.axis("off")

# Create the animation
frames = max(len(path) for path in paths.values())
ani = FuncAnimation(fig, update, frames=frames, repeat=False, interval=1000)

# Show the animation
plt.show()
