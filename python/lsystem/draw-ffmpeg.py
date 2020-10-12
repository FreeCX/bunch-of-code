# https://habr.com/ru/company/piter/blog/496538/
from copy import deepcopy
from pathlib import Path
import subprocess as sp
import argparse
import json
import math

from PIL import Image, ImageDraw


class ffmpeg:
    def __init__(self, fps, output):
        self.cmd_out = [
            'ffmpeg', '-i', '-', '-f', 'image2pipe', '-r', str(fps), '-c:v', 'libx264', '-preset', 'slow',
            '-profile:v', 'high', '-crf', '18', '-coder', '1', '-pix_fmt', 'yuv420p', '-vf', 'scale=iw:-2', 
            '-movflags', '+faststart', '-g', '30', '-bf', '2', '-y', str(output),
        ]
        self.pipe = sp.Popen(self.cmd_out, stdin=sp.PIPE)

    def push(self, frame):
        frame.save(self.pipe.stdin, 'PNG')

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
    if width % 2 != 0:
        width += 1
    if height % 2 != 0:
        height += 1
    shift_x = abs(xmin)
    shift_y = abs(ymin)

    return (width + 2 * border, height + 2 * border, shift_x + border, shift_y + border)


def render(output, state, cmds, angle, rules):
    px, py, lx, ly = [0] * 4
    w, h, sx, sy = state

    img = Image.new('RGB', (w, h), 'white')
    drw = ImageDraw.Draw(img)
    render = ffmpeg(fps=24, output=output)

    for symbol in cmds:
        px, py, angle = execute(px, py, angle, symbol, rules)
        drw.line((lx + sx, ly + sy, px + sx, py + sy), fill=(0, 0, 0))
        lx, ly = px, py
        render.push(img)


def execute_model(filename, *, savename=None):
    with open(filename, 'r') as jsf:
        data = json.load(jsf)
        result = generate(data['axiom'], data['iterations'], data['generate_rules'])
        state = prerender(result, data['start_angle'], data['draw_rules'])
        render(savename, state, result, data['start_angle'], data['draw_rules'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Draw L System model')
    parser.add_argument('-m', metavar='model', type=str, default=None, help='input model file')
    args = parser.parse_args()
    if args.m:
        renamer = lambda model: str(model).rsplit('.', 1)[0] + '.mp4'
        model = Path(args.m)
        if model.is_dir():
            for file in model.iterdir():
                print(f'> processing {file}')
                execute_model(file, savename=renamer(file))
        else:
            print(f'> processing {model}')
            execute_model(model, savename=renamer(model))
    else:
        parser.print_help()
