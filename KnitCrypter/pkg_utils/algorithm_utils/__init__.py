def default(a):
    return a


def equals(a, b):
    if a % b == 0:
        return a
    return a * -1


def notequals(a, b):
    if a % b != 0:
        return a
    return a * -1


def square(a):
    return a**2


def cube(a):
    return a**3


def powerof(a, b):
    return a**b
