def belonging(real, imag, max_iter=100, compiled=None):
    # eval(compile("lambda z, c: z**2 + c", "<string>", "eval"))
    # Belonging to a set of mandelbrot

    z = 0
    c = complex(real, imag)

    for i in range(max_iter):
        #z = z**2 + c
        #z = eval(compiled)
        #z = compiled(z, c)
        #z = form(z, c)
        z = compiled

        if abs(z) >= 2:
            return i

    return True
