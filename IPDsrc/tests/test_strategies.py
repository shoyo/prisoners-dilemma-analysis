from unittest import TestCase
from stratdata import *
from gendata import *
NUM_ROUNDS = 10


class TestStrategies(TestCase):
    def test1(self):
        p1 = Kantian()
        p2 = Kantian()
        p3 = Kantian()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        result = test.scores()
        print("Got: " + str(result))
        self.assert result == [40, 40, 40]

    def test2(self):
        p1 = Defector()
        p2 = Defector()
        p3 = Defector()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        result = test.scores()
        print("Got: " + str(result))
        self.assert result == [20, 20, 20]

    def test3(self):
        p1 = Kantian()
        p2 = Defector()
        p3 = TitForTat()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        result = test.scores()
        print("Got: " + str(result))
        assert result == [20, 42, 29]

    def test4(self):
        p1 = TitForTat()
        p2 = TitForTat()
        p3 = Defector()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        result = test.scores()
        print("Got: " + str(result))
        assert result == [29, 29, 24]

    def test5(self):
        p1 = Kantian()
        p2 = Defector()
        p3 = Pavlovian()
        test = Population([p1, p2, p3])
        round_robin(test, NUM_ROUNDS)
        result = test.scores()
        print("Got: " + str(result))
        assert result == [20, 42, 29]



