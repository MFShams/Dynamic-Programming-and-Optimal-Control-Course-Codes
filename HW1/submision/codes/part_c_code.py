import time
import numpy as np
import barrieres.HW1wBarrierPartC as pikfile
import evaluatePolIter as eval
import matplotlib.pyplot as plt

polStable = False
maze_size = 10
count = 0
maxiter = 10000
maxCost = 1100
pik = np.zeros((maze_size,maze_size))
piIterCostList = []

while not polStable and not count==maxiter:
    pik, countPi, polStable = pikfile.find_pi_i(maze_size, pik=pik)
    piIterCostList.append(eval.runOnCurPolicy(pik, maxCount=1100, render=False)[0])
print(piIterCostList)
plt.title("Running Cost at Each Policy Iteration")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.plot(piIterCostList)
plt.ylim(bottom=-1000)
plt.xticks([1]+[i for i in range(5,len(piIterCostList)+1,5)])
plt.savefig('plots/part_c_cost_per_iter.pdf')
