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


def drmon(quality, mode, processes_num, num, queue=0):
    num -= 1
    # quality*=2
    squeue = sqrt(quality)
    de = 100*quality
    h1 = de*-1.25
    v1 = de*-2.1  # quality*185
    hr, vr = (250/mode)*quality+1, (265/processes_num)*quality
    v1 += vr*num

    #print(-h1+(h1+hr), -v1+(v1+vr), quality, mode, processes_num, num)
    h1, v1, de, hr, vr = int(h1), int(v1), int(de), int(hr), int(vr)
    #print(-h1+(h1+hr), -v1+(v1+vr), quality, mode, processes_num, num)

    ww = [[[None, i/de, j/de] for j in range(h1, h1+hr)] for i in range(v1, v1+vr)]
    for i in ww:
        for j in i:
            j[0] = belonging(j[1], j[2])
    if queue != 0:
        queue.put(ww)
    else:
        return ww


def mp_setup_and_run(quality, mode, processes_num):
    range_ = range(processes_num)
    queue = {}
    processes = {}
    w = {}
    wg = []

    for i in range_:
        queue[i] = mp.Queue()
        processes[i] = Process(target=drmon, args=([quality, mode, processes_num, i, queue[i]]))
        processes[i].start()

    for i in range_:
        w[i] = queue[i].get()
        wg += w[i]
        processes[i].join()

    return wg


if __name__ == '__main__':
    factor = 0

    #while 1:
    factor += 1  # quality factor
    start = time.time()

    quality = 2**factor
    processes_num = 3  # number of processes used in multiprocessing
    mode = 2  # when “1” calculates the whole image,
    # when “2” calculates the mirror half; only affects performance
    # h1,v1 = 50,50
    set_ = mp_setup_and_run(quality, mode, processes_num)  # multiprocessing
    np.save(f"mandelbrot_set_{quality}", set_)

    end = time.time() - start
    print(f"{quality} - {end} sec")
