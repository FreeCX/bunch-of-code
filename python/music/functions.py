import numpy as np

LIST_FORMATS = (np.ndarray, list, tuple)


# signal generation funcs
def square(x):
    return np.clip(np.ceil(np.sin(x)), 0, 0.5)


def saw(x):
    c = x / np.pi - 0.5
    return 0.5 * (c - np.floor(0.5 + c)) + 0.25


def triangle(x):
    return np.abs(x % 6 - 3) / (2 * np.pi)


def noise(x):
    if type(x) is LIST_FORMATS:
        return np.array([np.random.rand() * 0.5 for _ in x])
    else:
        return np.random.rand() * 0.5


def exp_func_01(x):
    return saw(0.1 * x * np.sin(x))


def exp_func_02(x):
    return triangle(0.1 * x * np.sin(x))


# end of funcs
