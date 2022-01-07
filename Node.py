import itertools
import numpy as np
import pandas as pd
from scipy.stats import norm
import seaborn as sns

class Node:
    def __init__(self, id_name: str, states: list):
        '''
        :param id_name: name of node, for identify node
        :param states: states of node. For ex [low, high]
        '''
        self.id_name = id_name
        self.num_parent = 0
        self.parent = []
        self.states = states
        self.N = len(states)
        self.NPT = None

    def add_parent(self, node):
        self.num_parent += 1
        self.parent.append(node)

    def get_parent(self):
        '''
        :return: list of parent nodes
        '''
        return self.parent

    def set_NPT_from_csv(self, path):
        '''
        Set the value of node from csv file
        :param path: path to file
        '''
        self.NPT = pd.read_csv(path)

    def set_NPT_func(self):
        '''
        for function node
        '''
        pass



class Boolean_Node(Node):
    def __init__(self, id_name, states = [True, False]):
        super().__init__(id_name, states)



class OR_Node(Boolean_Node):
    def __init__(self, id_name):
        super().__init__(id_name)
        self.NPT = None
    def set_NPT_func(self):
        for node in self.get_parent():
            if not isinstance(node, Boolean_Node):
                raise Exception

        par = self.get_parent()
        columns = [i.id_name for i in par] + [self.id_name, "cond_prob"]
        states = [i.states for i in par] + [self.states] + [[0]]
        map_states = list(itertools.product(*states))
        baseNPT = [list(record) for record in map_states]
        for record in baseNPT:
            if (True in record[:-2] and record[-2] == True) or (False in record[:-2] and record[-2] == False):
                record[-1] = 1
        self.NPT = pd.DataFrame(baseNPT, columns=columns)


class AND_Node(Boolean_Node):
    def __init__(self, id_name):
        super().__init__(id_name)
        self.NPT = None
    def set_NPT_func(self):
        for node in self.get_parent():
            if not isinstance(node, Boolean_Node):
                raise Exception

        par = self.get_parent()
        columns = [i.id_name for i in par] + [self.id_name, "cond_prob"]
        states = [i.states for i in par] + [self.states] + [[0]]
        map_states = list(itertools.product(*states))
        baseNPT = [list(record) for record in map_states]
        for record in baseNPT:
            if (False not in record[:-2] and record[-2] == True) or (False in record[:-2] and record[-2] == False):
                record[-1] = 1

        self.NPT = pd.DataFrame(baseNPT, columns=columns)


class MtoN_Node(Boolean_Node):
    def __init__(self, id_name, M):
        super().__init__(id_name)
        self.NPT = None
        self.M = M #

    def set_NPT_func(self):
        if self.M > self.num_parent:
            raise Exception
        for node in self.get_parent():
            if not isinstance(node, Boolean_Node):
                raise Exception

        par = self.get_parent()
        columns = [i.id_name for i in par] + [self.id_name, "cond_prob"]
        states = [i.states for i in par] + [self.states] + [[0]]
        map_states = list(itertools.product(*states))
        baseNPT = [list(record) for record in map_states]
        for record in baseNPT:
            if (sum(record[:-2]) >= self.M and record[-2] == True) or (sum(record[:-2]) < self.M and record[-2] == False):
                record[-1] = 1

        self.NPT = pd.DataFrame(baseNPT, columns=columns)

class Label_Node(Node):
    def __init__(self, id_name, states: list):
        super().__init__(id_name, states)

class Ranked_Node(Node):
    def __init__(self, id_name, states: list, mean = 0, std = 1):
        super().__init__(id_name, states)

        self.numeric_states = np.linspace(0.0,1.0,len(states)+1)
        self.NPT = None
        self.mean = mean
        self.std = std
        self.gaussian = norm(mean,std)
        self.map = dict(zip(self.states,self.numeric_states[:-1]))


    def set_NPT_TNormal(self):
        y = []
        for i in range(len(self.numeric_states) - 1):
            y.append(self.gaussian.cdf(self.numeric_states[i + 1]) - self.gaussian.cdf(self.numeric_states[i]))

        prob = [i * 1 / sum(y) for i in y]
        columns = [self.id_name, "cond_prob"]
        baseNPT = (list(zip(self.states, prob)))

        self.NPT = pd.DataFrame(baseNPT, columns=columns)

class Weighted_Node(Ranked_Node):
    def __init__(self, id_name, states: list, weighted_mean:dict, mean = None, std = 0.1):
        super().__init__(id_name, states, mean, std)
        self.numeric_states = np.linspace(0.0, 1.0, len(states) + 1)
        self.weighted_mean = weighted_mean
        self.map = dict(zip(self.states,self.numeric_states[:-1]))

    def set_NPT_func(self):
        assert len(self.weighted_mean) == len(self.get_parent())
        for node in self.get_parent():
            if not isinstance(node, Ranked_Node):
                raise Exception

        par = self.weighted_mean.keys()
        columns = [i.id_name for i in par] + [self.id_name, "cond_prob"]
        states = [i.states for i in par]
        map_states = list(itertools.product(*states))
        map_states = [list(record) for record in map_states]

        baseNPT = []
        for record in map_states:
            mean = self.get_mean_from_par_state(record)

            y = []
            gaussian = norm(mean, self.std)
            for i in range(len(self.numeric_states) - 1):
                y.append(gaussian.cdf(self.numeric_states[i + 1]) - gaussian.cdf(self.numeric_states[i]))

            prob = [round(i * 1 / sum(y),3) for i in y]
            state_prob = list(zip(self.states, prob))
            for i in state_prob:
               baseNPT.append(record + list(i))

        self.NPT = pd.DataFrame(baseNPT, columns=columns)


    def get_mean_from_par_state(self,states:list):
        mean = 0
        for node,state in zip(self.weighted_mean.keys(),states):
            mean += self.weighted_mean[node]*node.map[state]
        return mean
