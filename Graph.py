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
        for pair_node in list_edge:
            node1,node2 = pair_node
            if node1 not in self.list_nodes or node2 not in self.list_nodes:
                raise NetworkException('Add node before add edge to Graph')
            self.edges.append((node1, node2))
            node2.num_parent += 1
            node2.add_parent(node1)

    def remove_node(self, node):
        for (n1,n2) in self.edges:
            if node == n1:
                # self.remove_edge((n1, n2))
                n2.remove_parent(n1)

            if node == n2:
                self.remove_edge((n1, n2))
        self.list_nodes.remove(node)
        self.num_nodes -= 1


    def remove_edge(self, edge):
        (n1, n2) = edge
        n2.remove_parent(n1)
        self.edges.remove(edge)



    def visualize(self,figsize = 'default',node_size = 3000):
        G = nx.DiGraph()
        G.add_edges_from([(i.id_name,j.id_name) for (i,j) in self.edges])
        pos = nx.spring_layout(G)
        # nx.draw(G,pos,with_labels=True,node_size=2000)

        if figsize != 'default':
            fig = plt.figure(1, figsize=figsize, dpi=60)

        nx.draw(G, pos, with_labels=True, node_size=node_size)

        plt.show()