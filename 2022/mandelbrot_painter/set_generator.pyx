import numpy as np
cimport cython

ctypedef complex complex_t
ctypedef complex_t [:, :] complex_mem

cdef complex_t function(complex_t z, complex_t c):
    return z**2 + c

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef complex_mem mem_function(complex_mem z, complex_mem c):
    cdef Py_ssize_t x_max = z.shape[0]
    cdef Py_ssize_t y_max = z.shape[1]
    cdef Py_ssize_t x, y

    for x in range(x_max):
        for y in range(y_max):
            z[x, y] = function(z[x, y], c[x, y])

    return z

cdef complex_mem compute_set(complex_mem arr):
    cdef complex_mem z = np.zeros_like(arr)
    return mem_function(z, arr)

cpdef complex_mem create_set(complex_t point, int width, int height, int dencity=1, double magnification=1.):
    xv, yv = np.meshgrid(
        np.linspace(-width*magnification/2, width*magnification/2, width*dencity),
        np.linspace(-height*magnification/2, height*magnification/2, height*dencity))
    return compute_set(xv + yv * 1j + point)
