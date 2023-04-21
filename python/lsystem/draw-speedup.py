# https://habr.com/ru/company/piter/blog/496538/
import argparse
import json
import math
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw


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
    shift_x = abs(xmin)
    shift_y = abs(ymin)

    return (width + 2 * border, height + 2 * border, shift_x + border, shift_y + border)


def render(state, cmds, angle, rules):
    px, py, lx, ly = [0] * 4
    w, h, sx, sy = state
    stack = []

    img = Image.new("RGB", (w, h))
    drw = ImageDraw.Draw(img)

    for symbol in cmds:
        px, py, angle, draw = execute(px, py, angle, symbol, rules, stack)
        if draw:
            drw.line((lx + sx, ly + sy, px + sx, py + sy), fill=(255, 255, 255))
        lx, ly = px, py

    return img


def animation(state, cmds, angle, rules):
    px, py, lx, ly = [0] * 4
    w, h, sx, sy = state
    stack = []

    images = [Image.new("RGB", (w, h))]

    for symbol in cmds:
        px, py, angle, draw = execute(px, py, angle, symbol, rules, stack)
        img = deepcopy(images[-1])
        drw = ImageDraw.Draw(img)
        if draw:
            drw.line((lx + sx, ly + sy, px + sx, py + sy), fill=(255, 255, 255))
        images.append(img)
        lx, ly = px, py

    return images


def execute_model(filename, *, savename=None, animate=False):
    with open(filename, "r") as jsf:
        data = json.load(jsf)
        result = generate(data["axiom"], data["iterations"], data["generate_rules"])
        state = prerender(result, data["start_angle"], data["draw_rules"])

        if animate:
            images = animation(state, result, data["start_angle"], data["draw_rules"])
            images[0].save(savename, save_all=True, append_images=images[1:], duration=10, loop=0)
            return

        result = render(state, result, data["start_angle"], data["draw_rules"])
        result.save(savename)


def main():
    model_to_png = lambda model: str(model).rsplit(".", 1)[0] + ".png"
    model_to_gif = lambda model: str(model).rsplit(".", 1)[0] + ".gif"

    parser = argparse.ArgumentParser(description="Draw L System model")
    parser.add_argument("-m", metavar="model", type=str, default=None, help="input model file")
    parser.add_argument("-a", action="store_true", default=False, help="create animation")
    args = parser.parse_args()

    if not args.m:
        parser.print_help()
        return

    renamer = model_to_gif if args.a else model_to_png
    model = Path(args.m)

    # process one file
    if model.is_file():
        print(f"> processing {model}")
        execute_model(model, savename=renamer(model), animate=args.a)
        return

    # process folder
    for file in model.iterdir():
        if file.suffix != ".json":
            print(f"> ignore {file}")
            continue
        print(f"> processing {file}")
        execute_model(file, savename=renamer(file), animate=args.a)


if __name__ == "__main__":
    main()
