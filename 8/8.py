class Instruction(object):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    @classmethod
    def parse(cls, string):
        parts = string.split(' ')
        return cls(parts[0], int(parts[1]))

    def __call__(self):
        if self.op == 'jmp':
            return (self.value, 0)

        if self.op == 'acc':
            return (1, self.value)

        if self.op == 'nop':
            return (1, 0)

    def __repr__(self):
        return 'Instruction(\'{}\', {})'.format(self.op, self.value)


class Machine(object):
    def __init__(self, instructions):
        self.ip = 0
        self.instructions = instructions
        self.acc = 0
        self.visited_ips = set()
        self.patched_ip = -1

    def step(self):
        self.visited_ips.add(self.ip)

        delta_ip, delta_acc = self.instructions[self.ip]()
        self.ip += delta_ip
        self.acc += delta_acc

    def reset(self):
        self.ip = 0
        self.acc = 0
        self.visited_ips.clear()
        if self.patched_ip != -1:
            self.patch_instruction(self.patched_ip)

        self.patched_ip = -1

    def run(self):
        while True:
            self.step()
            if self.is_loop() or self.is_finished():
                break

    def is_loop(self):
        return self.ip in self.visited_ips

    def is_finished(self):
        return self.ip >= len(self.instructions)

    def patch_instruction(self, i):
        instruction = self.instructions[i]
        instruction.op = 'nop' if instruction.op == 'jmp' else 'jmp'
        self.patched_ip = i

    @classmethod
    def parse(cls):
        with open('input', 'r') as f:
            return cls([Instruction.parse(line) for line in f.readlines()])


def first(machine):
    machine.run()
    return machine.acc


def second(machine):
    suspects = [i for i in machine.visited_ips if machine.instructions[i].op != 'acc']

    for i in suspects:
        machine.patch_instruction(i)
        machine.run()
        if machine.is_finished():
            return machine.acc

        machine.reset()


if __name__ == '__main__':
    machine = Machine.parse()

    print(first(machine))
    print(second(machine))
