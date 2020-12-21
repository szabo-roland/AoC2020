from functools import reduce
import operator
import pdb


def border_to_num(border, reverse=False):
    bitstring = "".join(border).replace('#', '1').replace('.', '0')
    if reverse:
        bitstring = bitstring[::-1]
    return int("".join(bitstring), 2)


def rotate(m):
    return ["".join(list(e)) for e in list(zip(*m[::-1]))]


def orient_adj(a, b):
    for a_i, a_num in enumerate(a.borders[0] + a.borders[1]):
        for b_i, b_num in enumerate(b.borders[0] + b.borders[1]):
            if b_num == a_num:
                break
        if b_num == a_num:
            break

    joint = a_num

    if a_i > 3:
        a.data = a.data[::-1]

    if b_i > 3:
        b.data = b.data[::-1]

    while joint != a.borders[0][3]:
        a.data = rotate(a.data)

    while joint != b.borders[0][2]:
        b.data = rotate(b.data)

    b.data = b.data[::-1]


class Tile(object):
    def __init__(self, tile_id, data):
        self.tile_id = tile_id
        self.data = data
        self.adjanced = set()
        self.placed = False

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data
        self.__generate_borders()

    def strip_borders(self):
        self.__data = ["".join([e for e in row[1:-1]]) for row in self.__data[1:-1]]

    def pretty_print(self):
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                print(self.data[x][y], end='')
            print()

    def print_with_adj(self, other):
        for a, b in zip(self.data, other.data):
            for e in a + '|' + b:
                print(e, end='')
            print()

    def __generate_borders(self):
        top = self.data[0]
        bottom = self.data[-1][::-1]
        left = "".join([row[0] for row in self.data[::-1]])
        right = "".join([row[-1] for row in self.data])
        self.borders = [
            [border_to_num(border) for border in [top, bottom, left, right]],
            [border_to_num(border, True) for border in [top, bottom, left, right]],
        ]

    def can_be_adjanced(self, other):
        if self == other:
            return False

        self_borders = self.borders[0] + self.borders[1]
        other_borders = other.borders[0] + other.borders[1]
        for border in other_borders:
            if border in self_borders:
                return True

        return False

    @classmethod
    def parse(cls, raw_data):
        parts = raw_data.split('\n')
        title_id = int(parts[0][5:-1])
        data = parts[1:]
        return cls(title_id, data)

    def __repr__(self):
        return str(self.tile_id)


def parse_input(file_name):
    with open(file_name, 'r') as f:
        return [Tile.parse(raw_tile.strip()) for raw_tile in f.read().split('\n\n')]


def get_neighbors(image, x, y):
    result = []
    count = 0
    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if 0 <= nx < 12 and 0 <= ny < 12:
            count += 1
            if image[nx][ny] is not None:
                result.append(image[nx][ny])

    return count, result


def assemble(tiles):
    corners = [tile for tile in tiles if len(tile.adjanced) == 2]
    borders = [tile for tile in tiles if len(tile.adjanced) == 3]
    inners = [tile for tile in tiles if len(tile.adjanced) == 4]

    image = [[None for _ in range(12)] for _ in range(12)]

    image[0][0] = corners[0]
    for x in range(12):
        for y in range(12):
            if x == 0 and y == 0:
                image[x][y] = corners[0]
                image[x][y].placed = True
            else:
                count, neighbors = get_neighbors(image, x, y)
                possibles = [neighbor for neighbor in set.intersection(*[neighbor.adjanced for neighbor in neighbors]) if not neighbor.placed]
                if count == 2:
                    container = corners
                elif count == 3:
                    container = borders
                elif count == 4:
                    container = inners

                possibles = [possible for possible in possibles if possible in container]

                image[x][y] = next(iter(possibles))
                image[x][y].placed = True
    return image


def orient(image):
    def flip_row(row):
        for tile in row:
            tile.data = tile.data[::-1]
    for row in image:
        for i in range(len(row) - 1):
            orient_adj(row[i], row[i + 1])

    for i in range(len(image) - 1):
        a = image[i]
        b = image[i + 1]
        if a[0].data[0] == b[0].data[0]:
            flip_row(a)
        elif a[0].data[0] == b[0].data[-1]:
            flip_row(a)
            flip_row(b)
        elif a[0].data[-1] == b[0].data[-1]:
            flip_row(b)


def strip_borders(image):
    for row in image:
        for tile in row:
            tile.strip_borders()


def join_tiles(image):
    result = []
    for row in image:
        for i in range(8):
            result.append('')
            for tile in row:
                result[-1] += tile.data[i]

    return result


def first(tiles):
    for tile_1 in tiles:
        for tile_2 in tiles:
            if tile_1.can_be_adjanced(tile_2):
                tile_1.adjanced.add(tile_2)

    corners = [tile for tile in tiles if len(tile.adjanced) == 2]
    return reduce(operator.mul, [tile.tile_id for tile in corners])


monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

monster_body_length = 15


def is_monster_there(image, dx, dy):

    if dx + len(monster) > len(image):
        return False
    if dy + len(monster[0]) > len(image[0]):
        return False

    for x in range(len(monster)):
        for y in range(len(monster[x])):
            if monster[x][y] == ' ':
                continue
            if image[x + dx][y + dy] != '#':
                return False

    return True


def find_fucking_seamonster(image):
    monsters = []
    for x in range(len(image)):
        for y in range(len(image[0])):
            if is_monster_there(image, x, y):
                monsters.append((x, y))

    return monsters


def look_at_image_until_monsters_found(image):
    ways_to_look = [
        rotate,
        rotate,
        rotate,
        lambda x: x[::-1],
        rotate,
        rotate,
        rotate
    ]
    for fn in ways_to_look:
        monsters = find_fucking_seamonster(image)
        if len(monsters) > 0:
            return monsters
        image = fn(image)

def count_hashmarks(image):
    result = 0
    for row in image:
        for e in row:
            if e == '#':
                result += 1

    return result


def second(tiles):
    image = assemble(tiles)
    orient(image)
    strip_borders(image)
    final_image = join_tiles(image)
    monsters = look_at_image_until_monsters_found(final_image)
    return count_hashmarks(final_image) - len(monsters) * monster_body_length


if __name__ == '__main__':
    tiles = parse_input('input')
    print(first(tiles))
    print(second(tiles))
