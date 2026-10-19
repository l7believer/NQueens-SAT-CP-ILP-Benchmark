from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SolverResult:
    problem_size: int
    solver_name: str
    encoding: Optional[str]
    is_sat: bool
    is_valid: bool
    solving_time: float      # in seconds
    num_variables: int
    num_clauses: int        # or constraints for ILP/CP
    solution: Optional[List[int]]  # solution[row] = col


def is_valid_nqueens_solution(n: int, solution: Optional[List[int]]) -> bool:
    if solution is None or len(solution) != n:
        return False

    rows = set()
    cols = set()
    diags = set()
    anti_diags = set()

    for r in range(n):
        c = solution[r]
        if not (0 <= c < n):
            return False

        if r in rows or c in cols or (r - c) in diags or (r + c) in anti_diags:
            return False

        rows.add(r)
        cols.add(c)
        diags.add(r - c)
        anti_diags.add(r + c)

    return len(rows) == n and len(cols) == n


def format_board(n: int, solution: Optional[List[int]], max_display: int = 16) -> str:
    if solution is None:
        return "No solution found."
    if n > max_display:
        return f"Board {n}x{n} too large for ASCII display. Queens at: {solution[:10]} ... {solution[-5:]}"

    lines = []
    lines.append("+" + "---+" * n)
    for r in range(n):
        row_str = "|"
        for c in range(n):
            if solution[r] == c:
                row_str += " Q |"
            else:
                row_str += " . |"
        lines.append(row_str)
        lines.append("+" + "---+" * n)
    return "\n".join(lines)
