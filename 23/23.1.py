from collections import deque


def normalize_circle(data, current_i, current):
    new_current_i = data.index(current)
    delta = current_i - new_current_i
    data = deque(data)
    data.rotate(delta)

    return list(data)


def round(data, current_i):
    current = data[current_i]

    removed = data[current_i + 1:current_i + 4]
    del data[current_i + 1:current_i + 4]
    if len(removed) < 3:
        remainder = len(removed)
        removed += data[0: 3 - remainder]
        del data[0: 3 - remainder]

    destination = current - 1
    if destination == 0:
        destination = 9
    while destination in removed:
        destination -= 1
        if destination == 0:
            destination = 9

    dest_i = data.index(destination)

    for index, e in enumerate(removed):
        data.insert(dest_i + 1 + index, e)

    for i in range(-10, 10):
        if data[(current_i + i) % len(data)] == current:
            current_i = current_i + i
            break

    return data, (current_i + 1) % len(data)


def first(data):
    current = 0
    for _ in range(100):
        data, current = round(data, current)

    data = normalize_circle(data, 0, 1)
    return "".join([str(e) for e in data[1:]])


if __name__ == '__main__':
    data = [3, 1, 5, 6, 7, 9, 8, 2, 4]
    print(first(data[:]))
