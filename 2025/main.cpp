#include <complex>
#include <stdio.h>
#include <stdint.h>
#include "raylib.h"

using i64 = int64_t;
using u64 = uint64_t;
using u32 = uint32_t;
using u16 = uint16_t;
using u8 = uint8_t;
using Point = std::complex<long double>;

u32 how_many_steps_to_diverge(Point point, u32 max_retries) {
    Point z = point;

    for (u32 step = 0; step < max_retries; step++) {
        if (std::norm(z) > 2*2) {
            // outside the cirle of radius 2 will always diverge
            return step;
        }
        z = z*z + point;
    }

    return max_retries;
}

float get_mondelbrot_gradient(Point point, u32 max_retries) {
    u32 steps = how_many_steps_to_diverge(point, max_retries);
    // + 1 since we need to include both 0 and max_retries
    return (float)steps / (max_retries + 1);
}

constexpr int screen_size = 800;
constexpr u32 max_retries = 100;
constexpr float frame_width = 4;

int main() {
    u16 side_length = 400;

    InitWindow(screen_size, screen_size, "Mondelbrot Set Explorer");

    const float spacing = (float)screen_size / side_length;

    while (!WindowShouldClose()) {
        BeginDrawing();
            ClearBackground(BLACK);

            for (size_t x = 0; x < side_length; x++) {
                for (size_t y = 0; y < side_length; y++) {
                    Point point(
                        ((float)x - side_length / 2) * frame_width / side_length,
                        ((float)y - side_length / 2) * frame_width / side_length
                    );
                    float scale = get_mondelbrot_gradient(point, max_retries);
                    Color color = {0, (u8)(scale*255), 0, 255};
#if 0
                    DrawCircle(x * spacing, y * spacing, spacing / 2, color);
#else
                    DrawRectangle(x * spacing, y * spacing, spacing, spacing, color);
#endif
                }
            }

            printf("frame done\n");
        EndDrawing();
    }

    CloseWindow();

    return 0;
}
