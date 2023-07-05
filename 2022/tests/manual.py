from time import perf_counter

import cv2 as cv
from colour import Color
from mandelbrot_painter.painter import make_palette, paint_the_set
from mandelbrot_painter.set_generator import compute_set, create_grid


def timer(f):
    def wrapper(*args, **kwargs):
        print("Starting", f.__name__)
        start = perf_counter()
        r = f(*args, **kwargs)
        print("Finishing", f.__name__, "time:", perf_counter() - start)
        return r
    return wrapper


create_grid = timer(create_grid)
compute_set = timer(compute_set)
make_palette = timer(make_palette)
paint_the_set = timer(paint_the_set)
imwrite = timer(cv.imwrite)

max_iter = 80

# grid = create_grid(
#     -0.75+0j,
#     width=13, height=10,
#     dencity=250, magnification=0.2)
grid = create_grid(
    -0.170337168373994-1.065060284305098j,
    width=13, height=10,
    dencity=100, magnification=1/50000)

palette = make_palette(max_iter, Color("black"), Color("red"), Color("white"))
image = paint_the_set(compute_set(grid, max_iter), palette)

name = "lightnings"
imwrite(f"images/{name}.png", image)
