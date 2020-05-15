import numpy as np
import random
import sys
from six import StringIO
from contextlib import closing
import colorama
from colorama import Fore, Back, Style

MAP = [
    "+---------+",
    "| : : : : |",
    "| : : : : |",
    "| : : : : |",
    "| : : : : |",
    "| : : : : |",
    "+---------+",
]

class Environment:

    def __init__(self):
        self.num_states = 46875
        self.num_actions = 16

        num_states = self.num_states
        self.num_rows = 5
        self.num_columns = 5
        num_positions = self.num_rows*self.num_columns
        num_seen = 3
        num_actions = self.num_actions # 4*4 for each agent

        self.num_positions = num_positions
        self.actions = {state: {action: []
                        for action in range(num_actions)} for state in range(num_states)}
        self.q_table = np.zeros([self.num_states, self.num_actions])

        for agent1 in range(num_positions):
            for agent2 in range(num_positions):
                for mrx in range(num_positions):
                    for seen in range(num_seen):

                        state = self.encode(agent1, agent2, mrx, seen)

                        for action in range(num_actions):
                            # 
                            new_agent1, new_agent2 = agent1, agent2
                            reward = 0

                            ## Reward -100 -> invalid move ##

                            # agent1
                            # -> up
                            if action % 4 == 0:
                                if agent1 - 5 >= 0:
                                    new_agent1 = agent1 - 5
                            
                            # -> down
                            elif action % 4 == 1:
                                if agent1 + 5 <= 24:
                                    new_agent1 = agent1 + 5
                                 
                            # -> right
                            elif action % 4 == 2:
                                if (agent1 + 1) % 5 != 0:
                                    new_agent1 = agent1 + 1
                                 
                            # -> left
                            elif action % 4 == 3:
                                if (agent1 - 1) % 5 != 4:
                                    new_agent1 = agent1 - 1
                                

                            # agent2
                            tmp_action = action // 4
                            # -> up
                            if tmp_action == 0:
                                if agent2 - 5 >= 0:
                                    new_agent2 = agent2 - 5
                                
                            # -> down
                            elif tmp_action == 1:
                                if agent2 + 5 <= 24:
                                    new_agent2 = agent2 + 5
                                
                            # -> right
                            elif tmp_action == 2:
                                if (agent2 + 1) % 5 != 0:
                                    new_agent2 = agent2 + 1
                                
                            # -> left
                            elif tmp_action == 3:
                                if (agent2 - 1) % 5 != 4:
                                    new_agent2 = agent2 - 1
                
                            # if agent would make invalid move, he does not move ->
                            # if agent does not move, reward = -100 -> means invalid move
                            # invalid move:
                            if new_agent1 == agent1 or new_agent2 == agent2 or new_agent1 == new_agent2:
                                reward = -100
                            
                            
                            new_state = self.encode(new_agent1, new_agent2, mrx, seen)
                            self.actions[state][action] = (new_state, reward)
                            self.q_table[state, action] = reward * 1000


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

        while agent1 == agent2 or agent1 == mrx or agent2 == mrx:
            agent1 = random.randint(0, self.num_positions - 1)
            agent2 = random.randint(0, self.num_positions - 1)
            mrx = random.randint(0, self.num_positions - 1)

        state = self.encode(agent1, agent2, mrx, 0)

        # returns generated state and mr.Xs real position
        return state, mrx


    def render(self, state, mrx_real_pos, action=-1):
        colorama.init()
        cols = self.num_columns
        rows = self.num_rows

        agent1, agent2, mrx_seen_pos, mrx_seen_ago = self.decode(state)
        
        out_map = [[' '] * self.num_columns for i in range(self.num_rows)]


        out_map[agent1 // rows][agent1 % cols] = Fore.BLUE + '1' + Style.RESET_ALL
        out_map[agent2 // rows][agent2 % cols] = Fore.BLUE + '2' + Style.RESET_ALL

        if mrx_seen_ago == 0:
            out_map[mrx_seen_pos // rows][mrx_seen_pos % cols] = Back.GREEN + 'X' + Style.RESET_ALL
        elif mrx_seen_ago == 1:
            out_map[mrx_seen_pos // rows][mrx_seen_pos % cols] = Back.YELLOW + 'x' + Style.RESET_ALL
            out_map[mrx_real_pos // rows][mrx_real_pos % cols] = 'X'
        else:
            if mrx_real_pos != mrx_seen_pos:
                out_map[mrx_seen_pos // rows][mrx_seen_pos % cols] = Back.RED + 'x' + Style.RESET_ALL
                out_map[mrx_real_pos // rows][mrx_real_pos % cols] = 'X'
            else:
                out_map[mrx_seen_pos // rows][mrx_seen_pos % cols] = Back.RED + 'X' + Style.RESET_ALL

        if mrx_real_pos == agent1 or mrx_real_pos == agent2:
            out_map[mrx_real_pos // rows][mrx_real_pos % cols] = Back.BLUE + '=' + Style.RESET_ALL


        # outfile.write("\n".join(["".join(row) for row in out]) + "\n")

        out = ""

        print("+---------+")
        for row in range(len(out_map)):
            out = "|"

            for column in range(len(out_map[row])):
                if column == len(out_map[row]):
                    out += out_map[row][column] + '|'
                else:
                    out += out_map[row][column] + ':'

            print(out)
        print("+---------+")

        if action != -1:
            actions = ["UP,UP", "DOWN,UP", "RIGHT,UP", "LEFT,UP", 
            "UP,DOWN", "DOWN,DOWN", "RIGHT,DOWN", "LEFT,DOWN", 
            "UP,RIGHT", "DOWN,RIGHT", "RIGHT,RIGHT", "LEFT,RIGHT",
            "UP,LEFT", "DOWN,LEFT", "RIGHT,LEFT", "LEFT,LEFT"]
            print(actions[action])
