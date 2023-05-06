import random
import sys

sys.path.insert(1, 'aima-python')
from collections import namedtuple
from games import *

GameState = namedtuple('GameState', 'to_move, utility, board, moves')

class UNO(Game):
    def __init__(self, players):
        self.players = players;
        self.playerCount = len(players)
        self.initialCardCount = 7
        self.direction = 1
        self.initial = GameState(to_move=0, utility=0, board=self.generate_initial_board(), moves=[])
    
    def generate_initial_board(self):
        board = {}
        board["draw"] = []
        board["discard"] = []
        
        # generate all cards for draw pile
        for color in ['r', 'y', 'g', 'b']:
            for num in range(15):
                board["draw"].append({"color": color, "value": num})
            
            for num in range(1, 15):
                board["draw"].append({"color": color, "value": num})
        
        # shuffle draw pile
        random.shuffle(board["draw"])
             
        for player in self.players:
            board[player] = []   
            
            for cardNum in range(self.initialCardCount):
                board[player].append(board["draw"].pop())  
        
        move = board["draw"][-1]
        board["discard"].append(move)
        
        return board
                    
                   
    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        moves = []
        topCard = state.board["discard"][-1]
        
        for card in state.board[self.players[state.to_move]]:
            if self.can_play_card(card, topCard):
                # change wildcard color to match topCard
                if card["value"] == 13 or card["value"] == 14:
                    card["color"] = topCard["color"]
                
                moves.append(card)
        
        return moves
    
    def can_play_card(self, topCard, bottomCard):
        # handle wild cards
        if topCard["value"] == 13 or topCard["value"] == 14:
            return True
        
        return topCard["color"] == bottomCard["color"] or topCard["value"] == bottomCard["value"]

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        
        board = state.board.copy()
        playerIndexDelta = 1
        
        if(move == None):
            if len(board["draw"]) == 0:
                discardTop = board["discard"].pop()
                board["draw"] = board["discard"].copy()
                random.shuffle(board["draw"])
                board["discard"] = [discardTop]
                
            self.draw_card(board[self.players[state.to_move]], board["draw"])
        else:
            board[self.players[state.to_move]].remove(move)    
            board["discard"].append(move)
        
            # handle skip turn for skip and +2
            if move["value"] == 10 or move["value"] == 11:
                playerIndexDelta = 2
            
            # handle reverse
            if move["value"] == 12:
                self.direction = -self.direction   
            
        unboundedNextPlayerIndex = state.to_move + playerIndexDelta * self.direction;
        
        if self.direction == 1:
            nextPlayerIndex = unboundedNextPlayerIndex if unboundedNextPlayerIndex < self.playerCount else unboundedNextPlayerIndex - self.playerCount
        else:
            nextPlayerIndex = unboundedNextPlayerIndex if unboundedNextPlayerIndex >= 0 else unboundedNextPlayerIndex + self.playerCount
        
        nextPlayer = self.players[nextPlayerIndex]
        
        if(move != None):
            # handle +2
            if move["value"] == 11:
                if len(board["draw"]) - 2 < 0:
                    if(len(board["draw"]) - 1 < 0):
                        discardTop = board["discard"].pop()
                        board["draw"] = board["discard"].copy()
                        random.shuffle(board["draw"])
                        board["discard"] = [discardTop]
                    
                    self.draw_card(board[nextPlayer], board["draw"])
                    
                    if(len(board["draw"]) - 1 < 0):
                        discardTop = board["discard"].pop()
                        board["draw"] = board["discard"].copy()
                        random.shuffle(board["draw"])
                        board["discard"] = [discardTop]
                    
                    self.draw_card(board[nextPlayer], board["draw"])
                    
                else:
                    self.draw_cards(board[nextPlayer], board["draw"], 2)
        
        return GameState(to_move=nextPlayerIndex, utility=0, board=board, moves=state.moves)
    
    def draw_card(self, hand, drawPile):
        hand.append(drawPile.pop())
    
    def draw_cards(self, hand, drawPile, amount):
        for i in range(amount):
            self.draw_card(hand, drawPile)
        
    def utility(self, state, player):
        """Return the value of this final state to player."""
        
        for playerName, hand in state.board.items():
            if playerName != "draw" and playerName != "discard" and len(hand) == 0:
                winningPlayer = playerName
                break
        
        return state.utility if player == winningPlayer else -state.utility

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        
        for player in self.players:
            if len(state.board[player]) == 0:
                return True
            
        return False

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print("draw : {}".format(state.board["draw"]))
        print("discard : {}".format(state.board["discard"]))
        
        for player in self.players:
            print("{0} : {1}".format(player, state.board[player]))

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, players, display):
        """Play an n-person, move-alternating game."""
        state = self.initial
        playerIndex = state.to_move
        
        while True:
            move = players[playerIndex](self, state)
            state = self.result(state, move)
            if self.terminal_test(state):
                if display:
                    self.display(state)
                    
                return self.get_winner(state)
            
            playerIndex = state.to_move
                
    def get_winner(self, state):
        for player in self.players:
            if len(state.board[player]) == 0:
                return player
        
        return None