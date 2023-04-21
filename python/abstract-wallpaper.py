import numpy as np
from PIL import Image

img_size = (2160, 3840)
X = 1.2
Y = 0.5
ax = -X * np.pi
bx = Y * np.pi
ay = -Y * np.pi
by = Y * np.pi
xshift = -np.pi * 0.5
yshift = np.pi * 0.5

np.random.seed(seed=1)

palette = np.zeros((256, 3), dtype=np.uint8)
palette[:, 0] = np.random.randint(0, 255, 256)
palette[:, 1] = 0.5 * (np.arange(0, 256, 1) + palette[:, 0])
palette[:, 2] = 256 - palette[:, 1]

p = np.zeros(img_size, dtype=np.uint8)
x = np.linspace(ax, bx, img_size[1])
y = np.linspace(ay, by, img_size[0])
xv, yv = np.meshgrid(x, y)

p[:] = np.round(0.25 * (np.sin(xv + xshift) + np.cos(yv + yshift) + 2) * 255)

img = Image.fromarray(p)
img.putpalette(palette)
img.save("output.png")
