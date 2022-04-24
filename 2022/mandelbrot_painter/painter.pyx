from typing import List, Optional, Tuple

import numpy as np
from colour import Color
from libc cimport stdint

cimport cython


PALETTE = List[Tuple[int, int, int]]


def make_palette(max_iter: int, *colors: Color,
                 set_color: Optional[Color] = None) -> PALETTE:

    assert set_color is None, "not implemented"

    palette = []
    indices = np.linspace(0, max_iter+1, len(colors), dtype=np.int32)

    for color1, color2, length in zip(colors, colors[1:], np.diff(indices)):
        palette.extend(color1.range_to(color2, length))
        palette.pop()

    palette.append(colors[-1])
    return np.array(list(color.get_rgb() for color in palette))


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef paint_the_set(const int [:, :] set, const double [:, :] palette):
    cdef stdint.uint8_t [:, :, :] mapped_set = np.zeros((set.shape[0], set.shape[1], 3), dtype=np.uint8)

    cdef Py_ssize_t i, j, k
    cdef const double [:] color

    for i in range(set.shape[0]):
        for j in range(set.shape[1]):
            color = palette[set[i, j]]
            for k in range(3)[::-1]:
                mapped_set[i, j, k] = <stdint.uint8_t>(color[k] * 255)

    return np.asarray(mapped_set)
