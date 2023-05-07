import sys

sys.path.insert(1, 'aima-python')
from collections import namedtuple
from games import *

def terminal_test(state):
    for player, hand in state.board.items():
        if player != "draw" or player != "discard" and len(hand) == 0:
            return True
        
    return False

def is_winner(state, potentialWinner):
    for player, hand in state.board.items():
            if player != potentialWinner:
                return len(state.board[player]) == 0
    
    return False

def uno_eval(state):        
    if terminal_test(state):
        if is_winner(state, 0):
            return 1;
        else:
            return -1;
        
    return 0
    
    #numCards = len(state.board[state.to_move])
    #return -((numCards - 1) / (numCards + 1))

        

def mini_max_uno_player(game, state):
    return alpha_beta_cutoff_search(state, game, d=0, eval_fn=uno_eval)