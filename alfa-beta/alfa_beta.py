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

    def explore_state_space(self, a1, a2, mrx):
        self.root.reset_root()

        self.root.a1 = a1
        self.root.a2 = a2
        self.root.mrx = mrx

        valid_moves = env.get_valid_moves_agents(a1, a2)
        
        for move in valid_moves:
            if move != False:
                # create new Node as children
                self.root.children.append(Node(move[0], move[1], mrx, parrent=self.root, alfa=self.root.alfa, beta=self.root.beta, depth=0, turn="B"))
                # make alfa-beta step with the last added child
                result = self.make_alfabeta_step(self.root.children[-1])
                if result > self.root.alfa:
                    self.root.alfa = result
                
    def choose_new_move(self):
        children_alfa_values = []
        for child in self.root.children:
            children_alfa_values.append(child.alfa)
        # get index of best branch
        new_move_index = children_alfa_values.index(self.root.alfa)
        # get new node
        new_move_node = self.root.children[new_move_index]

        self.root = new_move_node
    
        ## SHOW NEW POSITIONS OF AGENTS ##
        print([self.root.a1, self.root.a2])

        return self.root.a1, self.root.a2

    def make_alfabeta_step(self, node):
        if node.depth == 2 and node.turn == "B":
            return self.evaluate_state(node)

        if node.turn == "A":
            return self.player_A(node)
        else:
            return self.player_B(node)


    def player_A(self, node):
        
        valid_moves = env.get_valid_moves_agents(node.a1, node.a2)
        returned_values = []

        for move in valid_moves:
            if node.alfa < node.beta:
                if move != False:
                    node.children.append(Node(move[0], move[1], node.mrx, parrent=node, alfa=node.alfa, beta=node.beta, depth=node.depth, turn="B"))
                    node_result = self.make_alfabeta_step(node.children[-1])
                    returned_values.append(node_result)
        
                    # check if still A > B
                    if max(returned_values) < node.beta:
                        if max(returned_values) > node.alfa:
                            node.alfa = max(returned_values)
                    else:
                        break
            else:
                break
            
        return node.alfa

    def player_B(self, node):
        
        valid_moves = env.get_valid_moves(node.mrx)
        returned_values = []

        for move in valid_moves:
            if node.alfa < node.beta:
                if move != False:
                    node.children.append(Node(node.a1, node.a2, move, parrent=node, alfa=node.alfa, beta=node.beta, depth=node.depth + 1, turn="A"))
                    node_result = self.make_alfabeta_step(node.children[-1])
                    returned_values.append(node_result)

                    # check if still A > B
                    if min(returned_values) > node.alfa:
                        if min(returned_values) < node.beta:
                            node.beta = min(returned_values)
                    else: 
                        break
            else:
                break

            

        return node.beta

    def evaluate_state(self, node):
        return 0