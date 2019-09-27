import cv2 as cv
import time
import numpy as np
import multiprocessing as mp
from multiprocessing import Process


def st(z):
    r = z[0]**2-(z[1]**2)
    i = z[0]*z[1]*2
    return r, i


def f(z, c):
    s = st(z)
    r = s[0]+c[0]
    i = s[1]+c[1]
    return r, i


def mon(r, i, n=100):
    z = (0, 0)
    c = (r, i)
    try:
        for i in range(n):
            z = f(z, c)
    except OverflowError:
        p = False
    else:
        p = True
    return p


def drmon(an, devi1, devi2, par, qq=0):
    par -= 1
    # an*=2
    de = 100*an
    h1 = de*-1.25
    v1 = de*-2.1  # an*185
    hr, vr = (250/devi1)*an+1, (265/devi2)*an
    v1 += vr*par

    h1, v1, de, hr, vr = int(h1), int(v1), int(de), int(hr), int(vr)

    ww = [[[None, i/de, j/de] for j in range(h1, h1+hr)] for i in range(v1, v1+vr)]
    for i in ww:
        for j in i:
            j[0] = mon(j[1], j[2])
    if qq != 0:
        qq.put(ww)
    else:
        return ww


def funccol(an, dell, mode):
    ran = range(1, dell+1)
    qq, pr, w, wg = {}, {}, {}, []

    for i in ran:
        qq[i] = mp.Queue()
        pr[i] = Process(target=drmon, args=([an, mode, dell, i, qq[i]]))
        pr[i].start()

    for i in ran:
        w[i] = qq[i].get()
        wg += w[i]
        pr[i].join()

    return wg


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

if __name__ == '__main__':
    # factor = 0
    # while 1:
    factor = 1  # quality factor
    start_0 = time.time()
    qual = 2**factor  # quality
    processes_num = 8  # number of processes used in multiprocessing
    mode = 2  # when “1” calculates the whole image,
    # when “2” calculates the mirror half; only affects performance
    # h1,v1 = 50,50
    myar = funccol(qual, processes_num, mode)  # multiprocessing
    img = myar_to_img(myar, (255, 255, 255), (0, 0, 0), mode)
    end_0 = time.time() - start_0
    print(end_0, "sec")

    # cv.namedWindow ( "b" , cv.WINDOW_NORMAL)
    cv.imshow(f"mon_img_{qual}", img)
    cv.imwrite(f"mon_img_{qual}.png", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
