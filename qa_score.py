# coding: utf-8
import itertools


class QaScore(object):

    def __init__(self, qa_num=4, genNum=30):
        self.qaNum = qa_num
        self.genNum = genNum

    def _caculate_result(self, a, b, c, d):
        _result = itertools.combinations_with_replacement(
            [a, b, c, d], self.qaNum
        )
        _result = set(sum(x) for x in _result)
        return _result

    def generator_data(self):
        return (
            (a, b, c, d) for a in xrange(1, self.genNum)
            for b in xrange(a + 1, self.genNum)
            for c in xrange(b + 1, self.genNum)
            for d in xrange(c + 1, self.genNum)
        )

    def process(self, with_console=False):
        data = self.generator_data()
        max_result, caculate_result, = 0, None
        for a, b, c, d in data:
            if with_console:
                print '\n', a, b, c, d
            _caculate_results = self._caculate_result(a, b, c, d)
            if max_result < len(_caculate_results):
                max_result = len(_caculate_results)
                caculate_result = _caculate_results
                _result = [a, b, c, d]
        return _result, caculate_result


if __name__ == '__main__':
    t = QaScore(qa_num=10, genNum=100)
    print t.process(with_console=True)
