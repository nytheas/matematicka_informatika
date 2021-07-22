import math
import random
from PIL import ImageDraw, Image
import statistics

class Salesman:
    def __init__(self):
        self.order = []
        self.tp = 0
        self.dist = -1
        self.max_x_coord = 0
        self.max_y_coord = 0
        self.min_x_coord = 0
        self.min_y_coord = 0
        self.image_x = 1000
        self.image_y = 1000
        self.edge = 10
        self.tabu_length = 5
        self.calculations = 0


class TravelPoint:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y
        self.prev_label = ''
        self.prev_dist = -1
        self.next_label = ''
        self.next_dist = -1


def load_file(filename):
    global travel_points
    global s
    file = open(filename, 'r')
    for row in file:
        i = row.replace(",", ".").split(" ")
        travel_points[int(i[0])] = TravelPoint(int(i[0]), float(i[1]), float(i[2]))
        if float(i[1]) > s.max_x_coord:
            s.max_x_coord = float(i[1])
        if float(i[2]) > s.max_y_coord:
            s.max_y_coord = float(i[2])
        if float(i[1]) < s.min_x_coord:
            s.min_x_coord = float(i[1])
        if float(i[2]) < s.min_y_coord:
            s.min_y_coord = float(i[2])

    s.tp = len(travel_points)
    file.close()


def draw_picture(sorder=''):
    global travel_points
    global s

    if sorder == '':
        sorder = s.order[:]

    pic = Image.new("RGB", (s.image_x + 2 * s.edge, s.image_y + 2 * s.edge), (255, 255, 255))
    draw = ImageDraw.Draw(pic)
    for tp in travel_points:
        coord_x, coord_y = format_coord(travel_points[tp])
        draw.ellipse([coord_x-5, coord_y-5, coord_x+5, coord_y+5], fill=128)
    for ln in range(len(sorder)):
        #print(travel_points[sorder[ln]].x)
        x1, y1 = format_coord(travel_points[sorder[ln]])
        x2, y2 = format_coord(travel_points[(sorder[(ln+1) % len(sorder)])])
        draw.line((x1, y1, x2, y2), fill=128)
    pic.show()


def format_coord(coord):
    global s
    x_celk = 2 * s.edge + s.max_x_coord - s.min_x_coord
    y_celk = 2 * s.edge + s.max_y_coord - s.min_y_coord
    x = s.edge + (((coord.x - s.min_x_coord) / x_celk) * s.image_x)
    y = s.edge + (((coord.y - s.min_y_coord) / y_celk) * s.image_y)
    # print(x_celk, y_celk, coord.x, x, coord.y, y)
    return x, y


def distance(point_a, point_b):
    global counter_distance
    counter_distance += 1
    return math.sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)


def count_distance(order):
    global travel_points
    global s
    global counter_full_distance
    dist = 0
    counter_full_distance += 1
    for i in range(len(order)):
        dist += distance(travel_points[order[i]], travel_points[order[(i+1) % len(order)]])
    return dist


def update_values(l):
    global travel_points
    global s
    for i in range(len(l)):
        travel_points[l[i]].next_label = travel_points[l[(i+1) % s.tp]].label
        travel_points[l[i]].prev_label = travel_points[l[(i-1) % s.tp]].label
        travel_points[l[i]].next_dist = distance(travel_points[l[i]], travel_points[l[(i+1) % s.tp]])
        travel_points[l[i]].prev_dist = distance(travel_points[l[i]], travel_points[l[(i-1) % s.tp]])
        s.dist += distance(travel_points[l[i]], travel_points[l[(i+1) % s.tp]])


def algorithm_random():
    global travel_points
    global s
    visited = []
    not_visited = []
    for i in travel_points:
        not_visited.append(travel_points[i].label)
    while len(not_visited) > 0:
        now = random.randint(0, len(not_visited)-1)
        visited.append(not_visited[now])
        not_visited.pop(now)
    update_values(visited)
    s.order = visited[:]
    s.dist = count_distance(s.order)


def algorithm_greedy():
    global travel_points
    global s

    visited = []
    not_visited = []
    for i in travel_points:
        not_visited.append(travel_points[i].label)

    now = random.randint(0, len(not_visited) - 1)
    visited.append(not_visited[now])
    not_visited.pop(now)

    current = visited[0]
    while len(not_visited) > 0:
        closest_id = 0
        closest_dist = 10**100
        for tp in not_visited:
            tp_dist = distance(travel_points[current], travel_points[tp])
            if tp_dist < closest_dist:
                closest_dist = tp_dist
                closest_id = tp

        visited.append(closest_id)
        not_visited.pop(not_visited.index(closest_id))

    update_values(visited)
    s.order = visited[:]


