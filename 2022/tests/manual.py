import numpy as np
from colour import Color
from mandelbrot_painter.set_generator import create_grid, compute_set
from mandelbrot_painter.painter import make_palette, save_set_as_image


def arrprint(arr):
    for item in arr:
        print(*item)
    print()


# arrprint(compute_set(create_grid(-1+6j, 1, 2, dencity=3, magnification=1.5)))
# arrprint(compute_set(create_grid(-0.5+0j, 3, 2, dencity=30), 9))

max_iter = 50

set = compute_set(create_grid(-0.75+0j, 3, 2, dencity=1000), max_iter)

palette = make_palette(max_iter + 1, Color("black"), Color("green"))
# print(palette, len(palette))

save_set_as_image(set, palette, "test_img.png")

breakpoint

