import time
from src.sat_solver import solve_nqueens_sat
from src.cp_solver import solve_nqueens_cp

print("=== GIAI N = 100 TREN BAN CO 100x100 ===")

print("\n1. Chay SAT Solver (Glucose4 + Pairwise)...")
t0 = time.time()
res_sat = solve_nqueens_sat(100, amo_method="pairwise", solver_name="glucose4")
t_sat = time.time() - t0

print(f"-> KET QUA SAT: Thanh cong trong {t_sat:.2f} giay!")
print(f"   SAT status: {res_sat.is_sat}")
print(f"   Kiem tra hop le (no attack): {res_sat.is_valid}")
print(f"   So bien logic: {res_sat.num_variables:,}")
print(f"   So menh de (clauses): {res_sat.num_clauses:,}")
print(f"   Vi tri 100 con Hau tren 100 hang (solution):")
print(res_sat.solution)

print("\n2. Chay CP-SAT Solver (Google OR-Tools AllDifferent)...")
t0 = time.time()
res_cp = solve_nqueens_cp(100, formulation="alldifferent")
t_cp = time.time() - t0

print(f"-> KET QUA CP-SAT: Thanh cong trong {t_cp:.2f} giay!")
print(f"   CP status: {res_cp.is_sat}")
print(f"   Kiem tra hop le (no attack): {res_cp.is_valid}")
print(f"   Vi tri 100 con Hau tren 100 hang (solution):")
print(res_cp.solution)
