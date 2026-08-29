// Exact extreme-ray certificate for the integral Fano triangle cone
//
//   C = {h in R^7 : h_i >= 0 and
//        h_a <= h_b + h_c on every Fano line {a,b,c}}.
//
// Every extreme ray of this pointed seven-dimensional cone is the common
// zero-set of six linearly independent defining inequalities.  We enumerate
// every six-subset of the 28 defining inequalities, compute its generalized
// cross product over the integers, and retain precisely the feasible rays.
// No floating-point or external polyhedral package is used.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>

using Integer = std::int64_t;
using Row = std::array<Integer, 7>;
using Ray = std::array<Integer, 7>;

constexpr std::array<std::array<int, 3>, 7> LINES = {{
    {{0, 1, 2}}, {{0, 3, 4}}, {{0, 5, 6}}, {{1, 3, 5}},
    {{1, 4, 6}}, {{2, 3, 6}}, {{2, 4, 5}},
}};

Integer determinant6(std::array<std::array<Integer, 6>, 6> matrix) {
    Integer sign = 1;
    Integer previous = 1;
    for (int column = 0; column < 5; ++column) {
        int pivot_row = column;
        while (pivot_row < 6 && matrix[pivot_row][column] == 0) ++pivot_row;
        if (pivot_row == 6) return 0;
        if (pivot_row != column) {
            std::swap(matrix[pivot_row], matrix[column]);
            sign = -sign;
        }
        const Integer pivot = matrix[column][column];
        for (int row = column + 1; row < 6; ++row) {
            for (int next = column + 1; next < 6; ++next) {
                const Integer numerator =
                    matrix[row][next] * pivot -
                    matrix[row][column] * matrix[column][next];
                matrix[row][next] = numerator / previous;
            }
        }
        previous = pivot;
    }
    return sign * matrix[5][5];
}

Ray null_vector(const std::array<Row, 6>& matrix) {
    Ray result{};
    for (int omitted = 0; omitted < 7; ++omitted) {
        std::array<std::array<Integer, 6>, 6> minor{};
        for (int row = 0; row < 6; ++row) {
            int target = 0;
            for (int column = 0; column < 7; ++column) {
                if (column == omitted) continue;
                minor[row][target++] = matrix[row][column];
            }
        }
        const Integer determinant = determinant6(minor);
        result[omitted] = (omitted % 2 == 0) ? determinant : -determinant;
    }
    return result;
}

Integer dot(const Row& row, const Ray& ray) {
    Integer result = 0;
    for (int coordinate = 0; coordinate < 7; ++coordinate) {
        result += row[coordinate] * ray[coordinate];
    }
    return result;
}

bool normalize_feasible(Ray& ray, const std::vector<Row>& inequalities) {
    Integer divisor = 0;
    for (Integer value : ray) divisor = std::gcd(divisor, std::abs(value));
    if (divisor == 0) return false;
    for (Integer& value : ray) value /= divisor;

    bool nonnegative = true;
    bool nonpositive = true;
    for (const Row& inequality : inequalities) {
        const Integer value = dot(inequality, ray);
        nonnegative = nonnegative && value >= 0;
        nonpositive = nonpositive && value <= 0;
    }
    if (!nonnegative && !nonpositive) return false;
    if (nonpositive) {
        for (Integer& value : ray) value = -value;
    }
    return true;
}

int main() {
    std::vector<Row> inequalities;
    for (int coordinate = 0; coordinate < 7; ++coordinate) {
        Row row{};
        row[coordinate] = 1;
        inequalities.push_back(row);
    }
    for (const auto& line : LINES) {
        for (int distinguished : line) {
            Row row{};
            row[distinguished] = -1;
            for (int point : line) {
                if (point != distinguished) row[point] = 1;
            }
            inequalities.push_back(row);
        }
    }

    std::set<Ray> rays;
    std::uint64_t subsets = 0;
    for (int a = 0; a < 23; ++a)
    for (int b = a + 1; b < 24; ++b)
    for (int c = b + 1; c < 25; ++c)
    for (int d = c + 1; d < 26; ++d)
    for (int e = d + 1; e < 27; ++e)
    for (int f = e + 1; f < 28; ++f) {
        ++subsets;
        const std::array<Row, 6> matrix = {{
            inequalities[a], inequalities[b], inequalities[c],
            inequalities[d], inequalities[e], inequalities[f],
        }};
        Ray ray = null_vector(matrix);
        if (normalize_feasible(ray, inequalities)) rays.insert(ray);
    }

    const std::set<Ray> expected = {
        Ray{{0,0,0,1,1,1,1}}, Ray{{0,1,1,0,0,1,1}},
        Ray{{0,1,1,1,1,0,0}}, Ray{{1,0,1,0,1,0,1}},
        Ray{{1,0,1,1,0,1,0}}, Ray{{1,1,0,0,1,1,0}},
        Ray{{1,1,0,1,0,0,1}}, Ray{{1,1,2,1,2,2,1}},
        Ray{{1,1,2,2,1,1,2}}, Ray{{1,2,1,1,2,1,2}},
        Ray{{1,2,1,2,1,2,1}}, Ray{{2,1,1,1,1,2,2}},
        Ray{{2,1,1,2,2,1,1}}, Ray{{2,2,2,1,1,1,1}},
    };

    std::cout << "inequalities=" << inequalities.size()
              << " six_subsets=" << subsets
              << " extreme_rays=" << rays.size() << '\n';
    if (rays != expected) {
        std::cerr << "FAIL: enumerated extreme rays differ from the certificate\n";
        for (const Ray& ray : rays) {
            if (expected.count(ray)) continue;
            std::cerr << "unexpected=";
            for (Integer value : ray) std::cerr << value << ',';
            std::cerr << '\n';
        }
        for (const Ray& ray : expected) {
            if (rays.count(ray)) continue;
            std::cerr << "missing=";
            for (Integer value : ray) std::cerr << value << ',';
            std::cerr << '\n';
        }
        return 1;
    }
    std::cout << "PASS: the fourteen primitive extreme rays are complete\n";
    return 0;
}
