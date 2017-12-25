# POPULATION/GENERATION CLASS, TOURNAMENT EXECUTIONS
from copy import deepcopy


####################
# Population Class #
####################

class Population(object):
    """An object that represents a group of players.
    Manages players in a list."""

    def __init__(self, members):
        self.members = members

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

    def scoreboard(self):
        return [str(member.name) + ": " + str(member.score) for member in self.members]

    def reset_all_scores(self):
        for member in self.members:
            member.reset_score()

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

    def sort(self):
        """ Sorts members from highest to lowest with regards to score."""
        return Population(sorted(self, key=lambda member: member.score, reverse=True))

    def top_half(self):
        """ Returns top half of given population. """
        return Population(self[0: len(self) // 2])

    def create_next_gen(self):
        """
        Returns the next generation based on the successful members of
        current population. More specifically, the top 50% of the population
        (with respect to score) "breed", and 2 copies of each are appended
        to the next generation.
        """
        next_gen = Population([])
        sorted_population = self.sort()
        population_size = len(self)

        for member in sorted_population.top_half():
            next_gen.append(deepcopy(member))
            next_gen.append(deepcopy(member))

        # if population size is odd, the member at the 50% mark is
        # appended only once, to maintain population size
        if population_size % 2 != 0:
            next_gen.append(sorted_population[population_size // 2])

        return next_gen


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
