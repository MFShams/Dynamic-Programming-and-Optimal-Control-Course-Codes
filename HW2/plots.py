# Author: Mojtaba AlShams
# Professional email: mojtaba.alshams@kaust.edu.sa
# Personal email: m.f.shams@hotmail.com
# This project github link: https://github.com/MFShams/Dynamic-Programming-and-Optimal-Control-Course-Codes/tree/main/HW2

import matplotlib.pyplot as plt
import argparse

import write_read as wr

# title, xlabel, ylabel, arr_list
def build_list_args(args):
    args.epsilons = [float(e.strip()) for e in args.epsilons.split(',')]
    args.alphas = [float(a.strip()) for a in args.alphas.split(',')]
    for alpha in args.alphas:
        assert alpha >= 0 and alpha <=1, alpha
    for epsilon in args.epsilons:
        assert epsilon > 0
    return args
def plot_mult_arr(fname, title, xlabel, ylabel, legends, arr_list, saveEN = True):
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.yscale('log')
    for arr in arr_list:
        plt.plot(arr)
    # plt.ylim(bottom=-2000)
    # plt.ylim(top=500)
    plt.xticks([1]+[i for i in range(50,arr.shape[0]+1,50)])
    plt.legend(legends)
    if saveEN:
        plt.savefig(f'Qfiles/plots/plot_{fname}.pdf')

def plot_SARSAvsQLearning(fname, title, xlabel, ylabel, legends, arr_list, saveEN = True):
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.yscale('log')
    for arr in arr_list:
        plt.plot(arr)
    # plt.ylim(bottom=-2000)
    # plt.ylim(top=10)
    plt.xticks([1]+[i for i in range(50,arr.shape[0]+1,50)])
    plt.legend(legends)
    if saveEN:
        plt.savefig(f'Qfiles/plots/plot_{fname}.pdf')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameters to run Q-Learning algorithm with epsilon-greedy method')
    parser.add_argument("-me", "--max_epsds", default=500, type=int,
                        help="maximum learning episodes"
                             "default values: 500")
    parser.add_argument("-ms", "--max_stps", default=100000, type=int,
                        help="maximum steps per episode"
                             "default values: 100000")
    parser.add_argument("-e", "--epsilons", default=0.1, type=str,
                        help="epsilon value to be used in epsilon-greedy method"
                             "default values: 0.1")
    parser.add_argument("-a", "--alphas", default=0.1, type=str,
                        help="learning step size"
                             "default values: 0.1")
    parser.add_argument("-alg", "--algorithm", choices=['SARSA','QLearning'],
                        type=str, help="The used algorithm")
    # parser.add_argument("-d", "--decay", default='constant', choices=['constant','adaptive'],
    #                     type=str, help="learning step size decay mod"
    #                          "default values: constant")
    args = parser.parse_args()
    args = build_list_args(args)

    title = f"Sum of Rewards at Each Episode Using {args.algorithm} algorithm"
    xlabel = "Episode"
    ylabel = "Rewards Sum"
    saveEN = True
    legends = []
    arr_list = []
    for epsilon in args.epsilons:
        args.epsilon = epsilon
        args.alpha = 0.1
        args.decay = 'constant'
        # arr_list.append(wr.read_np_arr(f'eps_reward/{args.algorithm}_max_epsds{args.max_epsds}_max_stps{args.max_stps}_epsilon{epsilone}_alpha0.1_decayconstant'))
        arr_list.append(wr.read_np_arr(args, 'eps_reward/'+args.algorithm))
        legends.append('eps='+str(epsilon))
    fname = f'{args.algorithm} sweep eps'
    plot_mult_arr(fname, title, xlabel, ylabel, legends, arr_list, saveEN)
    legends = []
    arr_list = []
    for alpha in args.alphas:
        args.epsilon = 0.1
        args.alpha = alpha
        args.decay = 'constant'
        # arr_list.append(wr.read_np_arr(f'eps_reward/{args.algorithm}_max_epsds{args.max_epsds}_max_stps{args.max_stps}_epsilon0.1_alpha{alpha}_decayconstant'))
        arr_list.append(wr.read_np_arr(args, 'eps_reward/'+args.algorithm))
        legends.append('alpha='+str(alpha))
    args.alpha = 0.1
    args.decay = 'adaptive'
    arr_list.append(wr.read_np_arr(args, 'eps_reward/'+args.algorithm))
    legends.append('adaptive (1/t)')
    fname = f'{args.algorithm} sweep alpha'
    plot_mult_arr(fname, title, xlabel, ylabel, legends, arr_list, saveEN)
    
    # title = f"Sum of Rewards at Each Episode For alpha=0.5,epsilon=0.1"
    # xlabel = "Episode"
    # ylabel = "Rewards Sum"
    # saveEN = True
    # legends = []
    # arr_list = []
    # args.epsilon = 0.1
    # args.alpha = 0.5
    # args.decay = 'constant'
    # # arr_list.append(wr.read_np_arr(f'eps_reward/{args.algorithm}_max_epsds{args.max_epsds}_max_stps{args.max_stps}_epsilon{epsilone}_alpha0.1_decayconstant'))
    # arr_list.append(wr.read_np_arr(args, 'eps_reward/'+'SARSA'))
    # arr_list.append(wr.read_np_arr(args, 'eps_reward/'+'QLearning'))
    # legends = ['SARSA', 'QLearning']
    # fname = 'SARSAvsQLearning'
    # plot_mult_arr(fname, title, xlabel, ylabel, legends, arr_list, saveEN)