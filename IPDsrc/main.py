# TOURNAMENT AND GENERATIONAL LOGIC
from players import *
NUM_OF_GENS = 10
NUM_OF_ROUNDS = 200







current_gen = INITIAL_PROFILE()
for i in range(NUM_OF_GENS):
    print("Generation " + str(i + 1) + ":")
    print("Pre:")
    print(current_gen.scoreboard())
    round_robin(current_gen, NUM_OF_ROUNDS)
    print("Post:")
    print(current_gen.scoreboard())
    current_gen = current_gen.create_next_gen()
