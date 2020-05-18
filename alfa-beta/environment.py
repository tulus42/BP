import random

class Environment:
    def __init__(self):
        self.mrx = 0
        self.agent1 = 0
        self.agent2 = 0
        self.epochs = 0
        self.alfabeta_moves = 0
        
        self.cols = 5
        self.rows = 5

        self.reset()
        
        

    def reset(self):
        positions = [x for x in range(25)]

        self.mrx = random.choice(positions)
        positions.remove(self.mrx)
        
        self.agent1 = random.choice(positions)
        positions.remove(self.agent1)

        self.agent2 = random.choice(positions)

        self.epochs = 0

        self.alfabeta_moves = 0
        
    def move_agents(self, alfabeta):
        if self.alfabeta_moves % 3 == 0:
            alfabeta.explore_state_space(self.agent1, self.agent2, self.mrx)
        
        self.agent1, self.agent2 = alfabeta.choose_new_move()

        self.alfabeta_moves = (self.alfabeta_moves + 1) % 3

    # check if game finished
    def finished(self):
        if (self.agent1 == self.mrx) or (self.agent2 == self.mrx):
            return True
        return False

    def render(self):
        cols = self.cols
        rows = self.rows

        out_map = [[' '] * cols for i in range(rows)]

        out_map[self.agent1 // rows][self.agent1 % cols] = "1"
        out_map[self.agent2 // rows][self.agent2 % cols] = "2"
        out_map[self.mrx // rows][self.mrx % cols] = "X"

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
        return False
    return position - 5

# DOWN
def go_down(position):
    if (position + 5) > 24:
        return False
    return position + 5

# LEFT
def go_left(position):
    if (position % 5) == 0:
        return False
    return position - 1

# RIGHT
def go_right(position):
    if ((position + 1) % 5) == 0:
        return False
    return position + 1

# returns list of new positions or False if invalid move
def get_valid_moves(position):
    up = go_up(position)
    down = go_down(position)
    left = go_left(position)
    right = go_right(position)

    return [up, down, left, right]

def get_valid_moves_agents(position1, position2):
    agent1 = get_valid_moves(position1)
    agent2 = get_valid_moves(position2)

    possible_positions = []

    for i1 in agent1:
        for i2 in agent2:
            if i1 == False or i2 == False or i1 == i2:
                possible_positions.append(False)
            else:
                possible_positions.append([i1, i2])

    return possible_positions


