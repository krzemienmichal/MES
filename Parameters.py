import math


class Parameters:
    points = []
    wages = []
    npc = 0

    def __init__(self, npc):
        if npc == 2:
            self.npc = 2
            self.points = [-1.0/math.sqrt(3), 1/math.sqrt(3)]
            self.wages = [1, 1]
        if npc == 3:
            self.npc = 3
            self.points = [-math.sqrt(3/5), 0, math.sqrt(3/5)]
            self.wages = [5/9, 8/9, 5/9]


def calc1d(schema: Parameters):
    result = 0
    for n in range(schema.npc):
        result += schema.wages[n]*function1d(schema.points[n])
    return result


def calc2d(schema: Parameters):
    result = 0
    for i in range(schema.npc):
        for j in range(schema.npc):
            result += schema.wages[i] * schema.wages[j] * function2d(schema.points[i], schema.points[j])
    return result


def function1d(x):
    return 5*x*x + 3*x + 6


def function2d(x, y):
    return 5*x*x*y*y + 3*x*y + 6


if __name__ == "__main__":
    a = Parameters(2)
    b = Parameters(3)
    print(calc1d(a))
    print(calc1d(b))

    print()

    print(calc2d(a))
    print(calc2d(b))
