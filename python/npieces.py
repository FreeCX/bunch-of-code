import argparse
from pathlib import Path

from PIL import Image, UnidentifiedImageError

oversize_k = 1.5


def splitter(start, stop, count):
    for value in range(start, stop, count):
        if value + oversize_k * count < stop:
            yield value, value + count
        else:
            yield value, stop
            break


def split_image(image, count, side, shift):
    try:
        f = Image.open(image)
        print(f"[info]: split `{image}` into {count} images")
        fname = Path(image)
        size_part = f.size[side] // count
        for index, (start, stop) in enumerate(splitter(shift, f.size[side], size_part), 1):
            border = (0, start, f.size[0], stop) if side else (start, 0, stop, f.size[1])
            crop = f.crop(border)
            crop.save(fname.parent / str(fname.stem + f"_{index}" + fname.suffix))
    except UnidentifiedImageError:
        print(f"[error]: file `{image}` image not supported")


def iterate(image, count, side, *, level=0, shift=0):
    file = Path(image)
    if not file.exists():
        print(f"[ignore]: file `{image}` not found")
        return
    if file.is_dir():
        if level > 0:
            print(f"[info]: subfolder `{file}` is ignored")
            return
        print(f"[info]: iterate over `{image}` folder")
        for f in file.iterdir():
            iterate(f, count, side, level + 1, shift)
    else:
        split_image(image, count, side, shift)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split image into several")
    parser.add_argument(
        "-i", dest="inputs", metavar="image", type=str, nargs="+", required=True, help="input image file(s)"
    )
    parser.add_argument("-n", dest="count", metavar="count", type=int, required=True, help="split into N images")
    parser.add_argument("-w", dest="side", action="store_false", default=True, help="split by width (default: height)")
    parser.add_argument(
        "-s", dest="shift", metavar="shift", type=int, required=False, default=0, help="shift pixels count"
    )

    args = parser.parse_args()
    for image in args.inputs:
        iterate(image, args.count, args.side, shift=args.shift)
