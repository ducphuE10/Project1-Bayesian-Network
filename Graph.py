import networkx as nx
import matplotlib.pyplot as plt
from Node import *
from Exception import NetworkException
class Graph:
    def __init__(self):
        self.edges = []
        self.list_nodes = []
        self.num_nodes = 0

    def add_nodes(self, *nodes):
        self.list_nodes.extend(nodes)
        self.num_nodes += len(nodes)

    def add_edges(self, *list_edge):
        print(self.list_nodes)
        for pair_node in list_edge:
            node1,node2 = pair_node
            if node1 not in self.list_nodes or node2 not in self.list_nodes:
                raise NetworkException('Add node before add edge to Graph')
            self.edges.append((node1.id_name, node2.id_name))
            node2.num_parent += 1
            node2.add_parent(node1)

    def remove_node(self, *nodes):
        pass

    def remove_edges(self, node1: Node, node2: Node):
        pass

    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.edges)
        pos = nx.circular_layout(G)
        nx.draw(G,pos,with_labels=True,node_size=2000)
        plt.show()