def algorithm_tabu():
    global travel_points
    global s
    algorithm_greedy()
    order = s.order[:]

    #print(s.order, s.tp)
    tabu_list = []
    for i in range(1000):
        order, switch, tabu_list = tabu_best_switch(order, tabu_list)
        #print(count_distance(order))
        if switch == 0:
            break
        #draw_picture(order)
    s.order = order
    s.dist = count_distance(order)


def algorithm_stochastic_tabu(fes, fes_in_round):
    global travel_points
    global s
    algorithm_greedy()
    # algorithm_insertion('random')
    order = s.order[:]
    tabu_list = []
    intermitent_results = []
    while fes > 0:
        intermitent_results, fes, order, tabu_list = tabu_stochastic_best_switch(intermitent_results, fes, fes_in_round, order, tabu_list)

    best_dist = count_distance(order)
    if best_dist < s.dist:
        s.order = order[:]
        s.dist = count_distance(s.order)
    return intermitent_results


def tabu_stochastic_best_switch(intermitent_results, fes, fes_in_round, order, tabu_list):
    global travel_points
    global s
    count = len(order)
    best_dist = 10**100
    best_i = -1
    best_j = -1
    # for i, j in [(i, j) for i in range(count) for j in range(count) if i < j]:
    while fes_in_round > 0 and fes > 0:
        i = random.randint(0, count-1)
        j = random.randint(0, count-1)
        if i >= j:
            continue
        if (str(i) + '|' + str(j)) in tabu_list:
            continue

        tmp = order[:]
        tmp[j], tmp[i] = tmp[i], tmp[j]
        cur_dist = count_distance(tmp)
        fes_in_round -= 1
        fes -= 1
        if cur_dist < best_dist:
            best_dist = cur_dist
            best_i = i
            best_j = j
        if best_dist < s.dist:
            s.order = order[:]
    tabu_list.append(str(order[best_i]) + "|" + str(order[best_j]))
    if len(tabu_list) > s.tabu_length:
        tabu_list.pop(0)
    order[best_i], order[best_j] = order[best_j], order[best_i]
    if best_dist < s.dist:
        s.order = order[:]
        s.dist = best_dist
    intermitent_results.append(s.dist)
    return intermitent_results, fes, order, tabu_list


def tabu_best_switch(order, tabu_list):
    global travel_points
    global s
    count = len(order)
    best_dist = count_distance(order)
    best_i = -1
    best_j = -1
    #print(best_dist, order)
    for i, j in [(i, j) for i in range(count) for j in range(count) if i < j]:
        if (str(i) + '|' + str(j)) in tabu_list:
            continue
        tmp = order[:]
        tmp[j], tmp[i] = tmp[i], tmp[j]
        cur_dist = count_distance(tmp)
        if cur_dist < best_dist:
            best_dist = cur_dist
            best_i = i
            best_j = j

    if best_i == -1 and best_j == -1:
        return order, 0, tabu_list
    else:
        tabu_list.append(str(order[best_i]) + "|" + str(order[best_j]))
        if len(tabu_list) > s.tabu_length:
            tabu_list.pop(0)
        order[best_i], order[best_j] = order[best_j], order[best_i]
        return order, 1, tabu_list


def algorithm_insertion(type_of_insertion):
    global travel_points
    global s


    if type_of_insertion not in ['random', 'nearest', 'farthest', 'cheapest']:
        print("Wrong type of insertion, using default (random)")
        type_of_insertion = 'random'
    visited = []
    not_visited = []
    for i in travel_points:
        not_visited.append(travel_points[i].label)

    ## random select first 2
    for i in range(2):
        tp = random.randint(0, len(not_visited) - 1)
        visited.append(not_visited[tp])
        not_visited.pop(tp)

    while len(not_visited) > 0:
        visited, not_visited = insertion_next(type_of_insertion, visited, not_visited)
        # print(str(len(not_visited)) + "/" + str(len(visited)))
    s.order = visited[:]
    s.dist = count_distance(visited)


