import math


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
