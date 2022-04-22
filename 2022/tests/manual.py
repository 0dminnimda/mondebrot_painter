import numpy as np
from mandelbrot_painter.set_generator import create_set

print(np.asarray(create_set(-1+6j, 1, 2, dencity=3, magnification=1.5)))

breakpoint
