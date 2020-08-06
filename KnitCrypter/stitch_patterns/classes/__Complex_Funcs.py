class __summations_algorithm:

    __operations = {
        '-': lambda a, b: a - b,
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
        '**': lambda a, b: a ** b,
        '%': lambda a, b: a % b
    }

    def __init__(self, step: int, stop: int, mod: int, operator: str):
        self.__step = step
        self.__stop = step + stop
        self.__mod = mod
        self.__operator = operator

    def __call__(self):
        temp_value = 0
        for i in range(self.__step, self.__stop):
            temp_value += self.__operations[self.__operator](i, self.__mod)
        return temp_value


def Summations(step: int, stop: int, modifier: int, operator: str):
    """
    Return the sum of a range of integers, from step to end range, modified
    by an expression from the modifier and the given operator.
    """
    summation = __summations_algorithm(step, stop, modifier, operator)
    return summation()
