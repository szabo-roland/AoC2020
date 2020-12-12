from IntMathMixin import IntMathMixin


class Direction(IntMathMixin, int):
    def __new__(cls, value):
        return int.__new__(cls, value % 360)


class NavigationStep(object):
    def __init__(self, command, arg):
        self.command = command
        self.val = arg

    @classmethod
    def parse_step(cls, step):
        return cls(step[0], int(step[1:]))

    def __repr__(self):
        return '{}{}'.format(self.command, self.val)


class StateFirst(object):
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


class StateSecond(StateFirst):
    def __init__(self, x=0, y=0, wx=10, wy=-1):
        super().__init__(x, y)
        self.wx = wx
        self.wy = wy

    def __repr__(self):
        return '({}, {}) ({}, {})'.format(self.x, self.y, self.wx, self.wy)

    def __deg_to_dir(self, deg):
        if deg == 90:
            return (self.wy, -self.wx)
        elif deg == 180:
            return (-self.wx, -self.wy)
        elif deg == 270:
            return (-self.wy, self.wx)

    def __add__(self, step):
        if step.command == 'L':
            wx, wy = self.__deg_to_dir(step.val)
            return type(self)(self.x, self.y, wx, wy)
        elif step.command == 'R':
            return self + NavigationStep('L', 360 - step.val)

        elif step.command == 'N':
            return type(self)(self.x, self.y, self.wx, self.wy - step.val)
        elif step.command == 'S':
            return type(self)(self.x, self.y, self.wx, self.wy + step.val)
        elif step.command == 'E':
            return type(self)(self.x, self.y, self.wx + step.val, self.wy)
        elif step.command == 'W':
            return type(self)(self.x, self.y, self.wx - step.val, self.wy)

        elif step.command == 'F':
            new_x = self.x + step.val * self.wx
            new_y = self.y + step.val * self.wy
            return type(self)(new_x, new_y, self.wx, self.wy)


def parse_input():
    with open('input', 'r') as f:
        return [NavigationStep.parse_step(row) for row in f.readlines()]


def execute(steps, state_cls):
    state = state_cls()
    for step in steps:
        state += step

    return len(state)


def first(steps):
    return execute(steps, StateFirst)


def second(steps):
    return execute(steps, StateSecond)


if __name__ == '__main__':
    steps = parse_input()
    print(first(steps))
    print(second(steps))
