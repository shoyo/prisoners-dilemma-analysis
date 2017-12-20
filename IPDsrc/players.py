from data import *

p1 = Player(kantian)
p2 = Player(always_defect)
p3 = Player(tit_for_tat)
p4 = Player(tit_for_2tats)
p5 = Player(tester)
p6 = Player(grudger)
p7 = Player(random)

initial_population = [p1, p2, p3, p4, p5, p6, p7]
current_generation = Population(initial_population)
