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


def draw_graph(data, name, offset=0, labels=[], limits=(0, 0)):
    xace = []
    for a in range(1, 10001):
        xace.append(a)

    for i in data:
        if offset > 0:
            for j in range(offset):
                data[i].vysledky[j] = data[i].vysledky[offset]
        if len(labels) > 0:
            plt.plot(xace, data[i].vysledky, label=labels[i])
        else:
            plt.plot(xace, data[i].vysledky)
    if len(labels) > 0:
        plt.legend()
    if limits != (0, 0):
        plt.ylim(limits[0], limits[1])
    plt.title(name)
    plt.xlabel('CF')
    plt.ylabel('Hodnota')
    plt.savefig('figures//' + name +'.png')
    plt.close()



runtimes = 30
fes = 10000
dimensions = 10

talgs = ['RandomSearch', 'LocalSearch', 'HillClimbing', 'SimulatedAnnealing']
tfunctions = ['FirstDeJong', 'SecondDeJong', 'Schwefel']
# talgs = ['SimulatedAnnealing']
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
        x = Algorithms.HillClimbing(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=0, verbose=False, print_all=False,
                                   file='', id_spusteni=run)
        x.compute()
        result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])


'SIMULATEDANNEALING'
for funct in tfunctions:
    for run in range(1, runtimes+1):
        resid = "SimulatedAnnealing" + funct
        if resid not in result_list:
            result_list[resid] = Results('SimulatedAnnealing', funct, runtimes, fes, dimensions)
        x = Algorithms.SimulatedAnnealing(fes, 10, dimensions, 0.1, funct,
                                            pocatecni_teplota=10, konecna_teplota=1, redukce_teploty='',
                                            verbose=False, print_all=False, file='', id_spusteni=run)
        x.dynamicke_nastaveni(fes_na_kolo=50, nastaveni_redukce_teploty=True, nastaveni_velikosti_okoli=True,
                                pocatecni_velikost_okoli=0.09, konecna_velikost_okoli=0.0025,
                                nastaveni_poctu_prvku_v_okoli='dynamicky', modifikator_poctu_prvku=0.7)
        x.nastaveni_teploty()
        x.compute()
        result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])

file = open("figures//vysledky.txt","w")


for i in result_list:
    result_list[i].count_stats()
    print(result_list[i].printstats())
    file.write(result_list[i].printstats())
    file.write("\n")
file.close()

## průměrné hodntoy
# for x in range(1, 31):
#     print(len(result_list['SimulatedAnnealingFirstDeJong'].instances[x].vysledky))

['FirstDeJong', 'SecondDeJong', 'Schwefel']
funclimits = {}
funclimits['FirstDeJong'] = (0, 30)
funclimits['SecondDeJong'] = (0, 3000)
funclimits['Schwefel'] = (-3500, -1000)

for ta in talgs:
    for tf in tfunctions:
        prumery = []
        for num in range(10000):
            tmp = []
            for iters in range(1, 31):
                tmp.append(result_list[ta + tf].instances[iters].vysledky[num])
            oneavg = statistics.mean(tmp)
            prumery.append(oneavg)
            del tmp
        result_list['Average ' + ta + tf] = Results('Average ' + ta + tf, tf, 1, 10000, 10)
        result_list['Average ' + ta + tf].instances[1] = OneResult(1, [], 0, prumery[:])

## Grafy
for ta in talgs:
    for tf in tfunctions:
        draw_graph(result_list[ta + tf].instances, 'All Runs ' + ta + ' ' + tf, offset=0, limits=funclimits[tf])
        draw_graph(result_list['Average ' + ta + tf].instances, 'Average ' + ta + ' ' + tf, offset=0, limits=funclimits[tf])

for tf in tfunctions:
    i = 0
    result_list['Combined average ' + tf] = Results('Combined average ' + tf, tf, 1, 10000, 10)
    for ta in talgs:
        result_list['Combined average ' + tf].instances[i] = OneResult(1, [], 0, result_list['Average ' + ta + tf].instances[1].vysledky)
        i += 1
    draw_graph(result_list['Combined average ' + tf].instances, 'Combined average' + tf, offset=0, labels=talgs, limits=funclimits[tf])







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

#----- TestBed2020
# runtimes = 30
# dimensions = 10
# fes = 50000  # pro D5
# fes = 1000000  # pro D10
#
#
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
#     # for run in range(1, runtimes+1):
#     #     resid = "RandomSearch" + funct
#     #     if resid not in result_list:
#     #         result_list[resid] = Results('RandomSearch', funct, runtimes, fes, dimensions)
#     #     x = Algorithms.RandomSearch(fes, dimensions, funct, verbose=True, print_all=True, file='',
#     #                                 id_spusteni=run)
#     #     x.compute()
#     #     result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#     #     print(resid, run)
#     #
#     # for run in range(1, runtimes + 1):
#     #     resid = "LocalSearch" + funct
#     #     if resid not in result_list:
#     #         result_list[resid] = Results('LocalSearch', funct, runtimes, fes, dimensions)
#     #     x = Algorithms.LocalSearch(int(fes / 10), 10, dimensions, 0.1, funct, nb_max=1, verbose=False, print_all=False,
#     #                                file='', id_spusteni=run)
#     #     x.compute()
#     #     result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#     #     print(resid, run)
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
#
# file = open('tmp.txt',"w")
#
# for i in result_list:
#     result_list[i].count_stats()
#     print(result_list[i].printstats())
#     file.write(result_list[i].printstats())
#     file.write("\n")
#
# file.close()

# TESTBETD REAL
#
# runtimes = 30
# dimensions = 5
# fes = 50000  # pro D5
# # fes = 1000000  # pro D10
#
# # runtimes = 30
# # fes = 50000
#
#
# result_list = {}
# t0 = time.time()
# 'TestBed1'
#
# for konecna in [1]:
#     for id_funct in range(1, 11):
#         funct = "TB_" + str(id_funct)
#         for run in range(1, runtimes + 1):
#             resid = "SimulatedAnnealing, mpp = " + str(konecna) + "F:" + funct
#             if resid not in result_list:
#                 result_list[resid] = Results(resid, funct, runtimes, fes, dimensions)
#             x = Algorithms.SimulatedAnnealing(fes, 10, dimensions, 0.1, funct,
#                                               pocatecni_teplota=10,
#                                               konecna_teplota=1,
#                                               redukce_teploty='',
#                                               verbose=False, print_all=False, file='', id_spusteni=run)
#             x.dynamicke_nastaveni(fes_na_kolo=50, nastaveni_redukce_teploty=True, nastaveni_velikosti_okoli=True,
#                                   pocatecni_velikost_okoli=0.09, konecna_velikost_okoli=0.0025,
#                                   nastaveni_poctu_prvku_v_okoli='dynamicky', modifikator_poctu_prvku=0.7)
#             x.nastaveni_teploty()
#             x.compute()
#             # print("pocatecni teplota: %s, konecna teplota: %s, pocet prvku v okoli: %s, pocatecni velikost okoli: %s" % (x.pocatecni_teplota, x.konecna_teplota, x.okoli, x.smodch))
#             result_list[resid].instances[run] = OneResult(run, x.bestarg[:], x.vhodnost, x.vysledky[:])
#             print(resid, run)
#             print(time.time() - t0)
#             t0 = time.time()
# file = open('tmp.txt', "a")
#
# for i in result_list:
#     result_list[i].count_stats()
#     file.write(result_list[i].printstats())
#     file.write("\n")
#
#     # print(result_list[i].printstats())
#
# file.close()
# print(time.time() - t0)