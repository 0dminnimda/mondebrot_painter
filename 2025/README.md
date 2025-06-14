# 2025

This time I will try implementing real-time mondelbrot set explorer.
raylib is the graphics library of choise.
Later on I may try to also give this application an ability to explore infinitely - use arbitrary precision numbers, otherwise you hit a limit of resolution after some amount of zoom.

## Dependancies

You need to have [**raylib**](https://www.raylib.com/index.html) v5 installed, so your compiler can pick it up in the process of building.
You can install it via package manager, get precompiled binaries or compile it from scratch.

## Build & Run

First you need to initialize the builder (this needs to be done only once, even if you change the code)

```shell
clang nob.c -o nob.exe
```

Then this command will compile and run the program

```shell
./nob.exe run
```

To see all possible commands run

```shell
./nob.exe help
```

## Use

- `Scroll Down` / `Down Arrow` / `j` - Zoom In
- `Scroll Up`   / `Up Arrow`   / `k` - Zoom Out
- `Left Mouse` - moves the set around
- `Right Mouse` - moves the julia set point around
- `v` - switch mode (mondelbrot set <-> julia set)
