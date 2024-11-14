import gym
import gym_maze
import time
import numpy as np
import barrieres.allBarriers as allbar

barriers = allbar.barrierMaze10x10()
env = gym.make('maze-sample-10x10-v0')

def takeAction(pi, s):
    actionSpace = ["N", "S", "E", "W"]
    i = int(s[1])
    j = int(s[0])
    return actionSpace[int(pi[i][j])]
     
def runOnCurPolicy(pi, maxCount=620, render=False):
    #                 0 ,  1 ,  2 ,  3
    # action space: ["N", "S", "E", "W"]
    movesDic = {
        0: (-1, 0),
        1: (1, 0),
        2: (0, 1),
        3: (0, -1),
    }
    maze_size = pi.shape[0]
    (li, lj) = (0,0)
    allAction = []
    if render:
        env.render()
    obs = env.reset()
    done = False
    obs= np.int64(obs.copy())
    count = 0
    cost = 0

    while (not done) and (not count == maxCount):
        count += 1
        action = takeAction(pi, obs)
        bar, bord = allbar.isBarBord(barriers, maze_size, movesDic, obs, pi[obs[1]][obs[0]])
        if bar or bord:
            cost += -1-0.5
        else:
            cost += -1
        allAction.append(action)
        obs, reward, done, _ = env.step(action)
        if render:
            env.render()
            time.sleep(0.1)
    return cost, allAction, count
# pi = np.array([[2., 1., 1., 1., 2., 2., 2., 2., 1., 1.],
#        [1., 3., 1., 3., 0., 3., 3., 3., 2., 1.],
#        [1., 3., 3., 2., 0., 2., 2., 0., 1., 3.],
#        [1., 2., 2., 2., 2., 0., 1., 3., 2., 1.],
#        [1., 0., 0., 3., 2., 1., 1., 3., 3., 3.],
#        [1., 0., 3., 0., 3., 1., 1., 2., 2., 1.],
#        [2., 2., 2., 1., 0., 2., 1., 2., 2., 1.],
#        [1., 2., 1., 1., 0., 3., 1., 0., 1., 3.],
#        [1., 0., 1., 2., 2., 0., 2., 0., 1., 1.],
#        [2., 0., 2., 2., 2., 2., 2., 2., 2., 0.]])
# print(runOnCurPolicy(pi,620, True))