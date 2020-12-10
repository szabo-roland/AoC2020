from functools import reduce
from itertools import combinations


def parse_input():
    with open('input', 'r') as f:
        return [int(i) for i in f.readlines()]


def preprocess(data):
    result = sorted(data)
    result.append(result[-1] + 3)
    return [0] + result


def diff_reducer(acc, num):
    acc['diffs'].append(num - acc['last'])
    acc['last'] = num
    return acc


def get_diffs(data):
    return reduce(diff_reducer, data[1:], {'diffs': [], 'last': data[0]})['diffs']


def first(data):
    diffs = get_diffs(data)
    ones = len(filter(lambda e: e == 1, diffs))
    threes = len(filter(lambda e: e == 3, diffs))
    return ones * threes


def is_valid(data):
    return all([d <= 3 for d in get_diffs(data)])


def get_all_middle_combinations(middle):
    result = []
    for i in range(len(middle) + 1):
        result.extend([list(m) for m in combinations(middle, i)])

    return result


def count_valid_subsequences(data):
    if len(data) < 3:
        return 1

    first = data[0]
    last = data[-1]
    middles = get_all_middle_combinations(data[1:-1])
    valids = 0
    for middle in middles:
        if is_valid([first] + middle + [last]):
            valids += 1

    return valids


def get_partitions(data):
    result = []
    temp = []
    prev = 0
    for i in data:
        if i - prev < 3:
            temp.append(i)
        else:
            result.append(temp)
            temp = [i]
        prev = i

    return result


def second(data):
    result = 1
    partitions = get_partitions(data)
    for partition in partitions:
        result *= count_valid_subsequences(partition)

    return result


if __name__ == '__main__':
    data = preprocess(parse_input())
    print(first(data))
    print(second(data))
