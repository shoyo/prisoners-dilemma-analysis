from copy import deepcopy


class Population(object):
    """An object that represents a generation of players. Contains all players
    in a list."""
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

    def sort(self):
        """ Returns a ascending list of members with respect to score. """
        return Population(sorted(self, key=lambda member: member.value, reverse=True))

    def top_half(self):
        """ Returns top half of given population. """
        return Population(self[0:len(self) // 2])

    def create_next_gen(self):
        """
        Returns the next generation based on the successful members of
        current generation. More specifically, the top 50% of the population
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


class Number(object):
    def __init__(self, value):
        self.value = value
        self.name = ""

    def __repr__(self):
        return "{}".format(self.name)


class Even(Number):
    def __init__(self, value):
        super().__init__(value)
        self.name = "Even"


class Odd(Number):
    def __init__(self, value):
        super().__init__(value)
        self.name = "Odd"


class Big(Number):
    def __init__(self, value):
        super().__init__(value)
        self.name = "Big"


class Small(Number):
    def __init__(self, value):
        super().__init__(value)
        self.name = "Small"



###########
# Testing #
###########

print("Current Generation:")
p1 = Small(1)
p2 = Small(10)
p3 = Even(32)
p4 = Odd(45)
p5 = Small(-35)
p6 = Odd(17)
p7 = Big(1717)
members = [p1, p2, p3, p4, p5, p6, p7]
curr_gen = Population(members)
print(curr_gen)

print("Next Generation:")
next_gen = curr_gen.create_next_gen()
print(next_gen)


####################
# Running Doctests #
####################

# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
