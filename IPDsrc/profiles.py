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
    profile.append(WaryTitForTat())
    profile.append(Random())

    return Population(profile)


def cruel_world_with_a_tft():
    profile = []
    for i in range(99):
        profile.append(Defector())
    profile.append(TitForTat())

    return Population(profile)


def cruel_world_with_few_tft():
    profile = []
    for i in range(80):
        profile.append(Defector())
    for i in range(20):
        profile.append(TitForTat())

    return Population(profile)


def kantian_with_few_defectors():
    profile = []
    for i in range(97):
        profile.append(Kantian())
    for i in range(3):
        profile.append(Defector())

    return Population(profile)


def defectors_with_some_kantians():
    profile = []
    for i in range(70):
        profile.append(Defector())
    for i in range(30):
        profile.append(Kantian())

    return Population(profile)
