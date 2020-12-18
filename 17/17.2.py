from itertools import product
from copy import deepcopy

world = [[[['.' for _ in range(13)] for _ in range(13)] for _ in range(20)] for _ in range(20)]


def parse_input():
    with open('input', 'r') as f:
        return [list(row.strip()) for row in f.readlines()]


def inject_data(world, data):
    w = 6
    z = 6
    dx = 6
    dy = 6
    for x in range(len(data)):
        for y in range(len(data[x])):
            world[x + dx][y + dy][z][w] = data[x][y]

    return world


def get_active_neighbours(world, x, y, z, w):
    active = 0
    for dx, dy, dz, dw in product([-1, 0, 1], repeat=4):
        if dx == 0 and dy == 0 and dz == 0 and dw == 0:
            continue
        nx = x + dx
        ny = y + dy
        nz = z + dz
        nw = w + dw

        if nx < 0 or nx >= len(world):
            continue
        if ny < 0 or ny >= len(world[0]):
            continue
        if nz < 0 or nz >= len(world[0][0]):
            continue
        if nw < 0 or nw >= len(world[0][0][0]):
            continue

        if world[nx][ny][nz][nw] == '#':
            active += 1

    return active


def step(world):
    new_world = deepcopy(world)
    for x in range(len(world)):
        for y in range(len(world[x])):
            for z in range(len(world[x][y])):
                for w in range(len(world[x][y][z])):
                    active_neighbours = get_active_neighbours(world, x, y, z, w)
                    if world[x][y][z][w] == '#':
                        if active_neighbours not in [2, 3]:
                            new_world[x][y][z][w] = '.'
                    else:
                        if active_neighbours == 3:
                            new_world[x][y][z][w] = '#'

    return new_world


def count_active(world):
    active = 0
    for x in range(len(world)):
        for y in range(len(world[x])):
            for z in range(len(world[x][y])):
                for w in range(len(world[x][y][z])):
                    if world[x][y][z][w] == '#':
                        active += 1
    return active


def second(world):
    for i in range(6):
        print('{}. step'.format(i))
        world = step(world)
    return count_active(world)


if __name__ == '__main__':
    data = parse_input()
    world = inject_data(world, data)
    print(second(world))
