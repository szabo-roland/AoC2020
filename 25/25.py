def parse_input():
    with open('input') as f:
        return (int(f.readline().strip()), int(f.readline().strip()))


def transform(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227

    return value


def get_loop_size(pub_key):
    value = 1
    subject_number = 7
    loop_size = 0
    while value != pub_key:
        loop_size += 1
        value *= subject_number
        value = value % 20201227

    return loop_size


if __name__ == '__main__':
    card_pubkey, door_pubkey = parse_input()
    card_loopsize = get_loop_size(card_pubkey)
    door_loopsize = get_loop_size(door_pubkey)

    encryption_key = transform(card_pubkey, door_loopsize)
    print(encryption_key)
