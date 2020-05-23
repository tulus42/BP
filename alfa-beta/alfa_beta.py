import environment as env

class Node:
    def __init__(self, a1=0, a2=0, mrx=0, parrent = None, alfa = -9999, beta = 9999, depth = 0, turn = "A"):
        self.parrent = parrent
        self.alfa = alfa
        self.beta = beta
        self.depth = depth
        self.turn = turn
        self.children = []
        self.a1 = a1
        self.a2 = a2
        self.mrx = mrx
        self.number = 0

    def reset_root(self):
        self.parrent = None
        self.alfa = -9999
        self.beta = 9999
        self.depth = 0
        self.turn = "A"
        self.children = []
        self.a1 = 0
        self.a2 = 0
        self.mrx = 0


class AlfaBeta:
    def __init__(self):
        self.root = Node()
        self.evaluate = [0 for x in range(10000)]
        self.number = 0

    def choose_new_move_agents(self):
        children_alfa_values = []
        for child in self.root.children:
            children_alfa_values.append(child.beta)

        # get index of best branch
        new_move_index = children_alfa_values.index(self.root.alfa)
        # get new node
        new_move_node = self.root.children[new_move_index]

        self.root = new_move_node
    
        ## SHOW NEW POSITIONS OF AGENTS ##
        print("Agents:", [self.root.a1, self.root.a2])

        return self.root.a1, self.root.a2

    def choose_new_move_mrx(self):
        children_beta_values = []
        for child in self.root.children:
            children_beta_values.append(child.alfa)

        # get index of best branch
        new_move_index = children_beta_values.index(self.root.beta)
        # get new node
        new_move_node = self.root.children[new_move_index]

        self.root = new_move_node

        ## SHOW NEW POSITIONS OF AGENTS ##
        print("MrX:", self.root.mrx)

        return self.root.mrx


    def explore_state_space(self, a1, a2, mrx):
        self.root.reset_root()

        self.root.a1 = a1
        self.root.a2 = a2
        self.root.mrx = mrx

        valid_moves = env.get_valid_moves_agents(a1, a2)
        returned_values = []

        for move in valid_moves:
            if move != False:
                # create new Node as children
                self.root.children.append(Node(move[0], move[1], mrx, parrent=self.root, alfa=self.root.alfa, beta=self.root.beta, depth=0, turn="B"))
                # make alfa-beta step with the last added child
                result = self.make_alfabeta_step(self.root.children[-1])
                returned_values.append(result)

                self.root.alfa = max(returned_values)


    def make_alfabeta_step(self, node):
        # if node.depth == 0 and node.turn == "B":
        #     print("-----------------------------------")
        # print("SEND")
        # print("[{}, {}], depth={}, turn={}".format(node.a1, node.a2, node.depth, node.turn))
        # print("a =", node.alfa, "b =", node.beta)
        # print("")
        #########
        self.number += 1
        node.number = self.number

        # print("Node:", node.number)
        # print("parrent:", node.parrent.number)
        # print("a =", node.alfa, "b =", node.beta)
        # print("")
        #########


        if node.depth == 3 and node.turn == "A":
            node.alfa = self.evaluate_state(node)

            #########
            # print("Node:", node.number, "RETURNS", node.alfa)
            # print("parrent:", node.parrent.number)
            # print("a =", node.alfa, "b =", node.beta)
            # print("")
            #########

            return node.alfa

        if node.turn == "A":
            res = self.player_A(node)
            #########
            # print("Node:", node.number, "RETURNS", res)
            # print("parrent:", node.parrent.number)
            # print("a =", node.alfa, "b =", node.beta)
            # print("")
            #########
            return res
        else:
            res = self.player_B(node)
            #########
            # print("Node:", node.number, "RETURNS", res)
            # print("parrent:", node.parrent.number)
            # print("a =", node.alfa, "b =", node.beta)
            # print("")
            #########
            return res


    def player_A(self, node):
        
        valid_moves = env.get_valid_moves_agents(node.a1, node.a2)
        returned_values = []

        for move in valid_moves:
            if node.alfa < node.beta:
                if move != False:
                    node.children.append(Node(move[0], move[1], node.mrx, parrent=node, alfa=node.alfa, beta=node.beta, depth=node.depth, turn="B"))
                    node_result = self.make_alfabeta_step(node.children[-1])
                    returned_values.append(node_result)
        
                    if max(returned_values) > node.alfa:
                        node.alfa = max(returned_values)
                    
            else:
                break
            
        # print("RETURN")
        # print("[{}, {}], depth={}, turn={}".format(node.a1, node.a2, node.depth, node.turn))
        # print("a =", node.alfa, "b =", node.beta)
        # print("A", node.alfa)
        # print("")
        
        return node.alfa

    def player_B(self, node):
        
        valid_moves = env.get_valid_moves_mrx(node.mrx, node.a1, node.a2)
        returned_values = []

        for move in valid_moves:
            if node.alfa < node.beta:
                if move != False:
                    node.children.append(Node(node.a1, node.a2, move, parrent=node, alfa=node.alfa, beta=node.beta, depth=node.depth + 1, turn="A"))
                    node_result = self.make_alfabeta_step(node.children[-1])
                    returned_values.append(node_result)

                    if min(returned_values) < node.beta:
                        node.beta = min(returned_values)

            else:
                break

        # print("RETURN")            
        # print("[{}, {}], depth={}, turn={}".format(node.a1, node.a2, node.depth, node.turn))
        # print("a =", node.alfa, "b =", node.beta)
        # print("B", node.beta)
        # print("")
        return node.beta

    def evaluate_state(self, evalated_node):
        finished = False
        node = evalated_node
        value = 0
        while not finished:
            if node == self.root:
                finished = True

            # for every posible chatch during this branch is state
            if node.mrx == node.a1 or node.mrx == node.a2:
                value += node.depth * 50
            else:
                value -= self.evaluate_distance(node.mrx, node.a1)
                value -= self.evaluate_distance(node.mrx, node.a2) 
            
            node = node.parrent


        return value

    def evaluate_distance(self, pos1, pos2):
        p1x = pos1 % 5
        p1y = pos1 // 5

        p2x = pos2 % 5
        p2y = pos2 // 5

        distance = abs(p1x - p2x) + abs(p1y - p2y)

        return distance