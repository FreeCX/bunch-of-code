#!/usr/bin/env python3
from math import ceil, floor
from sys import argv

def norm(a):
    if a * 10 - floor(a) * 10 >= 5:
        return ceil(a)
    else:
        return floor(a)

def resize(a, b, c, d):
    scale = c / a
    res = d - ((d / scale) - b) * scale
    return norm(res)

if __name__ == '__main__':
    if len(argv) != 3:
        print(f'{argv[0]} image_dest_size image_size')
        exit(0)

    width, height = map(int, argv[1].split('x'))
    iwidth, iheight = map(int, argv[2].split('x'))

    size = resize(width, height, iwidth, iheight)
    w, h = (resize(height, width, iheight, iwidth), iheight) if size > iheight else (iwidth, size)

    print(f'{w}x{h}')
