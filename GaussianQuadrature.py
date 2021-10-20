import math

class GaussianQuadrature:
    schema = [[[0, 1], [-1/math.sqrt(3), 1/math.sqrt(3)], [1,1]],
              [[0, 1, 2], [-math.sqrt(3/5), 0, math.sqrt(3/5)], [5/9, 8/9, 5/9]]]


def calc1d(schema: GaussianQuadrature):
    result = 0
    for n in schema[0]:
        result += schema[2][n]*function1d(schema[1][n])
    return result


def calc2d(schema: GaussianQuadrature):
    result = 0
    for i in schema[0]:
        for j in schema[0]:
            result += schema[2][i] * schema[2][j] * function2d(schema[1][i], schema[1][j])
    return result


def function1d(x):
    return 5*x*x + 3*x + 6


def function2d(x,y):
    return 5*x*x*y*y + 3*x*y + 6


if __name__ == "__main__":
    a = GaussianQuadrature
    print(calc1d(a.schema[0]))
    print(calc1d(a.schema[1]))

    print()
    print(calc2d(a.schema[0]))
    print(calc2d(a.schema[1]))