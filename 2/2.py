import pdb


class PasswordEntry(object):
    def __init__(self, min_c, max_c, char, password):
        self.min_c = min_c
        self.max_c = max_c
        self.char = char
        self.password = password

    def is_complying(self):
        count = 0
        for c in self.password:
            if c == self.char:
                count += 1
        return self.min_c <= count and count <= self.max_c

    @classmethod
    def parse(cls, s):
        parts = s.split(' ')
        range_c = parts[0].split('-')

        min_c = int(range_c[0])
        max_c = int(range_c[1])

        char = parts[1][:-1]

        password = parts[2]

        return cls(min_c, max_c, char, password)

    def __repr__(self):
        return 'PasswordEntry(min_c={}, max_c={}, char={}, password={})'.format(
            self.min_c, self.max_c, self.char, self.password
        )


def parse_input():
    with open('input', 'r') as f:
        lines = f.readlines()
        return [PasswordEntry.parse(line) for line in lines]


def first():
    db = parse_input()
    print(len(filter(lambda e: e.is_complying(), db)))


if __name__ == '__main__':
    first()
