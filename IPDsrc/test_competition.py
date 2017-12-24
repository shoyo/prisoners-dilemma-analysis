from unittest import TestCase
from data import *
NUM_ROUNDS = 10


class TestCompetition(TestCase):
    def test1(self):
        p1 = Kantian()
        p2 = Kantian()
        p3 = Kantian()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        print("Got: " + str(test.scoreboard()))
        assert test.scoreboard() == [40, 40, 40]

    def test2(self):
        p1 = AlwaysDefect()
        p2 = AlwaysDefect()
        p3 = AlwaysDefect()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        print("Got: " + str(test.scoreboard()))
        assert test.scoreboard() == [20, 20, 20]

    def test3(self):
        p1 = Kantian()
        p2 = AlwaysDefect()
        p3 = TitForTat()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        print("Got: " + str(test.scoreboard()))
        assert test.scoreboard() == [20, 42, 29]

    def test4(self):
        p1 = TitForTat()
        p2 = TitForTat()
        p3 = AlwaysDefect()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        print("Got: " + str(test.scoreboard()))
        assert test.scoreboard() == [29, 29, 24]

    def test5(self):
        p1 = TitFor2Tats()
        p2 = AlwaysDefect()
        p3 = Pavlov()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        print("Got: " + str(test.scoreboard()))
        assert test.scoreboard() == [28, 26, 29]



