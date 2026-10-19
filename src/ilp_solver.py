import time
from typing import Optional, List
from ortools.linear_solver import pywraplp

from src.utils import SolverResult, is_valid_nqueens_solution


def solve_nqueens_ilp(
    n: int,
    solver_id: str = "SCIP",
    time_limit_sec: Optional[float] = 60.0,
) -> SolverResult:
    solver = pywraplp.Solver.CreateSolver(solver_id)
    if solver is None:
        raise RuntimeError(f"Could not initialize solver: {solver_id}")

    if time_limit_sec is not None:
        solver.SetTimeLimit(int(time_limit_sec * 1000))

    t_start = time.perf_counter()

    # Binary variables: x[r, c] in {0, 1}
    x = {}
    for r in range(n):
        for c in range(n):
            x[r, c] = solver.BoolVar(f"x_{r}_{c}")

    # Row constraints: sum_c x[r, c] == 1
    for r in range(n):
        solver.Add(solver.Sum([x[r, c] for c in range(n)]) == 1)

    # Column constraints: sum_r x[r, c] == 1
    for c in range(n):
        solver.Add(solver.Sum([x[r, c] for r in range(n)]) == 1)

    # Diagonals: at most 1 queen per diagonal
    diags = {}
    anti_diags = {}
    for r in range(n):
        for c in range(n):
            diags.setdefault(r - c, []).append(x[r, c])
            anti_diags.setdefault(r + c, []).append(x[r, c])

    num_diag_constraints = 0
    for d_vars in diags.values():
        if len(d_vars) > 1:
            solver.Add(solver.Sum(d_vars) <= 1)
            num_diag_constraints += 1

    for ad_vars in anti_diags.values():
        if len(ad_vars) > 1:
            solver.Add(solver.Sum(ad_vars) <= 1)
            num_diag_constraints += 1

    num_vars = n * n
    num_constraints = 2 * n + num_diag_constraints

    # Feasibility only (constant objective)
    solver.Minimize(0)

    status = solver.Solve()
    solving_time = time.perf_counter() - t_start

    is_sat = status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE)
    solution: Optional[List[int]] = None
    is_valid = False

    if is_sat:
        sol = []
        for r in range(n):
            queen_col = -1
            for c in range(n):
                if x[r, c].solution_value() > 0.5:
                    queen_col = c
                    break
            sol.append(queen_col)
        solution = sol
        is_valid = is_valid_nqueens_solution(n, solution)

    return SolverResult(
        problem_size=n,
        solver_name=f"ILP ({solver_id})",
        encoding="0-1_MIP",
        is_sat=is_sat,
        is_valid=is_valid,
        solving_time=solving_time,
        num_variables=num_vars,
        num_clauses=num_constraints,
        solution=solution,
    )
