import math
import operator
import time
from copy import deepcopy

s = 8
board = [[0 for x in range(s)] for y in range(s)]
middle = int(s / 2) - 1

board[middle][middle] = 1
board[middle + 1][middle + 1] = 1
board[middle + 1][middle] = -1
board[middle][middle + 1] = -1


# looks through the board for possible moves
# computer is white if pc = 1
def poss_move(board, pc):
    if pc:
        ai = 1
    else:
        ai = -1
    moves = {}
    legit_move = 0

    for i in range(s):
        for j in range(s):
            # here we find our own tile, we investigate its neighborhood
            if board[i][j] == ai:
                moves, lm = check_env(board, i, j, moves, pc)
                legit_move += lm
    if legit_move:
        return moves
    return 0


# updates moves around a base and how good it is, AI is white if pc = 1
def check_env(board, x, y, m, pc):
    legit_move = 0
    if pc:
        opponent = -1
    else:
        opponent = 1

    for ii in range(-1, 2):
        if not 0 <= x + ii <= 7:
            continue
        for jj in range(-1, 2):
            if not 0 <= y + jj <= 7:
                continue
            c = 1
            while board[x + c * ii][y + c * jj] == opponent:
                c += 1
                if not 0 <= x + c * ii <= 7 or not 0 <= y + c * jj <= 7:
                    c = 0
                    break
            if board[x + c * ii][y + c * jj] == 0 and c > 1:
                a, b = x + c * ii, y + c * jj
                if s * a + b in m:
                    m[s * a + b][0] += c - 1
                else:
                    m[s * a + b] = [c - 1]
                old_poss = x, y
                m[s * a + b].append(old_poss)
                legit_move = 1

    return m, legit_move


# checks if the users decided move is ok + saves info about how to update the board
def check_human_env(pos, opponent):
    if not opponent:
        opponent = -1
    moves = {}
    x, y = ord(pos[1]) - 49, ord(pos[0]) - 97
    if x < 0 or x > 7 or y < 0 or y > 7:
        return -1
    elif board[x][y] != 0:
        return -1

    moves[s * x + y] = [0]
    for ii in range(-1, 2):
        if not 0 <= x + ii <= 7:
            continue
        for jj in range(-1, 2):
            if not 0 <= y + jj <= 7:
                continue
            c = 1
            while board[x + c * ii][y + c * jj] == opponent:
                c += 1
                if not 0 <= x + c * ii <= 7 or not 0 <= y + c * jj <= 7:
                    c = 0
                    break
            if board[x + c * ii][y + c * jj] == -opponent and c > 1:
                base = x + c * ii, y + c * jj
                moves[s * x + y][0] += c - 1
                moves[s * x + y].append(base)
    if moves[s * x + y] == [0]:
        return -1
    else:
        return moves


# updates the board after a official move is made
def update_board(moves):
    key = max(moves.items(), key=operator.itemgetter(1))[0]
    old_poss = moves[key][1:]
    opt_poss = math.floor(key / s), key % s
    player = board[old_poss[0][0]][old_poss[0][1]]
    for op in old_poss:

        delta = op[0] - opt_poss[0], op[1] - opt_poss[1]

        if abs(delta[0]) >= abs(delta[1]):
            number_of_steps = abs(delta[0])
        else:
            number_of_steps = abs(delta[1])
        move_vec = int(delta[0] / number_of_steps), int(delta[1] / number_of_steps)

        for i in range(1, number_of_steps):
            board[opt_poss[0] + move_vec[0] * i][opt_poss[1] + move_vec[1] * i] = player
    board[opt_poss[0]][opt_poss[1]] = player


# Updates the temporary board made out of possible moves in the min max algo
def update_temp_board(board, key, values):
    old_poss = values[1:]
    opt_poss = math.floor(key / s), key % s
    player = board[old_poss[0][0]][old_poss[0][1]]
    for op in old_poss:

        delta = op[0] - opt_poss[0], op[1] - opt_poss[1]

        if abs(delta[0]) >= abs(delta[1]):
            number_of_steps = abs(delta[0])
        else:
            number_of_steps = abs(delta[1])
        move_vec = int(delta[0] / number_of_steps), int(delta[1] / number_of_steps)

        for i in range(1, number_of_steps):
            board[opt_poss[0] + move_vec[0] * i][opt_poss[1] + move_vec[1] * i] = player
    board[opt_poss[0]][opt_poss[1]] = player
    return board


# Prints the board, which is usefull to get a view over the game
def print_board():
    print('   a  b  c  d  e  f  g  h')
    for i in range(s):
        line = ' '
        for j in range(s):
            if board[i][j] == 0:
                line = line + ' . '
            elif board[i][j] == -1:
                line = line + ' B '
            else:
                line = line + ' W '
        print(str(i + 1) + line)
    print('-------------------------')


# Gives a score for how good a future board is. We value our # of tiles - opposition # of tiles.
# Corners are extra valuable
def evaluate(board):
    winner = 0
    for i in range(s):
        winner += sum(board[i])
        if i == 0 or i == s - 1:
            winner += (board[i][0] + board[i][s - 1]) * 9
    return winner


