import Algorithms
import statistics

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
            vals.append(self.instances[inst].vhodnost)

        self.minimum = min(vals)
        self.maximum = max(vals)
        self.median = statistics.median(vals)
        self.mean = statistics.mean(vals)
        self.stdev = statistics.stdev(vals)

    def printstats(self):
        text = "algorithm: %s; function: %s; runtimes: %s; minimum: %s; maximum: %s; mean: %s; median: %s; stdev: %s" \
               % (self.algorithm, self.function, self.runtimes, self.minimum, self.maximum, self.mean, self.median,
                  self.stdev)
        return text

class OneResult:
    def __init__(self, runid, bestarg, vhodnost, vysledky):
        self.runid = runid
        self.bestarg = bestarg
        self.vhodnost = vhodnost
        self.vysledky = vysledky



runtimes = 30
fes = 10000
dimensions = 10

tfunctions = ['FirstDeJong', 'SecondDeJong', 'Schwefel']

result_list = {}


'RANDOMSEARCH'
for funct in tfunctions:
    for run in range(1, runtimes+1):
        resid = "RandomSearch" + funct
        if resid not in result_list:
            result_list[resid] = Results('RandomSearch', funct, runtimes, fes, dimensions)
        x = Algorithms.RandomSearch(fes, dimensions, funct, verbose=False, print_all=False, file='',
                                    id_spusteni=run)
        x.compute()
        result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])

'LOCALSEARCH'
for funct in tfunctions:
    for run in range(1, runtimes+1):
        resid = "LocalSearch" + funct
        if resid not in result_list:
            result_list[resid] = Results('LocalSearch', funct, runtimes, fes, dimensions)
        x = Algorithms.LocalSearch(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=1, verbose=False, print_all=False,
                                   file='', id_spusteni=run)
        x.compute()
        result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])

'HILLCLIMBING'
for funct in tfunctions:
    for run in range(1, runtimes+1):
        resid = "HillClimbing" + funct
        if resid not in result_list:
            result_list[resid] = Results('HillClimbing', funct, runtimes, fes, dimensions)
        x = Algorithms.LocalSearch(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=0, verbose=False, print_all=False,
                                   file='', id_spusteni=run)
        x.compute()
        result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])

for i in result_list:
    result_list[i].count_stats()
    print(result_list[i].printstats())

