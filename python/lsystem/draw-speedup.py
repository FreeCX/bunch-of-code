# https://habr.com/ru/company/piter/blog/496538/
from PIL import Image, ImageDraw
from copy import deepcopy
from pathlib import Path
import argparse
import json
import math


def generate(init, iterations, rules):
    for _ in range(iterations):
        res = []
        for var in init:
            res.append(rules[var] if rules.get(var) else var)
        init = ''.join(res)
    return init


def execute(x, y, angle, symbol, rules):
    if rules.get(symbol):
        if ':' in rules[symbol]:
            cmd, var = rules[symbol].split(':')
            cmd, var = cmd.lower(), float(var) if var.isdigit() else None
        else:
            cmd = rules.get(symbol)
            var = None

        if cmd == 'forward':
            x += round(var * math.cos(math.radians(angle)))
            y += round(var * math.sin(math.radians(angle)))
        elif cmd == 'left':
            angle = (angle + var) % 360
        elif cmd == 'right':
            angle = (angle - var) % 360

    return x, y, angle


def prerender(cmds, angle, rules, border=10):
    xmin, xmax, ymin, ymax, x, y = [0] * 6

    for symbol in cmds:
        x, y, angle = execute(x, y, angle, symbol, rules)
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

    img = Image.new('RGB', (w, h))
    drw = ImageDraw.Draw(img)

    for symbol in cmds:
        px, py, angle = execute(px, py, angle, symbol, rules)
        drw.line((lx + sx, ly + sy, px + sx, py + sy), fill=(255, 255, 255))
        lx, ly = px, py

    return img


def animation(state, cmds, angle, rules):
    px, py, lx, ly = [0] * 4
    w, h, sx, sy = state

    images = [Image.new('RGB', (w, h))]

    for symbol in cmds:
        px, py, angle = execute(px, py, angle, symbol, rules)
        img = deepcopy(images[-1])
        drw = ImageDraw.Draw(img)
        drw.line((lx + sx, ly + sy, px + sx, py + sy), fill=(255, 255, 255))
        images.append(img)
        lx, ly = px, py

    return images


def execute_model(filename, *, savename=None, animate=False):
    with open(filename, 'r') as jsf:
        data = json.load(jsf)
        result = generate(data['axiom'], data['iterations'], data['generate_rules'])
        state = prerender(result, data['start_angle'], data['draw_rules'])
        if animate:
            images = animation(state, result, data['start_angle'], data['draw_rules'])
            images[0].save(savename, save_all=True, append_images=images[1:], duration=10, loop=0)
        else:
            result = render(state, result, data['start_angle'], data['draw_rules'])
            result.save(savename)


if __name__ == '__main__':
    model_to_png = lambda model: str(model).rsplit('.', 1)[0] + '.png'
    model_to_gif = lambda model: str(model).rsplit('.', 1)[0] + '.gif'

    parser = argparse.ArgumentParser(description='Draw L System model')
    parser.add_argument('-m', metavar='model', type=str, default=None, help='input model file')
    parser.add_argument('-a', action='store_true', default=False, help='create animation')
    args = parser.parse_args()
    if args.m:
        renamer = model_to_gif if args.a else model_to_png
        model = Path(args.m)
        if model.is_dir():
            for file in model.iterdir():
                print(f'> processing {file}')
                execute_model(file, savename=renamer(file), animate=args.a)
        else:
            print(f'> processing {model}')
            execute_model(model, savename=renamer(model), animate=args.a)
    else:
        parser.print_help()
