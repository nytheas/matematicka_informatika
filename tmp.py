

group_A = []

galen = 2001

for i in range(galen):
    group_A.append(i+1)





def pick_data_from_list(expected_length, data):
    data_len = len(data)
    if expected_length >= data_len:
        return data

    result = []
    divisor = data_len / expected_length
    last_divisor = divisor
    for i in range(0,data_len):
        if i >= last_divisor:
            last_divisor += divisor
            result.append(data[i])

    result.append(data[-1])
    return result

result = pick_data_from_list(273, group_A)

for i in result:
    print (i)


print(len(result))