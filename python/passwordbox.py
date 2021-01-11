#!/bin/env python
from pathlib import Path
import argparse
import secrets
import random
import string


def generate(args):
    """Функция генерации данных для 'коробки'.

    Входные параметры:
    args.alphabet   -- используемый алфавит
    args.length     -- длина файла в символах
    args.box        -- выходной файл
    """
    with args.box.open('w') as f:
        box = [secrets.choice(args.alphabet) for _ in range(args.length)]
        f.write(''.join(box))
        print(f'> Box `{args.box.name}` created')


def read(args):
    """Функция чтения пароля из 'коробки'.

    Входные параметры:
    args.box    -- входной файл
    args.seed   -- зерно для фунции random.seed
    args.length -- длина пароля
    """
    alphabet = args.box.open().read()
    random.seed(args.seed)
    print(''.join(random.choices(alphabet, k=args.length)))


def insert(args):
    """Функия добавления пароля в 'коробку'.

    Входные параметры:
    args.box        -- входной файл
    args.seed       -- зерно для фунции random.seed
    args.password   -- пароль для записи
    args.reseed     -- автоматическая генерация нового seed
    args.max_seed   -- максимальное число для генерации seed
    """
    def rewrite_box(file, box, key, positions):
        for key, index in zip(key, positions):
            box[index] = key
        with file.open('w') as f:
            f.write(''.join(box))
            print(f'> Box `{args.box.name}` updated')

    def pos(seed, box_size, key_size):
        random.seed(seed)
        box_iter = range(box_size)
        key_iter = range(key_size)
        return [random.choices(box_iter)[0] for _ in key_iter]

    def unique(data):
        return len(data) == len(set(data))

    box = list(args.box.open().read())
    if len(box) == 0:
        print('> Box is empty')
        return

    positions = pos(args.seed, len(box), len(args.password))

    if unique(positions):
        rewrite_box(args.box, box, args.password, positions)
    elif args.reseed:
        nseed_counter = 0
        while not unique(positions):
            new_seed = secrets.randbelow(args.max_seed)
            positions = pos(new_seed, len(box), len(args.password))
            nseed_counter += 1
            if nseed_counter > args.max_seed:
                print('> The number of attempts to generate new seed has been exceeded, please select a higher value max_seed')
                return
        print('> New seed: {new_seed}')
        rewrite_box(args.box, box, args.password, positions)
    else:
        print('> An intersection has occurred, please choose new seed value or use -r')


def analyze(args):
    """Функция построения графика энтропии файла.

    Входные параметры:
    args.box    -- входной файл для анализа
    args.save   -- выходное файл для сохранения графика
    """
    from collections import Counter
    import matplotlib.pyplot as plt

    data = args.box.open().read()
    box = dict(Counter(data))
    xs = list(range(256))
    total = len(data)
    ys = [box.get(chr(i), 0) / total for i in xs]

    plt.bar(xs, ys)
    plt.title('File entropy')
    plt.xlabel('Alphabet, [0, 255]')
    plt.ylabel('Percent count, %')
    plt.grid(alpha=0.5)
    if args.save:
        plt.savefig(args.save, bbox_inches='tight', pad_inches=0.1, dpi=300)
        print(f'> Plot `{args.save}` saved')
    else:
        plt.show()


if __name__ == '__main__':
    alphabet = string.ascii_letters + string.digits + string.punctuation

    parser = argparse.ArgumentParser(description='get your password from the box')
    subparser = parser.add_subparsers()

    p_read = subparser.add_parser('read', help='read password from the box', aliases=['r'])
    p_read.add_argument('-b', dest='box', type=Path, required=True, help='input box file')
    p_read.add_argument('-s', dest='seed', metavar='seed', type=int, required=True, help='initial seed value')
    p_read.add_argument('-l', dest='length', metavar='length', type=int, default=16, help='password length')
    p_read.set_defaults(func=read)

    p_create = subparser.add_parser('generate', help='generate password box', aliases=['g', 'gen'])
    p_create.add_argument('-b', dest='box', metavar='box', type=Path, required=True, help='input box file')
    p_create.add_argument('-l', dest='length', metavar='length', type=int, required=True, help='box length')
    p_create.add_argument('-a', dest='alphabet', metavar='alphabet', type=str, default=alphabet,
                          help='using alphabet')
    p_create.set_defaults(func=generate)

    p_insert = subparser.add_parser('insert', help='insert password to the box', aliases=['i', 'in'])
    p_insert.add_argument('-b', dest='box', metavar='box', type=Path, required=True, help='input box file')
    p_insert.add_argument('-s', dest='seed', metavar='seed', type=int, required=True, help='seed value')
    p_insert.add_argument('-p', dest='password', metavar='password', type=str, required=True, help='password to insert')
    p_insert.add_argument('-r', dest='reseed', metavar='reseed', type=bool, default=False, help='autogenerate new seed')
    p_insert.add_argument('-m', dest='max_seed', metavar='max_seed', type=int, default=1024, help='max seed value in reseed')
    p_insert.set_defaults(func=insert)

    p_analyze = subparser.add_parser('analyze', help='analyze file entropy', aliases=['a'])
    p_analyze.add_argument('-b', dest='box', metavar='box', type=Path, required=True, help='input box file')
    p_analyze.add_argument('-s', dest='save', metavar='save', type=Path, default=None, help='output plot file')
    p_analyze.set_defaults(func=analyze)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except FileNotFoundError:
            print(f'> File `{args.box}` not found')
    else:
        parser.print_help()