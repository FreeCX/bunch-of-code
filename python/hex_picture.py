#!/usr/bin/env python2
from PIL import Image, ImageFont, ImageDraw
import random as random_number

width = 1920
height = 1080
x_init = -10

img = Image.new('RGB', (width, height), (56, 56, 56))
draw = ImageDraw.Draw(img)

x = x_init
y = 0

text = ''
color = (0, 255, 0, 50)

while y < height:
    text = '0x%08x' % random_number.randint(0, 0xFFFFFFFF)
    draw.text((x, y), text, color)
    text = ''
    x += 70
    if x > width - x_init:
        x = x_init
        y += 12

img.save('test.png', 'PNG')
