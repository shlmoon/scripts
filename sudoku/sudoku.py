# coding: utf-8
import re

GIRDCOUNT = 81
ROWS = 'ABCDEFGHI'
COLS = '123456789'


class SudokuException(Exception):
    """ Exception raised when puzzle is not solvable"""
    pass


class Sudoku(object):
    """docstring for Sudoku
    puzzle like:
    ... .9. .64
    ... ..3 .2.
    ... ..1 7..
    ..1 ... ...
    ..9 ... ...
    ... 9.7 64.
    ... 37. ..6
    ... .2. .78
    .1. 8.5 29.
    """
    def __init__(self, puzzle):
        puzzle = re.sub(r'[^0-9\.]', '', puzzle)
        if not len(puzzle) == GIRDCOUNT:
            raise ValueError('Puzzle must contain 9*9 digits')
        self.result = {
            '%s%s' % (ROWS[ceil % 9], COLS[ceil / 9]): val if not val in '0.' else '123456789' for ceil, val in enumerate(puzzle)
        }

    def _pruning(self, rows, cols, func):
        """ Perform given function on a given set of cells """
        area = {'%s%s' % (row, col): self.result[row + col] for row in rows for col in cols}
        func(area)

    def Pruning(self, func):
        for row in ROWS:
            self._pruning(row, COLS, func)
        for col in COLS:
            self._pruning(ROWS, col, func)
        for rows in ('ABC', 'DEF', 'GHI'):
            for cols in ('123', '456', '789'):
                self._pruning(rows, cols, func)

    def complexity(self):
        return len(''.join(self.result.values()))

    def solved(self):
        """ Check if puzzle is solved """
        return self.complexity() == GIRDCOUNT

    def simplify(self):
        def _simplify(area):
            options = dict()
            for val in area.values():
                options[val] = options.setdefault(val, 0) + 1

            for option, freq in options.items():
                optlen = len(option)
                if optlen == freq:
                    for loc in area.keys():
                        selfloc = self.result[loc]
                        if selfloc != option:
                            for opt in option:
                                if opt in selfloc:
                                    selfloc = selfloc.replace(opt, '')
                            self.result[loc] = selfloc
                elif optlen < freq:
                    raise SudokuException("Puzzle is not solvable")

        after, before = self.complexity(), 0
        while not before == after:
            self.Pruning(_simplify)
            after, before = self.complexity(), after
        return self.solved()

    def _sudoku(self):
        minopt = 2
        result_stack = []
        while minopt < 10:
            minopt_flag = False
            for ceil, opts in self.result.items():
                if len(opts) == minopt:
                    minopt_flag = True
                    break
            if not minopt_flag:
                minopt += 1
                continue

            result = {k: v for k, v in self.result.items()}
            result_stack.append(result)

            for opt in opts:
                self.result[ceil] = opt
                try:
                    if self.simplify():
                        return
                    minopt = 2
                    break
                except SudokuException:
                    self.result = result_stack.pop()
        del result_stack[:]

    def sudoku(self):
        if self.simplify():
            return
        self._sudoku()

    def output_string(self, has_simply=False):
        if not has_simply:
            self.sudoku()

        def _genRowResult(row):
            return ' '.join(
                [self.result[row + col] for col in COLS]
            )
        _result = [_genRowResult(row) for row in ROWS]
        _result = '\n'.join(_result)
        return '''%s''' % _result

    def output_result(self):
        self.sudoku()
        return self.result


sudo = Sudoku(
    """
    000 045 006
    400 096 507
    050 000 409
    900 000 300
    500 003 900
    000 000 000
    000 030 600
    000 000 005
    000 000 003
    """
)
print sudo.output_string()
