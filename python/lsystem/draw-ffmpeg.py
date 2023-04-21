# https://habr.com/ru/company/piter/blog/496538/
import argparse
import json
import math
import subprocess as sp
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw


class ffmpeg:
    def __init__(self, fps, output):
        # fmt: off
        self.cmd_out = [
            "ffmpeg", "-i", "-", "-f", "image2pipe", "-r", str(fps), "-c:v", "libx264", "-preset", "slow",
            "-profile:v", "high", "-crf", "18", "-coder", "1", "-pix_fmt", "yuv420p", "-vf", "scale=iw:-2",
            "-movflags", "+faststart", "-g", "30", "-bf", "2", "-y", str(output),
        ]
        # fmt: on
        self.pipe = sp.Popen(self.cmd_out, stdin=sp.PIPE)

    def push(self, frame):
        frame.save(self.pipe.stdin, "PNG")

    def __del__(self):
        self.pipe.stdin.close()
        self.pipe.wait()

        if self.pipe.returncode != 0:
            raise sp.CalledProcessError(self.pipe.returncode, self.cmd_out)


def generate(init, iterations, rules):
    for _ in range(iterations):
        res = []
        for var in init:
            res.append(rules[var] if rules.get(var) else var)
        init = "".join(res)
    return init


def execute(x, y, angle, symbol, rules, stack):
    draw = False

    if cmd := rules.get(symbol):
        var = None
        if ":" in cmd:
            cmd, var = cmd.split(":")
            cmd = cmd.lower()
            if var.isdigit():
                var = float(var)

        match cmd:
            case "forward":
                x += round(var * math.cos(math.radians(angle)))
                y += round(var * math.sin(math.radians(angle)))
                draw = True
            case "left":
                angle = (angle + var) % 360
            case "right":
                angle = (angle - var) % 360
            case "push":
                stack.append((x, y, angle))
            case "pop":
                x, y, angle = stack.pop()
            case other:
                print(f"unknown command: {other}")

    return x, y, angle, draw


def prerender(cmds, angle, rules, border=10):
    xmin, xmax, ymin, ymax, x, y = [0] * 6
    stack = []

    for symbol in cmds:
        x, y, angle, _ = execute(x, y, angle, symbol, rules, stack)
        xmin, xmax = min(x, xmin), max(x, xmax)
        ymin, ymax = min(y, ymin), max(y, ymax)

    width = abs(xmin) + abs(xmax)
    height = abs(ymin) + abs(ymax)
    if width % 2 != 0:
        width += 1
    if height % 2 != 0:
        height += 1
    shift_x = abs(xmin)
    shift_y = abs(ymin)

    return (width + 2 * border, height + 2 * border, shift_x + border, shift_y + border)


def render(output, state, cmds, angle, rules, steps, fps):
    px, py, lx, ly = [0] * 4
    w, h, sx, sy = state
    stack = []

    img = Image.new("RGB", (w, h), "white")
    drw = ImageDraw.Draw(img)
    render = ffmpeg(fps=fps, output=output)

    for symbol in cmds:
        px, py, angle, draw = execute(px, py, angle, symbol, rules, stack)

        if px == lx and py == ly:
            continue

        if draw:
            deltaX = (px - lx) / steps
            deltaY = (py - ly) / steps
            for i in range(steps + 1):
                pvx = lx + deltaX * i
                pvy = ly + deltaY * i
                if i == 0:
                    lvx, lvy = lx, ly
                else:
                    lvx = lx + deltaX * (i - 1)
                    lvy = ly + deltaY * (i - 1)
                drw.line((lvx + sx, lvy + sy, pvx + sx, pvy + sy), fill=(0, 0, 0))
                render.push(img)

        lx, ly = px, py


def execute_model(filename, *, savename=None, steps=4, fps=25):
    with open(filename, "r") as jsf:
        data = json.load(jsf)
        result = generate(data["axiom"], data["iterations"], data["generate_rules"])
        state = prerender(result, data["start_angle"], data["draw_rules"])
        render(savename, state, result, data["start_angle"], data["draw_rules"], steps, fps)


def main():
    parser = argparse.ArgumentParser(
        description="Draw L System model", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-m", dest="model", metavar="model", type=str, default=None, help="input model file")
    parser.add_argument("-s", dest="steps", metavar="steps", type=int, default=4, help="line steps drawing")
    parser.add_argument("-f", dest="fps", metavar="fps", type=int, default=25, help="fps")
    args = parser.parse_args()

    if not args.model:
        parser.print_help()
        return

    renamer = lambda model: str(model).rsplit(".", 1)[0] + ".mp4"
    model = Path(args.model)

    # process one file
    if model.is_file():
        print(f"> processing {model}")
        execute_model(model, savename=renamer(model), steps=args.steps, fps=args.fps)
        return

    # process folder
    for file in model.iterdir():
        if file.suffix != ".json":
            print(f"> ignore {file}")
            continue
        print(f"> processing {file}")
        execute_model(file, savename=renamer(file), steps=args.steps, fps=args.fps)


if __name__ == "__main__":
    main()
