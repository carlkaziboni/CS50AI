"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Tracking number of each
    x = 0
    o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            if board[i][j] == O:
                o += 1
    if x <= o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(3):
        for j in range(3):
            if (board[i][j] is EMPTY):
                possible_actions.append((i, j))
    return set(possible_actions)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception
    current_player = player(board)
    board_new = copy.deepcopy(board)
    board_new[action[0]][action[1]] = current_player
    return board_new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Three in a row horizontal
        if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and (board[i][0] is not EMPTY)):
            return board[i][0]
        for j in range(3):
            # Checking cross way
            if (i == 0 and j == 0):
                if (board[i][j] == board[i+1][j+1] and board[i+1][j+1] == board[i+2][j+2] and (board[i][j] is not None)):
                    return board[i][j]
            # Checking vertical three in a row
            if (i == 0):
                if (board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j] and (board[i][j] is not None)):
                    return board[i][j]
            # Checking other cross way
            if (i == 0 and j == 2):
                if (board[i][j] == board[i+1][j-1] and board[i+1][j-1] == board[i+2][j-2] and (board[i][j] is not None)):
                    return board[i][j]       
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) is not None):
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) is None):
        return 0
    elif winner(board) == X:
        return 1
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # Get the minimum value
    def mini(boards):
        utilities = []
        for board in boards:
            possible_actions = actions(board[0])
            for action in possible_actions:
                resulting_board = result(board[0], action)
                if terminal(resulting_board):
                    utilities.append((utility(resulting_board), board[1]))
                    continue
                maxi_result = maxi([(resulting_board, board[1])])
                utilities.append(maxi_result)
        minimum = min(utilities)
        return minimum
    
    # Get the maximum value
    def maxi(boards):
        utilities = []
        for board in boards:
            possible_actions = actions(board[0])
            for action in possible_actions:
                resulting_board = result(board[0], action)
                if terminal(resulting_board):
                    utilities.append((utility(resulting_board), board[1]))
                    continue
                mini_result = mini([(resulting_board, board[1])])
                utilities.append(mini_result)
        maximum = max(utilities)
        return maximum
    
    # X playing 
    if player(board) == X:
        possible_actions = actions(board)
        utilities = []
        for action in possible_actions:
            resulting_board = result(board, action)
            if terminal(resulting_board):
                utilities.append((utility(resulting_board), action))
                continue
            mini_result = mini([(resulting_board, action)])
            utilities.append(mini_result)
        maximum = max(utilities)
        return maximum[1]
    
    # Y is playing
    if player(board) == O:
        possible_actions = actions(board)
        utilities = []
        for action in possible_actions:
            resulting_board = result(board, action)
            if terminal(resulting_board):
                utilities.append((utility(resulting_board), action))
                continue
            mini_result = maxi([(resulting_board, action)])
            utilities.append(mini_result)
        minimum = min(utilities)
        return minimum[1]
    
    raise Exception("Invalid board put in")