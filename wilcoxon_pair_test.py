import operator

class one_member:
    def __init__(self, id, real_value, abs_value):
        self.id = id
        self.real_value = real_value
        self.abs_value = abs_value
        if abs_value == real_value:
            self.sign = "+"
        else:
            self.sign = "-"
        self.order = ''


class row_of_file:
    def __init__(self, rownum, algorithm, function, dimension, values):
        self.rownum = rownum
        self.algorithm = algorithm
        self.function = function
        self.dimension = dimension
        self.values = values


table_95 = {6: 0, 7: 2, 8: 3, 9: 5, 10: 8, 11: 10, 12: 13, 13: 17, 14: 21, 15: 25, 16: 29, 17: 34, 18: 40, 19: 46,
            20: 52, 21: 58, 22: 65, 23: 73, 24: 81, 25: 89, 26: 98, 27: 107, 28: 116, 29: 126, 30: 137}
table_95_min_value = 6

table_99 = {8: 0, 9: 1, 10: 3, 11: 5, 12: 7, 13: 9, 14: 12, 15: 15, 16: 19, 17: 23, 18: 27, 19: 32, 20: 37, 21: 42,
            22: 48, 23: 54, 24: 61, 25: 68, 26: 75, 27: 83, 28: 91, 29: 100, 30: 109}
table_99_min_value = 8

# first_list = [1115.182031425913, 1171.9193363002414, 1100.1249088820769, 1106.892375816422, 1103.7194046009527, 1106.892375816422, 1125.8358482626154, 1117.0045207054873, 1107.1968197296828, 1118.8389815858263, 1121.762135037141, 1107.1152399330758, 1115.1195769848737, 1106.892375816422, 1107.1343652886435, 1103.5398695697686, 1121.9494983602563, 1118.5969921136038, 1118.472083231527, 1103.7272328928848, 1103.4774151287302, 1107.1968197296828, 1103.6647784518455, 1118.5969921136038, 1115.2444858669505, 1107.071910847605, 1133.5292057753622, 1118.5345376725654, 1103.781859041991, 1122.0119528012956]
# second_list = [1130.6609342053198, 1115.2444858669514, 1107.0172846984997, 1115.1195769848746, 1106.8299213753835, 1118.784355436721, 1110.2448820630743, 1110.3073365041137, 1106.892375816422, 1130.1766995287098, 1107.079739139538, 1118.6594465546432, 1103.5398695697686, 1121.9494983602572, 1113.659842750766, 1103.9067679240688, 1131.7613426623893, 1130.1142450876714, 1148.4614194371206, 1127.6416115651864, 1112.0168885023759, 1115.182031425913, 1123.5965959174819, 1147.0099718902793, 1148.697467028992, 1111.891979620299, 1106.9548302574603, 1110.3073365041137, 1115.2444858669514, 1128.6545108535638]


def wilcoxon_pair_test(first_list, second_list):
    if len(first_list) != len(second_list):
        return 0
    list_length = len(first_list)
    subtracted_list = {}
    abs_value_list = []
    n = list_length
    for i in range(list_length):
        value = first_list[i] - second_list[i]
        if value != 0:
            subtracted_list[i] = one_member(i, value, abs(value))
            abs_value_list.append(abs(value))
        else:
            n -= 1

    abs_value_list = sorted(abs_value_list)

    for i in range(len(abs_value_list)):
        for j in subtracted_list:
            if subtracted_list[j].abs_value == abs_value_list[i]:
                subtracted_list[j].order = i

    order_stats = {}
    order_stats["+"] = 0
    order_stats["-"] = 0

    for i in subtracted_list:
        if subtracted_list[i].sign == "+":
            order_stats["+"] += subtracted_list[i].order+1
        elif subtracted_list[i].sign == "-":
            order_stats["-"] += subtracted_list[i].order+1

    r0 = min(order_stats["+"], order_stats["-"])

    # test 95
    if n < table_95_min_value:
        test_95_result = "?"
    else:
        if r0 > table_95[n]:
            test_95_result = "="
        else:
            if order_stats["+"] < order_stats["-"]:
                test_95_result = "+"
            else:
                test_95_result = "-"

    # test 99
    if n < table_99_min_value:
        test_99_result = "?"
    else:
        if r0 > table_99[n]:
            test_99_result = "="
        else:
            if order_stats["+"] < order_stats["-"]:
                test_99_result = "+"
            else:
                test_99_result = "-"

    result = "95: %s; 99: %s" % (test_95_result, test_99_result)
    return result

file = open("C:\\Projects\\matematicka informatika\\figures_evt_tb\\vysledky.txt", "r")

read_rows = {}
rownum = 0
for row in file:
    rownum += 1
    text = row.split(";")
    values = text[9]
    values = values.replace("values: [", "").replace("]\n", "").replace(" ","")
    values = values.split(",")
    vals = []
    for v in values:
        vals.append(float(v))
    read_rows[rownum] = row_of_file(rownum, text[0], text[1], text[2], vals)

num_of_rows = len(read_rows)
half_num_of_rows = int(num_of_rows / 2)

for i in range(1, half_num_of_rows+1):
    result = wilcoxon_pair_test(read_rows[i].values, read_rows[i+half_num_of_rows].values)
    print(read_rows[i].function, read_rows[i].dimension, result)