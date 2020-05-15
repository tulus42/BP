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



# environment conains action_space and states received after aplying action
environment = envr.Environment()

q_table = environment.q_table

# TODO - load Q-table - does not work ####
# with open('q_table', 'rb') as input:
#     q_table = pickle.load(input)


# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

################################################
#### HERE YOU CAN CHANGE LENGTH OF TRAINING ####
################################################ 
num_episodes = 2000000
max_moves_in_episode = 20
prints = False


################################################
#### REWARDS                                ####
################################################
win_reward = 50
loose_reward = -10
standard_reward = -1

# For plotting metrics
all_epochs = np.zeros(num_episodes)
all_penalties = np.zeros(num_episodes)
all_rewards = np.zeros(num_episodes)
all_learned_actions = np.zeros(num_episodes)


######################
# For showing progress
timer = tm.Timer()
# Initial call to print 0% progress
progress_bar.show(0, num_episodes, timer, prefix = 'Progress:', suffix = 'Complete', length = 50)




################################################
#### START OF TRAINING                      ####
################################################
mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago = 0, 0, 0

for i in range(1, num_episodes):


    state, mrx_real_pos = environment.reset()
    mrx_last_seen_pos = mrx_real_pos

    epochs, penalties, reward, learned_action = 0, 0, 0, 0
    done = False

    if prints:
        environment.render(state, mrx_real_pos)

    while not done:

        # x = [x for x in q_table[state] if x > -100000]
        # x = [x for x in range(len(q_table[state])) if q_table[state][x] > -100000]

        ## Get valid moves - number of valid actions
        valid_moves = [key for key, value in environment.actions[state].items() if value[1] > - 100]

        # choose next action
        if random.uniform(0, 1) < epsilon:
            # choose only from valid actions:
            action = random.choice(valid_moves)     # Explore action space

        else:
            # valid_moves_values = [x for x in q_table[state] if x > -100000]
            # if np.sum(valid_moves_values) > 0:   # TODO not sure about this value - may cause problems when rewards are not set well
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
            reward = win_reward
            done = True
        else:
            reward = standard_reward

            ### change next state according to mrXs move ###
            mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago = minimax.get_next_move(agent1, agent2, mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago)

            next_state = environment.encode(agent1, agent2, mrx_last_seen_pos, mrx_seen_ago)
            ###


            if epochs == max_moves_in_episode:
                reward = loose_reward
                done = True


        # Q-table update
        update_q_table(state, next_state, action, reward, alpha, gamma)
        
        state = next_state
        epochs += 1


        # Statistics
        all_epochs[i] = epochs
        all_penalties[i] = penalties
        all_rewards[i] += reward
        all_learned_actions[i] = learned_action
     
        if prints:
            environment.render(state, mrx_real_pos, action=action)
            res = "Epochs"
            res += str(epochs)
            input(res)


    # Update Progress Bar
    progress_bar.show(i + 1, num_episodes, timer, prefix = 'Progress:', suffix = 'Complete', length = 50)



print("Training finished.")
timer.show()
################################################
#### END OF TRAINING                        ####
################################################


# TODO - save Q-table - does not work
with open('q_table.pkl', 'wb') as output:
    pickle.dump(q_table, output, pickle.HIGHEST_PROTOCOL)





################################################
#### EXAMPLE GAME                           ####
################################################

agent1, agent2, mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago, epochs = 0, 0, 0, 0, 0, 0

state, mrx_real_pos = environment.reset()
mrx_last_seen_pos = mrx_real_pos


done = False

environment.render(state, mrx_real_pos)

while not done:

    # find next action
    action = np.argmax(q_table[state])

    # find next state according to action
    next_state = environment.actions[state][action][0]


    agent1, agent2, _, _ = environment.decode(next_state)
    # if win
    if mrx_real_pos == agent1 or mrx_real_pos == agent2:
        done = True
    else:
        ### change next state according to mrXs move ###
        mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago = minimax.get_next_move(agent1, agent2, mrx_real_pos, mrx_last_seen_pos, mrx_seen_ago)

        next_state = environment.encode(agent1, agent2, mrx_last_seen_pos, mrx_seen_ago)
        ###

        if epochs == max_moves_in_episode:
            done = True
            print("LOOSE")

    

    
    state = next_state

    environment.render(state, mrx_real_pos)
    epochs += 1






# Plot statistics
fig, axs = plt.subplots(3, 1, constrained_layout=True)
axs[0].plot(all_epochs)
axs[0].set_title('Length of games')

axs[1].plot(all_rewards)
axs[1].set_title('Rewards')

axs[2].plot(all_learned_actions)
axs[2].set_title('Choose learned actions')

plt.show()
