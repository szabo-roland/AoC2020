from sympy.ntheory.modular import crt


def parse_input():
    with open('input', 'r') as f:
        timestamp = int(f.readline())
        buses = f.readline().strip().split(',')

    return (timestamp, buses)


def minutes_to_wait(timestamp, bus):
    return bus - timestamp % bus


def first(timestamp, buses):
    buses = [int(bus_id) for bus_id in buses if bus_id != 'x']
    sbuses = sorted(buses, key=lambda bus: minutes_to_wait(timestamp, bus))
    return sbuses[0] * minutes_to_wait(timestamp, sbuses[0])


def is_valid(timestamp, buses):
    for wait_time, bus in buses:
        if wait_time != minutes_to_wait(timestamp, bus):
            return False

    return True


def second(buses):
    buses = [(i, int(bus_id)) for i, bus_id in enumerate(buses) if bus_id != 'x']
    rems, mods = zip(*buses)
    rems = [-rem for rem in rems]
    return crt(mods, rems)[0]


if __name__ == '__main__':
    timestamp, buses = parse_input()
    print(first(timestamp, buses))
    print(second(buses))
