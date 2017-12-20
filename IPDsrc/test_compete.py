from unittest import TestCase
from player import *


class TestCompete(TestCase):
    def test1(self):
<<<<<<< HEAD
        nice = Kantian()
        mean = AlwaysDefect()
=======
        nice = Player(kantian)
        mean = Player(always_defect)
>>>>>>> 269cd92026f682869a343952d0c17c438d359f9e
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

<<<<<<< HEAD
=======
        
>>>>>>> 269cd92026f682869a343952d0c17c438d359f9e
