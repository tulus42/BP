import sys
import environment

def handle_input(mrx, a1, a2):
    c = ""
    while True:
        c = sys.stdin.read(1) # reads one byte at a time, similar to getchar()
        
        if c == ' ':
            return -1
        else:
            possible_moves = environment.get_valid_moves_mrx(mrx, a1, a2)
            next_move = -1
            if c == 'w':
                next_move = environment.go_up(mrx)
            elif c == 's':
                next_move = environment.go_down(mrx)
            elif c == 'a':
                next_move = environment.go_left(mrx)
            elif c == 'd':
                next_move = environment.go_right(mrx)

            if next_move in possible_moves:
                return next_move 
