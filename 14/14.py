def parse_input():
    with open('input', 'r') as f:
        return [parse_op(line.strip()) for line in f.readlines()]


def parse_op(line):
    parts = line.split(' = ')
    if parts[0] == 'mask':
        return (parts[0], parts[1])
    return (int(parts[0][4:-1]), int(parts[1]))


class Machine(object):
    def __init__(self):
        self.mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        self.mem = {}

    def execute(self, op, arg):
        if op == 'mask':
            self.mask = arg
        else:
            self.write(op, arg)

    def write(self, addr, val):
        self.mem[addr] = self.do_mask(val)

    def to_bitstring(self, val):
        return format(val, '0{}b'.format(len(self.mask)))

    def do_mask(self, val):
        val = self.to_bitstring(val)
        result = ''
        for m, v in zip(self.mask, val):
            if m == 'X':
                result += v
            else:
                result += m

        return int(result, 2)


def first(ops):
    m = Machine()
    for op, arg in ops:
        m.execute(op, arg)

    return sum(m.mem.values())


if __name__ == '__main__':
    ops = parse_input()
    print(first(ops))
