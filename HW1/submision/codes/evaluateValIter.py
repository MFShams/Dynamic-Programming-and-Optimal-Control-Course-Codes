import gym
import gym_maze
import time
import numpy as np
import barrieres.allBarriers as allbar

barriers = allbar.barrierMaze10x10()
env = gym.make('maze-sample-10x10-v0')

def takeAction(valFun, barriers, s, movesDic, observ):
    actionSpace = ["N", "S", "E", "W"]
    actAvl = []
    for a in actionSpace:
        if not allbar.isBar(barriers, s, movesDic, observ, a):
            actAvl.append(a)
    return findMinVal(valFun, movesDic, observ, actAvl)
     
def findMinVal(valFun, movesDic, observ, aAvl):
    possMoves = []
    valMov = []
    for a in aAvl:
        (i, j) = movesDic[a]
        k, l = observ[1]+i,observ[0]+j
        possMoves.append((k, l))
        valMov.append(valFun[k][l])
    inds = np.where(np.array(valMov) == max(np.array(valMov)))
    randInd = np.random.choice(inds[0], size=1)
    return aAvl[randInd[0]]

def runOnCurPolicy(valFun, maxCost=620, render=False):
    #                 0 ,  1 ,  2 ,  3
    # action space: ["N", "S", "E", "W"]
    movesDic = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }
    # barriers = allbar.barrierMaze10x10()
    s = valFun.shape[0]
    (li, lj) = (0,0)
    allAction = []
    # env = gym.make('maze-sample-10x10-v0')
    if render:
        env.render()
    obs = env.reset()
    done = False
    obs= np.int64(obs.copy())
    count = 0

    while (not done) and (not count == maxCost):
        count += 1
        action = takeAction(valFun, barriers, s, movesDic, obs)
        allAction.append(action)
        obs, reward, done, _ = env.step(action)
        if render:
            env.render()
            time.sleep(0.05)
    return count, allAction