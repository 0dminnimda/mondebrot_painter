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

#define DRAW_CENTERS 0

#define INVERSE_GRADIENT 1

#define SINEBOW_SCHEMA 0
#define RAINBOW_SCHEMA 1

#define SQUARE_BOUNDS 0

constexpr u16 screen_size = 800;
constexpr u16 status_bar_size = 25;
constexpr u32 max_retries = 200;
constexpr u16 points_per_side = 600;

constexpr float keyboard_zoom_multiplier = 32;
constexpr float scale_threthold = 1.5;
constexpr float image_scale = (float)screen_size / points_per_side;
constexpr long double circle_boundary = 4; // 2**2
constexpr long double square_boundary = 2.8284271247461903; // 8**0.5

struct State {
    bool showing_julia_set = false;
    Point julia_point = Point(0, 0);

    float scale = 1.0f;
    Vector2 center_pixel = Vector2{screen_size/2.0f, screen_size/2.0f};

    float frame_width = 2.5;
    Point center_point = Point(-0.75, 0);

    uint8_t image_data[3 * points_per_side * points_per_side];
};

State state = State();


u32 how_many_steps_to_diverge(Point point, u32 max_retries) {
    Point shift = state.showing_julia_set? state.julia_point : point;
    Point z = point;

    for (u32 step = 0; step < max_retries; step++) {
        if (
#if SQUARE_BOUNDS
            std::abs(z.real()) + std::abs(z.imag()) > square_boundary
#else
            std::norm(z) > circle_boundary
#endif
        ) {
            // points outside will always diverge
            return step;
        }
        z = z*z + shift;
    }

    /*z2 = z*z*z*z + 2*s*z*z + s*s + s*/

    return max_retries;
}

float get_mondelbrot_gradient(Point point, u32 max_retries) {
    return (float)how_many_steps_to_diverge(point, max_retries) / max_retries;
}


Color sinebow(double t) {
    // rainbow made of 3 sine waves out of phase
    // The 255 * sine^2 outputs range 255 * [0, 1] = [0, 255]
    // The period for sin(pi*t) is [0, 1], same as expected t

    double r_val = sin(M_PI * t + 0.0             );
    double g_val = sin(M_PI * t + 2.0 * M_PI / 3.0);
    double b_val = sin(M_PI * t + 4.0 * M_PI / 3.0);

    return Color{
        .r = (unsigned char)(r_val * r_val * r_val * r_val * 255.0),
        .g = (unsigned char)(g_val * g_val * g_val * g_val * 255.0),
        .b = (unsigned char)(b_val * b_val * b_val * b_val * 255.0),
        .a = 255
    };
}

Color gradient_to_color(float scale) {
#if INVERSE_GRADIENT
    scale = 1/scale;
#endif

#if SINEBOW_SCHEMA
    if (scale == 1.0) return Color{0, 0, 0, 255};
    return sinebow(scale);
#elif RAINBOW_SCHEMA
    if (scale == 1.0) return Color{0, 0, 0, 255};
    return ColorFromHSV(scale*360, 1, 1);
#else
#endif

    return Color{0, (u8)(scale*255), 0, 255};
}

Point convert_pixels_to_points(Vector2 pixel, float frame_width) {
    return Point(
        pixel.x * frame_width / screen_size,
        pixel.y * frame_width / screen_size
    );
}

/*Vector2 convert_points_to_pixels(Point point, float frame_width) {*/
/*    return Vector2{*/
/*        (float)(point.real() * screen_size / frame_width),*/
/*        (float)(point.imag() * screen_size / frame_width)*/
/*    };*/
/*}*/

void update_image_data(Point center_point, float frame_width) {
    uint8_t *image_pointer = state.image_data;
    for (size_t y = 0; y < points_per_side; y++) {
        for (size_t x = 0; x < points_per_side; x++) {
            Point point(
                ((float)x - (float)points_per_side / 2) * frame_width / points_per_side,
                ((float)y - (float)points_per_side / 2) * frame_width / points_per_side
            );
            point += center_point;
            float scale = get_mondelbrot_gradient(point, max_retries);
            Color color = gradient_to_color(scale);
            * image_pointer++ = color.r;
            * image_pointer++ = color.g;
            * image_pointer++ = color.b;
        }
    }
}

