import numpy as np
from cython.parallel import prange
from numpy.typing import NDArray

cimport cython

ctypedef complex complex_t


cpdef create_grid(complex_t point, int width, int height,
                  int dencity=1, double magnification=1.):
    xv, yv = np.meshgrid(
        np.linspace(-width*magnification/2, width*magnification/2, width*dencity),
        np.linspace(-height*magnification/2, height*magnification/2, height*dencity))
    return xv + yv * 1j + point


cdef inline complex_t function(complex_t z, complex_t c) nogil:
    return z*z + c


cdef inline bint out_of_bounds(complex_t x) nogil:
    return x.real*x.real + x.imag*x.imag > 4


cdef int number_of_iterations_for_the_point(complex_t z, complex_t c, int max_iter) nogil:
    cdef Py_ssize_t i

    for i in range(max_iter + 1):
        if out_of_bounds(z):
            return i
        z = function(z, c)

    return 0


@cython.boundscheck(False)
@cython.wraparound(False)
cdef int [:] compute_values(const complex_t [:] c, int max_iter):
    # cdef complex_t [:] z = np.zeros_like(c)
    cdef int [:] set = np.zeros((c.shape[0],), dtype=np.int32)

    cdef Py_ssize_t x

    for x in prange(set.shape[0], nogil=True):
        set[x] = number_of_iterations_for_the_point(0, c[x], max_iter)

    return set


@cython.boundscheck(False)
@cython.wraparound(False)
cdef int [:, :] compute_set_corrupted_xy(const complex_t [:, :] c, int max_iter):
    cdef complex_t [:, :] z = np.zeros_like(c)
    cdef int [:, :] set = np.zeros((c.shape[0], c.shape[1]), dtype=np.int32)

    cdef Py_ssize_t x, y, i
    cdef complex_t res

    for i in prange(1, max_iter + 1, nogil=True):
        for x in range(set.shape[0]):
            for y in range(set.shape[1]):
                if set[x, y] == 0:
                    res = z[x, y] = function(z[x, y], c[x, y])
                    if out_of_bounds(res):
                        set[x, y] = i

    return set


@cython.boundscheck(False)
@cython.wraparound(False)
cdef int [:] compute_set_corrupted_x(const complex_t [:] c, int max_iter):
    cdef complex_t [:] z = np.zeros_like(c)
    cdef int [:] set = np.zeros((c.shape[0],), dtype=np.int32)

    cdef Py_ssize_t x, i
    cdef complex_t res

    for i in prange(1, max_iter + 1, nogil=True):
        for x in range(set.shape[0]):
            if set[x] == 0:
                res = z[x] = function(z[x], c[x])
                if out_of_bounds(res):
                    set[x] = i

    return set


def compute_set(c: NDArray, max_iter: int = 100, algorithm: str = "normal") -> NDArray:
    if algorithm == "normal":
        return np.asarray(compute_values(c.ravel(), max_iter)).reshape(c.shape)
    elif algorithm == "corrupted_xy":
        return np.asarray(compute_set_corrupted_xy(c, max_iter))
    elif algorithm == "corrupted_x":
        return np.asarray(compute_set_corrupted_x(c, max_iter))
    else:
        raise ValueError(f"Unknown algorithm: '{algorithm}'")
