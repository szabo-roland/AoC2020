from collections import defaultdict

class Rule(object):
    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    @classmethod
    def parse(cls, raw_rule):
        parts = raw_rule.split(': ')
        name = parts[0]
        raw_ranges = parts[1].split(' or ')
        ranges = []
        for raw_range in raw_ranges:
            parts = raw_range.split('-')
            ranges.append(range(int(parts[0]), int(parts[1]) + 1))

        return cls(name, ranges)

    def __repr__(self):
        return 'Rule("{}", {})'.format(self.name, self.ranges)

    def can_field_be_valid(self, field):
        for range_ in self.ranges:
            if field in range_:
                return True

        return False

    def validate_fields(self, fields):
        for field in fields:
            if not self.can_field_be_valid(field):
                return False

        return True

    @staticmethod
    def is_field_invalid(rules, field):
        for rule in rules:
            if rule.can_field_be_valid(field):
                return False

        return True

    @classmethod
    def is_ticket_invalid(cls, rules, ticket):
        for field in ticket:
            if Rule.is_field_invalid(rules, field):
                return True

        return False

    @classmethod
    def is_ticket_valid(cls, rules, tickets):
        return not cls.is_ticket_invalid(rules, tickets)


def parse_rules(raw_rules):
    raw_rules = raw_rules.strip().split('\n')
    return [Rule.parse(rule) for rule in raw_rules]


def parse_ticket(row):
    return [int(val) for val in row.strip().split(',')]


def parse_input():
    with open('input') as f:
        parts = f.read().split('\n\n')
        rules = parse_rules(parts[0])
        your_ticket = parse_ticket(parts[1].split('\n')[1])
        tickets = [parse_ticket(ticket) for ticket in parts[2].strip().split('\n')[1:]]
        return (rules, your_ticket, tickets)


def get_all_invalid_fields(rules, tickets):
    invalid_fields = []
    for ticket in tickets:
        for field in ticket:
            if Rule.is_field_invalid(rules, field):
                invalid_fields.append(field)

    return invalid_fields


def first(rules, tickets):
    invalid_fields = get_all_invalid_fields(rules, tickets)
    return sum(invalid_fields)


def invert_tickets(tickets):
    result = [[] for _ in tickets[0]]

    for ticket in tickets:
        for i, field in enumerate(ticket):
            result[i].append(field)

    return result


def solve_conflicts(rule_map):
    def find_len_one(rule_map):
        for index, rule_list in enumerate(rule_map):
            if len(rule_list) == 1:
                return index

    def remove_from_map(rule_map, rule):
        for rule_list in rule_map:
            if rule in rule_list:
                rule_list.remove(rule)

    def is_empty(rule_map):
        for rule_list in rule_map:
            if len(rule_list) > 0:
                return False

        return True

    result = {}
    while not is_empty(rule_map):
        index = find_len_one(rule_map)
        rule = rule_map[index][0]
        remove_from_map(rule_map, rule)
        result[rule] = index

    return result


def second(rules, your_ticket, tickets):
    tickets = [ticket for ticket in tickets if Rule.is_ticket_valid(rules, ticket)]
    tickets.append(your_ticket)
    inverted = invert_tickets(tickets)
    rule_map = [[] for _ in inverted]
    for index, fields in enumerate(inverted):
        for rule in rules:
            if rule.validate_fields(fields):
                rule_map[index].append(rule)

    rule_map = solve_conflicts(rule_map)
    result = 1
    for rule in rule_map:
        if rule.name.startswith('departure'):
            result *= your_ticket[rule_map[rule]]

    return result



if __name__ == '__main__':
    rules, your_ticket, tickets = parse_input()
    print(first(rules, tickets))
    print(second(rules, your_ticket, tickets))
