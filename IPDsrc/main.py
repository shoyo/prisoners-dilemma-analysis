# TOURNAMENT AND GENERATIONAL LOGIC
from profiles import *
import csv

NUM_OF_GENS = 10
NUM_OF_ROUNDS = 200
current_gen = diverse()

for i in range(NUM_OF_GENS):
    print("Generation " + str(i + 1) + ":")

    print("Pre:")
    print(current_gen.scoreboard())

    round_robin(current_gen, NUM_OF_ROUNDS)

    print("Post:")
    print(current_gen.scoreboard())
    print("")

    current_gen = current_gen.create_next_gen()
    current_gen.reset_all_scores()
