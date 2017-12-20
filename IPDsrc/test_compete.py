from unittest import TestCase
from player import *


class TestCompete(TestCase):
    def test1(self):
        nice = Kantian()
        mean = AlwaysDefect()
        compete(nice, mean, 5)
        assert(nice.score == 0 and mean.score == 15)

    def test2(self):
        mean = AlwaysDefect()
        tft = TitForTat()
        compete(tft, mean, 10)
        assert(mean.score == 12 and tft.score == 9)

    def test3(self):
        mean = AlwaysDefect()
        tf2t = TitFor2Tats()
        compete(mean, tf2t, 10)
        assert(mean.score == 14 and tf2t.score == 8)

