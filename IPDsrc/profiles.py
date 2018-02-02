# INITIAL GENERATION PROFILE
from stratdata import *
from gendata import *

""" Various initial conditions for analysis. """


def diverse():
    profile = []
    for i in range(50):
        profile.append(Kantian())
        profile.append(Defector())
        profile.append(TitFor2Tats())
        profile.append(MeanTitForTat())
        profile.append(WaryTitForTat())
        profile.append(Random())
        profile.append(Grudger())
        profile.append(Conniver())
        profile.append(Tester())

    return Population(profile)


def defectors_with_a_tft():
    profile = []
    for i in range(99):
        profile.append(Defector())
    profile.append(TitForTat())

    return Population(profile)


def defectors_with_some_tft():
    profile = []
    for i in range(200):
        profile.append(Defector())
    for i in range(200):
        profile.append(Grudger())

    return Population(profile)


def kantian_with_few_defectors():
    profile = []
    for i in range(50):
        profile.append(Kantian())
    for i in range(50):
        profile.append(Defector())

    return Population(profile)


def defectors_with_some_kantians():
    profile = []
    for i in range(90):
        profile.append(Defector())
    for i in range(10):
        profile.append(Kantian())

    return Population(profile)


def kantian_with_tft():
    profile = []
    for i in range(50):
        profile.append(Kantian())
        profile.append(TitForTat())

    return Population(profile)


def tfts_with_tester():
    profile = []
    for i in range(50):
        profile.append(TitForTat())
        profile.append(TitFor2Tats())
        profile.append(Grudger())
        profile.append(MeanTitForTat())
        profile.append(Tester())
        profile.append(Conniver())

    return Population(profile)


def tft_test1():
    profile = []
    for i in range(50):
        profile.append(Kantian())
        profile.append(TitForTat())
        profile.append(TitFor2Tats())
        profile.append(Conniver())
        profile.append(Tester())

    return Population(profile)
