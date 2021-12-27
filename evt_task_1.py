import Diferencial_Evolution
import statistics
import matplotlib.pyplot as plt

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

    def count_stats(self):
        vals = []
        for inst in self.instances:
            vals.append(self.instances[inst].value)

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
        text = "algorithm: %s; function: %s; dimensions: %s; runtimes: %s; minimum: %s; maximum: %s; mean: %s; median: %s; stdev: %s" \
               % (self.algorithm, self.function, self.dimensions, self.runtimes, self.minimum, self.maximum, self.mean, self.median,
                  self.stdev)
        return text


class OneResult:
    def __init__(self, runid, best_member, value, round_results):
        self.runid = runid
        self.best_member = best_member
        self.value = value
        self.round_results = round_results


def draw_graph(data, name, offset=0, labels=[], limits=(0, 0), logscale=True):
    xace = []

    first_i = ''
    for i in data:
        if first_i == '':
            first_i = i

    for a in range(1, len(data[first_i].round_results)+1):
        xace.append(a)
    for i in data:
        if offset > 0:
            for j in range(offset):
                data[i].round_results[j] = data[i].round_results[offset]
        if len(labels) > 0:
            plt.plot(xace, data[i].round_results, label=labels[i])
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
    plt.savefig('figures_evt//' + name +'.png')
    plt.close()



# hlavní zápočtový úkol - algoritmus jDE

# algorithms = ['jDE-']
test_functions = ['FirstDeJong', 'SecondDeJong', 'Schwefel', 'Rastrigin']
dimensions = [10, 30]
number_of_runs = 30

#test_functions = ['Rastrigin']
#dimensions = [10, 30]
#number_of_runs = 5

result_list = {}

for dimension in dimensions:
    for test_function in test_functions:
        if test_function in ['FirstDeJong', 'SecondDeJong']:
            alg_min = -5
            alg_max = 5
        else:
            alg_min = -500
            alg_max = 500

        for run_number in range(number_of_runs):
            resid = "jDE(" + str(dimension) + "D)-" + test_function
            if resid not in result_list:
                result_list[resid] = Results('jDE', test_function, number_of_runs, 5000*dimension, dimension)
            print("running function: %s run: %s" % (resid, str(run_number+1)))
            x = Diferencial_Evolution.DifferencialEvolution(FES=5000*dimension, dimensions=dimension,
                                                            algorithm=test_function, mutation_type='DE/rand/1',
                                                            range_min=alg_min, range_max=alg_max)
            x.compute()
            result_list[resid].instances[run_number+1] = OneResult(run_number+1, x.members[:], x.stats['minimum'], x.round_best_value[:])
            #x.get_stats(members)
            #print(x.round_best_value)


file = open("figures_evt//vysledky.txt", "w")


for i in result_list:
    result_list[i].count_stats()
    print(result_list[i].printstats())
    file.write(result_list[i].printstats())
    file.write("\n")
file.close()

#talgs = algorithms
talgs= ['jDE(10D)-', 'jDE(30D)-']
tfunctions = test_functions

for ta in talgs:
    for tf in tfunctions:
        prumery = []
        for num in range(len(result_list[ta + tf].instances[1].round_results)):
            tmp = []
            for iters in range(1, number_of_runs+1):
                tmp.append(result_list[ta + tf].instances[iters].round_results[num])
            oneavg = statistics.mean(tmp)
            prumery.append(oneavg)
            del tmp
        result_list['Average ' + ta + tf] = Results('Average ' + ta + tf, tf, 1, 1000, 10)
        result_list['Average ' + ta + tf].instances[1] = OneResult(1, [], 0, prumery[:])

## Grafy
for ta in talgs:
    for tf in tfunctions:
        if tf == 'Schwefel':
            draw_log_scale = False
        else:
            draw_log_scale = True
        draw_graph(result_list[ta + tf].instances, 'All Runs ' + ta + ' ' + tf, offset=0, logscale=draw_log_scale)
        draw_graph(result_list['Average ' + ta + tf].instances, 'Average ' + ta + ' ' + tf, offset=0, logscale=draw_log_scale)


# for tf in tfunctions:
#     i = 0
#     result_list['Combined average ' + tf] = Results('Combined average ' + tf, tf, 1, 1000, 10)
#     for ta in talgs:
#         result_list['Combined average ' + tf].instances[i] = OneResult(1, [], 0, result_list['Average ' + ta + tf].instances[1].round_results)
#         i += 1
#     draw_graph(result_list['Combined average ' + tf].instances, 'Combined average' + tf, offset=0, labels=talgs)

