import numpy as np
import barrieres.allBarriers as allbar
# import allBarriers as allbar
import time

def find_pi_i(maze_size, pik=None, theta= 0.01, maxiterPi = 100, maxiterV = 10000):
    a = -1
    b = -0.5
    gamma = 1
    barriers = allbar.barrierMaze10x10()
    actionSpace =   [0,    1,   2,   3]
    # actionSpace = ["N", "S", "E", "W"]
    movesDic = {
        0: (-1, 0),
        1: (1, 0),
        2: (0, 1),
        3: (0, -1),
    }
    vk = np.zeros((maze_size,maze_size))
    if pik is not None:
        tillConverg = False
    else:
        tillConverg = True
        pik = np.zeros((maze_size,maze_size))
    pikp1 = np.zeros(pik.shape)
    countPi = 0
    polStable = False
    while not polStable and not countPi==maxiterPi:
        countPi += 1
        vk, deltalist = find_vk(a, b, gamma, pik, vk, movesDic, barriers, maze_size, maxiterV, theta)
        for i in range(maze_size):
            for j in range(maze_size): #for each s \in S
                if i < maze_size-1 or j < maze_size-1:
                    maxRes = -np.inf
                    for action in actionSpace:
                        bar, bord = allbar.isBarBord(barriers, maze_size, movesDic, np.array([j,i]), action)
                        if not (bar or bord):
                            k, l = movesDic[action]
                            # print(i, j, k, l)
                            # print(bar , bord)
                            # print(pik[i][j], action)
                            res = a + gamma*vk[i+k][j+l]
                        else:
                            res = a + b + gamma*vk[i][j]
                        if res > maxRes:
                            maxRes = res
                            pikp1[i][j] = action
                else:
                    pikp1[i][j] = 0
        polStable = np.all(pik == pikp1)
        pik = pikp1.copy()
        if not tillConverg:
            return pik, countPi, polStable
    return pik, countPi, polStable

def find_vk(a, b, gamma, pik, vk, movesDic, barriers, maze_size, maxiterV, theta):
    vkp1 = np.zeros(vk.shape)
    keepiterate = True
    deltalist = []
    countV = 0
    while keepiterate and not countV==maxiterV:
        countV += 1
        for i in range(maze_size):
            for j in range(maze_size): #for each s \in S
                if i < maze_size-1 or j < maze_size-1:
                    bar, bord = allbar.isBarBord(barriers, maze_size, movesDic, np.array([j,i]), pik[i][j]) #is barrier or border
                    if not (bar or bord):
                        k, l = movesDic[pik[i][j]]
                        vkp1[i][j] = a + gamma*vk[i+k][j+l]
                    else:
                        vkp1[i][j] = a + b + gamma*vk[i][j]
                else:
                    vkp1[i][j] = 0.0
        deltalist = np.append(deltalist, np.max(np.absolute(np.subtract(vk, vkp1))))
        keepiterate = deltalist[-1] > theta
        vk = vkp1.copy()
    return vk, deltalist
# vk, deltalist = find_vpi(10, theta= 0.1, maxiter = 10000)
# print(len(deltalist))
# maze_size = 10
# tok = time.time()
# print(find_pi_i(maze_size))
# tik = time.time()
# print(f"it took {(tik-tok)/60} minutes to finish!")