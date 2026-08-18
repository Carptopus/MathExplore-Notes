"""Parameterised construction primitives for the Hadamard-Sesqui family HSF(t)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable


@dataclass(frozen=True)
class HSFParameters:
    t: int

    def __post_init__(self) -> None:
        if self.t < 2:
            raise ValueError("t must be at least 2")

    @property
    def hadamard_order(self) -> int:
        return 4 * self.t

    @property
    def symmetric_points(self) -> int:
        return 4 * self.t - 1

    @property
    def symmetric_block_size(self) -> int:
        return 2 * self.t - 1

    @property
    def columns(self) -> int:
        return 2 * self.t

    @property
    def rows(self) -> int:
        return 2 * self.t - 1

    @property
    def symbols(self) -> int:
        return 4 * self.t - 2

    @property
    def row_size(self) -> int:
        return 2 * self.t

    @property
    def replication(self) -> int:
        return self.t

    @property
    def lambda_cc(self) -> int:
        return self.t - 1

    @property
    def lambda_rc(self) -> int:
        return self.t

    @property
    def residual_block_size(self) -> int:
        return self.t


def verify_hadamard(matrix: list[list[int]]) -> None:
    order = len(matrix)
    if order == 0 or any(len(row) != order for row in matrix):
        raise ValueError("Hadamard matrix must be nonempty and square")
    if any(value not in (-1, 1) for row in matrix for value in row):
        raise ValueError("Hadamard entries must be +/-1")
    if any(
        sum(matrix[left][column] * matrix[right][column] for column in range(order))
        != (order if left == right else 0)
        for left in range(order)
        for right in range(order)
    ):
        raise ValueError("matrix rows are not mutually orthogonal")


def derived_symmetric_design(
    matrix: list[list[int]], selected_row: int = 0, selected_column: int = 0
) -> list[frozenset[int]]:
    verify_hadamard(matrix)
    order = len(matrix)
    blocks: list[frozenset[int]] = []
    for row in range(order):
        if row == selected_row:
            continue
        block = []
        for column in range(order):
            if column == selected_column:
                continue
            normalized = (
                matrix[row][column]
                * matrix[selected_row][column]
                * matrix[row][selected_column]
                * matrix[selected_row][selected_column]
            )
            if normalized == 1:
                block.append(column if column < selected_column else column - 1)
        blocks.append(frozenset(block))
    return blocks


def verify_bibd(
    blocks: Iterable[Iterable[int]],
    point_count: int,
    block_size: int,
    replication: int,
    pair_lambda: int,
) -> None:
    normalized = [frozenset(block) for block in blocks]
    if len(set(normalized)) != len(normalized):
        raise ValueError("duplicate blocks")
    if any(len(block) != block_size for block in normalized):
        raise ValueError("unexpected block size")
    if any(sum(point in block for block in normalized) != replication for point in range(point_count)):
        raise ValueError("unexpected point replication")
    if any(
        sum(left in block and right in block for block in normalized) != pair_lambda
        for left, right in combinations(range(point_count), 2)
    ):
        raise ValueError("unexpected pair replication")


def residual_design(
    params: HSFParameters,
    symmetric_blocks: list[frozenset[int]],
    distinguished_block_index: int,
) -> list[frozenset[int]]:
    verify_bibd(
        symmetric_blocks,
        params.symmetric_points,
        params.symmetric_block_size,
        params.symmetric_block_size,
        params.lambda_cc,
    )
    distinguished = symmetric_blocks[distinguished_block_index]
    outside = sorted(set(range(params.symmetric_points)) - distinguished)
    relabel = {point: index for index, point in enumerate(outside)}
    residual = [
        frozenset(relabel[point] for point in block - distinguished)
        for index, block in enumerate(symmetric_blocks)
        if index != distinguished_block_index
    ]
    residual.sort(key=lambda block: sum(1 << point for point in block))
    verify_residual_design(params, residual)
    return residual


def verify_residual_design(params: HSFParameters, blocks: list[frozenset[int]]) -> None:
    if len(blocks) != params.symbols:
        raise ValueError("unexpected residual block count")
    verify_bibd(
        blocks,
        params.columns,
        params.residual_block_size,
        params.rows,
        params.lambda_cc,
    )


def column_symbol_sets(params: HSFParameters, blocks: list[frozenset[int]]) -> list[set[int]]:
    verify_residual_design(params, blocks)
    return [
        {symbol for symbol, block in enumerate(blocks) if column in block}
        for column in range(params.columns)
    ]


def rc_compatible_rows(params: HSFParameters, column_sets: list[set[int]]) -> list[int]:
    column_masks = [sum(1 << symbol for symbol in symbols) for symbols in column_sets]
    rows: list[int] = []
    for symbols in combinations(range(params.symbols), params.row_size):
        mask = sum(1 << symbol for symbol in symbols)
        if all((mask & column_mask).bit_count() == params.lambda_rc for column_mask in column_masks):
            rows.append(mask)
    return rows


def find_proper_balanced_rows(
    params: HSFParameters, row_masks: list[int]
) -> tuple[tuple[int, ...], int]:
    """Find one proper row collection by an exact multiplicity-constrained search."""
    chosen: list[int] = []
    chosen_set: set[int] = set()
    counts = [0] * params.symbols
    nodes = 0

    def search() -> tuple[int, ...] | None:
        nonlocal nodes
        nodes += 1
        if len(chosen) == params.rows:
            if counts != [params.replication] * params.symbols:
                return None
            intersections = {
                (row_masks[left] & row_masks[right]).bit_count()
                for left, right in combinations(chosen, 2)
            }
            return tuple(chosen) if len(intersections) > 1 else None

        remaining_slots = params.rows - len(chosen)
        if any(
            count > params.replication or count + remaining_slots < params.replication
            for count in counts
        ):
            return None

        eligible = [
            index
            for index, mask in enumerate(row_masks)
            if index not in chosen_set
            and all(
                counts[symbol] + ((mask >> symbol) & 1) <= params.replication
                for symbol in range(params.symbols)
            )
        ]
        deficient = [symbol for symbol, count in enumerate(counts) if count < params.replication]
        if not deficient:
            return None
        pivot = min(
            deficient,
            key=lambda symbol: sum((row_masks[index] >> symbol) & 1 for index in eligible),
        )
        for index in eligible:
            mask = row_masks[index]
            if not (mask >> pivot) & 1:
                continue
            chosen.append(index)
            chosen_set.add(index)
            for symbol in range(params.symbols):
                counts[symbol] += (mask >> symbol) & 1
            result = search()
            for symbol in range(params.symbols):
                counts[symbol] -= (mask >> symbol) & 1
            chosen_set.remove(index)
            chosen.pop()
            if result is not None:
                return result
        return None

    result = search()
    if result is None:
        raise RuntimeError("no proper balanced row collection was found")
    return result, nodes


def fill_cells(
    params: HSFParameters,
    row_sets: list[set[int]],
    column_sets: list[set[int]],
) -> tuple[list[list[int]], int]:
    options: list[tuple[int, int, int, tuple[tuple[object, ...], ...]]] = []
    active: dict[tuple[object, ...], set[int]] = {}
    for row, row_symbols in enumerate(row_sets):
        for column, column_symbols in enumerate(column_sets):
            for symbol in sorted(row_symbols & column_symbols):
                option_id = len(options)
                constraints = (
                    ("cell", row, column),
                    ("row_symbol", row, symbol),
                    ("column_symbol", column, symbol),
                )
                options.append((row, column, symbol, constraints))
                for constraint in constraints:
                    active.setdefault(constraint, set()).add(option_id)

    solution: list[int] = []
    nodes = 0

    def solve(current: dict[tuple[object, ...], set[int]]) -> bool:
        nonlocal nodes
        nodes += 1
        if not current:
            return True
        constraint = min(current, key=lambda key: len(current[key]))
        for option_id in sorted(current[constraint]):
            constraints = options[option_id][3]
            if any(item not in current or option_id not in current[item] for item in constraints):
                continue
            conflicts: set[int] = set()
            for item in constraints:
                conflicts.update(current[item])
            reduced = {item: set(ids) for item, ids in current.items() if item not in constraints}
            for conflict in conflicts:
                for item in options[conflict][3]:
                    if item in reduced:
                        reduced[item].discard(conflict)
            if any(not ids for ids in reduced.values()):
                continue
            solution.append(option_id)
            if solve(reduced):
                return True
            solution.pop()
        return False

    if not solve(active):
        raise RuntimeError("row and column components have no cell assignment")
    array = [[-1] * params.columns for _ in range(params.rows)]
    for option_id in solution:
        row, column, symbol, _ = options[option_id]
        array[row][column] = symbol
    return array, nodes


def analyze_array(params: HSFParameters, array: list[list[int]]) -> dict[str, object]:
    errors: list[str] = []
    if len(array) != params.rows or any(len(row) != params.columns for row in array):
        return {"valid": False, "errors": ["unexpected array dimensions"]}
    flat = [value for row in array for value in row]
    if any(type(value) is not int or not 0 <= value < params.symbols for value in flat):
        errors.append("symbol outside expected range")
    row_sets = [set(row) for row in array]
    column_sets = [
        {array[row][column] for row in range(params.rows)}
        for column in range(params.columns)
    ]
    if any(len(row) != params.row_size for row in row_sets):
        errors.append("a row repeats a symbol")
    if any(len(column) != params.rows for column in column_sets):
        errors.append("a column repeats a symbol")
    counts = Counter(flat)
    if any(counts[symbol] != params.replication for symbol in range(params.symbols)):
        errors.append("symbol replication is not constant")
    cc = [len(left & right) for left, right in combinations(column_sets, 2)]
    rc = [len(row & column) for row in row_sets for column in column_sets]
    rr = [len(left & right) for left, right in combinations(row_sets, 2)]
    if any(value != params.lambda_cc for value in cc):
        errors.append("column-column association is not constant")
    if any(value != params.lambda_rc for value in rc):
        errors.append("row-column association is not constant")
    if len(set(rr)) == 1:
        errors.append("row-row association is constant")
    histogram = lambda values: {str(key): value for key, value in sorted(Counter(values).items())}
    return {
        "valid": not errors,
        "errors": errors,
        "parameters": {
            "t": params.t,
            "symbols": params.symbols,
            "rows": params.rows,
            "columns": params.columns,
            "replication": params.replication,
            "lambda_cc": params.lambda_cc,
            "lambda_rc": params.lambda_rc,
        },
        "cc_histogram": histogram(cc),
        "rc_histogram": histogram(rc),
        "rr_histogram": histogram(rr),
    }


def construct_from_residual(params: HSFParameters, blocks: list[frozenset[int]]) -> dict[str, object]:
    column_sets = column_symbol_sets(params, blocks)
    row_masks = rc_compatible_rows(params, column_sets)
    selected_indices, row_search_nodes = find_proper_balanced_rows(params, row_masks)
    selected_rows = [
        {symbol for symbol in range(params.symbols) if (row_masks[index] >> symbol) & 1}
        for index in selected_indices
    ]
    array, ordering_nodes = fill_cells(params, selected_rows, column_sets)
    verification = analyze_array(params, array)
    if not verification["valid"]:
        raise RuntimeError(f"constructed array failed parameterised verification: {verification}")
    return {
        "t": params.t,
        "residual_blocks": [sorted(block) for block in blocks],
        "rc_compatible_row_count": len(row_masks),
        "selected_row_candidate_indices": list(selected_indices),
        "selected_row_masks": [row_masks[index] for index in selected_indices],
        "row_search_nodes": row_search_nodes,
        "ordering_exact_cover_nodes": ordering_nodes,
        "array": array,
        "verification": verification,
    }
