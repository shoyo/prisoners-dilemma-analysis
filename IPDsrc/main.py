from players import *

""" Prisoner's Dilemma Payoffs:
    Both cooperate              -> both +2 pts
    Both defect                 -> both +1 pts
    One cooperates, one defects -> cooperator +0 pts, defector +3 pts
"""

number_of_generations = 10
number_of_rounds = 100

round_robin(current_generation)