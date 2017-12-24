# TOURNAMENT AND GENERATIONAL LOGIC
from players import *
NUM_OF_GENS = 10
NUM_OF_ROUNDS = 200


class Generation(Population):
    def create_next_gen(self, last_gen):
        high_to_low(last_gen)
        most_fit =


current_gen = generate_initial_profile()
for i in range(0, NUM_OF_GENS):
    print("Generation " + str(i + 1) + ":")
    print("Pre:")
    print(current_gen.scoreboard())
    round_robin(current_gen, NUM_OF_ROUNDS)
    print("Post:")
    print(current_gen.scoreboard())
    current_gen = create_next_gen(current_gen)
