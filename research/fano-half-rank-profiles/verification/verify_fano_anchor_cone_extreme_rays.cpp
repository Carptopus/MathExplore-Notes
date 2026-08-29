// Exact extreme-ray certificate for C_0 = {h in Fano triangle cone: h_0 >= h_i}.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>

using Integer = std::int64_t;
using Row = std::array<Integer, 7>;
using Ray = std::array<Integer, 7>;

constexpr std::array<std::array<int, 3>, 7> LINES = {{
    {{0,1,2}}, {{0,3,4}}, {{0,5,6}}, {{1,3,5}},
    {{1,4,6}}, {{2,3,6}}, {{2,4,5}},
}};

static Integer determinant6(std::array<std::array<Integer, 6>, 6> matrix) {
    Integer sign = 1, previous = 1;
    for (int column = 0; column < 5; ++column) {
        int pivot = column;
        while (pivot < 6 && matrix[pivot][column] == 0) ++pivot;
        if (pivot == 6) return 0;
        if (pivot != column) { std::swap(matrix[pivot], matrix[column]); sign = -sign; }
        const Integer value = matrix[column][column];
        for (int row = column + 1; row < 6; ++row) {
            for (int next = column + 1; next < 6; ++next) {
                matrix[row][next] =
                    (matrix[row][next] * value - matrix[row][column] * matrix[column][next])
                    / previous;
            }
        }
        previous = value;
    }
    return sign * matrix[5][5];
}

static Ray null_vector(const std::array<Row, 6>& matrix) {
    Ray result{};
    for (int omitted = 0; omitted < 7; ++omitted) {
        std::array<std::array<Integer, 6>, 6> minor{};
        for (int row = 0; row < 6; ++row) {
            int target = 0;
            for (int column = 0; column < 7; ++column) {
                if (column != omitted) minor[row][target++] = matrix[row][column];
            }
        }
        result[omitted] = (omitted % 2 == 0 ? 1 : -1) * determinant6(minor);
    }
    return result;
}

static Integer dot(const Row& row, const Ray& ray) {
    Integer value = 0;
    for (int i = 0; i < 7; ++i) value += row[i] * ray[i];
    return value;
}

static bool normalize(Ray& ray, const std::vector<Row>& inequalities) {
    Integer divisor = 0;
    for (Integer value : ray) divisor = std::gcd(divisor, std::llabs(value));
    if (divisor == 0) return false;
    for (auto& value : ray) value /= divisor;
    bool positive = true, negative = true;
    for (const Row& row : inequalities) {
        Integer value = dot(row, ray);
        positive = positive && value >= 0;
        negative = negative && value <= 0;
    }
    if (!positive && !negative) return false;
    if (negative) for (auto& value : ray) value = -value;
    return true;
}

int main() {
    std::vector<Row> inequalities;
    for (int coordinate = 0; coordinate < 7; ++coordinate) {
        Row row{}; row[coordinate] = 1; inequalities.push_back(row);
    }
    for (const auto& line : LINES) for (int distinguished : line) {
        Row row{}; row[distinguished] = -1;
        for (int point : line) if (point != distinguished) row[point] = 1;
        inequalities.push_back(row);
    }
    for (int point = 1; point < 7; ++point) {
        Row row{}; row[0] = 1; row[point] = -1; inequalities.push_back(row);
    }

    std::set<Ray> rays;
    std::uint64_t subsets = 0;
    std::array<int, 6> choice{};
    std::function<void(int,int)> visit = [&](int depth, int start) {
        if (depth == 6) {
            ++subsets;
            std::array<Row, 6> matrix{};
            for (int i = 0; i < 6; ++i) matrix[i] = inequalities[choice[i]];
            Ray ray = null_vector(matrix);
            if (normalize(ray, inequalities)) rays.insert(ray);
            return;
        }
        for (int index = start; index <= static_cast<int>(inequalities.size()) - (6 - depth); ++index) {
            choice[depth] = index;
            visit(depth + 1, index + 1);
        }
    };
    visit(0, 0);

    const std::set<Ray> expected = {
        Ray{{1,0,1,0,1,0,1}}, Ray{{1,0,1,1,0,1,0}}, Ray{{1,0,1,1,1,1,1}},
        Ray{{1,1,0,0,1,1,0}}, Ray{{1,1,0,1,0,0,1}}, Ray{{1,1,0,1,1,1,1}},
        Ray{{1,1,1,0,1,1,1}}, Ray{{1,1,1,1,0,1,1}}, Ray{{1,1,1,1,1,0,1}},
        Ray{{1,1,1,1,1,1,0}}, Ray{{1,1,1,1,1,1,1}},
        Ray{{2,1,1,1,1,2,2}}, Ray{{2,1,1,1,2,2,2}}, Ray{{2,1,1,2,1,2,2}},
        Ray{{2,1,1,2,2,1,1}}, Ray{{2,1,1,2,2,1,2}}, Ray{{2,1,1,2,2,2,1}},
        Ray{{2,1,2,1,1,2,2}}, Ray{{2,1,2,1,2,2,1}}, Ray{{2,1,2,2,1,1,2}},
        Ray{{2,1,2,2,2,1,1}}, Ray{{2,2,1,1,1,2,2}}, Ray{{2,2,1,1,2,1,2}},
        Ray{{2,2,1,2,1,2,1}}, Ray{{2,2,1,2,2,1,1}}, Ray{{2,2,2,1,1,1,1}},
        Ray{{2,2,2,1,1,1,2}}, Ray{{2,2,2,1,1,2,1}}, Ray{{2,2,2,1,2,1,1}},
        Ray{{2,2,2,2,1,1,1}},
    };

    std::cout << "inequalities=" << inequalities.size() << " subsets=" << subsets
              << " rays=" << rays.size() << '\n';
    if (rays != expected) {
        for (const Ray& ray : rays) if (!expected.count(ray)) {
            std::cerr << "unexpected";
            for (Integer value : ray) std::cerr << ' ' << value;
            std::cerr << '\n';
        }
        for (const Ray& ray : expected) if (!rays.count(ray)) {
            std::cerr << "missing";
            for (Integer value : ray) std::cerr << ' ' << value;
            std::cerr << '\n';
        }
        return 1;
    }
    std::cout << "PASS: the thirty primitive anchored-chamber rays are complete\n";
    return 0;
}