# The min max algo with alpha beta pruning
def alpha_beta(board, nbr_of_layers, alpha, beta, time_vector, maximizing_player):
    if time.time() - time_vector[0] > time_vector[1]:
        return False
    if nbr_of_layers == 0:
        return evaluate(board)
    if maximizing_player:
        v = -s * s - 1
        moves = poss_move(board, 1)
        if moves == 0:
            v = max(v, alpha_beta(board, nbr_of_layers - 1, alpha, beta, time_vector, False))
        else:
            for key, values in moves.items():
                if values[0] != 0:
                    temp_board = update_temp_board(deepcopy(board), key, values)
                    v_eval = alpha_beta(temp_board, nbr_of_layers - 1, alpha, beta, time_vector, False)
                    if isinstance(v_eval, int):
                        v = max(v, v_eval)
                        alpha = max(alpha, v)
                        if alpha >= beta:
                            break
                    else:
                        return False
    else:
        v = s * s + 1
        moves = poss_move(board, 0)
        if moves == 0:
            v = min(v, alpha_beta(board, nbr_of_layers - 1, alpha, beta, time_vector, True))

        else:
            for key, values in moves.items():
                if values[0] != 0:
                    temp_board = update_temp_board(deepcopy(board), key, values)
                    v_eval = alpha_beta(temp_board, nbr_of_layers - 1, alpha, beta, time_vector, True)
                    if isinstance(v_eval, int):
                        v = min(v, v_eval)
                        beta = min(beta, v)
                        if alpha >= beta:
                            break
                    else:
                        return False
    return v


# This manages the AIs move, first it finds all the moves possible and then it finds which move that
# according to the min max algorithm, with pruning, is the best.
def optimal_move(board, pc, nbr_of_layers, time_vector):
    optimal_points = 65
    optimal_move = {}
    moves = poss_move(board, pc)
    maximizing_player = False
    if moves == 0:
        return 0
    if pc:
        maximizing_player = True
        optimal_points = -65

    for key, values in moves.items():
        if time.time() - time_vector[0] > time_vector[1]:
            return optimal_move
        temp_board = update_temp_board(deepcopy(board), key, values)
        points = alpha_beta(temp_board, nbr_of_layers - 1, -s * s - 1, s * s + 1, time_vector, not maximizing_player)
        if not isinstance(points, int):
            return -1
        if maximizing_player:
            if points > optimal_points:
                optimal_points = points
                optimal_move = {key: values}
        else:
            if points < optimal_points:
                optimal_points = points
                optimal_move = {key: values}
    return optimal_move


# The core method which is called from main for each round of play, calls the other methods in order to make a move
# It handles both human and AI moves.
def make_move(counter, pc, time_vector):
    if counter % 2:
        moves = -1
        c = 0
        while True:
            if c > 0 and moves == -1:
                print('Not a valid move, try again')
            move_input = input('Choose position of type \'a-h 1-8\', ex. b3. Or \'pass\'  : ')
            if len(move_input) == 2:
                move_input = [move_input[0], move_input[1]]
                moves = check_human_env(move_input, pc)
            elif move_input == 'pass':
                moves = 0
                break
            else:
                moves = -1
            if moves != -1:
                break
            c += 1

    else:
        depth = [2, 4, 8, 12, 20]
        moves = -1
        for d in depth:
            temp_m = optimal_move(board, pc, d, time_vector)
            if not temp_m == -1:
                moves = temp_m
            if time.time() - time_vector[0] > time_vector[1] / 2 or temp_m == -1:
                break

    if moves == 0:
        print('Could not make a move, passes on to next round')
        return 1
    elif moves == -1:
        print("Did not have time to finish even one layer")
        return 1
    else:
        update_board(moves)
        return 0


# The main method calls for initial information for the game, runs the game and then pressents the result when the
# game is finished
if __name__ == '__main__':
    # AI: white == 1
    while True:
        player_colour = input('Welcome to the Othello game! If you want to be black, press 1, otherwise press 0: ')
        if player_colour == '1' or player_colour == '0':
            player_colour = int(player_colour)
            break
        else:
            print('invalid input')

    while True:
        time_limit = input('Choose the maximum time (s) the AI is allowed to use for each move: ')
        try:
            time_limit = float(time_limit)
        except:
            print('invalid input')
        else:
            break

    c = player_colour
    ss = s * s
    if c:
        ss += 1
    print_board()
    while c < ss - 4:
        start_time = time.time()
        time_vector = [start_time, time_limit * 3 / 4]

        extra_rounds = make_move(c, player_colour, time_vector)
        print_board()
        if not c % 2:
            end_time = time.time()
            elapsed_time = str(end_time - start_time).split(".")
            print("Move took " + elapsed_time[0] + "." + elapsed_time[1][0] + " seconds.")
        ss += extra_rounds
        c += 1

    winner = 0
    for i in range(s):
        winner += sum(board[i])
    if winner > 0:
        print('White won with ', int((s * s + winner) / 2), ' to ', int((s * s - winner) / 2))
    elif winner < 0:
        print('Black won', int((s * s - winner) / 2), ' to ', int((s * s + winner) / 2))
    else:
        print('OMG it\'s a tie')






