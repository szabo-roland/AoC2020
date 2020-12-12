class Direction(int):
    def __new__(cls, value):
        return int.__new__(cls, value % 360)

    def __add__(self, value):
        return type(self)(int.__add__(self, value))

    def __sub__(self, value):
        return type(self)(int.__sub__(self, value))


class NavigationStep(object):
    def __init__(self, command, arg):
        self.command = command
        self.val = arg

    @classmethod
    def parse_step(cls, step):
        return cls(step[0], int(step[1:]))

    def __repr__(self):
        return '{}{}'.format(self.command, self.arg)


class State(object):
    deg_to_dir = {
        0: 'N',
        90: 'E',
        180: 'S',
        270: 'W'
    }

    def __init__(self, x=0, y=0, d=90):
        self.x = x
        self.y = y
        self.d = Direction(d)

    def __repr__(self):
        return "({}, {}) {}".format(self.x, self.y, self.deg_to_dir[self.d])

    def __add__(self, step):
        if step.command == 'L':
            return type(self)(self.x, self.y, self.d - step.val)

        elif step.command == 'R':
            return type(self)(self.x, self.y, self.d + step.val)

        elif step.command == 'F':
            return self + NavigationStep(self.deg_to_dir[self.d], step.val)

        elif step.command == 'N':
            return type(self)(self.x, self.y - step.val, self.d)
        elif step.command == 'S':
            return type(self)(self.x, self.y + step.val, self.d)
        elif step.command == 'E':
            return type(self)(self.x + step.val, self.y, self.d)
        elif step.command == 'W':
            return type(self)(self.x - step.val, self.y, self.d)

    def __len__(self):
        return abs(self.x) + abs(self.y)


def parse_input():
    with open('input', 'r') as f:
        return [NavigationStep.parse_step(row) for row in f.readlines()]


def first(steps):
    state = State()
    for step in steps:
        state += step

    return len(state)


if __name__ == '__main__':
    steps = parse_input()
    print(first(steps))
