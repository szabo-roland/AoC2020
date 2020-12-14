from itertools import product


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

    def run(self, program):
        for op, arg in program:
            self.execute(op, arg)


class MachineV2(Machine):
    def write(self, op, arg):
        addrs = self.get_addresses(op)
        for addr in addrs:
            super().write(addr, arg)

    def get_addresses(self, addr):
        mod_addr = ''
        for m, a in zip(self.mask, self.to_bitstring(addr)):
            if m == 'X':
                mod_addr += '0'
            else:
                mod_addr += a
        mod_addr = int(mod_addr, 2)

        fmt_mask = self.mask.replace('X', '{}')
        addrs = []
        for fmt_arg in product('01', repeat=self.mask.count('X')):
            mask = int(fmt_mask.format(*fmt_arg), 2)
            addrs.append(mask | mod_addr)

        return addrs

    def do_mask(self, val):
        return val

def first(ops):
    m = Machine()
    m.run(ops)
    return sum(m.mem.values())


def second(ops):
    m = MachineV2()
    m.run(ops)
    return sum(m.mem.values())

if __name__ == '__main__':
    ops = parse_input()
    print(first(ops))
    print(second(ops))
