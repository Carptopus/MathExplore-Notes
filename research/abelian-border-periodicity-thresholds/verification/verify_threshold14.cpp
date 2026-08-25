#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <stack>
#include <unordered_map>
#include <vector>

namespace {

constexpr int kThreshold = 14;
constexpr int kWindow = 36;

bool suffixes_are_valid(const std::vector<int>& prefix, int length) {
    for (int factor_length = kThreshold; factor_length <= length; ++factor_length) {
        const int start = length - factor_length;
        bool bordered = false;
        for (int border = 1; border <= factor_length / 2; ++border) {
            const int left_ones = prefix[start + border] - prefix[start];
            const int right_ones = prefix[length] - prefix[length - border];
            if (left_ones == right_ones) {
                bordered = true;
                break;
            }
        }
        if (!bordered) {
            return false;
        }
    }
    return true;
}

std::vector<std::uint64_t> enumerate_words() {
    std::vector<std::uint64_t> words;
    std::vector<int> prefix(kWindow + 1, 0);

    std::function<void(int, std::uint64_t)> visit = [&](int position, std::uint64_t word) {
        if (position == kWindow) {
            words.push_back(word);
            return;
        }
        for (int bit = 0; bit <= 1; ++bit) {
            prefix[position + 1] = prefix[position] + bit;
            if (position + 1 < kThreshold || suffixes_are_valid(prefix, position + 1)) {
                visit(position + 1, (word << 1U) | static_cast<std::uint64_t>(bit));
            }
        }
    };

    visit(0, 0);
    return words;
}

}  // namespace

int main() {
    const std::vector<std::uint64_t> words = enumerate_words();
    const std::uint64_t node_mask = (std::uint64_t{1} << (kWindow - 1)) - 1U;

    std::unordered_map<std::uint64_t, int> node_ids;
    auto node_id = [&](std::uint64_t node) {
        const auto [iterator, inserted] =
            node_ids.emplace(node, static_cast<int>(node_ids.size()));
        return iterator->second;
    };

    for (const std::uint64_t word : words) {
        node_id(word >> 1U);
        node_id(word & node_mask);
    }

    std::vector<std::vector<int>> adjacency(node_ids.size());
    for (const std::uint64_t word : words) {
        adjacency[node_ids.at(word >> 1U)].push_back(node_ids.at(word & node_mask));
    }

    const int node_count = static_cast<int>(adjacency.size());
    std::vector<int> index(node_count, -1);
    std::vector<int> low(node_count, -1);
    std::vector<int> component(node_count, -1);
    std::vector<bool> on_stack(node_count, false);
    std::vector<int> stack;
    std::vector<std::vector<int>> components;
    int next_index = 0;

    std::function<void(int)> tarjan = [&](int vertex) {
        index[vertex] = low[vertex] = next_index++;
        stack.push_back(vertex);
        on_stack[vertex] = true;
        for (const int target : adjacency[vertex]) {
            if (index[target] < 0) {
                tarjan(target);
                low[vertex] = std::min(low[vertex], low[target]);
            } else if (on_stack[target]) {
                low[vertex] = std::min(low[vertex], index[target]);
            }
        }
        if (low[vertex] != index[vertex]) {
            return;
        }
        components.emplace_back();
        const int component_id = static_cast<int>(components.size()) - 1;
        while (true) {
            const int member = stack.back();
            stack.pop_back();
            on_stack[member] = false;
            component[member] = component_id;
            components.back().push_back(member);
            if (member == vertex) {
                break;
            }
        }
    };

    for (int vertex = 0; vertex < node_count; ++vertex) {
        if (index[vertex] < 0) {
            tarjan(vertex);
        }
    }

    int cyclic_components = 0;
    int branching_components = 0;
    int maximum_cyclic_states = 0;
    for (int component_id = 0; component_id < static_cast<int>(components.size());
         ++component_id) {
        const auto& members = components[component_id];
        int internal_edges = 0;
        for (const int vertex : members) {
            for (const int target : adjacency[vertex]) {
                internal_edges += component[target] == component_id;
            }
        }
        const bool cyclic = members.size() > 1 || internal_edges > 0;
        if (!cyclic) {
            continue;
        }
        ++cyclic_components;
        maximum_cyclic_states =
            std::max(maximum_cyclic_states, static_cast<int>(members.size()));
        if (internal_edges > static_cast<int>(members.size())) {
            ++branching_components;
        }
    }

    std::cout << "threshold=" << kThreshold << '\n';
    std::cout << "window=" << kWindow << '\n';
    std::cout << "allowed_words=" << words.size() << '\n';
    std::cout << "graph_nodes=" << node_count << '\n';
    std::cout << "graph_edges=" << words.size() << '\n';
    std::cout << "cyclic_components=" << cyclic_components << '\n';
    std::cout << "maximum_cyclic_states=" << maximum_cyclic_states << '\n';
    std::cout << "branching_components=" << branching_components << '\n';

    return branching_components == 0 ? 0 : 1;
}
