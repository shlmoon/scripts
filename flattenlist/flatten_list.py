
import time
from collections import Iterable


def decorator_1(func):
    def _wrapper(*args, **kwargs):
        now = time.time()
        result = func(*args, **kwargs)
        print '\n', func.__name__, time.time() - now
        return result
    return _wrapper


def genlist_2(lst):
    def _checkend(lst):
        for x in lst:
            if isinstance(x, Iterable):
                return False
        return True

    if _checkend(lst):
        return lst

    def _genlist(v1, v2):
        if isinstance(v1, Iterable) and isinstance(v2, Iterable):
            return v1 + v2
        elif isinstance(v1, Iterable) and not isinstance(v2, Iterable):
            return v1 + [v2]
        elif not isinstance(v1, Iterable) and isinstance(v2, Iterable):
            return [v1] + v2
        elif not isinstance(v1, Iterable) and not isinstance(v2, Iterable):
            return [v1, v2]
    return genlist_2(reduce(_genlist, lst))


def genlist(lst):
    def _genlist(v1, v2):
        if isinstance(v1, Iterable) and isinstance(v2, Iterable):
            return v1 + v2
        elif isinstance(v1, Iterable) and not isinstance(v2, Iterable):
            return v1 + [v2]
        elif not isinstance(v1, Iterable) and isinstance(v2, Iterable):
            return [v1] + v2
        elif not isinstance(v1, Iterable) and not isinstance(v2, Iterable):
            return [v1, v2]
    data = reduce(_genlist, lst)
    if data == lst:
        return data
    return genlist_2(data)


def genlist_1(lst):
    if isinstance(lst, Iterable):
        return [t for x in lst for t in genlist_1(x)]
    return [lst]


# lst = [[1], [[2], [[3], [[4], [[5], [[6], [7]]]]]]
# lst = [[1], [[2], [[3], [[4], [[5], [[6], [7]]]]]]]
lst = [1, [2, [3, [4, [5, [6, [7]]]]]]]

print '\ngenlist: ', decorator_1(genlist)(lst)
print '\ngenlist_1: ', decorator_1(genlist_1)(lst)
