# INITIAL GENERATION PROFILE
from stratdata import *
from gendata import *

""" Various initial conditions for analysis. """


def diverse():
    profile = []
    profile.append(Kantian())
    profile.append(Defector())
    profile.append(TitForTat())
    profile.append(TitFor2Tats())
    profile.append(MeanTitForTat())
    profile.append(Random())

    return Population(profile)


def cruel_world_with_a_tft():
    return None


def cruel_world_with_some_tft():
    return None


def kantian_with_few_defectors():
    return None


def defectors_with_few_kantians():
    return None
