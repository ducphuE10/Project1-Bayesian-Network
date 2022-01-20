import pandas as pd
from Node import *
from Graph import Graph
from Network import Network

from networkx.algorithms.cycles import simple_cycles

if __name__ == '__main__':

    node1 = Boolean_Node('node1')
    node2 = Boolean_Node('node2')
    node3 = Boolean_Node('node3')
    node4 = OR_Node('node4')

    G = Graph()
    G.add_nodes(node1,node2,node3)
    G.add_edges((node1, node3),(node2,node3))



    G.remove_node(node1)

    G.visualize()

    net = Network(G)
    # net.help_generate_NPT(G.list_nodes,'data/')
    # net.set_NPT_from_csv(node1, 'data/ex1/node1.csv')
    # net.set_NPT_from_csv(node2, 'data/ex1/node2.csv')
    # net.set_NPT_from_csv(node3, 'data/ex1/node3.csv')


    # net.full_marginal({node1:True,node2:True, node3:True})




