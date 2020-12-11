def parse_input():
    with open('input', 'r') as f:
        return [list(row[:-1]) for row in f.readlines()]


def get_neighbors(x, y, map_):
    neighbors = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                xx = dx + x
                yy = dy + y
                if xx < 0 or yy < 0:
                    continue
                try:
                    neighbors.append(map_[x + dx][y + dy])
                except IndexError:
                    pass

    return neighbors


def get_next_state(x, y, map_):
    e = map_[x][y]
    if e == '.':
        return '.'

    if e == 'L':
        if len(list(filter(lambda e: e == '#', get_neighbors(x, y, map_)))) == 0:
            return '#'

    if e == '#':
        if len(list(filter(lambda e: e == '#', get_neighbors(x, y, map_)))) >= 4:
            return 'L'

    return e


def next_generation(map_):
    new_map = []
    for x in range(len(map_)):
        new_map.append([])
        for y in range(len(map_[x])):
            new_map[x].append(get_next_state(x, y, map_))

    return new_map


def run_until_stabilize(map_):
    old_map = []
    while map_ != old_map:
        old_map = map_
        map_ = next_generation(old_map)

    return map_


def first(map_):
    map_ = run_until_stabilize(map_)
    sum_occupied = 0
    for row in map_:
        for e in row:
            if e == '#':
                sum_occupied += 1

    return sum_occupied


if __name__ == '__main__':
    map_ = parse_input()
    print(first(map_))
