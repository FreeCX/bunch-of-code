from itertools import cycle
from pathlib import Path
import argparse

from PIL import Image
import numpy as np


def seed_from_key(key, max_seed=4096):
    result = 0x42
    for i, k in enumerate(key):
        result ^= ord(k)
        result *= i
        result %= max_seed
    return result


def censor_it(input, mask, key, output=None):
    filename = Path(input).stem

    data = np.array(Image.open(input))
    mask = np.array(Image.open(mask))

    np.random.seed(seed_from_key(key))
    pk = map(ord, cycle(key))

    lin_mask = mask.reshape(-1)
    items = np.where(lin_mask != 0)[0]
    g = np.random.randint(0, 255, items.shape[0] + 5)

    for index, xy in enumerate(items):
        x = xy % data.shape[1]
        y = xy // data.shape[1]

        p1, p2 = pk.__next__(), pk.__next__()

        if index % 3 == 0:
            data[y, x][0] ^= g[index + 0] ^ p1
            data[y, x][1] ^= g[index + 1] ^ p2
        elif index % 3 == 1:
            data[y, x][1] ^= g[index + 0] ^ p1
            data[y, x][2] ^= g[index + 1] ^ p2
        elif index % 3 == 2:
            data[y, x][0] ^= g[index + 0] ^ p1
            data[y, x][2] ^= g[index + 1] ^ p2
        data[y, x][0] = 255 - data[y, x][0] ^ g[index + 2]
        data[y, x][1] = 255 - data[y, x][1] ^ g[index + 3]
        data[y, x][2] = 255 - data[y, x][2] ^ g[index + 4]

    if output is None:
        output = filename + "_censored.png"

    Image.fromarray(data).save(output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="reversable image censor")
    parser.add_argument("-i", dest="input", metavar="image", type=Path, required=True, help="input image")
    parser.add_argument("-m", dest="mask", metavar="mask", type=Path, required=True, help="mask image")
    parser.add_argument("-c", dest="code", metavar="code", type=str, help="cipher key")
    parser.add_argument("-o", dest="output", metavar="output", type=Path, help="output image")
    parser.set_defaults(output=None)

    args = parser.parse_args()

    # censor_it('img.png', 'img_mask.png', 'deadbeef')
    censor_it(args.input, args.mask, args.code, args.output)
