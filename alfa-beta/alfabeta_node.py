class Node:
    def __init__(self, a1=0, a2=0, mrx=0, parrent = None, alfa = -9999, beta = 9999, depth = 0, turn = "A"):
        self.parrent = parrent      # reference to parrent node
        self.alfa = alfa            # alfa value
        self.beta = beta            # beta value
        self.best_way = None       # child node with best way 
        self.depth = depth          # depth in exploration/in tree
        self.turn = turn            # player A/player B
        self.children = []          # list of children nodes
        self.a1 = a1                # position of agent 1 in this node
        self.a2 = a2                # position of agent 2 in this node
        self.mrx = mrx              # position of mrX in this node
        self.number = 0             # order number of node

    def reset(self, turn="A"):
        self.parrent = None
        self.alfa = -9999
        self.beta = 9999
        self.best_way = None
        self.depth = 0
        self.turn = turn
        self.children = []
        self.a1 = 0
        self.a2 = 0
        self.mrx = 0