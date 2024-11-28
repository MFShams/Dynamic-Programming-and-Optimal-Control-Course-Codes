# Author: Mojtaba AlShams
# Professional email: mojtaba.alshams@kaust.edu.sa
# Personal email: m.f.shams@hotmail.com
# This project github link: https://github.com/MFShams/Dynamic-Programming-and-Optimal-Control-Course-Codes/tree/main/HW2

import os
import numpy as np

def qSARSA_exist(args, file_name):
    folder = 'Qfiles/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    identifier = f'_max_epsds{args.max_epsds}_max_stps{args.max_stps}_epsilon{args.epsilon}_alpha{args.alpha}_decay{args.decay}'
    path = folder+file_name+identifier+'.npy'
    # print(path)
    return os.path.exists(path)

def write_np_arr(args, arr, file_name):
    identifier = f'_max_epsds{args.max_epsds}_max_stps{args.max_stps}_epsilon{args.epsilon}_alpha{args.alpha}_decay{args.decay}'
    path = 'Qfiles/Qnparr'+file_name+identifier
    np.save(path, arr)

def read_np_arr(args, file_name):
    identifier = f'_max_epsds{args.max_epsds}_max_stps{args.max_stps}_epsilon{args.epsilon}_alpha{args.alpha}_decay{args.decay}'
    path = 'Qfiles/'+file_name+identifier+'.npy'
    return np.load(path)

def write_eps_reward(args, arr, alg):
    folder = 'Qfiles/eps_reward/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    fname= f'{alg}_max_epsds{str(args.max_epsds)}_max_stps{str(args.max_stps)}_epsilon{str(args.epsilon)}_alpha{str(args.alpha)}_decay{args.decay}'
    path = folder+fname
    np.save(path, arr)