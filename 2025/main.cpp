#include <complex>
#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include "raylib.h"

using i64 = int64_t;
using u64 = uint64_t;
using u32 = uint32_t;
using u16 = uint16_t;
using u8 = uint8_t;
using Point = std::complex<long double>;

#define COOL_SCHEMA 0
#define SLOW_SCHEMA 1
constexpr int screen_size = 800;
constexpr u32 max_retries = 200;
constexpr u16 points_per_side = 400;


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
    return (float)how_many_steps_to_diverge(point, max_retries) / max_retries;
}

Color gradient_to_color(float scale) {
#if COOL_SCHEMA
    if (scale == 1.0) {  // only precicely max_retries
        return Color{0, 0, 0, 255};
    }
    scale = 1/scale;
#elif SLOW_SCHEMA
    scale = 1 - (1-scale)*(1-scale);
#else
#endif
    return Color{0, (u8)(scale*255), 0, 255};
}

// TODO: support resizing window

int main() {
    float frame_width = 4;
    Point center(-1, 0);

    constexpr float spacing = (float)screen_size / points_per_side;

    InitWindow(screen_size, screen_size, "Mondelbrot Set Explorer");

    while (!WindowShouldClose()) {
        float wheel;

        if (IsKeyDown(KEY_UP) || IsKeyDown(KEY_K)) {
            wheel = GetFrameTime() * 64;
        } else if (IsKeyDown(KEY_DOWN) || IsKeyDown(KEY_J)) {
            wheel = -GetFrameTime() * 64;
        } else {
            wheel = GetMouseWheelMove();
        }

        if (wheel != 0) {
            frame_width = std::exp(std::log(frame_width) + wheel*0.1f);
        }


        if (IsMouseButtonDown(MOUSE_BUTTON_LEFT)) {
            Vector2 delta_pixels = GetMouseDelta();
            center -= Point(
                delta_pixels.x * frame_width / screen_size,
                delta_pixels.y * frame_width / screen_size
            );
        }

        BeginDrawing();
            ClearBackground(BLACK);

            for (size_t x = 0; x < points_per_side; x++) {
                for (size_t y = 0; y < points_per_side; y++) {
                    Point point(
                        ((float)x - (float)points_per_side / 2) * frame_width / points_per_side,
                        ((float)y - (float)points_per_side / 2) * frame_width / points_per_side
                    );
                    point += center;
                    float scale = get_mondelbrot_gradient(point, max_retries);
                    Color color = gradient_to_color(scale);
#if 0
                    DrawCircle(x * spacing, y * spacing, spacing / 2, color);
#else
                    DrawRectangle(x * spacing, y * spacing, spacing, spacing, color);
#endif
                }
            }

            char fps_buffer[16];
            sprintf(fps_buffer, "fps: %d", GetFPS());
            DrawText(fps_buffer, screen_size * 0.85, screen_size * 0.05, 20, RED);
        EndDrawing();
    }

    CloseWindow();

    return 0;
}
