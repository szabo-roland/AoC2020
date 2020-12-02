import pdb


class SRPPasswordEntry(object):
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
        return 'SRPPasswordEntry(min_c={}, max_c={}, char={}, password={})'.format(
            self.min_c, self.max_c, self.char, self.password
        )


class OTCASPasswordEntry(object):
    def __init__(self, first, second, char, password):
        self.first = first
        self.second = second
        self.char = char
        self.password = password

    def is_complying(self):
        return (self.password[self.first - 1] == self.char) != (self.password[self.second - 1] == self.char)

    @classmethod
    def parse(cls, s):
        parts = s.split(' ')
        range_c = parts[0].split('-')

        first = int(range_c[0])
        second = int(range_c[1])

        char = parts[1][:-1]

        password = parts[2]

        return cls(first, second, char, password)

    def __repr__(self):
        return 'OTCASPasswordEntry(first={}, second={}, char={}, password={})'.format(
            self.first, self.second, self.char, self.password
        )


def parse_input(cls):
    with open('input', 'r') as f:
        lines = f.readlines()
        return [cls.parse(line) for line in lines]


def count_complying(cls):
    db = parse_input(cls)
    return len(filter(lambda e: e.is_complying(), db))


def first():
    print(count_complying(SRPPasswordEntry))


def second():
    print(count_complying(OTCASPasswordEntry))


if __name__ == '__main__':
    first()
    second()
