import networkx as nx
import matplotlib.pyplot as plt
from Node import *

class Graph:
    def __init__(self):
        self.graph = []
        self.list_nodes = []
        self.num_nodes = 0
    def add_nodes(self, *nodes):
        self.list_nodes.extend(nodes)
        self.num_nodes += len(nodes)
    def remove_node(self, *nodes):
        pass

    def add_edges(self, *list_edge):
        for pair_node in list_edge:
            node1,node2 = pair_node
            self.graph.append((node1.id_name, node2.id_name))
            node2.num_parent += 1
            node2.add_parent(node1)

    def remove_edges(self, node1: Node, node2: Node):
        pass

    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.graph)
        pos = nx.circular_layout(G)
        nx.draw(G,pos,with_labels=True,node_size=2000)
        plt.show()