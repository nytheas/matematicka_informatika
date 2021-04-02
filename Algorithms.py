import random
import TFunctions
from statistics import NormalDist


class RandomSearch:
    def __init__(self, iterace, dimenze, algoritmus, verbose=False, print_all=False, file='',
                 id_spusteni=''):
        self.iterace = iterace
        self.bestarg = []
        self.vhodnost = 100000000000
        self.dimenze = dimenze
        self.algoritmus = algoritmus
        self.verbose = verbose
        self.print_all = print_all
        self.file = file
        self.id_spusteni = id_spusteni
        if self.algoritmus in ['FirstDeJong', 'SecondDeJong']:
            self.minnum = -5
            self.maxnum = 5
        elif self.algoritmus == 'Schwefel':
            self.minnum = -500
            self.maxnum = 500
        self.vysledky = []
    classname = 'RandomSearch'

    def generate(self):
        val = []
        for i in range(self.dimenze):
            val.append(self.minnum + (random.random() * (self.maxnum - self.minnum)))
        return val

    def compute(self):
        for i in range(self.iterace):
            randval = self.generate()
            if self.algoritmus == 'FirstDeJong':
                vnow = TFunctions.FirstDeJong(randval).compute()
            elif self.algoritmus == 'SecondDeJong':
                vnow = TFunctions.SecondDeJong(randval).compute()
            elif self.algoritmus == 'Schwefel':
                vnow = TFunctions.Schwefel(randval).compute()
            else:
                print("Špatný algoritmus!!!")
                vnow = 0
            self.return_values(randval, vnow, i)
            if vnow < self.vhodnost:
                self.vhodnost = vnow
                self.bestarg = randval[:]
            self.vysledky.append(self.vhodnost)

    def return_values(self, val, vnow, iters):
        if self.verbose:
            row = "%s; %s; %s; %s; %s; %s" % (str(self.id_spusteni), str(iters), str(self.classname),
                                              str(self.algoritmus), str(val), str(vnow))
        else:
            row = "%s; %s" % (str(val), str(vnow))
        if self.file != '':
            f = open(self.file, 'a')
            if self.print_all or self.vhodnost >= vnow:
                f.write("%s\n" % row)
            f.close()
        else:
            if self.print_all or self.vhodnost >= vnow:
                print("%s" % row)


class LocalSearch:
    def __init__(self, iterace, okoli, dimenze, smodch, algoritmus, nb_max=1, verbose=False, print_all=False, file='',
                 id_spusteni=''):
        self.iterace = iterace
        self.okoli = okoli
        self.bestarg = []
        self.tmp_bestarg = []
        self.vhodnost = 100000000000
        self.tmp_vhodnost = 100000000000
        self.dimenze = dimenze
        self.algoritmus = algoritmus
        self.smodch = smodch
        self.verbose = verbose
        self.print_all = print_all
        self.file = file
        self.id_spusteni = id_spusteni
        self.nb_max = nb_max
        if self.algoritmus in ['FirstDeJong', 'SecondDeJong']:
            self.minnum = -5
            self.maxnum = 5
        elif self.algoritmus == 'Schwefel':
            self.minnum = -500
            self.maxnum = 500
        self.vysledky = []

    classname = 'LocalSearch'

    def generate(self, input_vector):
        output_vector = []

        if len(input_vector) == 0:
            for i in range(self.dimenze):
                output_vector.append(self.minnum + (random.random() * (self.maxnum - self.minnum)))
        else:
            for i in range(self.dimenze):
                valcheck = False
                while not valcheck:
                    val = NormalDist(input_vector[i], (self.smodch * (self.maxnum - self.minnum)))
                    val = val.inv_cdf(random.random())
                    if self.minnum <= val <= self.maxnum:
                        valcheck = True
                output_vector.append(val)
        return output_vector

    def compute(self):
        nb_now = 0
        for j in range(self.iterace):
            if nb_now >= self.nb_max > 0:
                self.tmp_bestarg.clear()
                self.tmp_vhodnost = 1000000000000
            local_best_arg = self.tmp_bestarg[:]
            local_vhodnost = self.tmp_vhodnost
            for i in range(self.okoli):
                randval = self.generate(self.tmp_bestarg)
                if self.algoritmus == 'FirstDeJong':
                    vnow = TFunctions.FirstDeJong(randval).compute()
                elif self.algoritmus == 'SecondDeJong':
                    vnow = TFunctions.SecondDeJong(randval).compute()
                elif self.algoritmus == 'Schwefel':
                    vnow = TFunctions.Schwefel(randval).compute()
                else:
                    print("Špatný algoritmus!!!")
                    vnow = 0

                if vnow < local_vhodnost:
                    local_vhodnost = vnow
                    local_best_arg = randval[:]
            if local_vhodnost < self.tmp_vhodnost:
                self.tmp_bestarg = local_best_arg[:]
                self.tmp_vhodnost = local_vhodnost
                nb_now = 0
            else:
                nb_now += 1

            if self.tmp_vhodnost <= self.vhodnost:
                self.bestarg = self.tmp_bestarg[:]
                self.vhodnost = self.tmp_vhodnost
            self.return_values(self.bestarg, self.vhodnost, j, i)

    def return_values(self, val, vnow, neighbours, iters):
        if self.verbose:
            row = "%s; %s; %s; %s; %s; %s; %s" % (str(self.id_spusteni), str(neighbours), str(iters),
                                                  str(self.classname), str(self.algoritmus),
                                                  str(val), str(vnow))
        else:
            row = " %s; %s" % (str(val), str(vnow))
        if self.file != '':
            f = open(self.file, 'a')
            if self.print_all or self.vhodnost >= vnow:
                f.write("%s\n" % row)
            f.close()
        else:
            if self.print_all or self.vhodnost >= vnow:
                print("%s" % row)


