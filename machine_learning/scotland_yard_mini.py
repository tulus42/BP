import sys
from contextlib import closing
from six import StringIO
from gym import utils
from gym.envs.toy_text import discrete
import numpy as np
import random

MAP = [
    "+---------+",
    "| : : : : |",
    "| : : : : |",
    "| : : : : |",
    "| : : : : |",
    "| : : : : |",
    "+---------+",
]


class ScotlandYardMiniEnv(discrete.DiscreteEnv):
    """
    The Taxi Problem
    from "Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition"
    by Tom Dietterich
    Description:
    There are four designated locations in the grid world indicated by R(ed), G(reen), Y(ellow), and B(lue). When the episode starts, the taxi starts off at a random square and the passenger is at a random location. The taxi drives to the passenger's location, picks up the passenger, drives to the passenger's destination (another one of the four specified locations), and then drops off the passenger. Once the passenger is dropped off, the episode ends.
    Observations: 
    There are 500 discrete states since there are 25 taxi positions, 5 possible locations of the passenger (including the case when the passenger is in the taxi), and 4 destination locations. 
    
    Passenger locations:
    - 0: R(ed)
    - 1: G(reen)
    - 2: Y(ellow)
    - 3: B(lue)
    - 4: in taxi
    
    Destinations:
    - 0: R(ed)
    - 1: G(reen)
    - 2: Y(ellow)
    - 3: B(lue)
        
    Actions:
    There are 6 discrete deterministic actions:
    - 0: move south
    - 1: move north
    - 2: move east 
    - 3: move west 
    - 4: pickup passenger
    - 5: dropoff passenger
    
    Rewards: 
    There is a reward of -1 for each action and an additional reward of +20 for delivering the passenger. There is a reward of -10 for executing actions "pickup" and "dropoff" illegally.
    
    Rendering:
    - blue: passenger
    - magenta: destination
    - yellow: empty taxi
    - green: full taxi
    - other letters (R, G, Y and B): locations for passengers and destinations
    
    state space is represented by:
        (taxi_row, taxi_col, passenger_location, destination)
    """
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self):
        self.desc = np.asarray(MAP, dtype='c')
        self.mrx_real_pos = random.randint(0,24)
        self.mrx_seen_pos = self.mrx_real_pos
        self.last_seen = 0

        num_states = 46875
        num_rows = 5
        num_columns = 5
        num_positions = num_rows*num_columns
        num_seen = 3
        initial_state_distrib = np.zeros(num_states)
        num_actions = 16 # 4*4 for each agent
        P = {state: {action: []
                     for action in range(num_actions)} for state in range(num_states)}
        for agent1 in range (num_positions):
            for agent2 in range (num_positions):
                for mrx in range(num_positions):
                    self.mrx_seen_pos = mrx

                    for seen in range(num_seen):
                        self.last_seen = seen

                        state = self.encode(agent1, agent2, self.mrx_seen_pos, self.last_seen)
                        
                        # ??????
                        if agent1 != self.mrx_real_pos or agent2 != self.mrx_real_pos:
                            initial_state_distrib[state] += 1
                        # ??????

                        for action in range(num_actions):
                            # defaults
                            new_agent1, new_agent2 = agent1, agent2
                            reward = -1 # default reward when there is no pickup/dropoff
                            done = False

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
                           
                            
                            new_state = self.encode(new_agent1, new_agent2, self.mrx_seen_pos, self.last_seen)
                            P[state][action].append((1.0, new_state, reward, done))

        initial_state_distrib /= initial_state_distrib.sum()
        discrete.DiscreteEnv.__init__(
            self, num_states, num_actions, P, initial_state_distrib)

    def encode(self, a1, a2, mrx, seen):
        st = a1 + 25*a2 + 25*25*mrx + 25*25*25*seen
        return st

    def decode(self, i):
        out = []
        # agent1
        out.append(i % 25)
        i = i // 25
        # agent2
        out.append(i % 25)
        i = i // 25
        # mrX
        out.append(i % 25)
        i = i // 25
        # seen
        out.append(i)
        assert 0 <= i < 3
        return out

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        out = self.desc.copy().tolist()
        out = [[c.decode('utf-8') for c in line] for line in out]
        agent1, agent2, mrx, seen = self.decode(self.s)


        out[1 + agent1 // 5][1 + 2 * (agent1 % 5)] = utils.colorize(out[1 + agent1 // 5][1 + 2 * (agent1 % 5)], 'yellow', highlight=True)
        out[1 + agent2 // 5][1 + 2 * (agent2 % 5)] = utils.colorize(out[1 + agent2 // 5][1 + 2 * (agent2 % 5)], 'yellow', highlight=True)

        if self.last_seen == 0:
            self.mrx_seen_pos = self.mrx_real_pos
            out[1 + self.mrx_seen_pos // 5][1 + 2 * (self.mrx_seen_pos % 5)] = utils.colorize(out[1 + self.mrx_seen_pos // 5][1 + 2 * (self.mrx_seen_pos % 5)], 'green', highlight=True)
        elif self.last_seen == 1:
            out[1 + self.mrx_seen_pos // 5][1 + 2 * (self.mrx_seen_pos % 5)] = utils.colorize(out[1 + self.mrx_seen_pos // 5][1 + 2 * (self.mrx_seen_pos % 5)], 'magenta', highlight=True)
        else:
            out[1 + self.mrx_seen_pos // 5][1 + 2 * (self.mrx_seen_pos % 5)] = utils.colorize(out[1 + self.mrx_seen_pos // 5][1 + 2 * (self.mrx_seen_pos % 5)], 'red', highlight=True)


        outfile.write("\n".join(["".join(row) for row in out]) + "\n")
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["UP,UP", "DOWN,UP", "RIGHT,UP", "LEFT,UP", 
            "UP,DOWN", "DOWN,DOWN", "RIGHT,DOWN", "LEFT,DOWN", 
            "UP,RIGHT", "DOWN,RIGHT", "RIGHT,RIGHT", "LEFT,RIGHT",
            "UP,LEFT", "DOWN,LEFT", "RIGHT,LEFT", "LEFT,LEFT"][self.lastaction]))
        else: outfile.write("\n")

        # No need to return anything for human
        if mode != 'human':
            with closing(outfile):
                return outfile.getvalue()


    """def get_next_move(self, agent1, agent2):

        a1 = [agent1 % 5, agent1 // 5]
        a2 = [agent2 % 5, agent2 // 5]
        mrx = [self.mrx_real_pos % 5, self.mrx_real_pos // 5]
        
        possible_positions = [self.minimax_step(a1, a2, [mrx[0], mrx[1]-1], 0, False, 3), # UP
            self.minimax_step(a1, a2, [mrx[0], mrx[1]+1],  0, False, 3),                  # DOWN
            self.minimax_step(a1, a2, [mrx[0]-1, mrx[1]], 0, False, 3),                   # LEFT
            self.minimax_step(a1, a2, [mrx[0]+1, mrx[1]], 0, False, 3)]                   # RIGHT

        next_move = possible_positions.index(max(possible_positions))
        self.mrx_real_pos = self.mrx_real_pos + self.decode_move(next_move)

        self.last_seen = (self.last_seen + 1) % 3

        # every 3th move is mrX visible
        if self.last_seen == 0:
            self.mrx_seen_pos = self.mrx_real_pos

    
    def minimax_step(self, a1, a2, mrx, depth, is_mrx, h):
        if self.out_of_range(a1) or self.out_of_range(a2) or self.out_of_range(mrx):
            return 200 if is_mrx else -200

        if a1 == mrx or a2 == mrx:
            return -100

        if depth == h:
            return max(self.get_distance(a1, mrx), self.get_distance(a2, mrx)) if is_mrx else min(self.get_distance(a1, mrx), self.get_distance(a2, mrx))

        if is_mrx:
            return max(self.minimax_step(a1, a2, [mrx[0]+1, mrx[1]], depth + 1, False, h),
                    self.minimax_step(a1, a2, [mrx[0]-1, mrx[1]], depth + 1, False, h),
                    self.minimax_step(a1, a2, [mrx[0], mrx[1]+1], depth + 1, False, h),
                    self.minimax_step(a1, a2, [mrx[0], mrx[1]-1], depth + 1, False, h))
        else:
            return min(self.minimax_step([a1[0]+1, a1[1]], a2, mrx, depth + 1, True, h),
                    self.minimax_step([a1[0]-1, a1[1]], a2, mrx, depth + 1, True, h),
                    self.minimax_step([a1[0], a1[1]+1], a2, mrx, depth + 1, True, h),
                    self.minimax_step([a1[0], a1[1]-1], a2, mrx, depth + 1, True, h),
                    self.minimax_step(a1, [a2[0]+1, a2[1]], mrx, depth + 1, True, h),
                    self.minimax_step(a1, [a2[0]-1, a2[1]], mrx, depth + 1, True, h),
                    self.minimax_step(a1, [a2[0], a2[1]+1], mrx, depth + 1, True, h),
                    self.minimax_step(a1, [a2[0], a2[1]-1], mrx, depth + 1, True, h))


    def out_of_range(self, x):
        if x[0] < 0 or x[0] > 4 or x[1] < 0 or x[1] > 4:
            return True
        else:
            return False

    
    def get_distance(self, a, mrx):
        x = abs(a[0] - mrx[0])
        y = abs(a[1] - mrx[1])
        return x + y

    def decode_move(self, move):
        if move == 0:
            return -5
        elif move == 1:
            return 5
        elif move == 2:
            return -1
        else:
            return 1"""