import random
import TFunctions
import sys
import statistics
import supported_algorithms

class Member:
    def __init__(self, coords):
        self.coords = coords
        self.value = ''

    def compute_value(self, algorithm):
        if algorithm == 'FirstDeJong':
            self.value = TFunctions.FirstDeJong(self.coords).compute()
        elif algorithm == 'SecondDeJong':
            self.value = TFunctions.SecondDeJong(self.coords).compute()
        elif algorithm == 'Schwefel':
            self.value = TFunctions.Schwefel(self.coords).compute()
        elif algorithm == 'Rastrigin':
            self.value = TFunctions.Rastrigin(self.coords).compute()
        elif algorithm[:3] == 'TB_':
            self.value = TFunctions.TestBed(algorithm, self.coords).compute()
        else:
            print("Algorithm not supported!")
            sys.exit(0)


class DifferencialEvolution:
    def __init__(self):
        self.g_max = 1000
        self.NP = 50
        self.F = 0.5
        self.CR = 0.9
        self.range_min = -500
        self.range_max = 500
        self.dimensions = 10
        self.members = []
        self.algorithm = 'FirstDeJong'
        self.mutation_type = 'DE/rand/1'.split("/")
        self.crossbreeding_type = 'binomial'
        self.stats = {}
        self.strategy = 'DE'

    def compute(self):
        self.check_inputs()
        if len(self.members) == 0:
            self.initialize_vectors()
        self.get_stats()
        for i in range(1, self.g_max+1):
            print("Starting round %s " % str(i))
            self.evolution_round()
            self.get_stats()

    def check_inputs(self):
        if self.algorithm.lower() not in supported_algorithms.diferencial_evolution['supported_algorithm']:
            print("Algorithm not supported: %s" % self.algorithm)
            sys.exit(1)
        if self.mutation_type[1] not in supported_algorithms.diferencial_evolution['mutation_type']:
            print("Mutation type not supported %s" % self.mutation_type[1])
            sys.exit(1)
        if int(self.mutation_type[2]) > 5:
            print("Too many random mutations (max 5)")
            sys.exit(1)
        if self.crossbreeding_type.lower() not in supported_algorithms.diferencial_evolution['crossbreeding_type']:
            print("Crossbreeding type not supported: %s" % self.crossbreeding_type)
            sys.exit(1)

    def evolution_round(self):

        x = self.members[:]
        v = self.mutation(x)
        u = self.crossbreeding(x, v)
        y = self.selection(x, u)

        self.members = y[:]

    def initialize_vectors(self):
        for i in range(self.NP):
            coords = []
            for j in range(self.dimensions):
                val = self.range_min + random.random() * (self.range_max-self.range_min)
                coords.append(val)
            tmp = Member(coords)
            tmp.compute_value(self.algorithm)
            self.members.append(tmp)

    def mutation(self, x):
        v = []
        count = int(self.mutation_type[2])
        for i in range(self.NP):
            support = []
            # Special behavior for 'DE/randrl/1
            if self.mutation_type[1] in ['randrl']:
                count -= 1
                rand_1 = x[random.randint(0, self.NP-1)]
                rand_2 = x[random.randint(0, self.NP-1)]
                rand_3 = x[random.randint(0, self.NP-1)]
                if rand_1.value < rand_2.value and rand_1.value < rand_3.value:
                    main = rand_1
                    support.append(combine_vectors(rand_2.coords, rand_3.coords, full_mult=self.F, oper="-"))
                elif rand_2.value < rand_1.value and rand_2.value < rand_3.value:
                    main = rand_2
                    support.append(combine_vectors(rand_1.coords, rand_3.coords, full_mult=self.F, oper="-"))
                else:
                    main = rand_3
                    support.append(combine_vectors(rand_1.coords, rand_2.coords, full_mult=self.F, oper="-"))
            # First part (rand, best or current)
            else:
                if self.mutation_type[1] in ['rand', 'rand-to-best']:
                    main = x[random.randint(0, self.NP-1)].coords
                elif self.mutation_type[1] == 'best':
                    main = self.best_member(x).coords
                elif self.mutation_type[1] in ['current-to-best', 'current-to-rand']:
                    main = x[i].coords
                else:
                    print("Mutation type not supported")
                    sys.exit(0)

                # Middle part (for current-to-best, current-to-rand and rand-to-best)
                if self.mutation_type[1] == 'current-to-best':
                    support.append(combine_vectors(self.best_member(x).coords, x[i].coords, full_mult=random.random(), oper="-"))
                elif self.mutation_type[1] == 'current-to-rand':
                    support.append(combine_vectors(x[random.randint(0, self.NP-1)].coords, x[i].coords, full_mult=random.random(), oper="-"))
                elif self.mutation_type[1] == 'rand-to-best':
                    support.append(combine_vectors(self.best_member(x).coords, x[random.randint(0, self.NP-1)].coords, full_mult=self.F, oper="-"))

            # Last part (F * r1 - r2 for x times)
            for j in range(count):
                support.append(combine_vectors(x[random.randint(0, self.NP-1)].coords, x[random.randint(0, self.NP-1)].coords, full_mult=self.F, oper="-"))

            for s in support:
                main = combine_vectors(main, s, oper='+')

            v.append(self.check_boundries(main))
            del support
        return v

    def crossbreeding(self, x, v):
        u = []

        for i in range(self.NP):
            coords = []
            if self.crossbreeding_type == 'binomial':
                for j in range(self.dimensions):
                    if random.random() <= self.CR:
                        coords.append(v[i][j])
                    else:
                        coords.append(x[i].coords[j])
            elif self.crossbreeding_type == 'exponential':
                count = 1
                stop = False
                while count < self.dimensions and not stop:
                    if random.random() <= self.CR:
                        count += 1
                    else:
                        stop = True
                start_point = random.randint(0, self.dimensions-1)
                for j in range(self.dimensions):
                    if start_point <= j <= start_point + count - 1 or start_point <= j + self.dimensions <= start_point + count - 1:
                        coords.append(v[i][j])
                    else:
                        coords.append(x[i].coords[j])

            tmp = Member(coords)
            tmp.compute_value(self.algorithm)
            u.append(tmp)
            del coords

        return u

    def selection(self, x, u):
        y = []
        for i in range(self.NP):
            if x[i].value < u[i].value:
                y.append(x[i])
            else:
                y.append(u[i])

        return y

    def check_boundries(self, x):
        output = []
        for i in x:
            if i < self.range_min:
                output.append(self.range_min)
            elif i > self.range_max:
                output.append(self.range_max)
            else:
                output.append(i)
        return output

    def best_member(self, x):
        best = ''
        best_val = 10**1000
        for m in x:
            if m.value < best_val:
                best = m
                best_val = m.value
        return best

    def get_values(self):
        for i in range(len(self.members)):
            print(self.members[i].value)

    def get_stats(self):
        self.stats['count'] = len(self.members)
        vals = []
        for i in range(len(self.members)):
            vals.append(self.members[i].value)

        self.stats['minimum'] = min(vals)
        self.stats['maximum'] = max(vals)
        if len(vals) > 1:
            self.stats['median'] = statistics.median(vals)
            self.stats['mean'] = statistics.mean(vals)
            self.stats['stdev'] = statistics.stdev(vals)
        else:
            self.stats['median'] = min(vals)
            self.stats['mean'] = min(vals)
            self.stats['stdev'] = 0

        for i in self.stats:
            print(i, self.stats[i])


def combine_vectors(a, b, mult=1, full_mult=1, oper="+"):
    val = []
    for i in range(len(a)):
        if oper == "+":
            val.append(full_mult*(a[i] + mult*b[i]))
        elif oper == "-":
            val.append(full_mult*(a[i] - mult*b[i]))
    return val


xx = DifferencialEvolution()
xx.compute()