bool zoom_if_there_is_input() {
    float wheel;
    bool mouse_zoom = false;

    if (IsKeyDown(KEY_UP) || IsKeyDown(KEY_K)) {
        wheel = GetFrameTime() * keyboard_zoom_multiplier;
    } else if (IsKeyDown(KEY_DOWN) || IsKeyDown(KEY_J)) {
        wheel = -GetFrameTime() * keyboard_zoom_multiplier;
    } else {
        wheel = GetMouseWheelMove();
        mouse_zoom = true;
    }

    if (wheel != 0) {
        float old_scale = state.scale;
        state.scale /= std::exp(wheel*0.1f);
        if (mouse_zoom) {
            float scale_difference = old_scale - state.scale;
            Vector2 mouse = GetMousePosition();
            state.center_pixel = Vector2{
                state.center_pixel.x + screen_size * scale_difference * (mouse.x / screen_size - 0.5f),
                state.center_pixel.y + screen_size * scale_difference * (mouse.y / screen_size - 0.5f)
            };
        }
        return true;
    }
    return false;
}

// TODO: support resizing window
// TODO: support rainbow coloring
// TODO: display julia point
// TODO: allow to change color scheme in the app
// TODO: allow to alt+click to set the point
// TODO: allow to save the picture
// TODO: reproduce pfp effect
//
// TODO: look into <thread>, OpenMP, or pthreads
// TODO: make it possible to switch to GLSL fragment shader
// TODO: desyncronize zooming and rendering to the texture (like running in a separate thread)

int main() {
    Image image = {
        .data = state.image_data,
        .width = points_per_side,
        .height = points_per_side,
        .format = PIXELFORMAT_UNCOMPRESSED_R8G8B8,
        .mipmaps = 1
    };

    InitWindow(screen_size, screen_size + status_bar_size, "Mondelbrot Set Explorer");

    update_image_data(state.center_point, state.frame_width);
    Texture2D texture = LoadTextureFromImage(image);

    SetTargetFPS(120);

    while (!WindowShouldClose()) {
        bool force_render = false;

        zoom_if_there_is_input();

        if (IsKeyPressed(KEY_V)) {
            state.showing_julia_set = !state.showing_julia_set;
            force_render = true;
        }


        if (IsMouseButtonDown(MOUSE_BUTTON_LEFT)) {
            Vector2 delta = GetMouseDelta();
            state.center_pixel = Vector2{
                state.center_pixel.x + delta.x,
                state.center_pixel.y + delta.y
            };
        }
        if (IsMouseButtonDown(MOUSE_BUTTON_RIGHT)) {
            state.julia_point -= convert_pixels_to_points(GetMouseDelta(), state.frame_width);
            force_render = true;
        }

        bool zoomed_too_much = state.scale > scale_threthold || 1.0f > state.scale * scale_threthold;
        if (force_render || zoomed_too_much) {
            state.frame_width /= state.scale;
            Vector2 pixel_difference = {
                state.center_pixel.x - points_per_side*image_scale/2.0f,
                state.center_pixel.y - points_per_side*image_scale/2.0f
            };
            state.center_point -= convert_pixels_to_points(pixel_difference, state.frame_width);

            update_image_data(state.center_point, state.frame_width);
            UpdateTexture(texture, state.image_data);

            state.scale = 1.0f;
            state.center_pixel = Vector2{screen_size/2.0f, screen_size/2.0f};
        }

        BeginDrawing();
            ClearBackground(BLACK);

            Vector2 upper_left_corner = {
                state.center_pixel.x - points_per_side*state.scale*image_scale/2.0f,
                state.center_pixel.y - points_per_side*state.scale*image_scale/2.0f
            };
            DrawTextureEx(texture, upper_left_corner, 0.0f, state.scale * image_scale, WHITE);

#if DRAW_CENTERS
            DrawCircle(state.center_pixel.x, state.center_pixel.y, /*radius*/8.0f, WHITE);
            DrawCircle(state.center_pixel.x, state.center_pixel.y, /*radius*/5.0f, BLACK);

            DrawCircle(screen_size/2.0f, screen_size/2.0f, /*radius*/8.0f, RED);
            DrawCircle(screen_size/2.0f, screen_size/2.0f, /*radius*/5.0f, BLACK);
#endif

            DrawRectangle(0, screen_size, screen_size, status_bar_size, BLACK);
            char buffer[64];

            sprintf(buffer, "center: %+F%+Fi  width: %e", (double)state.center_point.real(), (double)state.center_point.imag(), state.frame_width);
            DrawText(buffer, screen_size * 0.01, screen_size + 1, 20, RED);

            sprintf(buffer, "fps: %d", GetFPS());
            DrawText(buffer, screen_size * 0.87, screen_size + 1, 20, RED);
        EndDrawing();
    }

    CloseWindow();

    return 0;
}
