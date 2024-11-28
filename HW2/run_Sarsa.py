# Author: Mojtaba AlShams
# Professional email: mojtaba.alshams@kaust.edu.sa
# Personal email: m.f.shams@hotmail.com
# This project github link: https://github.com/MFShams/Dynamic-Programming-and-Optimal-Control-Course-Codes/tree/main/HW2

# Some parts of this code were inspired from: https://www.geeksforgeeks.org/sarsa-reinforcement-learning/
# accessed on Nov 2024
import argparse
import numpy as np
import gym
import gym_maze
import time
from tqdm import tqdm

import write_read as wr

MAZE_SIZE = 10
SEED = 255
np.random.seed(seed=SEED)
def choose_action(args, env, state, Q, evaluate = False):
    if not evaluate and np.random.uniform(0, 1) < args.epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state[1],state[0], :])
    return action
 
#Function to learn the Q-value
def update(args, state, state2, reward, action, action2, Q, alpha):
    predict = Q[state[1], state[0], action]
    target = reward + args.gamma*Q[state2[1], state2[0], action2]
    Q[state[1], state[0], action] = predict + alpha*(target - predict)
    return Q[state[1], state[0], action]

def find_reward(state1, state2):
    if (state2 == np.array([9,9])).all():# or (state1 == state2).all(): #if terminal state
        reward = 0
    elif (state1 == state2).all(): #if hit a wall
        reward = -5
    else:
        reward = -1 #moving in the maze
    return reward

def train_agent(args, env, Q):
    print('training the agent is on progress...')
    all_ep_reward = np.array([])
    actionSpace = ["N", "S", "E", "W"]
    if args.decay == 'constant':
        a = args.alpha
    # Starting the SARSA learning
    for _ in tqdm(range(args.max_epsds), desc ='training is in progress'):
    # for _ in range(args.max_epsds):
        t = 0
        ep_tot_reward = 0
        state1 = env.reset().copy()
        action1 = choose_action(args, env, state1.astype(int), Q)
        while t < args.max_stps:
            if args.visualT:
                env.render() #Visualizing the training
            if args.decay == 'adaptive':
                a = 1/(t+1)
            #Getting the next state
            state2, _, done, _ = env.step(actionSpace[action1])
            reward = find_reward(state1,state2) # To Do

            #Choosing the next action
            action2 = choose_action(args, env, state2.astype(int), Q)
            
            #Learning the Q-value
            # print(int(state1[1]), int(state1[0]), state1.astype(int), state2.astype(int))
            # print(type(int(state1[1])), type(int(state1[0])), type(state1.astype(int)), type(state2.astype(int)), type(state1.astype(int)[0]), type(state2.astype(int)[0]))
            Q[int(state1[1]), int(state1[0]), action1] = update(args, state1.astype(int), state2.astype(int), reward, action1, action2, Q, a)
            state1 = state2.copy()
            action1 = action2
            t += 1
            ep_tot_reward += reward
            if done: #if terminal state was reached
                break
        all_ep_reward = np.append(all_ep_reward, ep_tot_reward)
    return Q, all_ep_reward

def eval_policy(args, env, Q):
    print('evaluating the agent is on progress...')
    actionSpace = ["N", "S", "E", "W"]
    t = 0
    state1 = env.reset()
    while t < args.max_stps:
        if args.visualE:
            env.render() #Visualizing the evaluation
            time.sleep(0.1)
        action1 = actionSpace[choose_action(args, env, state1.astype(int), Q, evaluate = True)]
        state2, reward, done, info = env.step(action1)
        t += 1
        state1 = state2.copy()
        if done: #if terminal state was reached
            break

def initQ(args):
    file_name = 'QnparrSARSA'
    if args.dontuseQ or not wr.qSARSA_exist(args, file_name):
        Q = np.random.rand(MAZE_SIZE*MAZE_SIZE*env.action_space.n).reshape((MAZE_SIZE, MAZE_SIZE, env.action_space.n))
        Q[-1,-1,:] = np.array([0]*env.action_space.n)
        assert args.dontskipT, 'Q is not trained yet or "--useQ" was not set!'
        return Q
    else:
        Q = wr.read_np_arr(args, file_name)
        Q[-1,-1,:] = np.array([0]*env.action_space.n)
        return Q

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameters to run Sarsa algorithm with epsilon-greedy method')
    parser.add_argument("-me", "--max_epsds", default=500, type=int,
                        help="maximum learning episodes"
                             "default values: 500")
    parser.add_argument("-ms", "--max_stps", default=100000, type=float,
                        help="maximum steps per episode"
                             "default values: 100000")
    parser.add_argument("-e", "--epsilon", default=0.1, type=float,
                        help="epsilon value to be used in epsilon-greedy method"
                             "default values: 0.1")
    parser.add_argument("-a", "--alpha", default=0.1, type=float,
                        help="learning step size"
                             "default values: 0.1")
    parser.add_argument("-d", "--decay", default='constant', choices=['constant','adaptive'],
                        type=str, help="learning step size decay mod"
                             "default values: constant")
    parser.add_argument("-g", "--gamma", default=1.0, type=float,
                        help="discount factor"
                             "default values: 1.0")
    parser.add_argument("-vt", "--visualT", action="store_true", default=True,
                        help="visualize the maze training training")
    parser.add_argument("--no-visualT", action="store_false", dest="visualT",
                        help="don't visualize the maze training")
    parser.add_argument("-ve", "--visualE", action="store_true", default=True,
                        help="visualize the maze evaluation")
    parser.add_argument("--no-visualE", action="store_false", dest="visualE",
                        help="don't visualize the maze evaluation training")
    parser.add_argument("-duq", "--dontuseQ", action="store_true", default=True,
                        help="don't use Q found from previous iterations")
    parser.add_argument("--useQ", action="store_false", dest="dontuseQ",
                        help="use Q found from previous iterations")
    parser.add_argument("-dst", "--dontskipT", action="store_true", default=True,
                        help="don't skip training Q")
    parser.add_argument("--skipTrain", action="store_false", dest="dontskipT",
                        help="skip training Q")
    args = parser.parse_args()
    assert args.epsilon <= 1 and args.epsilon > 0

    env = gym.make('maze-sample-10x10-v0')
    Q = initQ(args)
    if args.dontskipT:
        Q_learned, eps_reward = train_agent(args, env, Q)
        wr.write_np_arr(args, Q_learned, 'SARSA')
        wr.write_eps_reward(args, eps_reward, 'SARSA')
    else:
        Q_learned = Q
    eval_policy(args, env, Q_learned)
    print('The algorithm is done!')