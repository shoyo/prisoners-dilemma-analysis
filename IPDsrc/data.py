# PLAYER, STRATEGY, TOURNAMENT EXECUTION DATA
from random import randint


#####################
# Main Player class #
#####################

class Player(object):
    def __init__(self, score=0):
        self.score = score
        self.last_action = None
        self.this_action = None
        self.opponent = None

    def new_match_against(self, opponent):
        self.last_action = None
        self.opponent = opponent
        self.this_action = None

    def reset_score(self, score=0):
        self.score = score

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


###########################################
# Strategies (Inherits from Player class) #
###########################################

class Kantian(Player):
    """
    'Act only according to that maxim whereby you can at the same time
    will that it should become a universal law.'
    Always cooperates.
    """

    def decide_action(self):
        return True


class AlwaysDefect(Player):
    """Always defects."""

    def decide_action(self):
        return False


class TitForTat(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last move was defect."""

    first_move = True

    def decide_action(self):
        if not self.first_move:
            return self.opponent.last_action
        self.first_move = False
        return True

    def new_match_against(self, opponent):
        self.first_move = True
        super().new_match_against(opponent)


class TitFor2Tats(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last two moves were defect."""

    opponent_last_actions = (True, True)

    def decide_action(self):
        if self.opponent.last_action is None:
            self.opponent_last_actions = (self.opponent_last_actions[1], True)
        else:
            self.opponent_last_actions = (self.opponent_last_actions[1], self.opponent.last_action)
        return self.opponent_last_actions[0] or self.opponent_last_actions[1]

    def new_match_against(self, opponent):
        self.opponent_last_actions = (True, True)
        super().new_match_against(opponent)


class MeanTitForTat(TitForTat):
    """Identical to Tit for Tat. However, occasionally tries to take advantage of opponent
    by defecting."""

    def decide_action(self):
        action = super().decide_action()
        if randint(0, 50) == 0:
            return False
        else:
            return action


class WaryTitForTat(TitForTat):
    """Starts by defecting. After that, same as Tit for Tat."""

    first_move = False

    def decide_action(self):
        return super().decide_action()


class Tester(TitForTat):
    """Plays like Tit for Tat, but tests opponent's strategy by occasionally defecting,
    and following up with a turn of cooperation. If the opponent does not retaliate, continues
    alternating between defecting and cooperating."""


class Conniving(TitForTat):
    """Plays like Tit for Tat, but tests opponent's strategy by occasionally defecting,
    and following up with two turns of cooperation. If opponent does not defect back within
    2 turns of it defecting, it continues defecting."""

    has_tested = False
    opponent_retaliated = False

    def decide_action(self):
        return super().decide_action()

    def new_match_against(self, opponent):
        self.has_tested = False
        self.opponent_retaliated = False
        return super().new_match_against(opponent)


class Grudger(Player):
    """Starts by cooperating. After that, always cooperate until opponent defects.
    After that, always defects."""

    opponent_never_defected = True

    def decide_action(self):
        if not self.opponent.last_action:
            self.opponent_never_defected = False
        return self.opponent_never_defected

    def new_match_against(self, opponent):
        self.opponent_never_defected = True
        super().new_match_against(opponent)


class Pavlov(Player):
    """Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise, does opposite action."""

    last_score = 0
    last_action = False

    def decide_action(self):
        gained = self.score > self.last_score
        self.last_score = self.score
        if gained:
            return self.last_action
        else:
            return not self.last_action

    def new_match_against(self, opponent):
        self.last_score = 0
        self.last_action = False
        super().new_match_against(opponent)


class ClanGrunt(Player):
    """Always starts with sequence: DCCCD. If opponent starts with same sequence, cooperates
    for the rest of the game to maximize Clan Leader's gains. Otherwise plays Tit for Tat."""


class ClanLeader(Player):
    """Always starts with sequence: DCCCD. If opponent starts with same sequence, defects
    for the rest of the game to maximize its own gains. Otherwise plays Tit for Tat."""


class Random(Player):
    """Cooperates or defects at a 50/50 chance."""

    def decide_action(self):
        return randint(0, 1)


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

    def get_members(self):
        return self.members

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

    def scoreboard(self):
        return [member.score for member in self.members]


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
    for i in range(0, num_rounds):
        play_round(p1, p2)


def round_robin(population, num_rounds):
    """Competes every member of the population with every other member
    of the population for num_rounds each."""
    if not population.is_empty():
        other_members = population.excluding(population.first_member())
        for member in other_members:
            play_several_rounds(population.first_member(), member, num_rounds)
        round_robin(other_members, num_rounds)
