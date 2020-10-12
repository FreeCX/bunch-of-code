from tempfile import TemporaryDirectory
from pathlib import Path
from sys import stdout
from os import system
import argparse

from PIL import Image


def save_image(dir, img, index):
    tiff = Path(dir.name) / f'{index:04d}.tiff'
    djvu = Path(dir.name) / f'{index:04d}.djvu'
    img.save(str(tiff))
    system(f'cjb2 -clean {tiff} {djvu}')
    tiff.unlink(missing_ok=True)
    return index + 1


def split(img):
    i = Image.open(img)
    w, h = i.size
    if w > h:
        return [i.crop((0, 0, w // 2, h)), i.crop((w // 2, 0, w, h))]
    else:
        return [i]


def extract(filename):
    extracted = TemporaryDirectory()
    print('>> extract pages ...', end='')
    stdout.flush()
    system(f'ddjvu -eachpage -format=tiff {filename} {extracted.name}/%04d.tiff')
    print('\r>> extract pages ... [done]')
    return extracted


def process(dir):
    rendered = TemporaryDirectory()
    items = sorted(Path(dir.name).iterdir())
    count = len(items)
    index = 1
    for v, item in enumerate(items):
        for img in split(item):
            index = save_image(rendered, img, index)
        percent = v * 100 // count
        print(f'\r>> process images ... {percent:03d}%', end='')
        stdout.flush()
    print('\r>> process images ... [done]')
    return rendered


def render(dir, output):
    files = ' '.join(map(str, sorted(Path(dir.name).iterdir())))
    print(f'>> render {output} ...', end='')
    stdout.flush()
    system(f'djvm -c {output} {files}')
    print(f'\r>> render {output} ... [done]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split djvu pages')
    parser.add_argument('-i', dest='input', metavar='input', type=Path, required=True, help='input file')
    parser.add_argument('-o', dest='output', metavar='output', type=Path, required=True, help='output file')

    args = parser.parse_args()
    if args.input and args.output:
        render(process(extract(args.input)), args.output)