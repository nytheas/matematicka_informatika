import math
from ctypes import CDLL, POINTER, c_int, c_double, byref
import numpy

dll_lib = "./cec20_test_func.dll"

cec20 = CDLL(dll_lib)
cec20.cec20_test_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
cec20.cec20_test_func.restype = None


class FirstDeJong:
    def __init__(self, values):
        self.values = values

    def compute(self):
        x = 0
        for i in self.values:
            x += i ** 2
        return x


class SecondDeJong:
    def __init__(self, values):
        self.values = values

    def compute(self):
        x = 0
        for i in range(len(self.values) - 1):
            x += 100 * (self.values[i] ** 2 - self.values[i+1]) ** 2 + (1 - self.values[i]) ** 2
        return x


class Schwefel:
    def __init__(self, values):
        self.values = values

    def compute(self):
        x = 0
        for i in self.values:
            x += -1 * i * math.sin(math.sqrt(abs(i)))
        return x


class Rastrigin:
    def __init__(self, values):
        self.values = values

    # def compute(self):
    #     x = 0
    #     for i in self.values:
    #         x += (i**2 - 10*math.cos(2*math.pi*i))
    #     x = 10*len(self.values) * x
    #
    #     if x == 0:
    #         print(self.values)
    #     return x

    def compute(self):
        '''I had to improvise, because the "easy" version rounded 10 + 10^-18 to 10, so function hit 0
         when all values were around +- 10^-9  '''
        sum_1 = 0
        sum_2 = 0
        sum_3 = 10 * len(self.values)
        for i in self.values:
            sum_1 += i**2
            sum_2 -= 10*math.cos(2*math.pi*i)
        x = sum_3 + sum_2
        x += sum_1

        return x

class TestBed:
    def __init__(self, func, values):
        self.func = int(func.replace("TB_", ""))
        self.val = values
        self.values = numpy.array(values)

    def check_input(self):
        if self.func > 10:
            print("function not exist")
            return 0
        if (self.func == 6 or self.func == 7) and len(self.values) == 5:
            # print("combination not supported")
            return 0
        return 1

    def compute(self):
        x = c_double()
        if self.check_input() == 0:
            return 0
        cec20.cec20_test_func(self.values.ctypes.data_as(POINTER(c_double)), byref(x), len(self.values), 1, self.func)
        return x.value

