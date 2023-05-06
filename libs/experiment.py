import csv
import functools
from UNO import UNO
from UNO_Agent import *

import sys
sys.path.insert(1, 'aima-python')
from games import *

NUM_ITERATIONS = 10

class Experiment:
    def __init__(self, playerTypes, minGameSize, maxGameSize):
        self.playerTypes = playerTypes
        self.minGameSize = minGameSize
        self.maxGameSize= maxGameSize
        #self.playerNames = ["p{0}".format(x) for x in range(len(players))]
    
    def sim_game(self, wins, unoGame, playerNames, players):
        winner = unoGame.play_game(players, False)
        wins[playerNames.index(winner)] += 1

    def generate_win_percentages_per_game_size(self):
        winPercentagePerGameSize = {}
        
        for gameSize in range(self.minGameSize, self.maxGameSize + 1):
            wins = [0 for x in range(gameSize)]
            
            for iteration in range(0, NUM_ITERATIONS):
                playerNames = ["p{0}".format(x) for x in range(gameSize)]
                players = [self.playerTypes[0] if x == 0 else self.playerTypes[1] for x in range(gameSize)]
                unoGame = UNO(playerNames)
                
                self.sim_game(wins, unoGame, playerNames, players)
                
            winPercentagePerGameSize[gameSize] = [winNum / NUM_ITERATIONS for winNum in wins]
                
        return winPercentagePerGameSize
    
    def generate_overall_win_percentages(self):
        winPercentagePerGameSize = self.generate_win_percentages_per_game_size()
        winPercentagePrimaryAgent = 0
        winPercentageSecondaryAgent = 0
        
        for gameSize, winPercentages in winPercentagePerGameSize.items():
            winPercentagePrimaryAgent += winPercentages[0]
            winPercentageSecondaryAgent += winPercentages[1]
        
        numSizes = self.maxGameSize - self.minGameSize
        return {"primary" : [winPercentagePrimaryAgent / numSizes], "secondary" : [winPercentageSecondaryAgent / numSizes]}
    
    def generate_round_length_per_game_size(self):
        return None
    
    def generate_overall_avg_round_length(self):
        return None
    
    def generate_csv(self, name, fields, data):
        file = open(name, 'w', newline='')
        writer = csv.writer(file)
        
        writer.writerow(fields) 
        for key, value in data.items():
            value.insert(0, key)
            writer.writerow(value)
        
        file.close()
    
random_player_only_experiment = Experiment([random_player, random_player], 2, 6)
random_player_only_experiment.generate_csv("random_win_percentages_per_game_size.csv", ["game size", "win percentages"], random_player_only_experiment.generate_win_percentages_per_game_size())
random_player_only_experiment.generate_csv("random_overall_win_percentages.csv", ["agent type", "win percentages"], random_player_only_experiment.generate_overall_win_percentages())

mini_max_experiment = Experiment([mini_max_uno_player, random_player], 2, 6)
mini_max_experiment.generate_csv("minimax_win_percentages_per_game_size.csv", ["game size", "win percentages"], mini_max_experiment.generate_win_percentages_per_game_size())
mini_max_experiment.generate_csv("minimax_overall_win_percentages.csv", ["agent type", "win percentages"], mini_max_experiment.generate_overall_win_percentages())