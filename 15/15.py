from collections import defaultdict

num_list = [0, 6, 1, 7, 2, 19, 20]
data = defaultdict(list)

for i in range(len(num_list)):
    data[num_list[i]].append(i)

for i in range(len(data), 30000000):
    last_num = num_list[-1]
    if len(data[last_num]) < 2:
        data[0].append(i)
        num_list.append(0)
    else:
        num = data[last_num][-1] - data[last_num][-2]
        data[num].append(i)
        num_list.append(num)

print(num_list[2019])
print(num_list[-1])
