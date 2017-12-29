# TOURNAMENT AND GENERATIONAL LOGIC
from profiles import *
import csv

NUM_GENS = 35
NUM_ROUNDS = 100
current_gen = cruel_world_with_few_tft()

for i in range(NUM_GENS):
    print("Generation " + str(i + 1) + ":")

    round_robin(current_gen, NUM_ROUNDS)
    print("Distribution:")
    print(current_gen.distribution())
    print("Final Scores:")
    print(current_gen.scoreboard())
    print()

    current_gen = current_gen.create_next_gen()
    current_gen.reset_all_scores()
