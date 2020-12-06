import itertools

def parse_input():
    with open('input', 'r') as f:
        return [list(group) for k, group in itertools.groupby(f.read().split('\n'), bool) if k]

def count_all_yes_in_group(group):
    return len(reduce(set.intersection, map(lambda person: set(list(person)), group)))

def count_some_yes_in_group(group):
    return len(reduce(set.union, map(lambda person: set(list(person)), group)))

def count_all(mapper, groups):
    return sum(map(mapper, groups))

def first(groups):
    return count_all(count_some_yes_in_group, groups)

def second(groups):
    return count_all(count_all_yes_in_group, groups)

def main():
    groups = parse_input()
    print(first(groups))
    print(second(groups))


if __name__ == '__main__':
    main()
