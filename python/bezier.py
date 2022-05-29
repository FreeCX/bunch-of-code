#!/usr/bin/env python3
from functools import reduce
import operator
import pygame


test_points = [[50, 50], [500, 1500], [500, -800], [750, 750]]
background_color = (100, 100, 100)
game_clock = 60
quit_flag = False
window_size = (800, 800)


def memoize(f):
    memory = {}

    def memoized(*args):
        if args not in memory:
            memory[args] = f(*args)
        return memory[args]

    return memoized


def get_basis(i, n, t):
    @memoize
    def f(n):
        return reduce(operator.mul, range(1, n), 1)

    return (f(n) / (f(i) * f(n - i))) * (t**i) * (1 - t) ** (n - i)


def get_curve(arr, step=0.01, need_to_round=False):
    res = []
    t = 0
    while t < 1 + step:
        if t > 1:
            t = 1
        new_value_x = 0
        new_value_y = 0
        for index, (ax, by) in enumerate(arr):
            b = get_basis(index, len(arr) - 1, t)
            new_value_x += ax * b
            new_value_y += by * b
        if need_to_round:
            new_value_x = round(new_value_x)
            new_value_y = round(new_value_y)
        res.append([new_value_x, new_value_y])
        t += step
    return res


if __name__ == "__main__":
    curve = get_curve(test_points, need_to_round=True)
    b_pos = 0
    m_pos = len(curve) - 1
    direction = -1

    pygame.init()

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Bezier")
    clock = pygame.time.Clock()

    surface = pygame.Surface(window_size)

    while not quit_flag:
        surface.fill(background_color)

        pygame.draw.lines(surface, (255, 255, 255), False, curve)

        xp, yp = curve[b_pos]
        pygame.draw.circle(surface, (255, 0, 0), (xp, yp), 10)

        screen.blit(surface, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_flag = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    quit_flag = True

        if b_pos == m_pos or b_pos == 0:
            direction = -direction
        b_pos += direction

        clock.tick(game_clock)
