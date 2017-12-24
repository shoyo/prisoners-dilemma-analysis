# INITIAL GENERATION PROFILE
from data import *

p1 = Kantian()
p2 = AlwaysDefect()
p3 = TitForTat()
p4 = TitFor2Tats()
p5 = Grudger()
p6 = Random()

profile1 = [p1, p2, p3, p4, p5, p6]
diverse = Population(profile1)

# diverse, all Kantian (perfect world), all defectors (cruel world)
# a few defectors in a perfect world, 1 tft in cruel world,
# a few tfts in a cruel world
