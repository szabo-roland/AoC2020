from collections import defaultdict


def parse_line(line):
    parts = line.split(' (contains ')
    allergens = parts[1][:-1].split(', ')
    ingredients = parts[0].split(' ')
    return ingredients, allergens


def parse_input(file_name):
    with open(file_name) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def get_possible_sources(foods):
    possible_sources = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in possible_sources:
                possible_sources[allergen] = set(ingredients)
            else:
                possible_sources[allergen] = possible_sources[allergen].intersection(set(ingredients))
    return possible_sources


def resolve_allergens(possible_sources):

    def prune_from_sources(possible_sources, source):
        for allergene in possible_sources:
            if source in possible_sources[allergene]:
                possible_sources[allergene].remove(source)

    def find_resolved(possible_sources):
        for allergene in possible_sources:
            if len(possible_sources[allergene]) == 1:
                return allergene

        return None

    result = []
    while len(possible_sources) > 0:
        resolved = find_resolved(possible_sources)
        source = next(iter(possible_sources[resolved]))
        del possible_sources[resolved]
        prune_from_sources(possible_sources, source)
        result.append((resolved, source))

    return result


def second(foods):
    possible_sources = get_possible_sources(foods)
    allergene_list = resolve_allergens(possible_sources)
    allergene_list.sort(key=lambda e: e[0])
    result = ",".join([ingredient for _, ingredient in allergene_list])
    return result


def first(foods):
    possible_sources = get_possible_sources(foods)

    sources = set()
    for allergene in possible_sources:
        sources = sources.union(possible_sources[allergene])

    count = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient not in sources:
                count += 1

    return count

if __name__ == '__main__':
    foods = parse_input('input')
    print(first(foods))
    print(second(foods))
