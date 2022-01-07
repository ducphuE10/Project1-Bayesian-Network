from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

norm = norm(0,1)

x = [0,0.2,0.4,0.6,0.8,1]


y = []
for i in range(len(x)-1):
    y.append(norm.cdf(i+1) - norm.cdf(i))

# print(np.linspace(0,1,6))


# print(norm.cdf(5) - norm.cdf(0))

from Node import *

r1 = Ranked_Node('rank1',['1','2','3'],0.5,0.1**(1/2))
r2 = Ranked_Node('rank2',['1','2'],0,1)
r3 = Weighted_Node('rank2',['1','2','3'], {r1:1/2, r2:1/2})
r3.add_parent(r2)
r3.add_parent(r1)
r3.set_NPT_func()
print(r3.NPT)
# print(r3.map['1'])
# r3.test(['3','1'])