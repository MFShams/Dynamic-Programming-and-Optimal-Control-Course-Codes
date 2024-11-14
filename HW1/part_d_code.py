# Author: Mojtaba AlShams
# Professional email: mojtaba.alshams@kaust.edu.sa
# Personal email: m.f.shams@hotmail.com
# This project github link: https://github.com/MFShams/Dynamic-Programming-and-Optimal-Control-Course-Codes/tree/main/HW1

import time
import numpy as np
import barrieres.HW1wBarrierPartB as vkfilewbar
import barrieres.HW1wBarrierPartC as pikfile
import evaluatePolIter as evalPi
import evaluateValIter as evalV
import matplotlib.pyplot as plt
import os

folder_path = os.path.join(os.getcwd(),'plots')
if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
def initVkPik(maze_size, optCont):
    movesDic = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }
    actionSpace = {
        "N": 0,
        "S": 1,
        "E": 2,
        "W": 3
    }
    minVal = -len(optCont)
    i, j = 0, 0
    vk = np.ones((maze_size,maze_size))*-100
    pik = np.zeros((maze_size,maze_size))
    # vk, pik = initVkPikV2(maze_size)
    vk[0][0] = minVal
    for action in optCont:
        pik[i][j]= actionSpace[action]
        curVal = vk[i][j] + 1
        k, l = movesDic[action]
        i, j = i+k, j+l
        vk[i][j] =  curVal
    return vk, pik
def initVkPikV2(maze_size):
    vk = np.random.rand(maze_size**2).reshape((maze_size,maze_size))
    vk[-1][-1] = 0
    pik = np.random.randint(low = 0, high = 3, size = maze_size**2).reshape((maze_size,maze_size))
    return vk, pik
polStable = False
keepiterate = True
maze_size = 10
count = 0
maxiter = 10000
maxCost = 1100
optPath = ["E","S","W","S","S","S","S","S","E","E","E","S","S","E",
           "E","N","W","N","N","W","N","W","N","E","E","E","N","E",
           "E","N","W","W","W","N","E","E","E","E","S","E","S","W",
           "S","E","S","W","W","W","S","S","S","S","E","N","N","E",
           "E","S","W","S","S","E"]
vk, pik = initVkPik(maze_size, optPath)
piIterCostList = []
valIterCostList = []

while keepiterate and not count==maxiter:
    vk, delta, keepiterate = vkfilewbar.find_vpi(maze_size, False, vk)
    valIterCostList.append(-evalV.runOnCurPolicy(vk, maxCost)[0])
print(valIterCostList)
plt.figure()
plt.title("Running Cost at Each Value Iteration After Embeding $v_o$ and $\pi_o$")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.plot(valIterCostList)
# plt.ylim(bottom=-1000)
plt.xticks([1]+[i for i in range(5,len(valIterCostList)+1,5)])
plt.savefig('plots/part_d_v_costPerIter.pdf')

count = 0
while not polStable and not count==maxiter:
    pik, countPi, polStable = pikfile.find_pi_i(maze_size, pik=pik)
    piIterCostList.append(evalPi.runOnCurPolicy(pik, maxCount=620, render=False)[0])
print(piIterCostList)
plt.figure()
plt.title("Running Cost at Each Policy Iteration After Embeding $v_o$ and $\pi_o$")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.plot(piIterCostList)
# plt.ylim(top=1000)
plt.xticks([1]+[i for i in range(5,len(piIterCostList)+1,5)])
plt.savefig('plots/part_d_pi_costPerIter.pdf')

