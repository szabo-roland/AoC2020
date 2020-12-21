import re
import pdb
from parsimonious.grammar import Grammar


def parse_rule_def(rule_def):
    if '"' in rule_def:
        return rule_def[1:-1]
    if '|' in rule_def:
        parts = [parse_rule_def(subrule) for subrule in rule_def.split(' | ')]
        result = ['(']
        for part in parts:
            result += part + ['|']
        result[-1] = ')'
        return result
    else:
        return [int(rule_id) for rule_id in rule_def.strip().split(' ')]


def parse_rule(line):
    parts = line.strip().split(': ')
    rule_id = int(parts[0])
    rule_def = parse_rule_def(parts[1])
    return rule_id, rule_def


def parse_input(file_name):
    with open(file_name) as f:
        raw = f.read()
        parts = raw.split('\n\n')
        rules = {rule_id: rule_def for rule_id, rule_def in [parse_rule(line) for line in parts[0].strip().split('\n')]}

        messages = parts[1].strip().split('\n')
        return rules, messages


def to_parsimonious_rule(line):
    def rename_rules(line):
        return re.sub(r'(\d+)', r'r\g<1>', line)

    parts = line.split(': ')
    left = rename_rules(parts[0])

    right = parts[1]
    if '|' in right:
        parts = right.split(' | ')
        parts = ['({})'.format(part) for part in parts]
        right = ' / '.join(parts)

    right = rename_rules(right)
    return left + ' = ' + right


def parse_raw_input():
    with open('input') as f:
        raw = f.read()
        parts = raw.split('\n\n')
        rules = parts[0].split('\n')
        messages = parts[1].strip().split('\n')
        return rules, messages


def resolve_token(token, rules):
    if type(token) == str:
        return token
    else:
        return resolve_rule(rules, key=token)


def resolve_rule(rules, key=0):
    rule = rules[key]
    return [resolve_token(token, rules) for token in rule]


def flatten(items, seqtypes=(list, tuple)):
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i : i + 1] = items[i]
    return items


def get_regex_str(resolved):
    return "".join(flatten(resolved))


def solve(rules, messages):
    resolved = resolve_rule(rules)

    regex = re.compile(get_regex_str(resolved))
    return sum([1 for message in messages if regex.fullmatch(message)])


def first():
    rules, messages = parse_input('input')
    return solve(rules, messages)


def second():
    rules, messages = parse_input('input2')
    return solve(rules, messages)


if __name__ == '__main__':
    print(first())
    print(second())


def test_resolve_rule():
    ruleset = {0: [1, 2], 1: ['a'], 2: ['b']}
    assert get_regex_str(resolve_rule(ruleset)) == 'ab'
    ruleset = {0: [1, 2], 1: ['(', 3, 4, ')', '|', '(', 5, 6, ')'], 2: ['b'], 3: ['c'], 4: [2, 3], 5: ['d'], 6: [5, 5]}

    assert get_regex_str(resolve_rule(ruleset)) == '(cbc)|(ddd)b'
    compiled = re.compile(get_regex_str(resolve_rule(ruleset)))
    assert compiled.fullmatch('cbcb') is not None
    assert compiled.fullmatch('dddb') is not None
    assert not compiled.fullmatch('(cbc)b')
