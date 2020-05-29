import random
import sys
import player_input

class Environment:
    def __init__(self):
        self.mrx = 1
        self.mrx_last_seen = -1
        self.agent1 = 3
        self.agent2 = 7
        self.epochs = 0
        self.alfabeta_moves = 0
        
        self.cols = 5
        self.rows = 5

        self.reset()
        
        

    def reset(self):
        positions = [x for x in range(25)]

        self.mrx_last_seen = -1

        self.mrx = random.choice(positions)
        positions.remove(self.mrx)
        
        self.agent1 = random.choice(positions)
        positions.remove(self.agent1)

        self.agent2 = random.choice(positions)

        self.epochs = 0

        self.alfabeta_moves = 0
        
    def move_agents(self, alfabeta):
        # every 3th move explore state space with new information about Mr.X
        if self.alfabeta_moves % 3 == 0:
            alfabeta.explore_state_space(self.agent1, self.agent2, self.mrx)
        
        self.agent1, self.agent2 = alfabeta.choose_new_move_agents()
    
        self.alfabeta_moves = (self.alfabeta_moves + 1) % 3

    

    def move_mrx(self, alfabeta):
        new_mrx_position = alfabeta.move_mrx(self.agent1, self.agent2, self.mrx)   # AI vs AI
        # new_mrx_position = player_input.handle_input(self.mrx, self.agent1, self.agent2)        # AI vs player

        if new_mrx_position == -1:
            return False
        self.mrx = new_mrx_position

        if self.alfabeta_moves % 3 == 0:
            self.mrx_last_seen = self.mrx

        return True


        



    # check if game finished
    def finished(self):
        if (self.agent1 == self.mrx) or (self.agent2 == self.mrx):
            return True
        return False

    def render(self):
        cols = self.cols
        rows = self.rows

        out_map = [[' '] * cols for i in range(rows)]

        if self.mrx_last_seen != -1:
            out_map[self.mrx_last_seen // rows][self.mrx_last_seen % cols] = "-"
        out_map[self.mrx // rows][self.mrx % cols] = "X"
        out_map[self.agent1 // rows][self.agent1 % cols] = "1"
        out_map[self.agent2 // rows][self.agent2 % cols] = "2"
        

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

        return


# methods for movement #
# UP
def go_up(position):
    if (position - 5) < 0:
        return -1
    return position - 5

# DOWN
def go_down(position):
    if (position + 5) > 24:
        return -1
    return position + 5

# LEFT
def go_left(position):
    if (position % 5) == 0:
        return -1
    return position - 1

# RIGHT
def go_right(position):
    if ((position + 1) % 5) == 0:
        return -1
    return position + 1

# returns list of new positions or -1 if invalid move
def get_valid_moves(position):
    up = go_up(position)
    down = go_down(position)
    left = go_left(position)
    right = go_right(position)

    return [up, down, left, right]

# returns valid moves according to environment - not according to agents
def get_valid_moves_mrx_vs_player(mrx):
    valid_in_env = get_valid_moves(mrx)
    valid_moves = []

    for move in valid_in_env:
        if move != -1:
            valid_moves.append(move)

    return valid_moves

# returns valid moves according to environment and to agents
def get_valid_moves_mrx(mrx, a1, a2):
    valid_in_env = get_valid_moves(mrx)
    valid_moves = []

    for move in valid_in_env:
        if move != a1 and move != a2 and move != -1:
            valid_moves.append(move)

    return valid_moves

def get_valid_moves_agents(position1, position2):
    agent1 = get_valid_moves(position1)
    agent2 = get_valid_moves(position2)

    possible_positions = []

    for i1 in agent1:
        for i2 in agent2:
            if i1 != -1 and i2 != -1 and i1 != i2:
                possible_positions.append([i1, i2])

    return possible_positions


