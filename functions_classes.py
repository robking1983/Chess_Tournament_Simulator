from numpy import exp,log
from itertools import combinations
from scipy.stats import rankdata
from numpy.random import randint
import pandas as pd
from ipywidgets import FloatProgress
from IPython.display import display


# functions to simulate games

# the draw chances are based on a regression by http://kirill-kryukov.com/chess/kcec/draw_rate.html
def draw(R_a, R_b):
    diff = (R_b - R_a)
    return (((diff / 22.37) + 27.95) / 100)


# function that returns a sample space for expected wins, draws, losses for player A
def e(R_a, R_b):
    avg = (R_b + R_a) / 2
    diff = (R_b - R_a)

    e_a = 1.0 / (1.0 + exp(log(10) * (R_b - R_a) / 400))
    win_rate = int(100 * (e_a - draw(R_a, R_b) / 2))
    draw_rate = int(100 * draw(R_a, R_b))
    loss_rate = 100 - (win_rate + draw_rate)

    score = win_rate * [1] + draw_rate * [.5] + loss_rate * [0]

    return (score)


# function that calculates the percentage that a player finishes at least at a standing,  with ties counting
def percent_chance(player, standing, df):
    return (1.0 * len(df[df[player] <= standing]) / len(df))


# class to simulate a round robin tournament

class player:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.score = 0

    # add points to a players' score
    def add_points(self, num):
        self.score += num

    # simulate a game between an opponent based on ratings    
    def sim_game(self, opponent):
        # get probability space
        p_space = e(self.rating, opponent.rating)
        # randomly sample result
        i = randint(1, 100 + 1)
        result = p_space[i - 1]
        # add points
        if result == 1:
            self.score += result
        if result == .5:
            self.score += .5
            opponent.score += .5
        if result == 0:
            opponent.score += 1

    # reset the score of a player
    def reset_score(self):
        self.score = 0


class tournament:

    def __init__(self, name):
        self.name = name
        self.players = []
        self.player_names = []
        self.ranks = []
        self.scores = []

    # add a player to the tournament
    def add_player(self, player):
        self.players.append(player)
        self.player_names.append(player.name)

    # create the round robin pairings
    def create_round_robin(self):
        self.pairings = list(combinations(self.players, 2))

    # reset the scores of the players
    def reset_scores(self):
        for p in self.players:
            p.reset_score()

    # simulate a cross table just once
    def sim_1(self):
        results = []
        for p in self.pairings:
            p[0].sim_game(p[1])

        for x in self.players:
            results.append((x.name, x.score))

        return (results)

    # simulate the cross table, num number of times
    def sim(self, num):
        f = FloatProgress(min=0, max=num - 1)
        display(f)
        for n in range(0, num - 1):
            self.scores.append(self.sim_1())
            self.reset_scores()
            f.value += 1
        for s in self.scores:
            self.ranks.append(len(s) - rankdata([x[1] for x in s], method='max') + 1)

