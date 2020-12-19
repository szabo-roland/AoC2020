def tokenize(line):
    return line.replace('(', '( ').replace(')', ' )').split(' ')


def parse_exp(t_list, start=0):
    result = []
    ptr = start

    while ptr < len(t_list):
        if t_list[ptr] == '*' or t_list[ptr] == '+':
            result.append(t_list[ptr])
            ptr += 1
        elif t_list[ptr] == '(':
            ptr, subres = parse_exp(t_list, ptr + 1)
            result.append(subres)
        elif t_list[ptr] == ')':
            return ptr + 1, result
        else:
            result.append(int(t_list[ptr]))
            ptr += 1

    return result


def execute(parse_tree):
    ptr = 0
    stack = []
    while ptr < len(parse_tree):
        if type(parse_tree[ptr]) == str:
            stack.append(parse_tree[ptr])
            ptr += 1
        elif type(parse_tree[ptr]) == int:
            if len(stack) == 0:
                stack.append(parse_tree[ptr])
            else:

                op = stack.pop()
                val = stack.pop()
                if op == '+':
                    stack.append(parse_tree[ptr] + val)
                else:
                    stack.append(parse_tree[ptr] * val)
            ptr += 1
        else:
            parse_tree[ptr] = execute(parse_tree[ptr])

    return stack[0]


def execute_precedence(parse_tree):
    def execute_stack(stack):
        while len(stack) > 1:
            val1 = stack.pop()
            stack.pop()
            val2 = stack.pop()
            stack.append(val1 * val2)
        return stack

    ptr = 0
    stack = []
    while ptr < len(parse_tree):
        if type(parse_tree[ptr]) == str:
            stack.append(parse_tree[ptr])
            ptr += 1
        elif type(parse_tree[ptr]) == int:
            if len(stack) == 0:
                stack.append(parse_tree[ptr])
            else:
                op = stack.pop()
                if op == '*':
                    if len(parse_tree) > ptr + 1 and parse_tree[ptr + 1] == '+':
                        stack.append(op)
                        stack.append(parse_tree[ptr])
                        ptr += 1
                        continue

                val = stack.pop()
                if op == '+':
                    stack.append(parse_tree[ptr] + val)
                else:
                    stack.append(parse_tree[ptr] * val)
            ptr += 1
        else:
            parse_tree[ptr] = execute_precedence(parse_tree[ptr])

    return execute_stack(stack)[0]


def parse_input():
    with open('input') as f:
        return [parse_exp(tokenize(line.strip())) for line in f.readlines()]


def first():
    parse_trees = parse_input()
    return sum([execute(p) for p in parse_trees])


def second():
    parse_trees = parse_input()
    return sum([execute_precedence(p) for p in parse_trees])


if __name__ == '__main__':
    print(first())
    print(second())
