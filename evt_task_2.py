import Diferencial_Evolution
import SOMA
import statistics
import matplotlib.pyplot as plt
import time

class Results:
    def __init__(self, algorithm, function, runtimes, iterations, dimensions):
        self.algorithm = algorithm
        self.function = function
        self.runtimes = runtimes
        self.iterations = iterations
        self.dimensions = dimensions
        self.instances = {}
        self.minimum = ''
        self.maximum = ''
        self.mean = ''
        self.median = ''
        self.stdev = ''
        self.vals = ''

    def count_stats(self):
        vals = []
        for inst in self.instances:
            vals.append(self.instances[inst].value)
        self.vals = vals
        self.minimum = min(vals)
        self.maximum = max(vals)
        if len(vals) > 1:
            self.median = statistics.median(vals)
            self.mean = statistics.mean(vals)
            self.stdev = statistics.stdev(vals)
        else:
            self.median = min(vals)
            self.mean = min(vals)
            self.stdev = 0

    def printstats(self):
        text = "algorithm: %s; function: %s; dimensions: %s; runtimes: %s; minimum: %s; maximum: %s; mean: %s; median: %s; stdev: %s; values: %s" \
               % (self.algorithm, self.function, self.dimensions, self.runtimes, self.minimum, self.maximum, self.mean, self.median,
                  self.stdev, str(self.vals))
        return text


class OneResult:
    def __init__(self, runid, best_member, value, round_results):
        self.runid = runid
        self.best_member = best_member
        self.value = value
        self.round_results = round_results
        self.shortened_round_results = ''


def draw_graph(data, name, offset=0, labels=[], limits=(0, 0), logscale=True):
    xace = []


    first_i = ''
    for i in data:
        if first_i == '':
            first_i = i

    used_lengths = []

    for d in data:
        if len(data[d].round_results) not in used_lengths:
            used_lengths.append(len(data[d].round_results))

    if len(used_lengths) > 1:
        use_special = True
        shortest = min(used_lengths)
        range_to = shortest +1
        for d in data:
            data[d].shortened_round_results = pick_data_from_list(shortest, data[d].round_results)
    else:
        use_special = False
        range_to = len(data[first_i].round_results) + 1

    for a in range(1, range_to):
        xace.append(a)
    for i in data:
        if offset > 0:
            for j in range(offset):
                data[i].round_results[j] = data[i].round_results[offset]
        if len(labels) > 0:
            if use_special:
                plt.plot(xace, data[i].shortened_round_results, label=labels[i])
            else:
                plt.plot(xace, data[i].round_results, label=labels[i])
        else:
            if use_special:
                plt.plot(xace, data[i].shortened_round_results)
            else:
                plt.plot(xace, data[i].round_results)

    if len(labels) > 0:
        plt.legend()
    if limits != (0, 0):
        plt.ylim(limits[0], limits[1])
    plt.title(name)
    plt.xlabel('Evolution round')
    if logscale:
        plt.yscale('log')
        plt.ylabel('Value (log scale)')
    else:
        plt.ylabel('Value')
    plt.savefig('figures_evt_tb//' + name +'.png')
    plt.close()


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



# nepovinný zápočtový úkol - algoritmus jDE a T3A SOMA na testbed

algorithms = ['jDE', 'T3A-SOMA']
dimensions = [10, 20]
test_functions = ['TB_1', 'TB_2', 'TB_3', 'TB_4', 'TB_5', 'TB_6', 'TB_7', 'TB_8', 'TB_9', 'TB_10']
number_of_runs = 30

#test_functions = ['TB_9', 'TB_10']
#dimensions = [20]
number_of_runs = 30

result_list = {}

alg_min = -100
alg_max = 100


number_FES = {}
number_FES[10] = 1000000
number_FES[20] = 10000000



# for i in number_FES:
#     number_FES[i] = 100000

#jDE

starttime = time.time()

