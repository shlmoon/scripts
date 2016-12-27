#list去重 reduce(lambda x, y: x if y in x else x + [y], [[], ] + lst)
