import gym
# from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo
import gym_maze
import time
import numpy as np
import barrieres.HW1noBarrier as vkfile
# import HW1wBarrier as vkfilewbar
# import HW1wBarrierV2 as vkfilewbar
import barrieres.HW1wBarrierV3 as vkfilewbar
import allBarriers as allbar

ENABLE_RECORDING = True
recording_folder = "./recording"

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

def findNew_li_lj(i, j, a, movesDic):
    itemp, jtemp = movesDic[a]
    return i+itemp, j+jtemp

maze_size = 10
movesDic = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}
# valFun, deltalist = vkfile.find_vpi(maze_size)
valFun, deltalist = vkfilewbar.find_vpi(maze_size)
print(len(deltalist), deltalist[-20:])
print(np.round(valFun,1))
barriers = allbar.barrierMaze10x10()
s = valFun.shape[0]
(li, lj) = (0,0)
allAction = []
# maxiter = 20
# while (li, lj) != (0,0) or count == maxiter:
#     count += 1
#     action = takeAction(valFun, barriers, s, movesDic, np.array([lj,li]))
#     allAction.append(action)
#     li, lj = findNew_li_lj(li, lj, action, movesDic)
    
env = gym.make('maze-sample-10x10-v0')
env.render()
#   0 ,  1 ,  2 ,  3
# ["N", "S", "E", "W"]
obs = env.reset()
done = False
obs= np.int64(obs.copy())
count = 0
# if ENABLE_RECORDING:
#     env = RecordVideo(env, video_folder="recording", name_prefix="eval",
#                   episode_trigger=lambda x: True)
#     # env.monitor.start(recording_folder, force=True)
while not done:
    count += 1
    # action = env.action_space.sample()
    action = takeAction(valFun, barriers, s, movesDic, obs)
    allAction.append(action)
    obs, reward, done, _ = env.step(action)
    env.render()
    time.sleep(0.1)
# if ENABLE_RECORDING:
#     env.close()
#     # env.monitor.close()
print(count)