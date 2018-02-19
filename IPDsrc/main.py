# TOURNAMENT AND GRAPHING LOGIC
from profiles import *
import numpy as np
import matplotlib.pyplot as plt

NUM_GENS = 35
NUM_ROUNDS = 100
INITIAL_PROFILE = tft_test1()


def run_simulation(initial_gen, num_gens, num_rounds):
    """ Takes Population object made by 'function' in profiles.py and returns
    values for each strategy.
    """


def exec_print(initial_gen, num_gens, num_rounds):
    """Executes and prints out data for generational changes to initial population profile."""
    current_gen = initial_gen
    for gen in range(num_gens):
        print("Generation " + str(gen + 1) + ":")

        round_robin(current_gen, num_rounds)
        print("Distribution [%]:")
        print(current_gen.distribution())
        print("Final Scores:")
        print(current_gen.scoreboard())
        print()

        current_gen = current_gen.create_next_gen()
        current_gen.reset_all_scores()


def exec_plot(initial_gen, num_gens, num_rounds):
    """Executes and plots data for generational changes to initial population.
    Generation is plotted against each unique strategy's distribution."""
    all_strats = initial_gen.unique_strats()
    num_of_strats = len(all_strats)
    x = np.linspace(1, NUM_GENS, NUM_GENS)  # x-axis
    ys = np.zeros((num_of_strats, NUM_GENS))  # y-axis

    # Initializing first generation distribution
    for i in range(num_of_strats):
        ys[i][0] = initial_gen.distribution()[all_strats[i]]

    # Iteratively finding successive gen distributions up to num_gens
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

    # Plotting
    for i in range(num_of_strats):
        plt.plot(x, ys[i, :], label=all_strats[i])
    plt.title('Changes to population distribution with respect to time')
    plt.xlabel('Generation')
    plt.ylabel('Population Distribution [%]')
    plt.legend()
    plt.show()