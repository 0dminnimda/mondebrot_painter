import numpy as np
from mandelbrot_painter.set_generator import create_grid, compute_set


def arrprint(arr):
    for item in arr:
        print(*item)
    print()


arrprint(compute_set(create_grid(-1+6j, 1, 2, dencity=3, magnification=1.5)))
arrprint(compute_set(create_grid(-0.5+0j, 3, 2, dencity=30), 9))

breakpoint
