# 2025

This time I will try implementing real-time mondelbrot set explorer.
raylib is the graphics library of choise.
Later on I may try to also give this application an ability to explore infinitely - use arbitrary precision numbers, otherwise you hit a limit of resolution after some amount of zoom.

## Dependancies

You need to have [**raylib**](https://www.raylib.com/index.html) installed, so your compiler can pick it up in the process of building.
You can install it via package manager, get precompiled binaries or compile it from scratch.

## Build

First you need to initialize the builder, this needs to be done only once

```shell
clang nob.c -o nob.exe
```

Then run it (any changes to nob.c will be automatically picked up)

```shell
./nob.exe
```

Now you have `mondex.exe` you can run!

## Use

- `Scroll Down` / `Down Arrow` / `J` - Zoom In
- `Scroll Up`   / `Up Arrow`   / `K` - Zoom Out
- `Mouse` - moves the set around
