def tuple_decorator(function):
    def inner(a):
        return function(tuple(a))

    return inner


def cache_decorator(function):
    cache = {}

    def inner(a):
        return cache[a] if a in cache else function(a)

    return inner


# @tuple_decorator
# @cache_decorator
def sum_list(b):
    return sum(b)


sum_list = cache_decorator(sum_list)
sum_list = tuple_decorator(sum_list)




if __name__ == '__main__':
    c = [1, 2, 3, 4]
    print(sum_list(c))
