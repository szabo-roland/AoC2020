import pdb


def parse_input():
    tree_map = []
    with open('input', 'r') as f:
        row = f.readline()
        while row:
            tree_map.append([c for c in row[:-1]])
            row = f.readline()

    return tree_map


def get_tree_count(slope_x, slope_y, tree_map):
    x = 0
    y = 0
    period = len(tree_map[0])
    height = len(tree_map)
    tree_count = 0

    while y < height:
        if tree_map[y][x] == '#':
            tree_count += 1
        x = (x + slope_x) % period
        y = y + slope_y

    return tree_count


def first(tree_map):
    return get_tree_count(3, 1, tree_map)


def second(tree_map):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return reduce(lambda a, b: a * b, [get_tree_count(*slope, tree_map=tree_map) for slope in slopes])


def main():
    tree_map = parse_input()

    print(first(tree_map))
    print(second(tree_map))


if __name__ == '__main__':
    main()
