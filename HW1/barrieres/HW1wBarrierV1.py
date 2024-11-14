import numpy as np
import allBarriers as allbar

def updateDataList(alldelta, error, count=None, theta=0.00001, countMax=10000):
    alldelta = np.append(alldelta, error)
    if count is None:
        if len(alldelta)>10:
            contLoop = (np.max(alldelta[-10:])-np.min(alldelta[-10:]))>theta
            # print('here', alldelta[-10:], contLoop, np.max(alldelta[-10:])-np.min(alldelta[-10:]))
        else:
            contLoop = True
    elif count < countMax:
        contLoop = True
    else:
        contLoop = False
    return alldelta, contLoop
def find_vpi(maze_size):
    movesDic = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }
    vk = np.zeros((maze_size,maze_size))
    delta = np.array([0.0])#np.zeros((maze_size,maze_size))
    vkp1 = np.zeros(vk.shape)
    lastind = vk.shape[0]-1
    print(vk)
    keepiterate = True
    deltalist = np.array([])
    count = 0
    actionSpace = ["N", "S", "E", "W"]
    barriers = allbar.barrierMaze10x10()

    while keepiterate:
        for i in range(maze_size):
            for j in range(maze_size):
                barBorCost = []
                barBorInd = []
                for a in actionSpace:
                    bar, bord = allbar.isBarBord(barriers, maze_size, movesDic, np.array([j,i]), a)
                    if bar or bord:
                        barBorCost.append(1)
                        barBorInd.append(0)
                    else:
                        barBorCost.append(0)
                        barBorInd.append(1)
                a = 1
                b = 1
                gama = 1
                if i < maze_size-1 or j < maze_size-1: 
                    vkp1[i][j] = 0.25*((-a-b*barBorCost[0]+gama*vkp1[i+(-1*barBorInd[0])][j])+
                                    (-a-b*barBorCost[1]+gama*vkp1[i+(1*barBorInd[1])][j])+
                                    (-a-b*barBorCost[2]+gama*vkp1[i][j+(1*barBorInd[2])])+
                                    (-a-b*barBorCost[3]+gama*vkp1[i][j+(-1*barBorInd[3])]))
                else:
                    vkp1[i][j] = 0.0
        #find error between v_k and v_{k+1}
        delta[0] = np.max(np.absolute(np.subtract(vk, vkp1)))
        count += 1
        deltalist, keepiterate = updateDataList(deltalist, delta, None)#count)
        # print(vk-vkp1, keepiterate)
        vk = vkp1.copy()
    return vk, deltalist
# maze_size = 10

