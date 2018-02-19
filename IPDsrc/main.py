from profiles import *
import numpy as np
import matplotlib.pyplot as plt

NUM_GENS = 35
NUM_ROUNDS = 100
INITIAL_PROFILE = tft_test1()


def run_simulation(initial_gen, num_gens, num_rounds):
    pass


def execute_and_print(initial_gen, num_gens, num_rounds):
    current_gen = initial_gen
    for gen in range(num_gens):
        print("Generation " + str(gen + 1) + ":")

        round_robin(current_gen, num_rounds)
        print("Distribution [%]:")
        print(current_gen.distribution())
        print("Final Scores:")
        print([str(member.name) + ": " + str(member.score) for member in current_gen])
        print()

        current_gen = current_gen.create_next_gen()
        current_gen.reset_all_scores()


def execute_and_plot(initial_gen, num_gens, num_rounds):
    all_strats = initial_gen.unique_strats()
    num_of_strats = len(all_strats)
    x = np.linspace(1, NUM_GENS, NUM_GENS)
    ys = np.zeros((num_of_strats, NUM_GENS))

    for i in range(num_of_strats):
        ys[i][0] = initial_gen.distribution()[all_strats[i]]

    current_gen = initial_gen
    for gen in range(num_gens):
        round_robin(current_gen, num_rounds)
        current_gen = current_gen.create_next_gen()
        current_gen.reset_all_scores()

        dist = current_gen.distribution()
        i = 0
        for strat in all_strats:
            if strat in dist.keys():
                ys[i][gen] = dist[strat]
            i += 1

    for i in range(num_of_strats):
        plt.plot(x, ys[i, :], label=all_strats[i])
    plt.title('Changes to population distribution with respect to time')
    plt.xlabel('Generation')
    plt.ylabel('Population Distribution [%]')
    plt.legend()
    plt.show()


execute_and_plot(INITIAL_PROFILE, NUM_GENS, NUM_ROUNDS)
