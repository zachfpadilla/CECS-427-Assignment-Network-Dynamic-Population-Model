import networkx as nx

def add_attributes(G):
    custom_attributes = ["dead", "infected", "sheltered", "vaccinated"]
    for attr in custom_attributes:
        nx.set_node_attributes(G, False, attr)
