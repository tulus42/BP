def get_next_move(agent1, agent2, real_pos, seen_pos, seen_time):

    a1 = [agent1 % 5, agent1 // 5]
    a2 = [agent2 % 5, agent2 // 5]
    mrx = [real_pos % 5, real_pos // 5]
    
    possible_positions = [minimax_step(a1, a2, [mrx[0], mrx[1]-1], 0, False, 3),     # UP
            minimax_step(a1, a2, [mrx[0], mrx[1]+1],  0, False, 3),                  # DOWN
            minimax_step(a1, a2, [mrx[0]-1, mrx[1]], 0, False, 3),                   # LEFT
            minimax_step(a1, a2, [mrx[0]+1, mrx[1]], 0, False, 3)]                   # RIGHT

    next_move = possible_positions.index(max(possible_positions))
    next_pos = real_pos + decode_move(next_move)

    seen_time = (seen_time + 1) % 3

    # every 3th move is mrX visible
    if seen_time == 0:
        seen_pos = next_pos

    return next_pos, seen_pos, seen_time


#
#
def minimax_step(a1, a2, mrx, depth, is_mrx, h):
    if out_of_range(a1) or out_of_range(a2) or out_of_range(mrx):
        return 1000 if is_mrx else -1000

    if a1 == mrx or a2 == mrx:
        return -100 * (h - depth + 1) # caught sooner -> higher penalty

    if depth == h:
        return min(get_distance(a1, mrx), get_distance(a2, mrx))

    if is_mrx:
        return max(minimax_step(a1, a2, [mrx[0]+1, mrx[1]], depth + 1, False, h),
                   minimax_step(a1, a2, [mrx[0]-1, mrx[1]], depth + 1, False, h),
                   minimax_step(a1, a2, [mrx[0], mrx[1]+1], depth + 1, False, h),
                   minimax_step(a1, a2, [mrx[0], mrx[1]-1], depth + 1, False, h))
    else:
        return min(minimax_step([a1[0]+1, a1[1]], a2, mrx, depth + 1, True, h),
                   minimax_step([a1[0]-1, a1[1]], a2, mrx, depth + 1, True, h),
                   minimax_step([a1[0], a1[1]+1], a2, mrx, depth + 1, True, h),
                   minimax_step([a1[0], a1[1]-1], a2, mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0]+1, a2[1]], mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0]-1, a2[1]], mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0], a2[1]+1], mrx, depth + 1, True, h),
                   minimax_step(a1, [a2[0], a2[1]-1], mrx, depth + 1, True, h))


#
#
def out_of_range(x):
    if x[0] < 0 or x[0] > 4 or x[1] < 0 or x[1] > 4:
        return True
    else:
        return False


#
#
def get_distance(a, mrx):
    x = abs(a[0] - mrx[0])
    y = abs(a[1] - mrx[1])
    return x + y


def decode_move(move):
    if move == 0:       # UP
        return -5
    elif move == 1:     # DOWN
        return 5
    elif move == 2:     # LEFT
        return -1
    else:               # RIGHT
        return 1