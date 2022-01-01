import itertools
import numpy as np
import pandas as pd
from scipy.stats import norm

class Node:
    def __init__(self, name: str, states: list):
        '''
        :param name: name of node
        :param states: states of node. For ex [low, high]
        '''
        self.name = name
        self.num_parent = 0
        self.parent = []
        self.states = states
        self.N = len(states)
        self.NPT = None

    def add_parent(self, node):
        self.parent.append(node)

    def get_parent(self):
        return self.parent

    def set_NPT_from_csv(self, path):
        '''
        Set the value of node from csv file
        :param path: path to file
        '''
        file = pd.read_csv(path)
        # columns = [i.name for i in self.get_parent()] + [self.name, "cond_prob"]
        self.NPT = file

    def set_NPT_func(self):
        '''
        for function node implelement
        '''
        pass



class Boolean_Node(Node):
    def __init__(self, name,states = [True, False]):
        super().__init__(name,states)



class OR_Node(Boolean_Node):
    def __init__(self,name):
        super().__init__(name)
        self.NPT = None
    def set_NPT_func(self):
        for node in self.get_parent():
            if not isinstance(node, Boolean_Node):
                raise Exception

        par = self.get_parent()
        columns = [i.name for i in par] + [self.name, "cond_prob"]
        states = [i.states for i in par] + [self.states] + [[0]]
        map_states = list(itertools.product(*states))
        baseNPT = [list(record) for record in map_states]
        for record in baseNPT:
            if (True in record[:-2] and record[-2] == True) or (False in record[:-2] and record[-2] == False):
                record[-1] = 1
        self.NPT = pd.DataFrame(baseNPT, columns=columns)
        print("NPT of function OR node", self.name)
        print(self.NPT)

class AND_Node(Boolean_Node):
    def __init__(self,name):
        super().__init__(name)
        self.NPT = None
    def set_NPT_func(self):
        for node in self.get_parent():
            if not isinstance(node, Boolean_Node):
                raise Exception

        par = self.get_parent()
        columns = [i.name for i in par] + [self.name, "cond_prob"]
        states = [i.states for i in par] + [self.states] + [[0]]
        map_states = list(itertools.product(*states))
        baseNPT = [list(record) for record in map_states]
        for record in baseNPT:
            if (False not in record[:-2] and record[-2] == True) or (False in record[:-2] and record[-2] == False):
                record[-1] = 1

        self.NPT = pd.DataFrame(baseNPT, columns=columns)
        print("NPT of function AND node", self.name)
        print(self.NPT)

class MtoN_Node(Boolean_Node):
    def __init__(self, name, M):
        super().__init__(name)
        self.NPT = None
        self.M = M

    def set_NPT_func(self):
        if self.M > self.num_parent:
            raise Exception
        for node in self.get_parent():
            if not isinstance(node, Boolean_Node):
                raise Exception

        par = self.get_parent()
        columns = [i.name for i in par] + [self.name, "cond_prob"]
        states = [i.states for i in par] + [self.states] + [[0]]
        map_states = list(itertools.product(*states))
        baseNPT = [list(record) for record in map_states]
        for record in baseNPT:
            if (sum(record[:-2]) >= self.M and record[-2] == True) or (sum(record[:-2]) < self.M and record[-2] == False):
                record[-1] = 1

        self.NPT = pd.DataFrame(baseNPT, columns=columns)
        print("NPT of function AND node", self.name)
        print(self.NPT)





class Label_Node(Node):
    def __init__(self, name, states: list):
        super().__init__(name,states)


class Ranked_Node(Node):
    def __init__(self, name, states: list, mean, std):
        super().__init__(name,states)

        self.numeric_states = np.linspace(0.0,1.0,len(states))
        self.NPT = None
        self.mean = mean
        self.std = std
        self.norm = norm(mean,std)

    def set_NPT(self):
        y = []
        print(self.numeric_states)
        for i in range(len(self.numeric_states)-1):
            y.append(self.norm.cdf(self.numeric_states[i+1]) - self.norm.cdf(self.numeric_states[i]))

        prob =  [i * 1/sum(y) for i in y]

        self.NPT = (list(zip(self.states, prob)))

class Weighted_Node(Ranked_Node):
    def __init__(self, name, states: list,weighted_mean:dict ,mean = None, std = 0.01):
        super().__init__(name, states,mean, std)
        self.weighted_mean = weighted_mean

    def set_NPT(self):
        pass


