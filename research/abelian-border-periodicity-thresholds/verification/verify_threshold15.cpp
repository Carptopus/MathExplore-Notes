#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <set>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

#ifndef ABP_THRESHOLD
#define ABP_THRESHOLD 15
#endif

#ifndef ABP_WINDOW
#define ABP_WINDOW 30
#endif

#ifndef ABP_MAX_BLOCK
#define ABP_MAX_BLOCK 24
#endif

constexpr int kThreshold = ABP_THRESHOLD;
constexpr int kWindow = ABP_WINDOW;
constexpr int kMaxBlock = ABP_MAX_BLOCK;

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

struct Edge {
    int target;
    int weight;
};

struct PhaseResult {
    int covered = 0;
    bool uncovered_acyclic = false;
    int witness_period = 0;
    int witness_weight = 0;
    int witness_states = 0;
};

PhaseResult verify_phase_cover(
    const std::vector<int>& members,
    const std::vector<std::vector<Edge>>& adjacency,
    const std::vector<int>& component,
    int component_id) {
    const int size = static_cast<int>(members.size());
    std::unordered_map<int, int> local_id;
    for (int i = 0; i < size; ++i) {
        local_id.emplace(members[i], i);
    }

    std::vector<std::vector<Edge>> local(size);
    for (int i = 0; i < size; ++i) {
        for (const Edge edge : adjacency[members[i]]) {
            if (component[edge.target] == component_id) {
                local[i].push_back({local_id.at(edge.target), edge.weight});
            }
        }
    }

    std::vector<std::set<std::pair<int, int>>> transitions(size);
    for (int state = 0; state < size; ++state) {
        transitions[state].insert({state, 0});
    }
    std::vector<bool> covered(size, false);
    int witness_period = 0;
    int witness_weight = 0;
    int witness_states = 0;

    for (int period = 1; period <= kMaxBlock; ++period) {
        std::vector<std::set<std::pair<int, int>>> next(size);
        for (int state = 0; state < size; ++state) {
            for (const auto [middle, weight] : transitions[state]) {
                for (const Edge edge : local[middle]) {
                    next[state].insert({edge.target, weight + edge.weight});
                }
            }
        }
        transitions = std::move(next);

        for (int block_weight = 0; block_weight <= period; ++block_weight) {
            std::vector<bool> good(size, true);
            for (int state = 0; state < size; ++state) {
                if (transitions[state].empty()) {
                    good[state] = false;
                    continue;
                }
                for (const auto [target, weight] : transitions[state]) {
                    (void)target;
                    if (weight != block_weight) {
                        good[state] = false;
                        break;
                    }
                }
            }

            bool changed = true;
            while (changed) {
                changed = false;
                for (int state = 0; state < size; ++state) {
                    if (!good[state]) {
                        continue;
                    }
                    for (const auto [target, weight] : transitions[state]) {
                        (void)weight;
                        if (!good[target]) {
                            good[state] = false;
                            changed = true;
                            break;
                        }
                    }
                }
            }
            const int good_count =
                static_cast<int>(std::count(good.begin(), good.end(), true));
            if (good_count > witness_states) {
                witness_period = period;
                witness_weight = block_weight;
                witness_states = good_count;
            }
            for (int state = 0; state < size; ++state) {
                covered[state] = covered[state] || good[state];
            }
        }
    }

    std::vector<int> color(size, 0);
    std::function<bool(int)> has_cycle = [&](int state) {
        color[state] = 1;
        for (const Edge edge : local[state]) {
            if (covered[edge.target]) {
                continue;
            }
            if (color[edge.target] == 1) {
                return true;
            }
            if (color[edge.target] == 0 && has_cycle(edge.target)) {
                return true;
            }
        }
        color[state] = 2;
        return false;
    };

    bool complement_has_cycle = false;
    for (int state = 0; state < size; ++state) {
        if (!covered[state] && color[state] == 0 && has_cycle(state)) {
            complement_has_cycle = true;
            break;
        }
    }

    return {
        static_cast<int>(std::count(covered.begin(), covered.end(), true)),
        !complement_has_cycle,
        witness_period,
        witness_weight,
        witness_states,
    };
}

}  // namespace

