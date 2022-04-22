from time import perf_counter

import numpy as np
from colour import Color
from mandelbrot_painter.painter import make_palette, save_set_as_image
from mandelbrot_painter.set_generator import compute_set, create_grid


def arrprint(arr):
    for item in arr:
        print(*item)
    print()


# arrprint(compute_set(create_grid(-1+6j, 1, 2, dencity=3, magnification=1.5)))
# arrprint(compute_set(create_grid(-0.5+0j, 3, 2, dencity=30), 9))

max_iter = 50

start = perf_counter()
grid = create_grid(-0.75+0j, 3, 2, dencity=1000, magnification=1.25)

start_set = perf_counter()
set = compute_set(grid, max_iter)

start_palette = perf_counter()
palette = make_palette(max_iter + 3, Color("black"), Color("green"), Color("black"), Color("green"), Color("green"))
# print(palette, len(palette))

start_save = perf_counter()
save_set_as_image(set, palette, "test_img.png")

end = perf_counter()
print(f"Times: whole {end - start}, set {start_palette - start_set}, ",
      f"palette {start_save - start_palette}, save {end - start_save}")

breakpoint
