# coding: utf-8
import random


class Node(object):
    """docstring for Node"""
    def __init__(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError('Node must be int')
        if x > 9 or x <= 0 or y > 9 or y <= 0:
            raise ValueError('Node must be in 0, 9')
        self.x = x
        self.y = y


class Sudoku(object):
    """docstring for Sudoku"""
    def __init__(self, node_list):
        for node in node_list:
            if not isinstance(node, Node):
                raise ValueError('node Error')
        self.node_list = node_list
        self.node_all = [
            [node.y for node in node_list if node.x == i] for i in range(1, 10)
        ]
        self.node_count = [len(self.node_all[i]) for i in range(1, 10)]

    def run(self):
        match_list = [x for x in range(1, 10)]
        for i in range(1, 10):
            unexact_list = self.node_all[i]
            count = len(unexact_list)
            if not count == 9:
                value = random.choice(list(set(match_list) - set(unexact_list)))

        pass

    @staticmethod
    def generator_sudoku(cls, lst):
        return cls.__new__(cls, [Node(x, y) for x, y in lst])
