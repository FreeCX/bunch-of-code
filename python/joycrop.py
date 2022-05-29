from pathlib import Path
from PIL import Image
import argparse


def crop_image(file):
    img = Image.open(file)
    width, height = img.size
    return img.crop((0, 0, width, height - 14))


def process(iterator, *, level=0, backup=False):
    for item in iterator:
        if not item.exists():
            print(f"[warn]: file {item} not exist")
            continue
        if item.is_dir():
            if level > 0:
                print("[warn]: subfolder `{item}` bypass disabled")
                return
            process(item.iterdir(), level=level + 1, backup=backup)
        elif item.is_file():
            output = str(item)
            if backup:
                output = "crop_" + output
                print(f"[process]: {item} -> {output}")
            else:
                print(f"[process]: {item}")
            img = crop_image(item)
            img.save(output)
        else:
            print(f"[warn]: type of {item} is not supported")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="joyreactor banner crop app")
    parser.add_argument("-i", dest="input", metavar="input", type=Path, nargs="+", required=True, help="input files")
    parser.add_argument("-b", dest="backup", action="store_true", default=False, help="save original file")

    args = parser.parse_args()
    process(args.input, backup=args.backup)
