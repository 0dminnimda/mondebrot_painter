#!/usr/bin/env python3.8

import time
import cv2 as cv
import numpy as np
import colorsys as cs


def myar_to_img(w, scolor, fcolor, mode):
    hei = len(w)*1
    wid = len(w[0])*1
    ar1 = np.zeros((hei, wid, 3), np.uint8)
    ar1[:] = fcolor
    ar = np.zeros((hei*2, wid*2, 3), np.uint8)
    ii = -1
    for i in w:
        ii += 1
        jj = -1
        for j in i:
            jj += 1
            if j is True:
                ar1[ii][jj] = scolor
    ar2 = np.copy(ar1)
    for i in range(len(ar2)):
        ar2[i][::] = ar2[i][::-1]
    ar1 = ar1[0:len(ar1), 0:len(ar1[0])-1]
    ar = np.concatenate((ar1, ar2), axis=1)
    if mode == 1:
        return ar2
    elif mode == 2:
        return ar
    else:
        return "error"


def gradient(start_rgb, end_rgb, num):
    start_hsv = cs.rgb_to_hsv(*start_rgb)
    end_hsv = cs.rgb_to_hsv(*end_rgb)
    np.linspace()


if __name__ == '__main__':
    SET_COLOR = (0, 0, 0)
    GRADIENT_START = (255, 165, 0)
    GRADIENT_END = (0, 191, 255)
    OTHER_COLOR = (255, 255, 255)

    factor = 5.5
    quality = int(4**factor)

    data = np.load(f"mandelbrot_set_{quality}.npy", allow_pickle=True)

    set_, mode, quality, max_iter = data
    
    img = myar_to_img(set_, SET_COLOR, OTHER_COLOR, mode)

    while 1:
        # cv.namedWindow ( "b" , cv.WINDOW_NORMAL)
        cv.imshow(f"mandelbrot_set_{quality}", img)
        cv.imwrite(f"mandelbrot_set_{quality}.png", img)
        if cv.waitKey(0):# & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break