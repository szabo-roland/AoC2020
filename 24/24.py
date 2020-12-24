from functools import reduce

HEX_TO_CARTESIAN = {
    'w': (0, -1),
    'e': (0, 1),
    'nw': (-1, -1),
    'ne': (-1, 0),
    'se': (1, 1),
    'sw': (1, 0)
}


class ChainSet(set):
    def add(self, *args, **kwargs):
        super().add(*args, **kwargs)
        return self

    def remove(self, *args, **kwargs):
        super().remove(*args, **kwargs)
        return self


def reducer(coord, direction):
    x, y = coord
    dx, dy = HEX_TO_CARTESIAN[direction]
    return (x + dx, y + dy)


def parse_line(line):
    result = []
    ptr = 0
    while ptr < len(line):
        if line[ptr] in ('w', 'e'):
            result.append(line[ptr])
            ptr += 1
        else:
            result.append(line[ptr:ptr + 2])
            ptr += 2

    return result


def parse_input(file_name):
    with open(file_name) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def test_parse_line():
    assert parse_line('wwnwneseswee') == ['w', 'w', 'nw', 'ne', 'se', 'sw', 'e', 'e']


def first(lines):
    return len(execute_input(lines))


def execute_input(lines):
    return reduce(lambda s, v: s.remove(v) if v in s else s.add(v), [reduce(reducer, line, (0, 0)) for line in lines], ChainSet())

def get_neighbors(world, x, y):
    neighbors = []
    for dx, dy in HEX_TO_CARTESIAN.values():
        nx = dx + x
        ny = dy + y
        if 0 <= nx < len(world) and 0 <= ny < len(world[nx]):
            neighbors.append(world[nx][ny])

    return neighbors


def calculate_state(world, x, y):
    neighbors = get_neighbors(world, x, y)
    black_neighbors = neighbors.count(1)
    if world[x][y] == 1:
        if black_neighbors == 0 or black_neighbors > 2:
            return 0
        else:
            return 1
    else:
        if black_neighbors == 2:
            return 1
        else:
            return 0


def step(world):
    return [[calculate_state(world, x, y) for y in range(len(world[x]))] for x in range(len(world))]


def second(lines):
    size = 200
    blacks = execute_input(lines)
    origo = (size // 2, size // 2)
    world = [[0 for _ in range(size)] for _ in range(size)]
    for x, y in blacks:
        world[origo[0] + x][origo[1] + y] = 1

    for _ in range(100):
        world = step(world)

    return sum([sum(row) for row in world])

if __name__ == '__main__':
    lines = parse_input('input')
    print(first(lines))
    print(second(lines))
