import time
from typing import Optional, List
from pysat.solvers import Solver

from src.sat_encodings import build_nqueens_cnf
from src.utils import SolverResult, is_valid_nqueens_solution


def solve_nqueens_sat(
    n: int,
    amo_method: str = "pairwise",
    solver_name: str = "cadical153",
) -> SolverResult:
    # Build CNF formula
    t0 = time.perf_counter()
    cnf, num_base_vars, top_id = build_nqueens_cnf(n, amo_method=amo_method)
    encoding_time = time.perf_counter() - t0

    num_clauses = len(cnf.clauses)
    num_variables = top_id

    solution: Optional[List[int]] = None
    is_sat = False
    is_valid = False

    t_solve_start = time.perf_counter()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as s:
        is_sat = s.solve()
        solving_time = time.perf_counter() - t_solve_start

        if is_sat:
            raw_model = s.get_model()
            model_set = set(raw_model)
            # Map variable IDs back to queen column positions
            sol = []
            for r in range(n):
                queen_col = -1
                for c in range(n):
                    vid = r * n + c + 1
                    if vid in model_set:
                        queen_col = c
                        break
                sol.append(queen_col)
            solution = sol
            is_valid = is_valid_nqueens_solution(n, solution)

    total_time = encoding_time + solving_time

    return SolverResult(
        problem_size=n,
        solver_name=f"SAT ({solver_name})",
        encoding=amo_method,
        is_sat=is_sat,
        is_valid=is_valid,
        solving_time=total_time,
        num_variables=num_variables,
        num_clauses=num_clauses,
        solution=solution,
    )
