import environment as env
import alfabeta_node as nd


class AlfaBeta:
    def __init__(self):
        self.root = nd.Node()

    def choose_new_move_agents(self):
        new_move_node = self.root.best_way

        self.root = new_move_node
        new_a1, new_a2 = self.root.a1, self.root.a2

        ###############################################
        # MOVE WITH MR.X IN ALFA-BETA TREE ############
        new_move_node = self.root.best_way          ###
                                                    ###
        if new_move_node == False:                  ###
            raise Exception(SystemError)            ###
                                                    ###
        self.root = new_move_node                   ###
        ###############################################


        return new_a1, new_a2


    def explore_state_space(self, a1, a2, mrx):
        self.root.reset()

        self.root.a1 = a1
        self.root.a2 = a2
        self.root.mrx = mrx

        self.make_alfabeta_step(self.root)


    def make_alfabeta_step(self, node):
        if node.depth > 2:
            return self.evaluate_state(node)
        elif node.turn == "A":
            return self.player_A(node)
        elif node.turn == "B":
            return self.player_B(node)
        else:
            raise Exception(SystemError)
        


    def player_A(self, node):
        new_valid_locations = env.get_valid_moves_agents(node.a1, node.a2)
        
        if new_valid_locations == []:
            return self.evaluate_state(node)

        for new_location in new_valid_locations:
            if node.alfa < node.beta:
                new_node = nd.Node(new_location[0], new_location[1], node.mrx, parrent=node, alfa=node.alfa, beta=node.beta, depth=node.depth, turn="B")
                node.children.append(new_node)

                node_result = self.make_alfabeta_step(node.children[-1])

                if node_result > node.alfa:
                    node.alfa = node_result
                    node.best_way = node.children[-1]

            else:
                break

        return node.alfa


       
    def player_B(self, node):
        new_valid_locations = env.get_valid_moves_mrx_vs_player(node.mrx)               # variant for playing with player #
        # new_valid_locations = env.get_valid_moves_mrx(node.mrx, node.a1, node.a2) # use only when play only AI against itself
        
        if new_valid_locations == []:                                       # use only when play only AI against itself
            print("ERR: empty moves")
            return self.evaluate_state(node)

        for new_location in new_valid_locations:
            if node.alfa < node.beta:
                new_node = nd.Node(node.a1, node.a2, new_location, parrent=node, alfa=node.alfa, beta=node.beta, depth=node.depth+1, turn="A")
                node.children.append(new_node)

                node_result = self.make_alfabeta_step(node.children[-1])

                if node_result < node.beta:
                    node.beta = node_result
                    node.best_way = node.children[-1]

            else:
                break

        return node.beta


    def evaluate_state(self, evaluated_node):
        finished = False
        node = evaluated_node
        value = 0
        while not finished:
            if node == self.root:
                finished = True

            # for every posible chatch during this branch is state
            if node.mrx == node.a1:
                value += (3 - node.depth) * 50
                value -= self.evaluate_distance(node.mrx, node.a2)
            elif node.mrx == node.a2:
                value += (3 - node.depth) * 50
                value -= self.evaluate_distance(node.mrx, node.a1)
            else:
                value1 = self.evaluate_distance(node.mrx, node.a1)
                value2 = self.evaluate_distance(node.mrx, node.a2)
                value -= min(value1, value2)
                value -= max(value1, value2) // 2
            
            node = node.parrent


        return value

    def evaluate_distance(self, pos1, pos2):
        p1x = pos1 % 5
        p1y = pos1 // 5

        p2x = pos2 % 5
        p2y = pos2 // 5

        distance = abs(p1x - p2x) + abs(p1y - p2y)

        return distance