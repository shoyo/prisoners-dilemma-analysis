from random import randint

################
# Player Types #
################


class Player(object):
    def __init__(self, score=0):
        self.score = score
        self.last_action = None
        self.this_action = None
        self.opponent = None

    def new_match(self, opponent, score=0):
        self.score = score
        self.last_action = None
        self.opponent = opponent
        self.this_action = None

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

    def new_match(self, opponent, score=0):
        self.first_move = True
        super().new_match(opponent, score)


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

    def new_match(self, opponent, score=0):
        self.opponent_last_actions = (True, True)
        super().new_match(opponent, score)


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

    def new_match(self, opponent, score=0):
        self.has_tested = False
        self.opponent_retaliated = False
        return super().decide_action()


class Grudger(Player):
    """Starts by cooperating. After that, always cooperate until opponent defects.
    After that, always defects."""

    opponent_never_defected = True

    def decide_action(self):
        if not self.opponent.last_action:
            self.opponent_never_defected = False
        return self.opponent_never_defected

    def new_match(self, opponent, score=0):
        self.opponent_never_defected = True
        super().new_match(opponent, score)


class Pavlov(Player):
    """Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise, does opposite action."""

    last_score = 0

    def decide_action(self):
        gained = self.score > self.last_score
        self.last_score = self.score
        if gained:
            return self.last_action
        else:
            return not self.last_action

    def new_match(self, opponent, score=0):
        self.last_score = 0
        super().new_match(opponent, score)


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


def compete(p1, p2, n):
    p1.new_match(p2)
    p2.new_match(p1)
    for i in range(0, n):
        play_round(p1, p2)


def round_robin(population):
