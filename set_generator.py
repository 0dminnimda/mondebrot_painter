#!/usr/bin/env python3.8

import time
import numpy as np
from math import sqrt
import colorsys as cs
import multiprocessing as mp
from multiprocessing import Process


def belonging(real, imag, max_iter=100, compiled=None):
    # Belonging to a set of mandelbrot

    z = 0
    c = complex(real, imag)

    for i in range(max_iter):
        if compiled is not None:
            z = eval(compiled)
        else:
            z = z**2 + c
        if abs(z) >= 2:
            return i

    return True


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


def rectangle_division(pt0, pt1, total, num):
    x0, y0, x1, y1 = *pt0, *pt1

    part = (x1-x0)/total

    return x0 + part*num, x0 + part*(num+1), y0, y1


def make_set(senter, length, quality, processes_num, num, max_iter, formula, mode, queue=None):
    vertices = turning(senter, length)
    x0, x1, y0, y1 = rectangle_division(*vertices, processes_num, num)

    x_qual = round(quality/processes_num)
    y_qual = quality

    set_ = [
        [belonging(i, j, max_iter, formula) for j in np.linspace(y0, y1, quality)]
        for i in np.linspace(x0, x1, x_qual)
    ]
            
    if queue is not None:
        queue.put(set_)
    else:
        return set_


def mp_setup_and_run(senter, length, quality, processes_num, max_iter, formula, mode):
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
            args=[senter, length, quality, processes_num, i, max_iter, formula, mode, queue[i]])
        processes[i].start()

    for i in range_:
        sub_result[i] = queue[i].get()
        result += sub_result[i]
        processes[i].join()

    return result


if __name__ == '__main__':
    start = time.time()

    formula = None#"z**2 + c"
    compiled = compile(formula, '<string>', 'eval')
    max_iter = 100

    senter = np.array([-0.5, 0])
    length = 1.5


    at = belonging(-1.15, 0.30, max_iter, formula)


    factor = 5.5  # quality factor
    quality = int(4**factor)  # number of pixels on each side of the set/image
    processes_num = 4  # number of processes used in multiprocessing

    # mode is now useless
    mode = 1  # 1 - calculates the whole image; 2 only half, other half - mirror image

    # multiprocessing
    set_ = mp_setup_and_run(senter, length, quality, processes_num, max_iter, formula, mode)
    np.save(f"mandelbrot_set_{quality}", [set_, mode, quality, max_iter])

    end = time.time() - start
    print(f"{quality}: {end} sec")
