#!/usr/bin/env python3.8

import time
import numpy as np
from math import sqrt
import colorsys as cs
import multiprocessing as mp
from multiprocessing import Process


def belonging(real, imag, max_iter=100, formula="z**2 + c"):
    # Belonging to a set of mandelbrot

    z = 0
    c = complex(real, imag)

    for i in range(max_iter):
        #exec("z = "+formula) 
        z = z**2 + c
        if abs(z) >= 2:
            return False

    return True


def drmon(senter, quality, mode, processes_num, num, queue=0):
    # num -= 1
    # squeue = sqrt(quality)

    quality = 100*quality
    h1 = quality*-1.25
    v1 = quality*-2.1  # quality*185
    hr, vr = (250/mode)*quality+1, (265/processes_num)*quality
    v1 += vr*num

    #print(-h1+(h1+hr), -v1+(v1+vr), quality, mode, processes_num, num)
    h1, v1, quality, hr, vr = int(h1), int(v1), int(quality), int(hr), int(vr)
    #print(-h1+(h1+hr), -v1+(v1+vr), quality, mode, processes_num, num)

    ww = [[[None, i/quality, j/quality] for j in range(h1, h1+hr)] for i in range(v1, v1+vr)]
    for i in ww:
        for j in i:
            j[0] = belonging(j[1], j[2])
    if queue != 0:
        queue.put(ww)
    else:
        return ww


def turning(senter, length):
    diagonal_0 = np.array([length, length])
    #diagonal_1 = np.array([length, -length])

    vertices = [
        senter - diagonal_0,
        #senter - diagonal_1,
        #senter + diagonal_1,
        senter + diagonal_0,
    ]

    return vertices


def rectangle_division(x, y, total, num):
    #x0, y0, x1, y1 = *x, *y
    y1, x0, y0, x1 = *x, *y

    part = (y1-y0)/total

    #return x0, x1, y0, y1
    return x0, x1, y0+part*num, y0+part*(num+1)


def make_set(senter, length, quality, processes_num, num, mode, queue=None):

    vertices = turning(senter, length)

    x0, x1, y0, y1 = rectangle_division(*vertices, processes_num, num)

    with open("output.txt", "a") as file:
       file.write(f"{num}, {x0}, {x1}, {y0}, {y1} \n")
    print(num, x0, x1, y0, y1)

    

    # h1 = quality*-1.25
    # v1 = quality*-2.1  # quality*185
    # hr, vr = (250/mode)*quality+1, (265/processes_num)*quality
    # v1 += vr*num

    #print(-h1+(h1+hr), -v1+(v1+vr), quality, mode, processes_num, num)
    # h1, v1, quality, hr, vr = int(h1), int(v1), int(quality), int(hr), int(vr)
    #print(-h1+(h1+hr), -v1+(v1+vr), quality, mode, processes_num, num)

    x_qual = int(quality/processes_num)
    y_qual = quality

    set_ = [
        [(belonging(i, j), i, j) for j in np.linspace(y0, y1, y_qual)]
        for i in np.linspace(x0, x1, x_qual)
    ]
            
    if queue is not None:
        queue.put(set_)
    else:
        return set_


def mp_setup_and_run(senter, length, quality, processes_num, mode):
    if processes_num > quality:
        raise ValueError("the number of processes must be greater"\
            " than or equal to the quality number")
        # or "processes_num must be greater than or equal to the quality"

    range_ = range(processes_num)
    queue = {}
    processes = {}
    sub_result = {}
    result = []

    for i in range_:
        queue[i] = mp.Queue()
        processes[i] = Process(
            target=make_set,
            args=[senter, length, quality, processes_num, i, mode, queue[i]])
        processes[i].start()

    for i in range_:
        sub_result[i] = queue[i].get()
        result += sub_result[i]
        processes[i].join()

    return result


if __name__ == '__main__':
    start = time.time()

    with open("output.txt", "w") as file:
       file.write("")

    senter = np.array([0, 0.5])
    length = 1.5

    factor = 5#10  # quality factor
    quality = 2**factor  # number of pixels on each side of the set/image
    processes_num = 3  # number of processes used in multiprocessing
    mode = 1  # 1 - calculates the whole image; 2 only half, other half - mirror image

    # np.array(set_).shape

    tt = turning(senter, length)
    gg = [rectangle_division(*tt, 3, i) for i in range(3)]

    # multiprocessing
    set_ = mp_setup_and_run(senter, length, quality, processes_num, mode)
    np.save(f"mandelbrot_set_{quality}", [set_, mode, quality])

    end = time.time() - start
    print(f"{quality}: {end} sec")
