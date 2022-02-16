from hashlib import sha256 as hasher
from random import random


alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def as_text(value):
    result = ''
    for index in range(0, len(value), 2):
        block = int(value[index:index + 2], 16)
        symbol = chr(block)
        result += symbol if symbol in alphabet else '-'
    return result


if __name__ == '__main__':
    result = ''
    while 'cat' not in result:
        text = str(random())
        hashv = hasher(text.encode()).hexdigest()
        result = as_text(hashv)
    print(f"'{text}' -> {hashv} -> {result}")

