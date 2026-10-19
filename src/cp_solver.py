import time
from typing import Optional, List
from ortools.sat.python import cp_model

from src.utils import SolverResult, is_valid_nqueens_solution


def solve_nqueens_cp(
    n: int,
    formulation: str = "alldifferent",
    num_workers: int = 1,
) -> SolverResult:
    model = cp_model.CpModel()
    t_start = time.perf_counter()

    if formulation == "alldifferent":
        # 1D model: q[r] is the column index for queen in row r
        q = [model.NewIntVar(0, n - 1, f"q_{r}") for r in range(n)]

        model.AddAllDifferent(q)
        model.AddAllDifferent([q[r] - r for r in range(n)])
        model.AddAllDifferent([q[r] + r for r in range(n)])

        num_vars = n
        num_constraints = 3

    elif formulation == "boolean":
        # 2D model: x[r, c] is 1 if square (r, c) has a queen, 0 otherwise
        x = {}
        for r in range(n):
            for c in range(n):
                x[r, c] = model.NewBoolVar(f"x_{r}_{c}")

        # Row constraints
        for r in range(n):
            model.Add(sum(x[r, c] for c in range(n)) == 1)

        # Column constraints
        for c in range(n):
            model.Add(sum(x[r, c] for r in range(n)) == 1)

        # Diagonals
        diags = {}
        anti_diags = {}
        for r in range(n):
            for c in range(n):
                diags.setdefault(r - c, []).append(x[r, c])
                anti_diags.setdefault(r + c, []).append(x[r, c])

        diag_count = 0
        for d_vars in diags.values():
            if len(d_vars) > 1:
                model.Add(sum(d_vars) <= 1)
                diag_count += 1

        for ad_vars in anti_diags.values():
            if len(ad_vars) > 1:
                model.Add(sum(ad_vars) <= 1)
                diag_count += 1

        num_vars = n * n
        num_constraints = 2 * n + diag_count

    else:
        raise ValueError(f"Unknown CP formulation: {formulation}. Use 'alldifferent' or 'boolean'.")

    # Run CP-SAT solver
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = num_workers
    status = solver.Solve(model)
    solving_time = time.perf_counter() - t_start

    is_sat = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    solution: Optional[List[int]] = None
    is_valid = False

    if is_sat:
        if formulation == "alldifferent":
            solution = [int(solver.Value(q[r])) for r in range(n)]
        else:
            solution = []
            for r in range(n):
                col_found = -1
                for c in range(n):
                    if solver.Value(x[r, c]) == 1:
                        col_found = c
                        break
                solution.append(col_found)

        is_valid = is_valid_nqueens_solution(n, solution)

    return SolverResult(
        problem_size=n,
        solver_name="CP-SAT",
        encoding=f"cp_{formulation}",
        is_sat=is_sat,
        is_valid=is_valid,
        solving_time=solving_time,
        num_variables=num_vars,
        num_clauses=num_constraints,
        solution=solution,
    )
