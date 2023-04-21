from colorsys import hsv_to_rgb
from itertools import cycle

from PIL import Image, ImageDraw


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__rows = []
        self.__cols = []
        self.__grid = {}
        self.__margin = {}

    def add_row(self, unit):
        self.__rows.append(unit)

    def add_col(self, unit):
        self.__cols.append(unit)

    def set_rows(self, units):
        self.__rows = units

    def set_cols(self, units):
        self.__cols = units

    def set_margin(self, row, col, margin):
        # (left, right, top, bottom)
        self.__margin[(row, col)] = margin

    def set_margin_all(self, left, right, top, bottom):
        margin = (left, right, top, bottom)
        for row in range(0, self.rows()):
            for col in range(0, self.cols()):
                self.set_margin(row, col, margin)

    def rows(self):
        return len(self.__rows)

    def cols(self):
        return len(self.__cols)

    def calculate(self):
        coef_w = self.width / sum(self.__cols)
        coef_h = self.height / sum(self.__rows)
        curr_w = 0
        curr_h = 0

        for row in range(0, self.rows()):
            curr_w = 0
            unit_h = self.__rows[row]
            res_h = curr_h + unit_h * coef_h
            for col in range(0, self.cols()):
                unit_w = self.__cols[col]
                margin = self.__margin.get((row, col), (0, 0, 0, 0))
                res_w = curr_w + unit_w * coef_w
                self.__grid[(row, col)] = (curr_w + margin[0], curr_h + margin[2], res_w - margin[1], res_h - margin[3])
                curr_w = res_w
            curr_h = res_h

    def rect(self, row, col):
        # return (x1, y1, x2, y2)
        return self.__grid.get((row, col))


def arange(start, stop, step):
    curr = start
    while curr <= stop:
        yield curr
        curr += step


def generate_palette(*, saturation=1.0, brightness=0.6, count=3):
    hue = arange(0, 1.0, 1.0 / count)
    saturation = cycle([saturation])
    brightness = cycle([brightness])
    colors = []
    for h, s, l in zip(hue, saturation, brightness):
        r, g, b = hsv_to_rgb(h, l, s)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        colors.append((r, g, b))
    return colors


if __name__ == "__main__":
    width, height = 500, 200

    grid = Grid(width, height)
    grid.set_rows((1, 2, 3, 1))
    grid.set_cols((1, 2, 3, 2))
    grid.set_margin_all(2, 2, 2, 2)
    grid.calculate()

    colors = generate_palette(count=grid.rows() * grid.cols())
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    drw = ImageDraw.Draw(img)

    index = 0
    for row in range(0, grid.rows()):
        for col in range(0, grid.cols()):
            rect = grid.rect(row, col)
            drw.rectangle(rect, fill=colors[index])
            index += 1

    img.save("grid.png")
