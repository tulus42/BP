# from state_space import *
# from mrX import *

# stateSpace = StateSpaceClass()
# mrX = MrXClass()
#
# stateSpace.print_game()

import gym
import random
import numpy as np
from IPython.display import clear_output

env = gym.make("ScotlandYardMini-v0").env

env.render()

q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
all_penalties = []


#
#
def get_next_move(agent1, agent2, real_pos, seen_pos, seen_time):

    a1 = [agent1 % 5, agent1 // 5]
    a2 = [agent2 % 5, agent2 // 5]
    mrx = [real_pos % 5, real_pos // 5]
    
    possible_positions = [minimax_step(a1, a2, [mrx[0], mrx[1]+1], 0, False, 3), # UP
        minimax_step(a1, a2, [mrx[0], mrx[1]-1],  0, False, 3),                  # DOWN
        minimax_step(a1, a2, [mrx[0]+1, mrx[1]], 0, False, 3),                   # LEFT
        minimax_step(a1, a2, [mrx[0]-1, mrx[1]], 0, False, 3)]                   # RIGHT

    next_move = possible_positions.index(max(possible_positions))
    next_pos = real_pos + decode_move(next_move)

    seen_time = (seen_time + 1) % 3

    # every 3th move is mrX visible
    if seen_time == 0:
        seen_pos = next_pos

    return next_pos, seen_pos, seen_time


#
#
def minimax_step(a1, a2, mrx, depth, is_mrx, h):
    if out_of_range(a1) or out_of_range(a2) or out_of_range(mrx):
        return 100 if is_mrx else -100

    if a1 == mrx or a2 == mrx:
        return -100

    if depth == h:
        return max(get_distance(a1, mrx), get_distance(a2, mrx)) if is_mrx else min(get_distance(a1, mrx), get_distance(a2, mrx))

    if is_mrx:
        return max(minimax_step(a1, a2, [mrx[0]+1, mrx[1]], depth + 1, False, h),
                   minimax_step(a1, a2, [mrx[0]-1, mrx[1]], depth + 1, False, h),
                   minimax_step(a1, a2, [mrx[0], mrx[1]+1], depth + 1, False, h),
                   minimax_step(a1, a2, [mrx[0], mrx[1]-1], depth + 1, False, h))
    else:
        return min(minimax_step([a1[0]+1, a1[1]], a2, mrx, depth + 1, True, h),
                   minimax_step([a1[0]-1, a1[1]], a2, mrx, depth + 1, True, h),
                   minimax_step([a1[0], a1[1]+1], a2, mrx, depth + 1, True, h),
                   minimax_step([a1[0], a1[1]-1], a2, mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0]+1, a2[1]], mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0]-1, a2[1]], mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0], a2[1]+1], mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0], a2[1]-1], mrx, depth + 1, True, h))


#
#
def out_of_range(x):
    if x[0] < 0 or x[0] > 4 or x[1] < 0 or x[1] > 4:
        return True
    else:
        return False


#
#
def get_distance(a, mrx):
    x = abs(a[0] - mrx[0])
    y = abs(a[1] - mrx[1])
    return x + y


def decode_move(move):
    if move == 0:
        return 5
    elif move == 1:
        return -5
    elif move == 2:
        return 1
    else:
        return -1


##############
for i in range(1, 3):
    env.mrx_seen_pos = env.mrx_real_pos
    env.last_seen = 0

    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False

    

    while not done:
        # --------
        clear_output(wait=True)
        env.render()
        agent1, agent2, mrx_last_seen, seen = env.decode(state)
        print(agent1, agent2, mrx_last_seen)
        print("tu:", env.mrx_real_pos)
        # --------

        #env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
        env.mrx_real_pos += 1
        env.last_seen = (env.last_seen +1) %3
        state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)

        print("mrx: ", env.mrx_real_pos)

        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, info = env.step(action) 
        
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward == -10:
            penalties += 1

        # --------
        agent1, agent2, mrx_last_seen, seen = env.decode(next_state)
        # --------

        state = next_state

        # --------
        print("next: ", env.decode(next_state))
        # --------

        epochs += 1

    # --------
    env.render()
    agent1, agent2, mrx_last_seen, seen = env.decode(state)
    print(agent1, agent2, mrx_last_seen)
    print("END of epoch ----------------------------------------------")
    # --------

print("Training finished.\n")







"""int minimax(int depth, int nodeIndex, bool isMax, 
            int scores[], int h) 
{ 
    // Terminating condition. i.e 
    // leaf node is reached 
    if (depth == h) 
        return scores[nodeIndex]; 
  
    //  If current move is maximizer, 
    // find the maximum attainable 
    // value 
    if (isMax) 
       return max(minimax(depth+1, nodeIndex*2, false, scores, h), 
            minimax(depth+1, nodeIndex*2 + 1, false, scores, h)); 
  
    // Else (If current move is Minimizer), find the minimum 
    // attainable value 
    else
        return min(minimax(depth+1, nodeIndex*2, true, scores, h), 
            minimax(depth+1, nodeIndex*2 + 1, true, scores, h)); 
} """