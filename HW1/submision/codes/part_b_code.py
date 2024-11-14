import time
import numpy as np
import barrieres.HW1wBarrierPartB as vkfilewbar
import evaluateValIter as eval
import matplotlib.pyplot as plt

keepiterate = True
maze_size = 10
count = 0
maxiter = 10000
maxCost = 1100
vk = np.zeros((maze_size,maze_size))
deltalist = []
valIterCostList = []

while keepiterate and not count==maxiter:
    vk, delta, keepiterate = vkfilewbar.find_vpi(maze_size, False, vk)
    deltalist.append(delta)
    valIterCostList.append(-eval.runOnCurPolicy(vk, maxCost)[0])
print(valIterCostList)
plt.title("Running Cost at Each Value Iteration")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.plot(valIterCostList)
plt.ylim(bottom=-1000)
plt.xticks([1]+[i for i in range(5,len(valIterCostList)+1,5)])
plt.savefig('plots/part_b_costperiter.pdf')