for dimension in dimensions:
    for test_function in test_functions:
        for run_number in range(number_of_runs):
            startrun = time.time()
            resid = "jDE(" + str(dimension) + "D)-" + test_function
            if resid not in result_list:
                result_list[resid] = Results('jDE', test_function, number_of_runs, number_FES[dimension], dimension)
            print("running function: %s run: %s" % (resid, str(run_number+1)))
            x = Diferencial_Evolution.DifferencialEvolution(FES=number_FES[dimension], dimensions=dimension,
                                                            algorithm=test_function, mutation_type='DE/rand/1',
                                                            range_min=alg_min, range_max=alg_max)
            x.compute()
            result_list[resid].instances[run_number+1] = OneResult(run_number+1, x.members[:], x.stats['minimum'], x.round_best_value[:])
            print("Runtime: ",  time.time() - startrun)
            #x.get_stats(members)
            #print(x.round_best_value)

midtime = time.time()
print("jDA done, time: ", midtime - starttime)

#SOMA
for dimension in dimensions:
    for test_function in test_functions:
        for run_number in range(number_of_runs):
            startrun = time.time()
            resid = "T3A-SOMA(" + str(dimension) + "D)-" + test_function
            if resid not in result_list:
                result_list[resid] = Results('T3A-SOMA', test_function, number_of_runs, number_FES[dimension], dimension)
            print("running function: %s run: %s" % (resid, str(run_number+1)))
            x = SOMA.SOMA(max_fes=number_FES[dimension], dimensions=dimension, algorithm=test_function,
                          range_min=alg_min, range_max=alg_max, m=25, n=8, k=15)
            x.compute()
            result_list[resid].instances[run_number+1] = OneResult(run_number+1, x.members[:], x.stats['minimum'], x.round_best_value[:])
            print("Runtime: ", time.time() - startrun)
            #print(len(x.round_best_value))
            #x.get_stats(members)
            #print(x.round_best_value)

endtime = time.time()
print("SOMA done, time: ", endtime - midtime)
print("Total time: ", endtime - starttime)
file = open("figures_evt_tb//vysledky.txt", "w")


for i in result_list:
    result_list[i].count_stats()
    print(result_list[i].printstats())
    file.write(result_list[i].printstats())
    file.write("\n")
file.close()

#talgs = algorithms
talgs = ['jDE(20D)-', 'T3A-SOMA(20D)-']
#talgs = ['T3A-SOMA(10D)-']
tfunctions = test_functions

for ta in talgs:
    for tf in tfunctions:
        prumery = []
        for num in range(len(result_list[ta + tf].instances[1].round_results)):
            tmp = []
            for iters in range(1, number_of_runs+1):
                try:
                    tmp.append(result_list[ta + tf].instances[iters].round_results[num])
                    last_appended = result_list[ta + tf].instances[iters].round_results[num]
                except:
                    #print("Something went wrong while fetching numbers")
                    tmp.append(last_appended)
            oneavg = statistics.mean(tmp)
            prumery.append(oneavg)
            del tmp
        result_list['Average ' + ta + tf] = Results('Average ' + ta + tf, tf, 1, 1000, 10)
        result_list['Average ' + ta + tf].instances[1] = OneResult(1, [], 0, prumery[:])


## Grafy
for ta in talgs:
    for tf in tfunctions:
        draw_graph(result_list[ta + tf].instances, 'All Runs ' + ta + ' ' + tf, offset=0)
        draw_graph(result_list['Average ' + ta + tf].instances, 'Average ' + ta + ' ' + tf, offset=0)


for tf in tfunctions:
    i = 0
    result_list['Combined average ' + tf] = Results('Combined average ' + tf, tf, 1, 1000, 10)
    for ta in talgs:
        result_list['Combined average ' + tf].instances[i] = OneResult(1, [], 0, result_list['Average ' + ta + tf].instances[1].round_results)
        i += 1
    draw_graph(result_list['Combined average ' + tf].instances, 'Combined average' + tf, offset=0, labels=talgs)

