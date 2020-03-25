# from state_space import *
# from mrX import *

# stateSpace = StateSpaceClass()
# mrX = MrXClass()
#
# stateSpace.print_game()

import random
import matplotlib as plt
import matplotlib.style
import matplotlib.pyplot as plt
import numpy as np
import sys 
import pickle

from collections import defaultdict 

# import own files
import minimax
import environment as envr
import timer as tm
import progress_bar


matplotlib.style.use('ggplot') 



# Reward table
environment = envr.Environment()

# with open('q_table', 'rb') as input:
#     q_table = pickle.load(input)

q_table = np.zeros([environment.num_states, environment.num_actions])



# TODO dopisat licenciu
# https://gist.github.com/kastnerkyle/d127197dcfdd8fb888c2
def update_q_table(state, next_state, action, reward, alpha, gamma):
    old_q_value = q_table[state, action]
    next_max = np.max(q_table[next_state])

    new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)
    q_table[state, action] = new_q_value

    # renormalize row to be between 0 and 1
    rn = q_table[state][q_table[state] > 0] / np.sum(q_table[state][q_table[state] > 0])
    q_table[state][q_table[state] > 0] = rn




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


##############
# For showing progress
timer = tm.Timer()
# Initial call to print 0% progress
progress_bar.show(0, num_episodes, timer, prefix = 'Progress:', suffix = 'Complete', length = 50)


mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago = 0, 0, 0



for i in range(1, num_episodes):
    

    state, mrx_real_pos = environment.reset()

    epochs, penalties, reward, learned_action = 0, 0, 0, 0
    done = False

    

    while not done:

        x = environment.actions[state]
        ## Get valid moves - number of valid actions
        valid_moves = [key for key, value in environment.actions[state].items() if value[1] > - 100]

        # choose next action
        if random.uniform(0, 1) < epsilon:
            # choose only from valid actions:
            action = random.choice(valid_moves)     # Explore action space

        else:
            # if np.sum(q_table[state]) > 0:
            #     action = np.argmax(q_table[state]) # Exploit learned values

            #     learned_action += 1
            # else:
            #     # at the start choose only from valid moves
            #     action = random.choice(valid_moves)
            
            action = np.argmax(q_table[state])


        # find next state according to action
        next_state = environment.actions[state][action][0]


        agent1, agent2, _, _ = environment.decode(next_state)
        # if win
        if mrx_real_pos == agent1 or mrx_real_pos == agent2:
            reward = 20
            done = True
        else:
            reward = -1

            ### change next state according to mrXs move ###
            mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago = minimax.get_next_move(agent1, agent2, mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago)

            next_state = environment.encode(agent1, agent2, mrx_last_seen_pos, mrx_seen_ago)
            ###


            if epochs == max_moves_in_episode:
                reward = -10
                done = True


        # Q-table update
        update_q_table(state, next_state, action, reward, alpha, gamma)
        
        state = next_state
       


        # Statistics
        all_epochs[i] = epochs
        all_penalties[i] = penalties
        all_rewards[i] += reward
        all_learned_actions[i] = learned_action
     

        

        epochs += 1


    # Update Progress Bar
    progress_bar.show(i + 1, num_episodes, timer, prefix = 'Progress:', suffix = 'Complete', length = 50)


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


# env.render()

# while not done:
        
#     # choose next action
#     if random.uniform(0, 1) < epsilon:
#         action = env.action_space.sample() # Explore action space
#     else:
#         action = np.argmax(q_table[state]) # Exploit learned values

#     # find next state according to action
#     next_state, reward, done, info = env.step(action) 

#     agent1, agent2, mrx_last_seen, seen = env.decode(next_state)


#     ### change next state according to mrXs move
#     env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = minimax.get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
#     next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
#     ###


#     if epochs == max_moves_in_episode:
#         reward = -20



#     # TD update
#     old_value = q_table[state, action]
#     next_max = np.max(q_table[next_state])
    
#     new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
#     q_table[state, action] = new_value



#     if reward == -10:
#         penalties += 1

#     # Statistics
#     all_epochs[i] = epochs
#     all_penalties[i] = penalties
#     all_rewards[i] += reward

#     if epochs == max_moves_in_episode:
#         break

#     # --------
#     agent1, agent2, mrx_last_seen, seen = env.decode(next_state)
#     # --------

#     # if done
#     if agent1 == env.mrx_real_pos or agent2 == env.mrx_real_pos or reward >= 20:
#         done = True
#     else:
#         done = False

#         #### Choose next move for mrX and change
#         # env.mrx_real_pos, env.mrx_seen_pos, env.last_seen = get_next_move(agent1, agent2, env.mrx_real_pos, env.mrx_seen_pos, env.last_seen)
#         # next_state = env.encode(agent1, agent2, env.mrx_seen_pos, env.last_seen)
#         ####


#     state = next_state

#     epochs += 1

#     env.render()



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
