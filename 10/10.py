from functools import reduce


def parse_input():
    with open('input', 'r') as f:
        return [int(i) for i in f.readlines()]


def preprocess(data):
    result = sorted(data)
    result.append(result[-1] + 3)
    return result


def diff_reducer(acc, num):
    acc['diffs'].append(num - acc['last'])
    acc['last'] = num
    return acc


def get_diffs(data):
    return reduce(diff_reducer, data, {'diffs': [], 'last': 0})['diffs']


def first(data):
    diffs = get_diffs(data)
    ones = len(filter(lambda e: e == 1, diffs))
    threes = len(filter(lambda e: e == 3, diffs))
    return ones * threes

if __name__ == '__main__':
    data = preprocess(parse_input())
    print(first(data))