int main() {
    const std::vector<std::uint64_t> words = enumerate_words();
    const std::uint64_t node_mask = (std::uint64_t{1} << (kWindow - 1)) - 1U;

    std::unordered_map<std::uint64_t, int> node_ids;
    std::vector<std::uint64_t> node_values;
    auto node_id = [&](std::uint64_t node) {
        const auto [iterator, inserted] =
            node_ids.emplace(node, static_cast<int>(node_ids.size()));
        if (inserted) {
            node_values.push_back(node);
        }
        return iterator->second;
    };
    for (const std::uint64_t word : words) {
        node_id(word >> 1U);
        node_id(word & node_mask);
    }

    std::vector<std::vector<Edge>> adjacency(node_ids.size());
    for (const std::uint64_t word : words) {
        adjacency[node_ids.at(word >> 1U)].push_back(
            {node_ids.at(word & node_mask), static_cast<int>(word & 1U)});
    }

    const int node_count = static_cast<int>(adjacency.size());
    std::vector<int> index(node_count, -1), low(node_count, -1), component(node_count, -1);
    std::vector<bool> on_stack(node_count, false);
    std::vector<int> stack;
    std::vector<std::vector<int>> components;
    int next_index = 0;

    std::function<void(int)> tarjan = [&](int vertex) {
        index[vertex] = low[vertex] = next_index++;
        stack.push_back(vertex);
        on_stack[vertex] = true;
        for (const Edge edge : adjacency[vertex]) {
            if (index[edge.target] < 0) {
                tarjan(edge.target);
                low[vertex] = std::min(low[vertex], low[edge.target]);
            } else if (on_stack[edge.target]) {
                low[vertex] = std::min(low[vertex], index[edge.target]);
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
    int phase_failures = 0;
    std::vector<PhaseResult> phase_results;
    for (int component_id = 0; component_id < static_cast<int>(components.size());
         ++component_id) {
        const auto& members = components[component_id];
        int internal_edges = 0;
        for (const int vertex : members) {
            for (const Edge edge : adjacency[vertex]) {
                internal_edges += component[edge.target] == component_id;
            }
        }
        const bool cyclic = members.size() > 1 || internal_edges > 0;
        if (!cyclic) {
            continue;
        }
        ++cyclic_components;
        if (internal_edges <= static_cast<int>(members.size())) {
            continue;
        }
        ++branching_components;
        const PhaseResult phase =
            verify_phase_cover(members, adjacency, component, component_id);
        phase_results.push_back(phase);
        if (!phase.uncovered_acyclic) {
            ++phase_failures;
#ifdef ABP_DUMP_FAILURES
            std::cout << "failure_component_begin\n";
            for (const int vertex : members) {
                for (const Edge edge : adjacency[vertex]) {
                    if (component[edge.target] == component_id) {
                        std::cout << "edge source=0x" << std::hex
                                  << node_values[vertex] << " target=0x"
                                  << node_values[edge.target] << std::dec
                                  << " weight=" << edge.weight << '\n';
                    }
                }
            }
            std::cout << "failure_component_end\n";
#endif
        }
        std::cout << "branching_component_states=" << members.size()
                  << " internal_edges=" << internal_edges
                  << " covered_states=" << phase.covered
                  << " uncovered_acyclic=" << phase.uncovered_acyclic
                  << " witness_period=" << phase.witness_period
                  << " witness_weight=" << phase.witness_weight
                  << " witness_states=" << phase.witness_states << '\n';
    }

    std::cout << "threshold=" << kThreshold << '\n';
    std::cout << "window=" << kWindow << '\n';
    std::cout << "allowed_words=" << words.size() << '\n';
    std::cout << "graph_nodes=" << node_count << '\n';
    std::cout << "graph_edges=" << words.size() << '\n';
    std::cout << "cyclic_components=" << cyclic_components << '\n';
    std::cout << "branching_components=" << branching_components << '\n';
    std::cout << "phase_failures=" << phase_failures << '\n';

#if ABP_THRESHOLD == 15 && ABP_WINDOW == 30
    return branching_components == 4 && phase_failures == 0 ? 0 : 1;
#else
    return phase_failures == 0 ? 0 : 1;
#endif
}
