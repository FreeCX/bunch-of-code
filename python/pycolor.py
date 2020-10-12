from PIL import Image, ImageDraw
from colorsys import hsv_to_rgb
from itertools import cycle
import numpy as np


def generate_colors(saturation=0.8, brightness=0.9, count=3):
    max_value = 1.0
    hue = np.arange(0, max_value, max_value / count)
    saturation = cycle([saturation])
    brightness = cycle([brightness])
    return zip(hue, saturation, brightness)


def to_rgb(color_list):
    colors = []
    for h, s, l in color_list:
        r, g, b = hsv_to_rgb(h, l, s)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    return colors


if __name__ == '__main__':
    max_colors = 64
    block_size = 16
    i_index_max = 8
    i_index, j_index = 0, 0
    
    colors = to_rgb(generate_colors(count=max_colors))
    img_size = (block_size * i_index_max, block_size * int(np.ceil(max_colors / i_index_max)))
    
    image = Image.new('RGB', img_size, 'white')
    draw = ImageDraw.Draw(image)

    for color in colors:
        points = [
            (block_size * i_index, block_size * j_index),
            (block_size * (i_index + 1), block_size * (j_index + 1))
        ]
        draw.rectangle(points, fill=color)
        if i_index + 1 >= i_index_max:
            j_index += 1
            i_index = 0
        else:
            i_index += 1
    image.save('test.png')
