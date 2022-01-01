from Node import *
from Graph import Graph
import pandas as pd
import itertools
from prettytable import PrettyTable


class Network:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.num_nodes = graph.num_nodes
        self.list_nodes = self.graph.list_nodes

    def help_generate_NPT(self, list_nodes, path_to_forder=None):
        for node in list_nodes:
            if node not in self.list_nodes :
                print("Error: node ",node.name," not in network")
                raise Exception


        for node in list_nodes:
            par = node.get_parent()
            columns = [i.name for i in par] + [node.name, "cond_prob"]
            states = [i.states for i in par] + [node.states] + [[0]]
            map_states = list(itertools.product(*states))
            df = pd.DataFrame(map_states, columns=columns)
            if path_to_forder is not None:
                zero_NPT_path = path_to_forder + '/' + node.name + '.csv'
                df.to_csv(zero_NPT_path)
                print("base NPT node of " + node.name + " is stored in: " + zero_NPT_path)
            else:
                return df
    def set_NPT_from_csv(self, node: Node, path):
        if node not in self.graph.list_nodes:
            print("Node is not available in network")
        else:
            node.set_NPT_from_csv(path)

    def set_NPT_func(self, func_node: Node):
        if func_node in self.list_nodes:
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
            print("Node is not available in network")

        else:
            columns = [i.name for i in node.get_parent()] + [node.name, "cond_prob"]
            node.NPT = NPT[columns]

    def set_evidence(self, evidence: dict):
        print("******************************")
        print("set evidence", {i.name: j for i, j in evidence.items()})
        for node in self.list_nodes:
            if node not in evidence.keys():
                table = PrettyTable(['state', 'prob'])
                for state in node.states:
                    table.add_row([state, self.conditional_probability({node: state}, evidence)])
                print("Table of node: ", node.name)
                print(table)

        print("******************************\n")

    def full_marginal(self, observation: dict):
        assert self.num_nodes == len(observation)
        result = 1
        for node in self.graph.list_nodes:
            # if node.name == 'node4':
            par = node.get_parent()
            npt = node.NPT
            node_value = observation[node]
            npt = npt[npt[node.name] == node_value]
            for p in par:
                node_value = observation[p]
                npt = npt[npt[p.name] == node_value]
                # break

                # print(npt)
            # print(npt['cond_prob'])
            result *= npt['cond_prob'].values.item()

        return round(result, 3)

    def marginal_probability(self, observation: dict):
        if self.num_nodes < len(observation):
            print("Invalid input")
        else:
            result = 0
            list_observation = []
            hidden_nodes = [i for i in self.graph.list_nodes if i not in observation]
            # print(hidden_nodes)
            list_hidden_node_states = []
            for node in hidden_nodes:
                list_hidden_node_states.append(node.states)

            map_hidden_states = list(itertools.product(*list_hidden_node_states))
            for values in map_hidden_states:
                hidden_dict = {hidden_nodes[i]: values[i] for i in range(len(values))}
                full_observation = {**observation, **hidden_dict}
                result += self.full_marginal(full_observation)

            return round(result, 3)

    def conditional_probability(self, observation: dict, conditional: dict):
        try:
            result = (self.marginal_probability({**observation, **conditional})) / (
                self.marginal_probability(conditional))
            return round(result, 3)
        except ZeroDivisionError as e:
            print("Error: ", str(e))

    def initial_states(self):
        print("******************************")
        print("Initial states")
        for node in self.list_nodes:
            table = PrettyTable(['state', 'prob'])
            for state in node.states:
                table.add_row([state, self.marginal_probability({node: state})])
            print("Table of node: ", node.name)
            print(table)
        print("******************************\n")
