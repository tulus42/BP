import gym
import random
import matplotlib as plt
import matplotlib.style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import time
from IPython.display import clear_output
import pickle

from collections import defaultdict 

import minimax

# environment
env = gym.make("ScotlandYardMini-v0").env



# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

with open('/home/adrian/skola/bc/q_table.pkl', 'rb') as input:
    q_table = pickle.load(input)

# EXAMPLE GAME
print("------ Example game: ------")
state = env.reset()

env.mrx_seen_pos = env.mrx_real_pos
env.last_seen = 0

epochs, penalties, reward, = 0, 0, 0
done = False

env.render

while not done:
    action = np.argmax(q_table[state])
    
    # find next state according to action
    next_state, reward, done, info = env.step(action) 

    agent1, agent2, mrx_last_seen, seen = env.decode(next_state)


    ### change next state according to mrXs move
    env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = minimax.get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
    next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
    ###

    env.render()

    # if done
    if agent1 == env.mrx_real_pos or agent2 == env.mrx_real_pos or reward == 20:
        done = True
    else:
        done = False

    state = next_state

    epochs += 1

    if epochs == 20:
        print("FAIL")
        break
