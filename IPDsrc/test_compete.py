from unittest import TestCase
from data import *


class TestCompete(TestCase):
    def test1(self):
        nice = Player(kantian)
        mean = Player(always_defect)
        compete(nice, mean, 5)
        assert(nice.score == 0 and mean.score == 15)

    def test2(self):
        mean = Player(always_defect)
        tft = Player(tit_for_tat)
        compete(tft, mean, 10)
        assert(mean.score == 12 and tft.score == 9)

    def test3(self):
        mean = Player(always_defect)
        tf2t = Player(tit_for_2tats)
        compete(mean, tf2t, 10)
        assert(mean.score == 14 and tf2t.score == 8)

        
