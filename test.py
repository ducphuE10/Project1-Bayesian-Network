from Node import *
from Graph import Graph
from Network import Network


if __name__ == '__main__':
    # success = Boolean_Node('success')
    handome = Boolean_Node('handsome')
    rich = Boolean_Node('rich')
    kind = Boolean_Node('kind')
    success = MtoN_Node('sucess',M = 2 )


    G = Graph()
    G.add_nodes(handome,rich,success,kind)
    G.add_edges((handome,success),(rich, success),(kind, success))

    net = Network(G)
    # net.help_generate_NPT([handome,rich,kind,success],path_to_forder='data/tangai')
    net.set_NPT_from_csv(handome,path = 'data/tangai/handsome.csv')
    net.set_NPT_from_csv(rich,path = 'data/tangai/rich.csv')
    net.set_NPT_from_csv(kind,path = 'data/tangai/kind.csv')
    net.set_NPT_func(success)

    net.set_evidence({success:True})