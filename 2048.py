import random
import operator

def get_truth(inp, relate, cut):
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq}
    return ops[relate](inp, cut)

GAME_FINISHED = False

def get_row_col_from_orig(compare, col_orig, row_orig, i, op):
    if compare == "col":
        col = col_orig - i if op == ">" else col_orig + i
        row = row_orig
    else:
        row = row_orig - i if op == ">" else row_orig + i
        col = col_orig
    interested = col if compare == "col" else row
    return row, col, interested

def bring_to_current(row_orig, col_orig, op, board, compare):
    border = 0 if op == ">" else 3
    if board[row_orig][col_orig] == 0:
        bring_closest_non_zero_in(row_orig, col_orig, op, board, compare, border)

def bring_to_neighbour(row_orig, col_orig, op, board, compare):
    border = 0 if op == ">" else 3
    interested_orig = col_orig if compare == "col" else row_orig
    if get_truth(interested_orig, op, border) and board[row_orig][col_orig] == 0:
        bring_closest_non_zero_in(row_orig, col_orig, op, board, compare, border)

def bring_closest_non_zero_in(row_orig, col_orig, op, board, compare, border):
    i = 0
    row, col, interested = get_row_col_from_orig(compare, col_orig, row_orig, i, op)
    while board[row][col] == 0 and get_truth(interested, op, border):
        i += 1
        row, col, interested = get_row_col_from_orig(compare, col_orig, row_orig, i, op)

    board[row_orig][col_orig] = board[row][col]
    board[row][col] = 0



def spawn(board):
    random_num = random.randint(0, 100)
    free_spots = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                free_spots.append((i, j))
    if not free_spots:
        print("You lost")
        global GAME_FINISHED
        GAME_FINISHED = True
        return
    free_spot = random_num % len(free_spots)
    board[free_spots[free_spot][0]][free_spots[free_spot][1]] = 2


def handle_right(board):
    for row in range(4):
        for col in reversed(range(4)):
            # If the current value is 0, bring the first non 0 to the left in
            bring_to_current(row, col, ">", board, "col")
            # If the neighour to the left is 0, bring the first non 0 to the left in
            bring_to_neighbour(row, col-1, ">", board, "col")
            # If the current value is the same as the neighour to the left, sum
            if col > 0 and board[row][col - 1] == board[row][col] and board[row][col] != 0:
                board[row][col] = 2 * board[row][col]
                board[row][col - 1] = 0

    spawn(board)


def handle_left(board):
    for row in range(4):
        for col in range(4):
            bring_to_current(row, col, "<", board, "col")
            bring_to_neighbour(row, col+1, "<", board, "col")

            if col < 3 and board[row][col + 1] == board[row][col] and board[row][col] != 0:
                board[row][col] = 2 * board[row][col]
                board[row][col + 1] = 0
    spawn(board)


def handle_down(board):
    for col in range(4):
        for row in reversed(range(4)):
            bring_to_current(row, col, ">", board, "row")
            bring_to_neighbour(row-1, col, ">", board, "row")

            if row > 0 and board[row - 1][col] == board[row][col] and board[row][col] != 0:
                board[row][col] = 2 * board[row][col]
                board[row - 1][col] = 0
    spawn(board)


def handle_up(board):
    for col in range(4):
        for row in range(4):
            bring_to_current(row, col, "<", board, "row")
            bring_to_neighbour(row+1, col, "<", board, "row")
            if row < 3 and board[row + 1][col] == board[row][col] and board[row][col] != 0:
                board[row][col] = 2 * board[row][col]
                board[row + 1][col] = 0
    spawn(board)


def handle_action(action, board):
    if action == "w":
        handle_up(board)
    if action == "d":
        handle_right(board)
    if action == "a":
        handle_left(board)
    if action == "s":
        handle_down(board)
    if action == "f":
        global GAME_FINISHED
        GAME_FINISHED = True


def create_board():
    return [[0 for x in range(4)] for y in range(4)]


def main():
    board = create_board()
    spawn(board)
    print("use W-A-S-D to control game, press F to exit. Press enter after each command")
    while not GAME_FINISHED:
        print(*board, sep="\n")
        action = input()
        handle_action(action, board)


if __name__ == "__main__":
    main()
