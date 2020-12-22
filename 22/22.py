def parse_input(file_name):
    with open(file_name) as f:
        return [[int(card) for card in player.strip().split('\n')[1:]] for player in f.read().split('\n\n')]


def calculate_score(deck):
    return sum([(index + 1) * value for index, value in enumerate(deck[::-1])])


def second(players):
    configs = []

    while len(players[0]) != 0 and len(players[1]) != 0:
        if players in configs:
            return 0, players[0]

        configs.append([players[0][:], players[1][:]])
        dealt = [players[0].pop(0), players[1].pop(0)]
        if dealt[0] <= len(players[0]) and dealt[1] <= len(players[1]):
            winner, _ = second([players[0][:dealt[0]], players[1][:dealt[1]]])
            if winner == 0:
                players[winner] += dealt
            else:
                players[winner] += dealt[::-winner]
        else:
            if dealt[0] > dealt[1]:
                players[0] += dealt
            else:
                players[1] += dealt[::-1]

    winner = 0 if len(players[0]) > 0 else 1
    winner_deck = players[winner]

    return winner, winner_deck


def first(players):
    players = [players[0][:], players[1][:]]
    while len(players[0]) != 0 and len(players[1]) != 0:
        p1 = players[0].pop(0)
        p2 = players[1].pop(0)
        if p1 > p2:
            players[0] += [p1, p2]
        else:
            players[1] += [p2, p1]

    winner = players[0] if len(players[0]) > 0 else players[1]

    return calculate_score(winner)


if __name__ == '__main__':
    players = parse_input('input')
    print(first(players))
    _, deck = second(players)
    print(calculate_score(deck))
