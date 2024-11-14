import gym
import gym_maze
import time

env = gym.make('maze-sample-10x10-v0')
# print(env.observation_space)
# print(env.action_space)
# obs = env.reset()
# print('-----------------------------')
# # for i in env.action_space:
# print(env.action_space)
# for _ in range(50):
#     a = env.action_space.sample()
#     print(a, type(a))
# print('-----------------------------')

env.render()

# for _ in range(10):
# 2: right
# 3: left
#   0 ,  1 ,  2 ,  3
# ["N", "S", "E", "W"]
obs = env.reset()
for a in [2,1,3,1,1,1]:#["N","S","S","S","S","S","E","E","E"]:
    # print(isinstance(a, int))
    
    done = False
    # while not done:
    # action = env.action_space.sample()
    # print(action)
    # obs, reward, done, _ = env.step(action)
    obs, reward, done, _ = env.step(a)
    env.render()
    time.sleep(1)