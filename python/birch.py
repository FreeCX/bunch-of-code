from pathlib import Path
from random import randint
import argparse
import sys

from PIL import Image, ImageDraw
import numpy as np

# extra params
USE_GRAY_CODE = False
USE_BW = False

# color params
BIRCH_LINE_COLOR = 130
BIRCH_BG_COLOR = 230
BG_COLOR = 'white'
MAIN_COLOR = 'black'

# image params
SIZE = 8
WIDTH = 3
MARGIN = (SIZE - WIDTH + 1) // 2
BORDER = 2
IMG_MARGIN = 5


def to_gray(block):
    result = []
    new_block = [0] + block[:-1]
    for a, b in zip(block, new_block):
        result.append(a ^ b)
    return result


def from_gray(b):
    g = [0] * 4
    while sum(b) != 0:
        g = [a ^ b for a, b in zip(g, b)]
        b = [0] + b[:-1]
    return g


def to_symbol(block):
    result = 0
    if USE_GRAY_CODE:
        block = from_gray(block[:4]) + from_gray(block[4:])
    for index, item in enumerate(block[::-1]):
        result += item * (2 ** index)
    return result.to_bytes(length=1, byteorder='little')


def bits(x):
    result = []
    while x > 0:
        result.append(x % 2)
        x //= 2
    padding = 8 - len(result)
    if USE_GRAY_CODE:
        return to_gray(result[:4]) + to_gray(result[4:])
    return [0] * padding + result[::-1]


def draw_one(drw, size, index_x, c):
    shift_x = index_x * size[0]
    if not USE_BW:
        drw.rectangle(xy=[(shift_x, 0), (shift_x + size[0], size[1])], fill=BIRCH_BG_COLOR)
    xpos = [(shift_x + 2, shift_x + 10), (shift_x + 10, shift_x + 18), (shift_x + 18, shift_x + 26)]

    for index_y, bit in enumerate(bits(c)):
        y = index_y * SIZE + MARGIN
        if not bit:
            p = xpos[(shift_x + index_y) % len(xpos)]
            drw.line(xy=[(p[0], y), (p[1], y)], fill=BIRCH_LINE_COLOR, width=WIDTH)

    drw.line(xy=[(shift_x, 0), (shift_x, size[1])], fill=MAIN_COLOR, width=BORDER)
    drw.line(xy=[(shift_x + size[0], 0), (shift_x + size[0], size[1])], fill=MAIN_COLOR, width=BORDER)


def birch_code_encode(text):
    size = 26, 64
    img_size = (size[0] * len(text) + BORDER, size[1])
    img = Image.new(mode='L', size=img_size, color=BG_COLOR)
    drw = ImageDraw.Draw(img)

    for index, symbol in enumerate(text):
        draw_one(drw, size, index, symbol)

    result = Image.new(mode='L', size=(img_size[0] + 2 * IMG_MARGIN, img_size[1] + 2 * IMG_MARGIN), color=BG_COLOR)
    drw = ImageDraw.Draw(result)
    drw.point(xy=[(2, 2), (2, 4), (4, 2)], fill=MAIN_COLOR)
    result.paste(img, box=(IMG_MARGIN, IMG_MARGIN))

    return result


def birch_code_decode(filename):
    step_x, step_y = 26, 8

    if USE_BW:
        img = np.array(Image.open(filename).convert('1'))
    else:
        img = np.array(Image.open(filename).convert('L'))
    h, w = img.shape

    if USE_BW:
        # convert to 0|1
        img = img.astype(np.uint8)
        # invert
        img = 1 - img
    else:
        # remove birch background
        img[img > 200] = 255
        # birch lines to black 
        img[img < 200] = 0
        # normalize
        img = 1 - img // 255
    # remove image margin
    img = img[5:h-5,5:w-5]

    # collect bits
    data = []
    for x_window in range(0, img.shape[1] - step_x, step_x):
        for y_window in range(0, img.shape[0], step_y):
            block = img[y_window:y_window + step_y,x_window + 2:x_window + step_x]
            data.append(int(not block.any()))

    # convert to symbols
    result = b''
    for index in range(0, len(data), step_y ):
        block = data[index:index + step_y]
        result += to_symbol(block)

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Birch Code')
    parser.add_argument('-e', dest='encode', metavar='encode', type=str, help='text to encode')
    parser.add_argument('-f', dest='file', metavar='file', type=Path, help='file to encode')
    parser.add_argument('-d', dest='decode', metavar='decode', type=str, help='input file')
    parser.add_argument('-o', dest='output', metavar='output', type=str, help='output file')

    args = parser.parse_args()
    if args.encode and args.output:
        birch_code_encode(args.encode.encode()).save(args.output)
    elif args.file and args.output:
        data = args.file.open('rb').read()
        birch_code_encode(data).save(args.output)
    elif args.decode:
        result = birch_code_decode(args.decode)
        sys.stdout.buffer.write(result)
    else:
        parser.print_help()
