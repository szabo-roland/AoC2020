def parse_input():
    with open('input', 'r') as f:
        return [list(row[:-1]) for row in f.readlines()]


def is_valid(x, y, map_):
    return x in range(len(map_)) and y in range(len(map_[x]))


def find_seat_in_direction(x, y, map_, dir_x, dir_y):
    x = x + dir_x
    y = y + dir_y
    while is_valid(x, y, map_) and map_[x][y] == '.':
        x += dir_x
        y += dir_y

    if is_valid(x, y, map_):
        return map_[x][y]
    return None


def get_directions():
    directions = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                directions.append((dx, dy))

    return directions


def get_far_neighbors(x, y, map_):
    directions = get_directions()
    neighbors = []
    for dir_x, dir_y in directions:
        seat = find_seat_in_direction(x, y, map_, dir_x, dir_y)
        if seat is not None:
            neighbors.append(seat)

    return neighbors


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


def get_next_state_first(x, y, map_):
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


def get_next_state_second(x, y, map_):
    e = map_[x][y]
    if e == '.':
        return '.'

    if e == 'L':
        if len(list(filter(lambda e: e == '#', get_far_neighbors(x, y, map_)))) == 0:
            return '#'

    if e == '#':
        if len(list(filter(lambda e: e == '#', get_far_neighbors(x, y, map_)))) >= 5:
            return 'L'

    return e



def next_generation(map_, next_state_fn):
    new_map = []
    for x in range(len(map_)):
        new_map.append([])
        for y in range(len(map_[x])):
            new_map[x].append(next_state_fn(x, y, map_))

    return new_map


def run_until_stabilize(map_, next_state_fn):
    old_map = []
    while map_ != old_map:
        old_map = map_
        map_ = next_generation(old_map, next_state_fn)

    return map_


def occupied_after_stabilize(map_, next_state_fn):
    map_ = run_until_stabilize(map_, next_state_fn)
    sum_occupied = 0
    for row in map_:
        for e in row:
            if e == '#':
                sum_occupied += 1

    return sum_occupied


def first(map_):
    return occupied_after_stabilize(map_, get_next_state_first)


def second(map_):
    return occupied_after_stabilize(map_, get_next_state_second)


if __name__ == '__main__':
    map_ = parse_input()
    print(first(map_))
    print(second(map_))
