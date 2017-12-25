# PLAYER, STRATEGY DATA
from random import randint


#####################
# Base Player class #
#####################

class Player(object):
    def __init__(self, score=0):
        self.name = None
        self.score = score
        self.last_action = None
        self.this_action = None
        self.opponent = None
        self.successful = False

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


#####################################
# Strategies (inherits from Player) #
#####################################

class Kantian(Player):
    """
    'Act only according to that maxim whereby you can at the same time
    will that it should become a universal law.'
    Always cooperates.
    """
    def __init__(self):
        super().__init__()
        self.name = "Kantian"

    def decide_action(self):
        return True


class Defector(Player):
    """Always defects."""

    def __init__(self):
        super().__init__()
        self.name = "Defector"

    def decide_action(self):
        return False


class TitForTat(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last move was defect."""

    first_move = True

    def __init__(self):
        super().__init__()
        self.name = "Tit for Tat"

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

    def __init__(self):
        super().__init__()
        self.name = "Tit for 2 Tats"

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

    def __init__(self):
        super().__init__()
        self.name = "Mean Tit for Tat"

    def decide_action(self):
        if not randint(0, 50):
            return False
        else:
            return super().decide_action()


class WaryTitForTat(TitForTat):
    """Starts by defecting. After that, same as Tit for Tat."""

    first_move = False

    def __init__(self):
        super().__init__()
        self.name = "Wary Tit for Tat"

    def decide_action(self):
        return super().decide_action()


class Tester(TitForTat):
    """Plays like Tit for Tat, but tests opponent's strategy by occasionally defecting,
    and following up with a turn of cooperation. If the opponent does not retaliate, continues
    alternating between defecting and cooperating."""

    def __init__(self):
        super().__init__()
        self.name = "Tester"


class Conniver(TitForTat):
    """Plays like Tit for Tat, but tests opponent's strategy by occasionally defecting,
    and following up with two turns of cooperation. If opponent does not defect back within
    2 turns of it defecting, it continues defecting."""

    has_tested = False
    opponent_retaliated = False

    def __init__(self):
        super().__init__()
        self.name = "Conniver"

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

    def __init__(self):
        super().__init__()
        self.name = "Grudger"

    def decide_action(self):
        if not self.opponent.last_action:
            self.opponent_never_defected = False
        return self.opponent_never_defected

    def new_match_against(self, opponent):
        self.opponent_never_defected = True
        super().new_match_against(opponent)


class Pavlovian(Player):
    """Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise, does opposite action."""

    last_score = 0
    last_action = False

    def __init__(self):
        super().__init__()
        self.name = "Pavlovian"

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

    def __init__(self):
        super().__init__()
        self.name = "Clan Grunt"


class ClanLeader(Player):
    """Always starts with sequence: DCCCD. If opponent starts with same sequence, defects
    for the rest of the game to maximize its own gains. Otherwise plays Tit for Tat."""

    def __init__(self):
        super().__init__()
        self.name = "Clan Leader"


class Random(Player):
    """Cooperates or defects at a 50/50 chance."""

    def __init__(self):
        super().__init__()
        self.name = "Random"

    def decide_action(self):
        return randint(0, 1)
