import Algorithms
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

    def count_stats(self):
        vals = []
        for inst in self.instances:
            vals.append(self.instances[inst].vhodnost)

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


# runtimes = 30
# fes = 10000
# dimensions = 10
#
# talgs = ['RandomSearch', 'LocalSearch', 'Hill Climber']
# tfunctions = ['FirstDeJong', 'SecondDeJong', 'Schwefel']
#
# result_list = {}
#

# 'RANDOMSEARCH'
# for funct in tfunctions:
#     for run in range(1, runtimes+1):
#         resid = "RandomSearch" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('RandomSearch', funct, runtimes, fes, dimensions)
#         x = Algorithms.RandomSearch(fes, dimensions, funct, verbose=False, print_all=False, file='',
#                                     id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#
# 'LOCALSEARCH'
# for funct in tfunctions:
#     for run in range(1, runtimes+1):
#         resid = "LocalSearch" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('LocalSearch', funct, runtimes, fes, dimensions)
#         x = Algorithms.LocalSearch(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=1, verbose=False, print_all=False,
#                                    file='', id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#
# 'HILLCLIMBING'
# for funct in tfunctions:
#     for run in range(1, runtimes+1):
#         resid = "HillClimbing" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('HillClimbing', funct, runtimes, fes, dimensions)
#         x = Algorithms.HillClimbing(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=0, verbose=False, print_all=False,
#                                    file='', id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#
#
# 'SIMULATEDANNEALING'
# for funct in tfunctions:
#     for run in range(1, runtimes+1):
#         resid = "SimulatedAnnealing" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('SimulatedAnnealing', funct, runtimes, fes, dimensions)
#         x = Algorithms.SimulatedAnnealing(fes, 10, dimensions, 0.1, funct, 1000, 0.1, 0.991, verbose=False,
#                                           print_all=False, file='', id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#
# for i in result_list:
#     result_list[i].count_stats()
#     print(result_list[i].printstats())


#
# xace = []
# for a in range(1, 10001):
#     xace.append(a)
#
# fun = []
#
# for i in result_list['RandomSearchFirstDeJong'].instances:
#     plt.plot(x, result_list['RandomSearchFirstDeJong'].instances[i].vysledky)
# plt.savefig('test.png')
# plt.close()
# for i in result_list['RandomSearchSecondDeJong'].instances:
#     plt.plot(x, result_list['RandomSearchSecondDeJong'].instances[i].vysledky)
# plt.savefig('test2.png')
#
# #
#
# runtimes = 10
# 'SIMULATEDANNEALING'
# for funct in tfunctions:
#     for run in range(1, runtimes+1):
#         resid = "SimulatedAnnealing" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('SimulatedAnnealing', funct, runtimes, fes, dimensions)
#         x = Algorithms.SimulatedAnnealing(fes, 10, dimensions, 0.1, funct,
#                                           pocatecni_teplota=1000,
#                                           konecna_teplota=0.1,
#                                           redukce_teploty=0.991,
#                                           verbose=False, print_all=False, file='', id_spusteni=run)
#         # x.nastaveni_teploty(100, 0.1)
#         x.dynamicke_nastaveni(100, nastaveni_redukce_teploty=True, pocatecni_teplota='', konecna_teplota='',
#                               nastaveni_velikosti_okoli='staticky')
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#         # print("TEPLOTA:", x.soucasna_teplota, "FES", x.fes)
#
# for i in result_list:
#     result_list[i].count_stats()
#     print(result_list[i].printstats())
#
# y = result_list['SimulatedAnnealingFirstDeJong'].instances[1].vysledky
#
#
#
# plt.plot(xace, y)
# plt.savefig('test.png')

# ----- TestBed2020
# runtimes = 30
# dimensions = 5
# fes = 50000  # pro D5
# fes = 1000000  # pro D10
#
# fes = 50000
#
# talgs = ['RandomSearch', "LocalSearch"]
# tfunctions = 'TB_'
#
# result_list = {}
#
#
# 'TestBed1'
# for tmp in range(1, 11):
#     funct = "TB_" + str(tmp)
#     for run in range(1, runtimes+1):
#         resid = "RandomSearch" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('RandomSearch', funct, runtimes, fes, dimensions)
#         x = Algorithms.RandomSearch(fes, dimensions, funct, verbose=True, print_all=True, file='',
#                                     id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#         print(resid, run)
#
#     for run in range(1, runtimes + 1):
#         resid = "LocalSearch" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('LocalSearch', funct, runtimes, fes, dimensions)
#         x = Algorithms.LocalSearch(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=1, verbose=False, print_all=False,
#                                    file='', id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#         print(resid, run)
#
#     for run in range(1, runtimes + 1):
#         resid = "HillClimbing" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('HillClimbing', funct, runtimes, fes, dimensions)
#         x = Algorithms.HillClimbing(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=0, verbose=False, print_all=False,
#         file='', id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#         print(resid, run)
#
#     for run in range(1, runtimes + 1):
#         resid = "SimulatedAnnealing" + funct
#         if resid not in result_list:
#             result_list[resid] = Results('SimulatedAnnealing', funct, runtimes, fes, dimensions)
#         x = Algorithms.SimulatedAnnealing(fes, 10, dimensions, 0.1, funct,
#                                           pocatecni_teplota=1000,
#                                           konecna_teplota=0.1,
#                                           redukce_teploty=0.991,
#                                           verbose=False, print_all=False, file='', id_spusteni=run)
#         x.compute()
#         result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#         print(resid, run)
#
# for i in result_list:
#     result_list[i].count_stats()
#     print(result_list[i].printstats())

# TESTBETD REAL

runtimes = 30
dimensions = 5
fes = 50000  # pro D5
fes = 1000000  # pro D10

runtimes = 30
fes = 50000


result_list = {}
t0 = time.time()
'TestBed1'

for kon_teplota in [1]: #[10**0, 10**1, 10**2, 10**3, 10**4]:
    for pt in [100]: #[10**1, 10**2, 10**3, 10**4, 10**5]:
        poc_teplota = kon_teplota * pt
        for pocet_kol in  [1000]: # [10, 50, 100, 500, 1000]:
            for id_funct in range(1, 11):
                funct = "TB_" + str(id_funct)
                for run in range(1, runtimes + 1):
                    resid = "SimulatedAnnealing" +", KT:" + str(kon_teplota) +", PT:" + str(poc_teplota) +", PK:" + str(pocet_kol) + ', F:' +  funct
                    if resid not in result_list:
                        result_list[resid] = Results(resid, funct, runtimes, fes, dimensions)
                    x = Algorithms.SimulatedAnnealing(fes, 10, dimensions, 0.1, funct,
                                                      pocatecni_teplota=poc_teplota,
                                                      konecna_teplota=kon_teplota,
                                                      redukce_teploty='',
                                                      verbose=False, print_all=False, file='', id_spusteni=run)
                    x.dynamicke_nastaveni(pocet_kol=fes/50, nastaveni_redukce_teploty=True)
                    x.nastaveni_teploty()
                    x.compute()
                    # print(x.vhodnost, x.soucasna_teplota)
                    result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])


file = open('tmp.txt',"w")

for i in result_list:
    result_list[i].count_stats()
    file.write(result_list[i].printstats())
    file.write("\n")

    # print(result_list[i].printstats())

file.close()
print(time.time() - t0)