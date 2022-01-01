from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

norm = norm(0,1)

x = [0,0.2,0.4,0.6,0.8,1]


y = []
for i in range(len(x)-1):
    y.append(norm.cdf(i+1) - norm.cdf(i))

print(np.linspace(0,1,6))


print(norm.cdf(5) - norm.cdf(0))