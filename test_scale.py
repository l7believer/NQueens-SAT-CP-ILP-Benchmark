import time
from src import solve_nqueens_sat, solve_nqueens_cp, solve_nqueens_ilp

header = f"{'N':>4} | {'SAT-Cadical':>12} | {'SAT-Glucose4':>12} | {'CP-AllDiff':>12} | {'ILP-SCIP':>12}"
print(header)
print("-" * len(header))

for n in [8, 16, 24, 32, 40, 50, 60, 80, 100]:
    r_sat1 = solve_nqueens_sat(n, amo_method='pairwise', solver_name='cadical153')
    t_sat1 = r_sat1.solving_time

    r_sat2 = solve_nqueens_sat(n, amo_method='pairwise', solver_name='glucose4')
    t_sat2 = r_sat2.solving_time

    r_cp = solve_nqueens_cp(n, formulation='alldifferent')
    t_cp = r_cp.solving_time

    if n <= 24:
        r_ilp = solve_nqueens_ilp(n, solver_id='SCIP', time_limit_sec=15.0)
        t_ilp = f"{r_ilp.solving_time:.2f}s" if r_ilp.is_sat else "TO"
    else:
        t_ilp = "Skipped"

    print(f"{n:>4} | {t_sat1:>11.3f}s | {t_sat2:>11.3f}s | {t_cp:>11.3f}s | {t_ilp:>12}")
