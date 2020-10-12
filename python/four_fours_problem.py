#!/usr/bin/env python
from random import random, randint

"""
four fours problem
(4 + 4) - (4 + 4) = 0
(4 + 4) / (4 + 4) = 1
(4 / 4) + (4 / 4) = 2
 4 - 4 ^ (4 - 4)  = 3 
4 + ((4 - 4) * 4) = 4
...
"""

CHANCE_PERCENT = 50
INIT_POPULATION = 1000

search_list = list(map(lambda x: x * 1.0, range(100)))

# get last element from list
last = lambda lst: lst[len(lst)-1]

# iterate list by two elements
def iterByTwo(lst):
    for index in range(0, len(lst), 2):
        yield lst[index+0], lst[index+1]

"""
pack genome list for compute

[4, 4, 4, '+', '(', 4, '-', '4', ')']
transform to
[444, '+', '(', 4, '-', '4', ')']
"""
def pack(lst):
    number = 0
    result = []
    for item in lst:
        if type(item) is int:
            number *= 10
            number += item
        else:
            if number != 0:
                result.append(number)
                number = 0
            result.append(item)
    if type(last(lst)) is int:
        result.append(number)
    return result

"""
pack genome list for evalute

[444, '+', '(', 4, '-', '4', ')']
transform to
[4, 4, 4, '+', '(', 4, '-', '4', ')']
"""
def unpack(lst):
    result = []
    for item in lst:
        if type(item) is int:
            while item != 0:
                result.append(item % 10)
                item //= 10
        else:
            result.append(item)
    return result

"""
statement parser
"""
def infix2rpn(text):
    def get_priority(operator):
        if operator == '(':
            return -1
        elif operator == '*' or operator == '/':
            return 1
        elif operator == '+' or operator == '-':
            return 2
        elif operator == '^':
            return 0

    def can_pop(op1, stack):
        if len(stack) == 0:
            return False
        p1 = get_priority(op1)
        p2 = get_priority(last(stack))
        return p1 >= 0 and p2 >= 0 and p1 >= p2
    result = []
    func = []
    for item in text:
        if type(item) is int:
            result.append(item)
        else:
            if item == ')':
                while len(func) > 0 and last(func) != '(':
                    result.append(func.pop())
            else:
                while can_pop(item, func):
                    result.append(func.pop())
                func.append(item)
    while len(func) > 0:
        f = func.pop()
        if f not in ['(', ')']:
            result.append(f)
    return result

"""
RPN executor
"""
def rpn_exec(expression):
    def executor(op, a, b):
        try:
            if op == '+':
                return b + a
            elif op == '-':
                return b - a
            elif op == '*':
                return b * a
            elif op == '/':
                return b / a
            elif op == '^':
                return b ** a
        except:
            return None
    stack = []
    for item in expression:
        if type(item) is int:
            stack.append(item)
        else:
            try:
                op1 = float(stack.pop())
                op2 = float(stack.pop())
            except:
                return None
            stack.append(executor(item, op1, op2))
    return stack

"""
Genetic Algorithm
"""
def generate(count):
    symbols = ['+', '-', '*', '/', '^', '(', ')']
    populations = []
    for _ in range(count):
        current_population = []
        four_count = 4
        while four_count > 0:
            if random() * 100 >= CHANCE_PERCENT and four_count > 0:
                get_rnd_symbol = 4
                four_count -= 1
            else:
                get_rnd_symbol = symbols[randint(0, len(symbols)-1)]
            current_population.append(get_rnd_symbol)
        populations.append(current_population)
    return pack(populations)

def mutate(population):
    new_population = []
    for block in population:
        L = len(block)-1
        a = b = 0
        while a == b:
            a, b = randint(0, L), randint(0, L)
        block[a], block[b] = block[b], block[a]
        new_population.append(block)
    return new_population

def crossover(population):
    pass

def selection(population):
    pass

"""
Main code 
"""
def results(found_list):
    found_list.sort(key=lambda x: x[0])
    for res, item in found_list:
        res_str = ' '.join(map(lambda x: str(x), item))
        print('{} `{}` = {}'.format(infix2rpn(item), res_str, res[0]))

if __name__ == '__main__':
    population = generate(INIT_POPULATION)
    iteration = 0
    found_list = []
    for _ in range(10):
        print('iteration', iteration)
        for item in population:
            packed = pack(item)
            res = rpn_exec(infix2rpn(packed))
            if res is not None and len(res) == 1:
                if res[0] is not None and res[0] in search_list:
                    found_list.append([res, packed])
                    search_list.remove(res[0])
            if len(search_list) == 0:
                results(found_list)
                exit()
        population = crossover(population) if random() >= 50 else mutate(population)
        iteration += 1
    results(found_list)