#include <complex>
#include <functional>
#include <iostream>

template <typename PartT, typename T>
constexpr std::complex<PartT> operator/(const std::complex<PartT> &rhs, const T &lhs) {
    return std::complex<PartT>(rhs.real() / lhs, rhs.imag() / lhs);
}

template <typename PartT, typename T>
constexpr std::complex<PartT> operator*(const std::complex<PartT> &rhs, const T &lhs) {
    return std::complex<PartT>(rhs.real() * lhs, rhs.imag() * lhs);
}

using part_t = long double;
using complex_t = std::complex<part_t>;

const char set_color = ' ';
const std::string pallet = ".:-=+*#%@";
const std::size_t N = 32;

bool out_of_bounds_abs(const complex_t &c) {
    return abs(c.real()) > 2.0 || abs(c.imag()) > 2.0;
}

bool out_of_bounds_circle(const complex_t &c) {
    return c.real() * c.real() + c.imag() * c.imag() > 4;
}

using boundary_func_t = std::function<bool(const complex_t &)>;

struct Mondelbrot {
public:
    std::size_t max_iter = 100;
    boundary_func_t boundary = out_of_bounds_circle;
    complex_t initial = complex_t(0, 0);

    std::size_t calculate_at(const complex_t &c) const {
        complex_t z = initial;
        for (std::size_t i = 0; i < max_iter; ++i) {
            z = z * z + c;
            if (boundary(z)) { return i; }
        }
        return max_iter;
    }
};

int main() {
    bool abs_bound = true;

    part_t width = abs_bound ? 3.3 : 2.5;
    complex_t center = complex_t(abs_bound ? -0.5 : -0.75, 0);

    complex_t side_1 = complex_t(width, 0);
    complex_t side_2 = complex_t(0, width);

    complex_t diagonal = side_1 + side_2;
    complex_t helf_diagonal = diagonal / 2;
    complex_t upper_left_corner = center - helf_diagonal;

    complex_t c[N][N];
    for (std::size_t i = 0; i < N; ++i) {
        for (std::size_t j = 0; j < N; ++j) {
            c[i][j] = upper_left_corner + (side_1 * i / (N - 1)) + (side_2 * j / (N - 1));
        }
    }

    const Mondelbrot mondelbrot = {
        .max_iter = 10, .boundary = abs_bound ? out_of_bounds_abs : out_of_bounds_circle};
    std::size_t iterations[N][N];
    for (std::size_t i = 0; i < N; ++i) {
        for (std::size_t j = 0; j < N; ++j) {
            iterations[i][j] = mondelbrot.calculate_at(c[i][j]);
        }
    }

    for (std::size_t i = 0; i < N; ++i) {
        for (std::size_t j = 0; j < N; ++j) {
            std::size_t iter = iterations[i][j];
            if (iter != mondelbrot.max_iter) {
                // nither mondelbrot.max_iter or pallet.size() should never be reached
                std::size_t frac_index = (part_t)iter / (mondelbrot.max_iter - 1) * (pallet.size() - 1);
                std::cout << pallet[frac_index] << pallet[frac_index];
            } else {
                std::cout << set_color << set_color;
            }
        }
        std::cout << std::endl;
    }

    return 0;
}