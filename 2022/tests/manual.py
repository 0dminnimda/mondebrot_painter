from time import perf_counter

from colour import Color
from mandelbrot_painter.painter import make_palette, save_set_as_image
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
save_set_as_image = timer(save_set_as_image)

max_iter = 55

grid = create_grid(
    -0.75+0j,
    13, 10, dencity=100, magnification=0.2)
# grid = create_grid(
#     -0.170337168373994-1.065060284305098j,
#     13, 10, dencity=100, magnification=1/5000000000000)

set = compute_set(grid, max_iter)

palette = make_palette(max_iter, Color("black"), Color("white"))

name = "black_n_white"
save_set_as_image(set, palette, f"images/{name}.png")
