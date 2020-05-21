#!/usr/bin/env python3.8

import time
import cv2 as cv
import numpy as np
from math import sqrt
import colorsys as cs
import multiprocessing as mp
from multiprocessing import Process


def myar_to_img(w, fcolor, scolor, mode):
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
            if j[0] is True:
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
    GRADIENT_START = (255, 255, 255)
    GRADIENT_END = (255, 255, 255)
    OTHER_COLOR = (255, 255, 255)

    #for i in range(1,11):
    #    drmon(2**i,2,1,1)
    factor = 0
    while 1:
        factor += 1  # quality factor
        start = time.time()
        qual = 2**factor  # quality
        processes_num = 3  # number of processes used in multiprocessing
        mode = 2  # when “1” calculates the whole image,
        # when “2” calculates the mirror half; only affects performance
        # h1,v1 = 50,50
        myar = funccol(qual, mode, processes_num)  # multiprocessing
        img = myar_to_img(myar, (255, 255, 255), (0, 0, 0), mode)
        end = time.time() - start
        print(f"{qual} - {end} sec")

        # cv.namedWindow ( "b" , cv.WINDOW_NORMAL)
        cv.imshow(f"mandelbrot_set_{qual}", img)
        cv.imwrite(f"mandelbrot_set_{qual}.png", img)
        cv.waitKey(0)
    cv.destroyAllWindows()
