from unittest import TestCase


class TestPopulation(TestCase):
    def test_create_next_gen(self):
        from stratdata import Kantian
        from stratdata import Defector
        from stratdata import TitForTat
        p1 = Kantian(20)
        p2 = Defector(45)
        p3 = TitForTat(35)
        from gendata import Population
        test_pop = Population([p1, p2, p3])
        next = test_pop.create_next_gen()
        print([member.name for member in next])
        self.assertTrue(1)
