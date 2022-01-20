from Node import *
from Graph import Graph
import pandas as pd
import itertools
from prettytable import PrettyTable
import networkx as nx
from networkx import cycle_basis
from Exception import NetworkException
from tabulate import tabulate

class Network:
    def __init__(self, graph: Graph):
        self.graph = graph
        '''
        check DAG
        '''
        if self.checkCycle(graph.edges):
            raise NetworkException('the graph must be DAG !!!')

        self.num_nodes = graph.num_nodes
        self.list_nodes = self.graph.list_nodes


    def checkValidNPT(self, node):
        npt = node.NPT
        id_name_par = [i.id_name for i in node.parent]
        print(npt)
        if len(id_name_par) > 0:
            list_prob = npt.groupby(id_name_par)['cond_prob'].sum().tolist()
            if not (all(i==1 for i in list_prob)):
                raise NetworkException(f'invalid NPT for node: {node.id_name}')
        else:
            if npt['cond_prob'].sum() != 1:
                raise NetworkException(f'invalid NPT for node: {node.id_name}')

    def checkCycle(self, edges):
        di_graph = nx.DiGraph(edges)
        if len(list(nx.simple_cycles(di_graph))) > 0:
            return True
        return False

    def help_generate_NPT(self, list_nodes, path_to_folder=None):
        for node in list_nodes:
            if node not in self.list_nodes:
                raise NetworkException(f"Error: node {node.id_name} has not been added to the network")

        for node in list_nodes:
            if node.isFunc == True:
                print('function nodes do not need to create NPT manually: ',node.id_name)
                continue

            par = node.get_parent()
            columns = [i.id_name for i in par] + [node.id_name, "cond_prob"]
            states = [i.states for i in par] + [node.states] + [[0]]
            map_states = list(itertools.product(*states))
            df = pd.DataFrame(map_states, columns=columns)
            if path_to_folder is not None:
                zero_NPT_path = path_to_folder + '/' + node.id_name + '.csv'
                df.to_csv(zero_NPT_path)
                print(f"base NPT of {node.id_name}  is stored in:  {zero_NPT_path}")
            else:
                raise NetworkException('path to folder is None')

    def set_NPT_from_csv(self, node: Node, path):
        if node not in self.graph.list_nodes:
            raise NetworkException(f"Error: node {node.id_name} has not been added to the network")
        else:
            if node.isFunc == True:
                print('function nodes do not need to create NPT manually: ',node.id_name)
            else:
                node.set_NPT_from_csv(path)
                self.checkValidNPT(node)

    def set_NPT_func(self, func_node):
        if func_node not in self.graph.list_nodes:
            raise NetworkException(f"Error: node {func_node.id_name} has not been added to the network")
        else:
            func_node.set_NPT_func()


    def set_NPT(self, node: Node, NPT):
        '''
            Ví dụ node1 --> node2
            node1 có 3 state: low, medium, high
            node2 có 2 state: false, true
            NPT có dạng:
            pd.DataFrame([
            ['low','false', 1],
            ['low', 'true', 0],
            ['medium', 'false', 0.5],
            ['medium', 'true', 0.5],
            ['high', 'false', 0],
            ['high', 'true', 1]],columns = ['node1','node2', 'cond_prob'])
        '''
        if node not in self.graph.list_nodes:
            raise NetworkException(f"Error: node {node.id_name} has not been added to the network")
        else:
            columns = [i.id_name for i in node.get_parent()] + [node.id_name, "cond_prob"]
            node.NPT = NPT[columns]

    def set_evidence(self, evidence: dict):
        for node in evidence.keys():
            if node not in self.list_nodes:
                raise NetworkException(f"Error: node {node.id_name} has not been added to the network")

        print("******************************")
        print("set evidence ", {i.id_name: j for i, j in evidence.items()})
        for node in self.list_nodes:
            if node not in evidence.keys():
                table = PrettyTable(['state', 'prob'])
                for state in node.states:
                    table.add_row([state, self.conditional_probability({node: state}, evidence)])
                print("Table of node: ", node.id_name)
                print(table)
        print("******************************\n")

    def full_marginal(self, observation: dict):
        assert self.num_nodes == len(observation)
        result = 1
        for node in observation.keys():
            if node not in self.list_nodes:
                raise NetworkException(f"Error: node {node.id_name} has not been added to the network")

        for node in self.graph.list_nodes:
            par = node.get_parent()
            npt = node.NPT
            node_value = observation[node]
            npt = npt[npt[node.id_name] == node_value]
            for p in par:
                node_value = observation[p]
                npt = npt[npt[p.id_name] == node_value]
            result *= npt['cond_prob'].values.item()
        return round(result, 5)

    def marginal_probability(self, observation: dict):
        if self.num_nodes < len(observation):
            raise NetworkException(f"Invalid input")
        else:
            result = 0
            hidden_nodes = [i for i in self.graph.list_nodes if i not in observation]
            list_hidden_node_states = []
            for node in hidden_nodes:
                list_hidden_node_states.append(node.states)
            map_hidden_states = list(itertools.product(*list_hidden_node_states))

            for values in map_hidden_states:
                hidden_dict = {hidden_nodes[i]: values[i] for i in range(len(values))}
                full_observation = {**observation, **hidden_dict}
                result += self.full_marginal(full_observation)

            return round(result, 5)

    def conditional_probability(self, observation: dict, conditional: dict):

        try:
            result = (self.marginal_probability({**observation, **conditional})) / (
                self.marginal_probability(conditional))
            return round(result, 5)
        except ZeroDivisionError as e:
            print("Error: ", str(e))

    def initial_states(self):
        print("******************************")
        print("Initial states")
        for node in self.list_nodes:
            table = PrettyTable(['state', 'prob'])
            if node.num_parent > 0:
                for state in node.states:
                    table.add_row([state, self.marginal_probability({node: state})])
            else:
                table = tabulate(node.NPT, headers=['state','prob'], tablefmt='psql',showindex=False)

            print("Table of node: ", node.id_name)
            print(table)
        print("******************************\n")
