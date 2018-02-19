from copy import deepcopy
from random import randint


class Player(object):
    def __init__(self, score=0):
        self.name = None
        self.score = score
        self.last_action = None
        self.this_action = None
        self.opponent = None

    def new_match_against(self, opponent):
        self.last_action = None
        self.this_action = None
        self.opponent = opponent

    def reset_score(self):
        self.score = 0

    def action(self):
        self.this_action = self.decide_action()
        return self.this_action

    def decide_action(self):
        return True

    def update_last_action(self):
        self.last_action = self.this_action
        self.this_action = None

    def add_points(self, points):
        self.score += points


class Kantian(Player):
    """ Always cooperates. """
    def __init__(self, score=0):
        super().__init__()
        self.name = "Kantian"


class Defector(Player):
    """Always defects."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Defector"

    def decide_action(self):
        return False


class TitForTat(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last move was defect."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Tit for Tat"
        self.is_first_move = True

    def decide_action(self):
        if not self.is_first_move:
            return self.opponent.last_action
        else:
            self.is_first_move = False
            return True

    def new_match_against(self, opponent):
        self.is_first_move = True
        super().new_match_against(opponent)


class TitFor2Tats(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last two moves were defect."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Tit for 2 Tats"
        self.opponent_last_actions = (True, True)

    def decide_action(self):
        if self.opponent.last_action is None:
            self.opponent_last_actions = (self.opponent_last_actions[1], True)
        else:
            self.opponent_last_actions =\
                (self.opponent_last_actions[1], self.opponent.last_action)
        return self.opponent_last_actions[0] or self.opponent_last_actions[1]

    def new_match_against(self, opponent):
        self.opponent_last_actions = (True, True)
        super().new_match_against(opponent)


class MeanTitForTat(TitForTat):
    """ Tit for Tat, but occasionally defects. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Mean Tit for Tat"

    def decide_action(self):
        if not randint(0, 5):
            return False
        else:
            return super().decide_action()


class WaryTitForTat(TitForTat):
    """ Tit for Tat, but starts by defecting. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Wary Tit for Tat"

    def decide_action(self):
        if self.is_first_move:
            self.is_first_move = False
            return False
        else:
            return super().decide_action()


class Tester(TitForTat):
    """ Tit for 2 Tats exploiter. Tit for Tat, but occasionally defects
    then cooperates for a turn. If the opponent doesn't retaliate immediately,
    alternates between cooperating and defecting. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Tester"
        self.turn = 0
        self.testing_turn = 0
        self.opponent_retaliated = False

    def decide_action(self):
        self.turn += 1
        if self.testing_turn == 0 and not randint(0, 5):
            self.testing_turn += 1
            return False
        elif 0 < self.testing_turn <= 1:
            self.testing_turn += 1
            if not self.opponent.last_action:
                self.opponent_retaliated = True
            return True
        elif self.testing_turn > 1 and not self.opponent_retaliated:
            return self.turn % 2
        else:
            return super().decide_action()

    def new_match_against(self, opponent):
        self.turn = 0
        self.testing_turn = 0
        self.opponent_retaliated = False
        return super().new_match_against(opponent)


class Conniver(TitForTat):
    """ Kantian exploiter. Tit for Tat, but occasionally defects then cooperates
    for 2 turns. If opponent doesn't retaliate within 2 turns, defects until end. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Conniver"
        self.testing_turn = 0
        self.opponent_retaliated = False

    def decide_action(self):
        if self.testing_turn == 0 and not randint(0, 5):
            self.testing_turn += 1
            return False
        elif 0 < self.testing_turn <= 2:
            self.testing_turn += 1
            if not self.opponent.last_action:
                self.opponent_retaliated = True
            return True
        elif self.testing_turn > 2 and not self.opponent_retaliated:
            return False
        else:
            return super().decide_action()

    def new_match_against(self, opponent):
        self.testing_turn = 0
        self.opponent_retaliated = False
        return super().new_match_against(opponent)


class Grudger(Player):
    """ Cooperates until opponent defects. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Grudger"
        self.opponent_never_defected = True

    def decide_action(self):
        if not self.opponent.last_action:
            self.opponent_never_defected = False
        return self.opponent_never_defected

    def new_match_against(self, opponent):
        self.opponent_never_defected = True
        super().new_match_against(opponent)


class Pavlovian(Player):
    """ Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise does opposite action. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Pavlovian"
        self.last_score = 0

    def decide_action(self):
        temp = self.last_score
        self.last_score = self.score
        if self.score > temp:
            return self.last_action
        else:
            return not self.last_action

    def new_match_against(self, opponent):
        self.last_action = True
        super().new_match_against(opponent)


class ClanGrunt(Player):
    """ Tit for Tat, but starts with sequence: DCCCD. If opponent starts with same
    sequence, cooperates until end. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Clan Grunt"


class ClanLeader(Player):
    """ Tit for Tat, but starts with sequence: DCCCD. If opponent starts with same
    sequence, defects until end. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Clan Leader"


class Random(Player):
    """ Cooperates or defects at 50/50. """
    def __init__(self, score=0):
        super().__init__()
        self.name = "Random"

    def decide_action(self):
        return randint(0, 1)


# -------------------------------------------------- #

class Population(object):

    def __init__(self, members: list):
        self.members = members

    def __repr__(self):
        return "{}".format(self.members)

    def __iter__(self):
        return iter(self.members)

    def __len__(self):
        return len(self.members)

    def __getitem__(self, item):
        return self.members[item]

    def append(self, member):
        self.members.append(member)

    def scores(self):
        return [member.score for member in self.members]

    def reset_all_scores(self):
        for member in self.members:
            member.reset_score()

    def first_member(self):
        return self.members[0]

    def excluding(self, excluded_member):
        copy = self.members[:]
        return Population([member for member in copy if member is not excluded_member])

    def is_empty(self):
        return not self.members

    def total_score(self):
        total = 0
        for member in self.members:
            total += member.score
        return total

    def create_next_gen(self):
        """ Returns the next generation based on the current population.

        Example --
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

    def distribution(self):
        distribution = {}
        total_num_players = 0

        for member in self.members:
            if member.name in distribution:
                distribution[member.name] += 1
            else:
                distribution[member.name] = 1
            total_num_players += 1

        for member in distribution.keys():
            prop = distribution[member] / total_num_players * 100
            distribution[member] = prop

        return distribution

    def unique_strats(self):
        return [member for member in self.distribution().keys()]


def play_round(p1, p2):
    """ Payoffs:
        Both cooperate              -> both +2 pts
        Both defect                 -> both +1 pts
        One cooperates, one defects -> cooperator +0 pts, defector +3 pts
    """
    p1_action, p2_action = p1.action(), p2.action()

    if p1_action and p2_action:
        p1.add_points(2)
        p2.add_points(2)
    elif p1_action and not p2_action:
        p2.add_points(3)
    elif not p1_action and p2_action:
        p1.add_points(3)
    else:
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
    of the population for num_rounds each.
    """
    if not population.is_empty():
        other_members = population.excluding(population.first_member())
        for member in other_members:
            play_several_rounds(population.first_member(), member, num_rounds)
        round_robin(other_members, num_rounds)
