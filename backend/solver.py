"""
AI-Based Sudoku Solver
Algorithms: Constraint Propagation (AC-3) + Backtracking with MRV heuristic
"""

from typing import Optional


def parse_grid(grid: list[list[int]]) -> dict:
    """Convert 9x9 grid to dict of possible values per cell."""
    values = {(r, c): set(range(1, 10)) for r in range(9) for c in range(9)}
    for r in range(9):
        for c in range(9):
            digit = grid[r][c]
            if digit != 0:
                if not assign(values, r, c, digit):
                    return {}  # Contradiction
    return values


def peers(r: int, c: int) -> set:
    """Return all peer positions of (r, c) — same row, col, and 3×3 box."""
    row_peers = {(r, cc) for cc in range(9) if cc != c}
    col_peers = {(rr, c) for rr in range(9) if rr != r}
    box_r, box_c = (r // 3) * 3, (c // 3) * 3
    box_peers = {
        (box_r + dr, box_c + dc)
        for dr in range(3) for dc in range(3)
        if (box_r + dr, box_c + dc) != (r, c)
    }
    return row_peers | col_peers | box_peers


# Precompute peers for performance
PEERS = {(r, c): peers(r, c) for r in range(9) for c in range(9)}

# Precompute units (rows, cols, boxes)
UNITS = {}
for r in range(9):
    for c in range(9):
        units = [
            [(r, cc) for cc in range(9)],            # row
            [(rr, c) for rr in range(9)],            # col
            [(r // 3 * 3 + dr, c // 3 * 3 + dc)     # box
             for dr in range(3) for dc in range(3)]
        ]
        UNITS[(r, c)] = units


def assign(values: dict, r: int, c: int, d: int) -> dict | bool:
    """Assign digit d to (r,c) and propagate constraints. Return False on contradiction."""
    other_values = values[(r, c)] - {d}
    for d2 in other_values:
        if not eliminate(values, r, c, d2):
            return False
    return values


def eliminate(values: dict, r: int, c: int, d: int) -> dict | bool:
    """Eliminate digit d from values[r,c]. Apply constraint propagation."""
    if d not in values[(r, c)]:
        return values  # Already eliminated

    values[(r, c)].discard(d)

    # 1) If a cell is reduced to one value, eliminate that value from peers
    if len(values[(r, c)]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[(r, c)]) == 1:
        d2 = next(iter(values[(r, c)]))
        for peer in PEERS[(r, c)]:
            if not eliminate(values, peer[0], peer[1], d2):
                return False

    # 2) If a unit has only one place for a digit, put it there
    for unit in UNITS[(r, c)]:
        dplaces = [(rr, cc) for (rr, cc) in unit if d in values[(rr, cc)]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for digit
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0][0], dplaces[0][1], d):
                return False

    return values


def backtrack(values: dict) -> dict | bool:
    """Backtracking search with Minimum Remaining Values (MRV) heuristic."""
    if values is False:
        return False
    if all(len(values[(r, c)]) == 1 for r in range(9) for c in range(9)):
        return values  # Solved!

    # MRV: pick cell with fewest possible values (>1)
    _, (r, c) = min(
        (len(values[(r, c)]), (r, c))
        for r in range(9) for c in range(9)
        if len(values[(r, c)]) > 1
    )

    for d in sorted(values[(r, c)]):
        result = backtrack(assign(dict({k: set(v) for k, v in values.items()}), r, c, d))
        if result:
            return result
    return False


def solve(grid: list[list[int]]) -> Optional[list[list[int]]]:
    """
    Main solve function.
    Returns solved 9x9 grid or None if unsolvable.
    """
    values = parse_grid(grid)
    if not values:
        return None

    result = backtrack(values)
    if not result:
        return None

    return [[next(iter(result[(r, c)])) for c in range(9)] for r in range(9)]


def validate_grid(grid: list) -> tuple[bool, str]:
    """Validate input grid format."""
    if not isinstance(grid, list) or len(grid) != 9:
        return False, "Grid must be a 9x9 list"
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False, "Each row must have exactly 9 cells"
        for cell in row:
            if not isinstance(cell, int) or not (0 <= cell <= 9):
                return False, "Cell values must be integers 0–9 (0 = empty)"
    return True, "Valid"


def is_valid_solution(grid: list[list[int]]) -> bool:
    """Verify that a solved grid satisfies all Sudoku constraints."""
    expected = set(range(1, 10))
    for i in range(9):
        if set(grid[i]) != expected:
            return False
        if {grid[r][i] for r in range(9)} != expected:
            return False
    for br in range(3):
        for bc in range(3):
            box = {grid[br*3+dr][bc*3+dc] for dr in range(3) for dc in range(3)}
            if box != expected:
                return False
    return True


def count_filled(grid: list[list[int]]) -> int:
    return sum(1 for r in range(9) for c in range(9) if grid[r][c] != 0)


def difficulty(grid: list[list[int]]) -> str:
    filled = count_filled(grid)
    if filled >= 36:
        return "Easy"
    elif filled >= 27:
        return "Medium"
    elif filled >= 22:
        return "Hard"
    else:
        return "Expert"
