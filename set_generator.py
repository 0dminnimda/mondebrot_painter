#!/usr/bin/env python3.8

import os
import time
import numpy as np
#from decimal import *
import multiprocessing as mp
from multiprocessing import Process


def belonging(c, max_iter=100, z=0):
    # Belonging to a set of mandelbrot

    for i in range(max_iter):
        z = z**2 + c

        if abs(z) >= 2:
            return i

    return True


def turning(senter, length, total, num):
    diagonal = np.array([length, length])

    x0, y0 = senter - diagonal
    x1, y1 = senter + diagonal

    part = (x1-x0)/total

    return x0 + part*num, x0 + part*(num+1), y0, y1


def make_set(senter, length, quality, processes_num, num, max_iter, queue=None):
    x0, x1, y0, y1 = turning(np.array(senter), length, processes_num, num)

    x_qual = round(quality/processes_num)

    set_ = [
        [
            belonging(complex(i, j), max_iter)
            for j in np.linspace(y0, y1, quality)
        ]
        for i in np.linspace(x0, x1, x_qual)
    ]
            
    if queue is not None:
        queue.put(set_)
    else:
        return set_


def mp_setup_and_run(senter, length, quality, processes_num, max_iter):
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
            args=[senter, length, quality, processes_num, i, max_iter, queue[i]],
            daemon=True)
        processes[i].start()

    for i in range_:
        sub_result[i] = queue[i].get()
        result += sub_result[i]
        processes[i].join()

    return result


if __name__ == '__main__':
    start = time.time()

    saves_path = "saves"

    max_iter = 100

    senter = [-0.5, 0]
    length = 1.5

    factor = 5.5  # quality factor
    quality = int(4**factor)  # number of pixels on each side of the set/image
    processes_num = 4  # number of processes used in multiprocessing

    # multiprocessing
    set_ = mp_setup_and_run(senter, length, quality, processes_num, max_iter)

    try:
        os.mkdir(saves_path)
    except OSError: pass
    
    np.save(f"{saves_path}\\mandelbrot_set_{quality}", [set_, quality, max_iter])

    end = time.time() - start
    print(f"{quality}: {end} sec")
