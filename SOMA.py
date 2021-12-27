import math

import TFunctions
import sys
import random
import operator
import statistics

class Member:
    def __init__(self, member_id, coords):
        self.member_id = member_id
        self.coords = coords
        self.value = ''
        self.next_coords = []
        self.next_value = ''

    def update_values(self):
        if self.next_value != '' and self.next_value < self.value:
            self.value = self.next_value
            self.next_value = ''
            self.coords = self.next_coords[:]
            self.next_coords.clear()

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


class SOMA:
    def __init__(self, max_fes=10000, NP=50, dimensions=10, algorithm="FirstDeJong", prt=0.3, path_length=3, step=0.33,
                 range_min=-5, range_max=5, m=20, n=10, k=5):
        self.max_fes = max_fes
        self.used_fes = 0
        self.out_of_budget = False
        self.NP = NP
        self.dimensions = dimensions
        self.prt = prt
        self.path_length = path_length
        self.step = step
        self.members = []
        self.range_min = range_min
        self.range_max = range_max
        self.m = m
        self.n = n
        self.k = k
        self.algorithm = algorithm
        self.stats = {}
        self.round_stats = {}
        self.round_best_value = []

    def compute(self):
        self.initialize_vectors()
        round_num = 0
        self.get_round_stats(round_num)
        while not self.out_of_budget:
            round_num += 1
            self.update_parameters()
            self.soma_round()
            self.get_round_stats(round_num)

    def evaluate_fitness_function(self, member):
        if self.used_fes < self.max_fes:
            self.used_fes += 1
            member.compute_value(self.algorithm)
        else:
            self.out_of_budget = True
            self.path_length = 0
        return member

    def initialize_vectors(self):
        for i in range(self.NP):
            coords = []
            for j in range(self.dimensions):
                val = self.range_min + random.random() * (self.range_max-self.range_min)
                coords.append(val)
            tmp = Member(i, coords)
            tmp = self.evaluate_fitness_function(tmp)
            self.members.append(tmp)

    def soma_round(self):
        # step 1 - choose migrants
        migrants = self.choose_members(self.n, self.m)

        # step 2 - for each migrant:
        for migrant in migrants:
            # step 2.1 - find leader
            leader = self.choose_members(1, self.k)[0]

            if migrant.member_id == leader.member_id:
                pass
            else:
                t = self.step
                while t <= self.path_length:
                    possible_member = self.find_new_position(migrant, leader, t)
                    if possible_member != 0 and possible_member.value != '':
                        if (migrant.next_value == '' and possible_member.value < migrant.value) or (migrant.next_value != '' and possible_member.value < migrant.next_value):
                            migrant.next_value = possible_member.value
                            migrant.next_coords = possible_member.coords
                    t += self.step
                if migrant.next_value != '' and (migrant.next_value < self.members[migrant.member_id].value):
                    self.members[migrant.member_id].next_value = migrant.next_value
                    self.members[migrant.member_id].next_coords = migrant.next_coords

        for member in range(len(self.members)):
            self.members[member].update_values()

    def choose_members(self, choose_num, out_of):
        # step 1 - generate 'choose_num' random numbers from interval [0,NP-1]
        mem_id = []
        while len(mem_id) < out_of:
            test_m = random.randint(0, self.NP-1)
            if test_m not in mem_id:
                mem_id.append(test_m)

        # step 2 - create list of members at indexes mem_id
        mem = []
        for i in mem_id:
            mem.append(self.members[i])

        # step 3 - create sorted list of mem
        sorted_mem = sorted(mem, key=operator.attrgetter('value'))

        # step 4 - get first 'out of' from list and return that list
        res = []
        for i in range(choose_num):
            res.append(sorted_mem[i])

        return res

    def generate_prt_vector(self):
        prt_vector = []
        for i in range(self.dimensions):
            if random.random() < self.prt:
                prt_vector.append(1)
            else:
                prt_vector.append(0)
        return prt_vector

    def find_new_position(self, member, leader, t):
        new_coords = []
        prt_vector = self.generate_prt_vector()
        v_check = False
        for i in prt_vector:
            if prt_vector[i] == 1:
                v_check = True
        if not v_check:
            return 0

        for i in range(self.dimensions):
            new = member.coords[i] + (leader.coords[i] - member.coords[i]) * t * prt_vector[i]
            if new < self.range_min:
                new = self.range_min
            elif new > self.range_max:
                new = self.range_max
            new_coords.append(new)

        tmp = Member(0, new_coords)
        tmp = self.evaluate_fitness_function(tmp)

        return tmp

    def update_parameters(self):
        self.prt = 0.08 + 0.9 * (self.used_fes / self.max_fes)
        self.step = 0.02 + 0.005 * math.cos(0.5 * math.pi * 10**-7 * self.used_fes)

    def get_stats(self, value_list='', round_num=0):

        vals = []
        if value_list == '':
            value_list == self.members
            for i in range(len(value_list)):
                vals.append(self.members[i].value)
        else:
            vals = value_list
        self.stats['count'] = len(vals)
        self.stats['minimum'] = min(vals)
        self.stats['maximum'] = max(vals)
        self.stats['FES_remaining'] = self.max_fes - self.used_fes
        if len(vals) > 1:
            self.stats['median'] = statistics.median(vals)
            self.stats['mean'] = statistics.mean(vals)
            self.stats['stdev'] = statistics.stdev(vals)
        else:
            self.stats['median'] = min(vals)
            self.stats['mean'] = min(vals)
            self.stats['stdev'] = 0

        output = ''
        for i in self.stats:
            output += str(i) + ": " + str(self.stats[i]) + "; "
            #print(i, self.stats[i])
        return output

    def get_round_stats(self, round):
        vals = []
        for i in self.members:
            vals.append(i.value)

        stats = self.get_stats(vals, round)
        self.round_best_value.append(self.stats['minimum'])
        self.round_stats[round] = stats

