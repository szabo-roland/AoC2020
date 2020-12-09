def parse_input():
    with open('input', 'r') as f:
        return [int(i) for i in f.readlines()]


def _is_valid(num, arr):
    for i, a in enumerate(arr):
        for j, b in enumerate(arr):
            if i != j:
                if a + b == num:
                    return True

    return False


def is_valid(i, arr):
    if i < 25:
        return True
    num = arr[i]
    arr_slice = arr[i - 25:i]
    return _is_valid(num, arr_slice)


def first(data):
    for i in range(len(data)):
        if not is_valid(i, data):
            return (data[i], i)


def second(data, i):
    target = data[i]
    for start in range(i):
        total = data[start]
        for end in range(start + 1, i - 1):
            total += data[end]
            if total == target:
                return min(data[start:end + 1]) + max(data[start:end + 1])


if __name__ == '__main__':
    data = parse_input()
    invalid, i = first(data)
    print(invalid)
    print(second(data, i))
