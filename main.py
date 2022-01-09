import pandas as pd
from Node import *
from Graph import Graph
from Network import Network


if __name__ == '__main__':

    node1 = Boolean_Node('node1')
    node2 = Boolean_Node('node2')
    node3 = Boolean_Node('node3')

    G = Graph()
    G.add_nodes(node1,node2,node3)
    G.add_edges((node1, node3),(node2,node3))

    G.visualize()

    net = Network(G)
    net.help_generate_NPT([node1,node2,node3],'data/')
    # net.set_NPT_from_csv(node1, 'data/node1.csv')
    # net.set_NPT_from_csv(node2, 'data/node2.csv')
    # net.set_NPT_from_csv(node3, 'data/node3.csv')

    # net.full_marginal({node1:True,node2:True, node3:True})

