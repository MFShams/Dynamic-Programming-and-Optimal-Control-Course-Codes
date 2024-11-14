import numpy as np
def updateDataList(alldelta, error, theta=0.0001):
    alldelta = np.append(alldelta, error)
    if len(alldelta)>100:
        contLoop = (np.max(alldelta[-100:])-np.min(alldelta[-100:]))>theta
        # print('here', alldelta[-10:], contLoop, np.max(alldelta[-10:])-np.min(alldelta[-10:]))
    else:
        contLoop = True
    return alldelta, contLoop

def find_vpi(maze_size):
    vk = np.zeros((maze_size,maze_size))
    delta = np.array([0.0])#np.zeros((maze_size,maze_size))
    vkp1 = np.zeros(vk.shape)
    lastind = vk.shape[0]-1
    # print('The inatial value function:\n',vk)
    keepiterate = True
    deltalist = np.array([])
    count = 0
    while keepiterate:
    # for _ in range(100):
        count += 1
        for i in range(1,lastind): #fill the inside cells
            vkTemp1 = vk[i-1]
            vkTemp2 = vk[i+1]
            vkTemp3 = vk[i]
            vkp1[i][1:-1] = 0.25*((-1+vkTemp1[1:-1])+(-1+vkTemp2[1:-1])+(-1+vkTemp3[0:-2])+(-1+vkTemp3[2:]))

        #fill the upper and lower border cells
        vkTemp1 = vk[0]
        vkTemp2 = vk[1]
        vkp1[0][1:-1] = 0.25*((-1+vkTemp1[1:-1])+(-1+vkTemp2[1:-1])+(-1+vkTemp1[0:-2])+(-1+vkTemp1[2:]))

        #fill the lower border cells
        vkTemp1 = vk[-1]
        vkTemp2 = vk[-2]
        vkp1[-1][1:-1] = 0.25*((-1+vkTemp1[1:-1])+(-1+vkTemp2[1:-1])+(-1+vkTemp1[0:-2])+(-1+vkTemp1[2:]))

        #fill the right border cells
        vkTemp1 = vk[:,-1]
        vkTemp2 = vk[:,-2]
        vkp1[:,-1][1:-1] = 0.25*((-1+vkTemp1[1:-1])+(-1+vkTemp2[1:-1])+(-1+vkTemp1[0:-2])+(-1+vkTemp1[2:]))

        #fill the left border cells
        vkTemp1 = vk[:,0]
        vkTemp2 = vk[:,1]
        vkp1[:,0][1:-1] = 0.25*((-1+vkTemp1[1:-1])+(-1+vkTemp2[1:-1])+(-1+vkTemp1[0:-2])+(-1+vkTemp1[2:]))

        #fill the corners
        vkp1[0][-1] = 0.25*((-1+vk[0][-2])+(-1+vk[1][-1])+(-1+vk[0][-1])+(-1+vk[0][-1]))
        vkp1[-1][0] = 0.25*((-1+vk[-1][0])+(-1+vk[-1][0])+(-1+vk[-1][1])+(-1+vk[-2][0]))
        vkp1[0][0] = 0.25*((-1+vk[0][0])+(-1+vk[1][0])+(-1+vk[0][1])+(-1+vk[0][0]))

        #find error between v_k and v_{k+1}
        delta[0] = np.max(np.absolute(np.subtract(vk, vkp1)))
        deltalist, keepiterate = updateDataList(deltalist, delta)
        # print(vk-vkp1, keepiterate)
        vk = vkp1.copy()
    return vk, deltalist
# maze_size = 10
# vk, deltalist = find_vpi(maze_size)
# print(f'It took {len(deltalist)} iterations to reach this value function.')
# print('The final value function:\n',np.round(vk,1))
