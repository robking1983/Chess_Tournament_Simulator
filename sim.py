import pandas as pd
from functions_classes import Player, Tournament, percent_chance, yes_no

# Get the players and ratings from the user
new_player = True
players = []

while new_player:
    p_name = raw_input("What is the Player's name?")
    p_rating = int(raw_input("What is the Player's rating?"))
    # Add the player
    players.append(Player(p_name, p_rating))
    new_player = yes_no("Add New Player?")

# Create the tournament
t = Tournament('T')

# add the players to the tournaments
for p in players:
    t.add_player(p)

# create all of the pairings
t.create_round_robin()

# simulate the tournament 100,000 times
results = t.sim(50000)

# view the resulting standings for each sim
df = pd.DataFrame(t.ranks, columns=t.player_names)

# calculate the probability that each player will finish in at least shared first
for p in t.player_names:
    print(p + ' - ' + str(100 * percent_chance(p, 1, df)))
