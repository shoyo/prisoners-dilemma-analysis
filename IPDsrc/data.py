from random import randint


# Player class
class Player(object):
    def __init__(self, strategy):
        self.strategy = strategy
        self.score = 0
        self.is_first_turn = True
        self.last_two_actions = [True, True]
        self.never_defected = True
        self.gained_last_turn = True
        self.has_tested = False
        self.total_testing_turns = 0
        self.has_retaliated = False

    def last_action(self):
        return self.last_two_actions[0]

    def last_last_action(self):
        return self.last_two_actions[1]

    def reset(self):
        self.score = 0
        self.is_first_turn = True
        self.last_two_actions = [True, True]
        self.never_defected = True
        self.gained_last_turn = True
        self.has_tested = False
        self.total_testing_turns = 0
        self.has_retaliated = False


# Population class, a collection of players
class Population(object):
    def __init__(self, members):
        self.members = members

    def first_member(self):
        if not self.members:
            return None
        else:
            return self.members[0]

    def excluding(self, member):
        temp = self.members()
        temp.remove(member)
        return temp

    def remove(self, member):
        self.members.remove(member)

    def get_members(self):
        return self.members


# Strategies
def kantian(self, opponent):
    """
    'Act only according to that maxim whereby you can at the same time
    will that it should become a universal law.'
    Always cooperates.
    """
    return True


def always_defect(self, opponent):
    """Always defects."""
    return False


def tit_for_tat(self, opponent):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last move was defect."""
    return opponent.last_action


def tit_for_2tats(self, opponent):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last two moves were defect."""
    return opponent.last_action or opponent.last_last_action


def mean_tit_for_tat(self, opponent):
    """Identical to tit_for_tat. However, occasionally tries to take advantage of opponent
    by defecting."""
    if randint(0, 50) == 0:
        return False
    else:
        return tit_for_tat(self, opponent)


def wary_tit_for_tat(self, opponent):
    """Starts by defecting. After that, same as tit_for_tat."""
    if self.is_first_turn:
        self.is_first_turn = False
        return False
    else:
        return tit_for_tat(self, opponent)


def tester(self, opponent):
    """Plays like tit_for_tat, but tests opponent's strategy by occasionally defecting,
    and following up with a turn of cooperation. If the opponent does not retaliate, continues
    alternating between defecting and cooperating."""
    return None


def conniving(self, opponent):
    """Plays like tit_for_tat, but tests opponent's strategy by occasionally defecting,
    and following up with two turns of cooperation. If opponent does not defect back within
    2 turns of it defecting, it continues defecting."""
    if self.has_tested:
        if opponent.has_retaliated:
            return tit_for_tat(self, opponent)
        elif self.total_testing_turns < 3:
            self.total_testing_turns += 1
            if not opponent.last_action:
                opponent.has_retaliated = True
                return tit_for_tat(self, opponent)
            return True
        else:
            return False
    else:
        if randint(0, 50) == 0:
            self.has_tested = True
            return False
        else:
            return tit_for_tat(self, opponent)


def grudger(self, opponent):
    """Starts by cooperating. After that, always cooperate until opponent defects.
    After that, always defects."""
    return opponent.never_defected


def pavlov(self, opponent):
    """Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise, does opposite action."""
    if self.gained_last_turn:
        return self.last_action
    else:
        return not self.last_action


def clan_grunt(self, opponent):
    """Always starts with sequence: DCCCD. If opponent starts with same sequence, cooperates
    for the rest of the game to maximize clan leader's gains. Otherwise plays tit_for_tat."""
    return None


def clan_leader(self, opponent):
    """Always starts with sequence: DCCCD. If opponent starts with same sequence, defects
    for the rest of the game to maximize its own gains. Otherwise plays tit_for_tat."""
    return None


def random(self, opponent):
    """Cooperates or defects at a 50/50 chance."""
    return randint(0, 1) == 0


# Executions
def compete(p1, p2, n):
    """Adjusts the scores of player1 and player2 after interacting n times
    Example:
    >>> p1 = Player(kantian)
    >>> p2 = Player(always_defect)
    >>> compete(p1, p2, 1)
    >>> (p1.score, p2.score)
    (0, 3)
    >>> p3 = Player(tit_for_tat)
    >>> compete(p1, p3, 2)
    >>> (p1.score, p3.score)
    (4, 4)
    """
    for i in range(0, n):
        p1_action, p2_action = p1.strategy(p1, p2), p2.strategy(p2, p1)
        p1.last_action, p1.last_last_action = p1_action, p1.last_action
        p2.last_action, p2.last_last_action = p2_action, p2.last_action

        if p1_action and p2_action:
            p1.score += 2
            p2.score += 2
            p1.gained_last_turn, p2.gained_last_turn = True, True
        elif p1_action and not p2_action:
            p2.score += 3
            p2.never_defected = False
            p1.gained_last_turn, p2.gained_last_turn = False, True
        elif not p1_action and p2_action:
            p1.score += 3
            p1.never_defected = False
            p1.gained_last_turn, p2.gained_last_turn = True, False
        else:
            p1.score += 1
            p2.score += 1
            p1.never_defected, p2.never_defected = False, False
            p1.gained_last_turn, p2.gained_last_turn = True, True


def round_robin(population):
    """Competes each player of population against every other player in population."""
    p1 = population.first_member()
    for player in population.excluding(p1):
        compete(p1, player)
    round_robin(population.remove(p1))
