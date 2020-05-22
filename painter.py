#!/usr/bin/env python3.8

import time
import cv2 as cv
import numpy as np
from colour import Color


def myar_to_img(w, scolor, fcolor, mode, gradient=None):
    height = len(w)*1
    width = len(w[0])*1
    ar1 = np.zeros((height, width, 3), np.uint8)

    ar1[:] = fcolor
    ar = np.zeros((height*2, width*2, 3), np.uint8)
    ii = -1
    for i in w:
        ii += 1
        jj = -1
        for j in i:
            jj += 1
            if j is True:
                ar1[ii][jj] = scolor
            elif gradient is not None and isinstance(j, int):
                ar1[ii][jj] = gradient[j]
                
    ar2 = np.copy(ar1)
    for i in range(len(ar2)):
        ar2[i][::] = ar2[i][::-1]
    

    if mode == 1:
        return ar2

    elif mode == 2:
        ar1 = ar1[0:len(ar1), 0:len(ar1[0])-1]
        ar = np.concatenate((ar1, ar2), axis=1)

        return ar
    else:
        raise ValueError("wrong mode")


def make_gradient(start_rgb, end_rgb, num):
    if isinstance(start_rgb, Color):
        start_clr = start_rgb
    else:
        start_clr = Color(rgb=norm(start_rgb))

    if isinstance(end_rgb, Color):
        end_clr = end_rgb
    else:
        end_clr = Color(rgb=norm(end_rgb))

    colors = [to_rgb(clr) for clr in start_clr.range_to(end_clr, num)]
    return colors


def norm(color):
    return np.array(color) / 255


def to_rgb(color):
    return np.array(color.rgb)*255


if __name__ == '__main__':
    SET_COLOR = (0, 0, 0)
    GRADIENT_START = Color("blue")#(255, 165, 0)
    GRADIENT_END = Color("white")#(0, 191, 255)
    OTHER_COLOR = (255, 255, 255)


    factor = 5.5
    quality = int(4**factor)

    data = np.load(f"mandelbrot_set_{quality}.npy", allow_pickle=True)
    set_, mode, quality, max_iter = data
    
    gradient = make_gradient(GRADIENT_START, GRADIENT_END, max_iter)
    img = myar_to_img(set_, SET_COLOR, OTHER_COLOR, mode, gradient=gradient)

    while 1:
        # cv.namedWindow ( "b" , cv.WINDOW_NORMAL)
        cv.imshow(f"mandelbrot_set_{quality}", img)
        cv.imwrite(f"mandelbrot_set_{quality}.png", img)
        if cv.waitKey(0):# & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break