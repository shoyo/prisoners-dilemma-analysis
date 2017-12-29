from unittest import TestCase
from stratdata import *
from gendata import *


class TestGenLogic(TestCase):
    def test1(self):
        p1 = Player(20)
        p2 = Player(45)
        p3 = Player(35)
        pop_test = Population([p1, p2, p3])
        next_gen_test = pop_test.create_next_gen()
        print(next_gen_test)
        assert next_gen_test == Population([p2, p2, p2])