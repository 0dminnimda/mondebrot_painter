from typing import Iterable, List, Optional, Tuple

import cv2 as cv
import numpy as np
from colour import Color
from numpy.typing import NDArray


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
    return list(color.get_rgb() for color in palette)


def save_set_as_image(set: NDArray, palette: PALETTE, path: str) -> None:
    mapped_array = [palette[value][::-1] for value in set.flatten()]
    mapped_set = np.array(mapped_array).reshape(set.shape + (3,))
    cv.imwrite(path, (mapped_set * 255).astype(np.uint8))
