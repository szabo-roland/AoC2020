
def main():
    expense_sheet = []
    with open('input', 'r') as f:
        expense_sheet = [int(i) for i in f.readlines()]

    for i in range(len(expense_sheet)):
        for j in range(len(expense_sheet)):
            if i != j:
                if expense_sheet[i] + expense_sheet[j] == 2020:
                    print(expense_sheet[i] * expense_sheet[j])
                    return

if __name__ == '__main__':
    main()
