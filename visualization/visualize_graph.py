import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(G, round_num):
    # Set colors based on node state
    node_colors = []
    for n in G.nodes:
        if G.nodes[n].get("dead", False):
            node_colors.append("black")
        elif G.nodes[n].get("infected", False):
            node_colors.append("red")
        elif G.nodes[n].get("vaccinated", False):
            node_colors.append("green")
        elif G.nodes[n].get("sheltered", False):
            node_colors.append("blue")
        else:
            node_colors.append("lightgray")

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)  # consistent layout
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10)
    plt.title(f"Round {round_num}")
    plt.show()
