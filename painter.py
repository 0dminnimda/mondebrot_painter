#!/usr/bin/env python3.8

import os
import time
import cv2 as cv
import numpy as np
from colour import Color


def create_img(set_, set_color, other_color, mode, gradient=None):
    if gradient is not None:
        max_iter = len(gradient)

    height, width = np.array(set_).shape[:2]
    img = np.full((height, width, 3), other_color, np.uint8)

    for h in range(height):
        for w in range(width):
            value = set_[h][w]

            if value is True:
                img[h, w] = set_color
            elif gradient is not None and isinstance(value, int):
                img[h, w] = gradient[(value + 1) % max_iter]

    if mode == 1:
        return img
    elif mode == 2:
        return np.concatenate((img, img[:, ::-1]), axis=1)
    else:
        raise ValueError("wrong mode")


def make_gradient(rgb_array, num, collision=None):
    colors = []

    max = len(rgb_array)
    nums = equalspace(num, max)

    for i in range(len(rgb_array)-1):
        start_rgb, end_rgb = rgb_array[i], rgb_array[i+1]

        if isinstance(start_rgb, Color):
            start_clr = start_rgb
        else:
            start_clr = Color(rgb=norm(start_rgb))

        if isinstance(end_rgb, Color):
            end_clr = end_rgb
        else:
            end_clr = Color(rgb=norm(end_rgb))


        if collision is None:
            add = [to_rgb(clr) for clr in start_clr.range_to(end_clr, nums[i])]
        else:
            if i == 0:
                add = [to_rgb(clr) for clr in start_clr.range_to(end_clr, nums[i])]
            else:
                add = [to_rgb(clr) for clr in end_clr.range_to(start_clr, nums[i]+1)][:-1][::-1]

        colors += add

    return colors


def equalspace(num, max):
    linnums = np.linspace(0, num, max, dtype=int)

    nums = []

    for i in range(len(linnums)-1):
        nums += [linnums[i+1]-linnums[i]]

    return nums


def norm(color):
    return np.array(color) / 255


def to_rgb(color):
    return np.array(color.rgb)*255


if __name__ == '__main__':
    imgs_path = "imgs"
    saves_path = "saves"

    SET_COLOR = (0, 0, 0) #to_rgb(Color("green"))#
    GRADIENT_COLORS = [
        #Color("black"),
        #Color("white"),
        Color("Orange"),
        Color("DeepSkyBlue"),
 ]
    OTHER_COLOR = (255, 255, 255) #(0, 0, 0)#

    divider = 1
    collision = None

    factor = 5.5
    quality = int(4**factor)

    data = np.load(f"{saves_path}\\mandelbrot_set_{quality}.npy", allow_pickle=True)
    set_, mode, quality, max_iter = data
    
    #max_iter = None
    #mode = 2

    if max_iter:
        clrs = ""
        for gr_color in GRADIENT_COLORS:
            clrs += Color(pick_for=gr_color).get_hex()+"_"
        clrs = clrs[:-1]
    else:
        clrs = Color(pick_for=OTHER_COLOR).get_hex()

    gradient = None
    if max_iter:
        gradient = make_gradient(GRADIENT_COLORS, max_iter/divider, collision)
    img = create_img(set_, SET_COLOR, OTHER_COLOR, mode, gradient=gradient)

    try:
        os.mkdir(imgs_path)
    except OSError: pass

    cv.imwrite(f"{imgs_path}\\mandelbrot_set_{quality}_{clrs}.png", img)

    while 1:
        # cv.namedWindow ( "b" , cv.WINDOW_NORMAL)
        cv.imshow(f"mandelbrot_set_{quality}_{clrs}", img)
        if cv.waitKey(0):# & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break