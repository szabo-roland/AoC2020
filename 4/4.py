from functools import reduce
import re

validators = {
    'byr' : lambda x: 1920 <= int(x) <= 2002,
    'iyr' : lambda x: 2010 <= int(x) <= 2020,
    'eyr' : lambda x: 2020 <= int(x) <= 2030,
    'hgt' : lambda x: re.match(r'^\d+(cm|in)$', x) and (150 <= int(x[:-2]) <= 193 if x[-2:] == 'cm' else 59 <= int(x[:-2]) <= 76),
    'hcl' : lambda x: bool(re.match(r'^#[0-9a-f]{6}$', x)),
    'ecl' : lambda x: x in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid' : lambda x: bool(re.match(r'^\d{9}$', x)),
    'cid' : lambda x: True
}

def is_valid_strict(data):
    return is_valid_lose(data) and all([validators[field](data[field]) for field in data])

def is_valid_lose(data):
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    return all([field in data for field in required])

def update_dict(d, e):
    d[e[0]] = e[1]
    return d

def parse(passport):
    return reduce(update_dict, [kv.split(':') for kv in passport.split(' ')], {})

def parse_input():
    with open('input', 'r') as f:
        return [parse(row.replace('\n', ' ').strip()) for row in f.read().split('\n\n')]


def first(passports):
    return sum(map(is_valid_lose, passports))

def second(passports):
    return sum(map(is_valid_strict, passports))

if __name__ == '__main__':
    passports = parse_input()
    print(first(passports))
    print(second(passports))
