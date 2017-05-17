list去重 reduce(lambda x, y: x if y in x else x + [y], [[], ] + lst)

二维数组翻转:  map(lambda x: sorted(x, reverse=True), zip(*result))
