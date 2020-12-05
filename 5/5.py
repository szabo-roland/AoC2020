def parse_ticket(ticket):
    return int(ticket.replace('F', '0').replace('B', '1').replace('R', '1').replace('L', '0'), 2)

def parse_input():
    with open('input', 'r') as f:
        return [parse_ticket(ticket.strip()) for ticket in f.readlines()]

def first(tickets):
    return tickets[-1]

def second(tickets):
    for i in range(1, len(tickets) - 1):
        if tickets[i] - 1 > tickets[i-1]:
            return tickets[i] - 1
def main():
    tickets = parse_input()
    tickets.sort()
    print(first(tickets))
    print(second(tickets))

if __name__ == '__main__':
    main()
