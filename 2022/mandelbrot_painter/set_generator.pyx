import numpy as np
cimport cython
from cython.parallel import prange

ctypedef complex complex_t
ctypedef complex_t [:, :] complex_mem
ctypedef int [:, :] mandelbrot_set


cpdef complex_mem create_grid(complex_t point, int width, int height,
                              int dencity=1, double magnification=1.):
    xv, yv = np.meshgrid(
        np.linspace(-width*magnification/2, width*magnification/2, width*dencity),
        np.linspace(-height*magnification/2, height*magnification/2, height*dencity))
    return xv + yv * 1j + point


cdef inline complex_t function(complex_t z, complex_t c) nogil:
    return z**2 + c


@cython.boundscheck(False)
@cython.wraparound(False)
cdef mandelbrot_set compute_set_(complex_mem c, int max_iter):
    cdef complex_mem z = np.zeros_like(c)
    cdef mandelbrot_set set = np.zeros((c.shape[0], c.shape[1]), dtype=np.int32)

    cdef Py_ssize_t x, y, i
    cdef complex_t res

    for i in prange(1, max_iter + 1, nogil=True):
        for x in range(set.shape[0]):
            for y in range(set.shape[1]):
                if set[x, y] == 0:
                    res = z[x, y] = function(z[x, y], c[x, y])
                    if res.real**2 + res.imag**2 > 4:
                        set[x, y] = i

    return set


def compute_set(c, max_iter=100):
    return np.asarray(compute_set_(c, max_iter))