class HillClimbing:
    def __init__(self, iterace, okoli, dimenze, smodch, algoritmus, nb_max=0, verbose=False, print_all=False, file='',
                 id_spusteni=''):
        self.iterace = iterace
        self.okoli = okoli
        self.bestarg = []
        self.tmp_bestarg = []
        self.vhodnost = 100000000000
        self.tmp_vhodnost = 100000000000
        self.dimenze = dimenze
        self.algoritmus = algoritmus
        self.smodch = smodch
        self.verbose = verbose
        self.print_all = print_all
        self.file = file
        self.id_spusteni = id_spusteni
        self.nb_max = nb_max
        if self.algoritmus in ['FirstDeJong', 'SecondDeJong']:
            self.minnum = -5
            self.maxnum = 5
        elif self.algoritmus == 'Schwefel':
            self.minnum = -500
            self.maxnum = 500
        self.vysledky = []

    classname = 'HillClimbing'

    def generate(self, input_vector):
        output_vector = []

        if len(input_vector) == 0:
            for i in range(self.dimenze):
                output_vector.append(self.minnum + (random.random() * (self.maxnum - self.minnum)))
        else:
            for i in range(self.dimenze):
                valcheck = False
                while not valcheck:
                    val = NormalDist(input_vector[i], (self.smodch * (self.maxnum - self.minnum)))
                    val = val.inv_cdf(random.random())
                    if self.minnum <= val <= self.maxnum:
                        valcheck = True
                output_vector.append(val)
        return output_vector

    def compute(self):
        nb_now = 0
        for j in range(self.iterace):
            if nb_now >= self.nb_max > 0:
                self.tmp_bestarg.clear()
                self.tmp_vhodnost = 1000000000000
            local_best_arg = self.tmp_bestarg[:]
            local_vhodnost = self.tmp_vhodnost
            for i in range(self.okoli):
                randval = self.generate(self.tmp_bestarg)
                if self.algoritmus == 'FirstDeJong':
                    vnow = TFunctions.FirstDeJong(randval).compute()
                elif self.algoritmus == 'SecondDeJong':
                    vnow = TFunctions.SecondDeJong(randval).compute()
                elif self.algoritmus == 'Schwefel':
                    vnow = TFunctions.Schwefel(randval).compute()
                else:
                    print("Špatný algoritmus!!!")
                    vnow = 0

                if vnow < local_vhodnost:
                    local_vhodnost = vnow
                    local_best_arg = randval[:]

            self.tmp_vhodnost = local_vhodnost
            self.tmp_bestarg = local_best_arg[:]
            # if local_vhodnost < self.tmp_vhodnost:
            #     self.tmp_bestarg = local_best_arg[:]
            #     self.tmp_vhodnost = local_vhodnost
            #     nb_now = 0
            # else:
            #     nb_now += 1

            if self.tmp_vhodnost <= self.vhodnost:
                self.bestarg = self.tmp_bestarg[:]
                self.vhodnost = self.tmp_vhodnost
            self.return_values(self.bestarg, self.vhodnost, j, i)

    def return_values(self, val, vnow, neighbours, iters):
        if self.verbose:
            row = "%s; %s; %s; %s; %s; %s; %s" % (str(self.id_spusteni), str(neighbours), str(iters),
                                                  str(self.classname), str(self.algoritmus),
                                                  str(val), str(vnow))
        else:
            row = " %s; %s" % (str(val), str(vnow))
        if self.file != '':
            f = open(self.file, 'a')
            if self.print_all or self.vhodnost >= vnow:
                f.write("%s\n" % row)
            f.close()
        else:
            if self.print_all or self.vhodnost >= vnow:
                print("%s" % row)


