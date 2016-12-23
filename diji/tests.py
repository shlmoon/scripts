# coding: utf-8

from .dk import Dkalgorithm, MaxCost
from unittest import TestCase


class Dktestcase(TestCase):
    def test_run(self):
        rule = {
            'A': {'B': 10, 'C': MaxCost, 'D': MaxCost, 'E': 20, 'F': MaxCost},
            'B': {'A': 10, 'C': 16, 'D': 30, 'E': MaxCost, 'F': 20},
            'C': {'A': MaxCost, 'B': 20, 'D': MaxCost, 'E': 20, 'F': 10},
            'D': {'A': MaxCost, 'B': 30, 'C': MaxCost, 'E': 10, 'F': 30},
            'E': {'A': 20, 'B': MaxCost, 'C': 20, 'D': 10, 'F': MaxCost},
            'F': {'A': MaxCost, 'B': 20, 'C': 10, 'D': 30, 'E': MaxCost}
        }
        source = 'A'
        nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        dk = Dkalgorithm(rule=rule, source=source, nodes=nodes)
        dk.run()

        print dk.min_cost
        print dk.step
        self.assertEqual(1, 0)
