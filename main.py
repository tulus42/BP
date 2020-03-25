# from state_space import *
# from mrX import *

# stateSpace = StateSpaceClass()
# mrX = MrXClass()
#
# stateSpace.print_game()

import gym
import random
import matplotlib as plt
import matplotlib.style
import matplotlib.pyplot as plt
import numpy as np
import sys 
import time
from IPython.display import clear_output
import pickle

from collections import defaultdict 

import minimax


matplotlib.style.use('ggplot') 


class Timer():
    def __init__(self):
        self.init_time = time.time()
        self.actual_time = time.time()
        self.end_time = time.time()

    def get_time(self):
        self.actual_time = time.time()
        exec_time = self.actual_time - self.init_time

        return self.parse(exec_time)

    def get_estimated_time(self, i, max_i):
        self.actual_time = time.time()

        elapsed_time = self.actual_time - self.init_time
        
        if i == 0:
            return 0, 0
        else:
            estimated_time = (elapsed_time / i) * (max_i - i)

        return self.parse(estimated_time)

    def parse(self, time):
        mins = 0
        secs = 0
        if time > 60:
            mins = time / 60
            
        secs = time % 60

        mins = round(mins)
        secs = round(secs)

        return mins, secs


    def show(self):
        m, s = self.get_time()
        print("Execution time:", m, "mins", s, "s")


# Print iterations progress
def printProgressBar (iteration, total, timer, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    if (iteration % 10) == 0:
        mins, secs = timer.get_time()
        e_mins, e_secs = timer.get_estimated_time(iteration, total)
        clear_output(wait=False)
        print('\r%s |%s| %s%% %s\tElapsed: %dm %ds\tEstimated: %dm %ds' % (prefix, bar, percent, suffix, mins, secs, e_mins, e_secs), end = printEnd)
    else:
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

#
#



##############
# For showing progress
timer = Timer()

# environment
env = gym.make("ScotlandYardMini-v0").env

# with open('q_table', 'rb') as input:
#     q_table = pickle.load(input)

q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1


num_episodes = 10000
max_moves_in_episode = 20

# For plotting metrics
all_epochs = np.zeros(num_episodes)
all_penalties = np.zeros(num_episodes)
all_rewards = np.zeros(num_episodes)
all_learned_actions = np.zeros(num_episodes)



# Initial call to print 0% progress
printProgressBar(0, num_episodes, timer, prefix = 'Progress:', suffix = 'Complete', length = 50)



for i in range(1, num_episodes):
    

    state = env.reset()

    env.mrx_seen_pos = env.mrx_real_pos
    env.last_seen = 0

    epochs, penalties, reward, learned_action = 0, 0, 0, 0
    done = False

    

    while not done:

        ## Get valid moves - equivalent to: ##
        # for x in env.P[state]:
        #     if x.value[0][2] > -100:
        #         valid_moves.append(x.key)
        valid_moves = [key for key, value in env.P[state].items() if value[0][2] > -100]

        # x[0][2] for x in env.P[state].values()

        # choose next action
        if random.uniform(0, 1) < epsilon:
            # action = env.action_space.sample() # Explore action space
            
            # choose only from valid actions:
            action = random.choice(valid_moves)

        else:
            if np.sum(q_table[state]) > 0:
                action = np.argmax(q_table[state]) # Exploit learned values

                learned_action += 1
            else:
                # at the start choose only from valid moves
                action = random.choice(valid_moves)
            

        # find next state according to action
        next_state, reward, done, info = env.step(action) 

        agent1, agent2, mrx_last_seen, seen = env.decode(next_state)

        # if win
        if env.mrx_real_pos == agent1 or env.mrx_real_pos == agent2:
            reward = 20
            done = True

        else:
            ### change next state according to mrXs move
            env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = minimax.get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
            next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
            ###


            if epochs == max_moves_in_episode:
                reward = -10


        # TD update
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value



        if reward == -100:
            penalties += 1

        # Statistics
        all_epochs[i] = epochs
        all_penalties[i] = penalties
        all_rewards[i] += reward
        all_learned_actions[i] = learned_action

        if epochs == max_moves_in_episode:
            break

        # --------
        agent1, agent2, mrx_last_seen, seen = env.decode(next_state)
        # --------

        #### Choose next move for mrX and change
        # env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
        # next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
        ####


        state = next_state

        epochs += 1


    # Update Progress Bar
    printProgressBar(i + 1, num_episodes, timer, prefix = 'Progress:', suffix = 'Complete', length = 50)


    # 
    # percent.show(i, num_episodes, timer)
    # --------


print("Training finished.")
timer.show()


with open('q_table.pkl', 'wb') as output:
    pickle.dump(q_table, output, pickle.HIGHEST_PROTOCOL)


# # EXAMPLE GAME
# print("------ Example game: ------")
# state = env.reset()
# epochs, penalties, reward = 0, 0, 0

# env.render()

# done = False

# while not done:
#     action = np.argmax(q_table[state])
#     state, reward, done, info = env.step(action)

#     agent1, agent2, mrx_last_seen, seen = env.decode(next_state)


#     ### change next state according to mrXs move
#     env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = minimax.get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
#     state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
#     ###

#     env.render()

#     if reward == 20:
#         done = True


env.render()

while not done:
        
    # choose next action
    if random.uniform(0, 1) < epsilon:
        action = env.action_space.sample() # Explore action space
    else:
        action = np.argmax(q_table[state]) # Exploit learned values

    # find next state according to action
    next_state, reward, done, info = env.step(action) 

    agent1, agent2, mrx_last_seen, seen = env.decode(next_state)


    ### change next state according to mrXs move
    env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = minimax.get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
    next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
    ###


    if epochs == max_moves_in_episode:
        reward = -20



    # TD update
    old_value = q_table[state, action]
    next_max = np.max(q_table[next_state])
    
    new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
    q_table[state, action] = new_value



    if reward == -10:
        penalties += 1

    # Statistics
    all_epochs[i] = epochs
    all_penalties[i] = penalties
    all_rewards[i] += reward

    if epochs == max_moves_in_episode:
        break

    # --------
    agent1, agent2, mrx_last_seen, seen = env.decode(next_state)
    # --------

    # if done
    if agent1 == env.mrx_real_pos or agent2 == env.mrx_real_pos or reward >= 20:
        done = True
    else:
        done = False

        #### Choose next move for mrX and change
        # env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
        # next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
        ####


    state = next_state

    epochs += 1

    env.render()



# Plot statistics
fig, axs = plt.subplots(4, 1, constrained_layout=True)
axs[0].plot(all_epochs)
axs[0].set_title('Length of games')

axs[1].plot(all_penalties)
axs[1].set_title('Penalties')

axs[2].plot(all_rewards)
axs[2].set_title('Rewards')

axs[3].plot(all_learned_actions)
axs[3].set_title('Choose learned actions')

plt.show()
