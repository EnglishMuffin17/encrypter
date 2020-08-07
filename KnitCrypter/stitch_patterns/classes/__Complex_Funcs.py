__operations = {
        '-': lambda a, b: a - b,
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
        '**': lambda a, b: a ** b,
        '%': lambda a, b: a % b,
        '>': lambda a, b: max(a, b),
        '<': lambda a, b: min(a, b),
        '~': lambda a, b: (sum([n for n in range(a, b)])) // abs(b - a)
    }

def _calculate(a: int, b: int, operator: str):
    try:
        return __operations[operator](a, b)
    except ZeroDivisionError:
        return 0


class __collatz_algorithm:

    def __init__(self, initial: int, operator: str):
        self.__initial = initial
        self.__op = operator

    def __call__(self):
        return self._calc(self.__initial)
    
    def _calc(self, value: int):
        if value <= 1:
            return value
        if value % 2 == 0:
            return _calculate(value, self._calc(value // 2), self.__op)
        return _calculate(value, self._calc((value * 3) + 1), self.__op)


class __summations_algorithm:

    def __init__(self, step: int, stop: int, mod: int, operator: str):
        self.__step = step
        self.__stop = step + stop
        self.__mod = mod
        self.__operator = operator

    def __call__(self):
        temp_value = 0
        for i in range(self.__step, self.__stop):
            temp_value += _calculate(i, self.__mod, self.__operator)
        return temp_value


def Summations(step: int, stop: int, modifier: int, operator: str):
    """
    Return the sum of a range of integers, from step to end range, modified
    by an expression from the modifier and the given operator.
    """
    summation = __summations_algorithm(step, stop, modifier, operator)
    return summation()


def Collatz(step: int, operator: str):
    """
    Return an operation of from the step, based on the Collatz conjecture.
    """
    collatz = __collatz_algorithm(step, operator)
    return collatz()
