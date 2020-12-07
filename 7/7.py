import pdb
from collections import defaultdict

def parse_containee(c):
    parts = c.split(' ')
    count = int(parts[0])
    name = ' '.join(parts[1:3])
    return (count, name)

def parse_containee_list(s):
    if s.strip() == 'no other bags.':
        return []
    parts = s.split(', ')
    return [parse_containee(containee) for containee in parts]

def invert(graph):
    result = defaultdict(set)
    for node in graph:
        for child in graph[node]:
            result[child[1]].add(node)

    return result

def parse_input():
    result = {}
    with open('input', 'r') as f:
        line = f.readline()
        while line:
            parts = line.split(' bags contain ')
            container = parts[0]
            containees = parse_containee_list(parts[1])
            result[container] = containees
            line = f.readline()

    return result

def first(graph):
    graph = invert(graph)

    parents = set()
    parents.update(graph['shiny gold'])
    while True:
        new_parents = set()
        for parent in parents:
            new_parents.update(graph[parent])

        old_size = len(parents)
        parents.update(new_parents)
        new_size = len(parents)
        if old_size == new_size:
            break

    return len(parents)

def main():
    graph = parse_input()
    print(first(graph))


if __name__ == '__main__':
    main()
