from BaseAI import BaseAI
import math
import numpy as np

def getNewNode(board):
    possible = [0, 1, 2, 3]
    newNodes = []
    movesMade = []
    for i in possible:
        boardReplica = list(board)
        change = playerAIMoves(boardReplica, i)
        if change == True:
            newNodes.append(boardReplica)
            movesMade.append(i)
    return [newNodes, movesMade]


def possibleMoves(board):
    if 0 in board:
        return True
    for i in range(16):
        if i+1 not in [4,8,12,16]:
            if board[i]==board[i+1]:
                return True
        elif i not in [0,4,8,12]:
            if board[i] == board[i - 1]:
                return True
        if i<12:
            if board[i]==board[i+4]:
                return True
    return False

def playerAIMoves(board, mv):
    complete = False
    if mv == 0:
        for i in range(4):
            pieces = []
            for j in range(i,i+13,4):
                piece = board[j]
                if piece != 0:
                    pieces.append(piece)
            collapase(pieces)
            for j in range(i,i+13,4):
                value = pieces.pop(0) if pieces else 0
                if board[j] != value:
                    complete = True
                board[j] = value
        return complete
    elif mv == 1:
        for i in range(4):
            pieces = []
            for j in range(i+12,i-1,-4):
                piece = board[j]
                if piece != 0:
                    pieces.append(piece)
            collapase(pieces)
            for j in range(i+12,i-1,-4):
                value = pieces.pop(0) if pieces else 0
                if board[j] != value:
                    complete = True
                board[j] = value
        return complete
    elif mv == 2:
        for i in [0,4,8,12]:
            pieces = []
            for j in range(i,i+4):
                piece = board[j]
                if piece != 0:
                    pieces.append(piece)
            collapase(pieces)
            for j in range(i,i+4):
                value = pieces.pop(0) if pieces else 0
                if board[j] != value:
                    complete = True
                board[j] = value
        return complete
    elif mv == 3:
        for i in [3,7,11,15]:
            pieces = []
            for j in range(i,i-4,-1):
                piece = board[j]
                if piece != 0:
                    pieces.append(piece)
            collapase(pieces)
            for j in range(i,i-4,-1):
                value = pieces.pop(0) if pieces else 0
                if board[j] != value:
                    complete = True
                board[j] = value
        return complete


def collapase(pieces):
    if len(pieces) <= 1:
        return pieces
    i = 0
    while i < len(pieces)-1:
        if pieces[i] == pieces[i+1]:
            pieces[i] *= 2
            del pieces[i+1]
        i += 1


def pair_heuristics(board):
    pair_hcost = 0
    for i in [0,1,2,4,5,6,8,9,10]:
        if board[i] == board[i+1]:
            pair_hcost += board[i]
            if board[i] == board[i+4]:
                pair_hcost += board[i]
    for i in [3,7,11]:
        if board[i] == board[i+4]:
            pair_hcost += board[i]
    return pair_hcost

def heuristic(board):
    boardMax = max(board)
    emptyTiles = len([i for i, x in enumerate(board) if x == 0])
    boardFactor = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    utility = 0
    multiplying_factor = 16
    ctr = 0
    for i in board:
        if i !=0:
            boardFactor[ctr] = (math.log(i)/0.693)
            ctr += 1
        else:
            ctr += 1

    priority = [4096,2048,1024,512,32,64,128,256,16,8,4,2,0.125,0.25,0.5,1]

    if boardMax == board[0]:
        utility += boardFactor[0] * priority[0] * multiplying_factor
    for i in xrange(16):
        if board[i] >= 8:
            utility += priority[i] * boardFactor[i] * multiplying_factor
        if i < 4 and board[i] == 0 :
            utility -= priority[i] * boardFactor[0] * multiplying_factor
    return (utility/(16-emptyTiles))



def minimax(board, border, alpha, beta, minmax):
    if border == 0:
        return heuristic(board)
    if not possibleMoves(board):
        return heuristic(board)
    if minmax:
        lower_bound = -np.inf
        [nodes, mv] = getNewNode(board)
        for node in nodes:
            lower_bound = max(lower_bound,minimax(node,border-1,alpha,beta,False))
            if lower_bound >= beta:
                return lower_bound
            alpha = max(alpha,lower_bound)
        return lower_bound
    else:
        empty_nodes = [i for i, x in enumerate(board) if x == 0]
        nodes = []
        for n in empty_nodes:
            new_board = list(board)
            new_board[n]=2
            nodes.append(new_board)
            new_board = list(board)
            new_board[n]=4
            nodes.append(new_board)
        upper_bound = np.inf
        for node in nodes:
            upper_bound = min(upper_bound,minimax(node,border-1,alpha,beta,True))
            if upper_bound <= alpha:
                return upper_bound
            beta = min(beta,upper_bound)
        return upper_bound



class PlayerAI(BaseAI):
    def getMove(self, board):
        boardList = []
        for i in range(4):
            boardList.extend(board.map[i])
        [nodes, mv] = getNewNode(boardList)
        lower_bound = -np.inf
        move = 0
        for i in range(len(nodes)):
            moves = mv[i]
            node = nodes[i]
            upper_bound = -np.inf
            border = 4
            upper_bound = minimax(node, border, -np.inf, np.inf, False)
            if moves == 0:
                upper_bound += 10000
            if moves == 2:
                upper_bound += 10000
            if upper_bound > lower_bound:
                move = moves
                lower_bound = upper_bound
        return move


