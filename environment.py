import numpy as np
import random

class Environment:

    def __init__(self):
        self.num_states = 46875
        self.num_actions = 16

        num_states = self.num_states
        num_rows = 5
        num_columns = 5
        num_positions = num_rows*num_columns
        num_seen = 3
        num_actions = self.num_actions # 4*4 for each agent

        self.num_positions = num_positions
        self.actions = {state: {action: []
                        for action in range(num_actions)} for state in range(num_states)}

        for agent1 in range(num_positions):
            for agent2 in range(num_positions):
                for mrx in range(num_positions):
                    for seen in range(num_seen):

                        state = self.encode(agent1, agent2, mrx, seen)

                        for action in range(num_actions):
                            # defaults
                            new_agent1, new_agent2 = agent1, agent2
                            reward = -1 # default reward when there is no pickup/dropoff

                            ## Reward -100 -> invalid move ##

                            # agent1
                            # -> up
                            if action % 4 == 0:
                                if agent1 - 5 >= 0:
                                    new_agent1 = agent1 - 5
                                else:
                                    reward = -100
                            # -> down
                            elif action % 4 == 1:
                                if agent1 + 5 <= 24:
                                    new_agent1 = agent1 + 5
                                else:
                                    reward = -100    
                            # -> right
                            elif action % 4 == 2:
                                if (agent1 + 1) % 5 != 0:
                                    new_agent1 = agent1 + 1
                                else:
                                    reward = -100    
                            # -> left
                            elif action % 4 == 3:
                                if (agent1 - 1) % 5 != 4:
                                    new_agent1 = agent1 - 1
                                else:
                                    reward = -100

                            # agent2
                            tmp_action = action // 4
                            # -> up
                            if tmp_action == 0:
                                if agent2 - 5 >= 0:
                                    new_agent2 = agent2 - 5
                                else:
                                    reward = -100
                            # -> down
                            elif tmp_action == 1:
                                if agent2 + 5 <= 24:
                                    new_agent2 = agent2 + 5
                                else:
                                    reward = -100
                            # -> right
                            elif tmp_action == 2:
                                if (agent2 + 1) % 5 != 0:
                                    new_agent2 = agent2 + 1
                                else:
                                    reward = -100
                            # -> left
                            elif tmp_action == 3:
                                if (agent2 - 1) % 5 != 4:
                                    new_agent2 = agent2 - 1
                                else:
                                    reward = -100
                

                            # invalid move
                            if new_agent1 == agent1 or new_agent2 == agent2 or new_agent1 == new_agent2:
                                reward = -100
                            
                            
                            new_state = self.encode(new_agent1, new_agent2, mrx, seen)
                            self.actions[state][action] = (new_state, reward)


    def encode(self, a1, a2, mrx, seen):
        state = a1 + 25*a2 + 25*25*mrx + 25*25*25*seen
        return state

    def decode(self, i):
        # agent1
        agent1 = i % 25
        i = i // 25
        # agent2
        agent2 = i % 25
        i = i // 25
        # mrX
        mrx = i % 25
        i = i // 25
        # seen
        seen = i
        assert 0 <= i < 3
        return agent1, agent2, mrx, seen

    def reset(self):
        agent1 = random.randint(0, self.num_positions - 1)
        agent2 = random.randint(0, self.num_positions - 1)
        mrx = random.randint(0, self.num_positions - 1)

        state = self.encode(agent1, agent2, mrx, 0)

        # returns generated state and mr.Xs real position
        return state, mrx