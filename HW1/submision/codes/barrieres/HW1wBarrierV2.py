import numpy as np
import allBarriers as allbar

def find_vpi(maze_size, theta= 0.01, maxiter = 10000):
    barriers = allbar.barrierMaze10x10()
    actionSpace = ["N", "S", "E", "W"]
    movesDic = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }
    vk = np.zeros((maze_size,maze_size))
    vkp1 = np.zeros(vk.shape)
    keepiterate = True
    deltalist = np.array([])
    count = 0
    print(vk)
    while keepiterate:
        count += 1
        for i in range(maze_size):
            for j in range(maze_size):
                if i < maze_size-1 or j < maze_size-1:
                    minV = np.inf
                    for a in actionSpace:
                        bar, bord = allbar.isBarBord(barriers, maze_size, movesDic, np.array([j,i]), a)
                        if not (bar or bord):
                            k, l = movesDic[a]
                            newV = -1 + 0.25*vk[i+k][j+l]
                            if newV < minV:
                                minV = newV                  
                    vkp1[i][j] = minV
                else:
                    vkp1[i][j] = 0.0
        deltalist = np.append(deltalist, np.max(np.absolute(np.subtract(vk, vkp1))))
        # print(deltalist, type(deltalist),deltalist[-1], type(deltalist[-1]),theta, type(theta),deltalist[-1] < theta)
        keepiterate = deltalist[-1] > theta
        vk = vkp1.copy()
        if count >maxiter:
            break
    print(np.round(vk,1))
    return vk, deltalist
vk, deltalist = find_vpi(10, theta= 0.00000000001, maxiter = 10000)
print(len(deltalist))