def insertion_next(inner_function, visited, not_visited):
    if inner_function in ['random', 'nearest', 'farthest']:
        visited, not_visited = insertion_indirect(inner_function, visited, not_visited)
    elif inner_function == 'cheapest':
        visited, not_visited = insertion_direct(visited, not_visited)
    return visited, not_visited


def insertion_direct(visited, not_visited):
    global travel_points
    best_dist = 10**100
    best_position = ''
    best_n = ''
    best_n_val = ''
    for n in range(len(not_visited)):
        tp = not_visited[n]
        for position in range(len(visited)+1):
            tmp_visited = visited[:]
            tmp_visited.insert(position, tp)
            now_distance = count_distance(tmp_visited)
            if now_distance < best_dist:
                best_dist = now_distance
                best_position = position
                best_n = n
                best_n_val = tp
            del tmp_visited
    visited.insert(best_position, best_n_val)
    not_visited.pop(best_n)
    return visited, not_visited


def insertion_indirect(inner_function, visited, not_visited):
    global travel_points
    if inner_function == 'random':
        tp = random.randint(0, len(not_visited) - 1)
    elif inner_function in ['nearest', 'farthest']:
        tp = insertion_distance(inner_function, visited, not_visited)

    tp_point = not_visited[tp]
    not_visited.pop(tp)

    best_distance = 10**100
    best_position = -1
    for position in range(len(visited)):
        tmp_visited = visited[:]
        tmp_visited.insert(position, tp_point)
        now_distance = count_distance(tmp_visited)
        if now_distance < best_distance:
            best_distance = now_distance
            best_position = position

    visited.insert(best_position, tp_point)
    return visited, not_visited


def insertion_distance(inner_function, visited, not_visited):
    global travel_points
    if inner_function == 'nearest':
        best_dist = 10**100
    else:
        best_dist = 0
    best_n = ''
    for v, n in [(v, n) for v in visited for n in not_visited]:
        dist = distance(travel_points[v], travel_points[n])
        if (inner_function == 'nearest' and dist < best_dist) or (inner_function == 'farthest' and dist > best_dist):
            best_n = n
    for i in range(len(not_visited)):
        if best_n == not_visited[i]:
            return i


def compute_results(results, algorithm=''):
    min_result = 10**100
    max_result = 0
    median_result = statistics.median(results)
    stdev_result = statistics.stdev(results)

    for i in results:
        if i < min_result:
            min_result = i
        if i > max_result:
            max_result = i

    min_result = round(min_result, 2)
    max_result = round(max_result, 2)
    median_result = round(median_result, 2)
    stdev_result = round(stdev_result, 2)
    print("algorithm: %s; iterations: %s; min: %s; max: %s; median: %s; stdev: %s" % (algorithm, str(len(results)), str(min_result), str(max_result),
          str(median_result), str(stdev_result)))


s = Salesman()
travel_points = {}

load_file("tsp.txt")

counter_distance = 0
counter_full_distance = 0

iterations = 30

results = []
used_distance = []
used_full_distance = []

partial_results = {}

for i in range(iterations):
    s = Salesman()
    travel_points = {}
    load_file("tsp.txt")
    #partial_results[i] = algorithm_stochastic_tabu(10000, 100)
    algorithm_tabu()
    print("iteration %s: %s; computations: %s, full computations: %s" % (str(i), str(s.dist), str(counter_distance), str(counter_full_distance)))
    results.append(s.dist)
    used_distance.append(counter_distance)
    used_full_distance.append(counter_full_distance)
    del s
    del travel_points
    counter_distance = 0
    counter_full_distance = 0

compute_results(results, "Tabu")
compute_results(used_distance, "Tabu - Used Distance")
compute_results(used_full_distance, "Tabu - Used Full Distnance")

#
# for i in partial_results:
#         print(partial_results[i])

#
# for i in distances:
#     print(i, distances[i])

#algorithm_random()

# algorithm_greedy()
# draw_picture()
# algorithm_stochastic_tabu(10000, 100)
# for i in travel_points:
#     print(travel_points[i].prev_label, travel_points[i].label, travel_points[i].next_label, travel_points[i].prev_dist, travel_points[i].next_dist )

# algorithm_insertion()
# draw_picture()

# print("order:", s.order)
# print("distance:", s.dist)

# algorithm_tabu()
# draw_picture()
#
# print("order:", s.order)
# print("distance:", s.dist)
