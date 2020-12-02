
def first():
    expense_sheet = []
    with open('input', 'r') as f:
        expense_sheet = [int(i) for i in f.readlines()]

    for i in range(len(expense_sheet)):
        for j in range(len(expense_sheet)):
            if i != j:
                if expense_sheet[i] + expense_sheet[j] == 2020:
                    print(expense_sheet[i] * expense_sheet[j])
                    return

def second():
    expense_sheet = []
    with open('input', 'r') as f:
        expense_sheet = [int(i) for i in f.readlines()]

    for i in range(len(expense_sheet)):
        for j in range(len(expense_sheet)):
            for k in range(len(expense_sheet)):
                if i != j and j != k and i != k:
                    if expense_sheet[i] + expense_sheet[j] + expense_sheet[k] == 2020:
                        print(expense_sheet[i] * expense_sheet[j] * expense_sheet[k])
                        return


if __name__ == '__main__':
    first()
    second()
