from itertools import combinations
from pathlib import Path
import argparse
import json

import imagehash as ih
from PIL import Image
import numpy as np


def process(args):
    hash_func_list = [ih.average_hash, ih.dhash, ih.phash, ih.whash]
    files = {}
    hashed = {}

    for file in Path(args.input).iterdir():
        print(f"\r" + "".ljust(120), end="")
        print(f"\r> process `{file.name}`", end="")
        try:
            img = Image.open(file)
            hash_values = [hash_func(img) for hash_func in hash_func_list]
            files[file.name] = hash_values
            # use last hv as main hash (whash)
            hv = hash_values[-1]
        except Exception as e:
            continue
        if hv in hashed:
            hashed[hv].append(file.name)
        else:
            hashed[hv] = [file.name]

    dublicates = list(filter(lambda x: len(x[1]) > 1, hashed.items()))
    if len(dublicates) > 0:
        for k, _ in dublicates:
            hashed.pop(k)

    similar = []
    for a, b in combinations(hashed.keys(), 2):
        distance = lambda a, b: (a - b) / len(a.hash) ** 2
        file1, file2 = hashed[a][0], hashed[b][0]
        distances = np.mean([distance(a, b) for a, b in zip(files[file1], files[file2])])
        if distances < args.diff:
            similar.append(
                {
                    "items": [file1, file2],
                    "similarity": 1.0 - distances,
                }
            )

    output = {"dublicates": [x[1] for x in dublicates], "similarity": similar}
    with args.output.open("w") as f:
        json.dump(output, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="find similar images", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-i", dest="input", metavar="input", type=Path, required=True, help="input folder")
    parser.add_argument("-d", dest="diff", metavar="diff", type=float, default=0.1, help="hash difference")
    parser.add_argument("-s", dest="size", metavar="size", type=int, default=8, help="hash size")
    parser.add_argument(
        "-o", dest="output", metavar="output", type=Path, default="report.json", help="output report file"
    )

    args = parser.parse_args()
    process(args)
