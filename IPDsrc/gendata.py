# POPULATION/GENERATION CLASS, TOURNAMENT EXECUTIONS
from random import randint
from copy import deepcopy


####################
# Population Class #
####################

class Population(object):
    """An object that represents a group of players.
    Manages players in a list."""

    def __init__(self, members):
        self.members = members

    # Methods to manipulate Population class as lists:

    def __repr__(self):
        return "{}".format(self.members)

    def __iter__(self):
        return iter(self.members)

    def __len__(self):
        return len(self.members)

    def __getitem__(self, item):
        return self.members[item]

    def append(self, item):
        self.members.append(item)

    # Methods for score manipulation:

    def scoreboard(self):
        return [str(member.name) + ": " + str(member.score) for member in self.members]

    def scores(self):
        return [member.score for member in self.members]

    def reset_all_scores(self):
        for member in self.members:
            member.reset_score()

    # Methods for 'round_robin' function:

    def first_member(self):
        if not self.members:
            raise Exception("There are no players in this population.")
        else:
            return self.members[0]

    def excluding(self, excluded_member):
        copy = self.members[:]
        return Population([member for member in copy if member is not excluded_member])

    def is_empty(self):
        return not self.members

    # Methods for generation logic:

    def total_score(self):
        """ Returns the sum of all scores in the population. """
        total = 0
        for member in self.members:
            total += member.score
        return total

    def create_next_gen(self):
        """
        Returns the next generation based on the current population.
        Each member of the next generation is determined by chance proportionate to
        each member of the current population's relative final score.

        For example:
        Population is comprised of Player 1 and Player 2.
        Player 1 has a final score of 10. Player 2 has a final score of 20.
        Each new member of the new generation has a 33% chance (1/3) chance of being an
        offspring of Player 1, and a 67% chance (2/3) of being an offspring of Player 2.
        """
        next_gen = Population([])

        total_score = self.total_score()
        for i in range(len(self.members)):
            rand = randint(1, total_score)
            curr = 0
            for member in self.members:
                curr += member.score
                if rand <= curr:
                    next_gen.append(deepcopy(member))
                    break

        return next_gen

    # Methods for checking population data

    def distribution(self):
        distribution = {}
        total_num_players = 0

        for member in self.members:
            if member.name in distribution:
                distribution[member.name] += 1
            else:
                distribution[member.name] = 1
            total_num_players += 1

        for key in distribution.keys():
            prop = distribution[key] / total_num_players * 100
            distribution[key] = str("%.2f" % prop) + "%"

        return distribution

    def check_for_convergence(self):
        return None


#########################
# Tournament Executions #
#########################

""" Prisoner's Dilemma Payoffs:
    Both cooperate              -> both +2 pts
    Both defect                 -> both +1 pts
    One cooperates, one defects -> cooperator +0 pts, defector +3 pts
"""


def play_round(p1, p2):
    p1_action, p2_action = p1.action(), p2.action()

    if p1_action and p2_action:  # Both players cooperate
        p1.add_points(2)
        p2.add_points(2)
    elif p1_action and not p2_action:  # Player 1 cooperates and Player 2 defects
        p2.add_points(3)
    elif not p1_action and p2_action:  # Player 2 cooperates and Player 1 defects
        p1.add_points(3)
    else:  # Both players defect
        p1.add_points(1)
        p2.add_points(1)

    p1.update_last_action()
    p2.update_last_action()


def play_several_rounds(p1, p2, num_rounds):
    p1.new_match_against(p2)
    p2.new_match_against(p1)
    for i in range(num_rounds):
        play_round(p1, p2)


def round_robin(population, num_rounds):
    """Competes every member of the population with every other member
    of the population for num_rounds each."""
    if not population.is_empty():
        other_members = population.excluding(population.first_member())
        for member in other_members:
            play_several_rounds(population.first_member(), member, num_rounds)
        round_robin(other_members, num_rounds)
