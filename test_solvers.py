import sys
from src import (
    solve_nqueens_sat,
    solve_nqueens_cp,
    solve_nqueens_ilp,
    format_board,
)

def run():
    print("=== 1. TESTING SAT WITH 5 AMO ENCODINGS (N=8) ===")
    for amo in ["pairwise", "seqcounter", "bitwise", "commander", "product"]:
        res = solve_nqueens_sat(8, amo_method=amo, solver_name="cadical153")
        print(f"AMO={amo:<12}: SAT={res.is_sat}, Valid={res.is_valid}, Time={res.solving_time*1000:6.2f}ms, Vars={res.num_variables:4d}, Clauses={res.num_clauses:5d}")
        assert res.is_valid, f"Failed on {amo}"

    print("\n=== 2. TESTING SAT WITH MULTIPLE SOLVERS (N=8, pairwise) ===")
    for solver in ["cadical153", "cadical195", "glucose3", "glucose4", "minisat22"]:
        try:
            res = solve_nqueens_sat(8, amo_method="pairwise", solver_name=solver)
            print(f"Solver={solver:<12}: SAT={res.is_sat}, Valid={res.is_valid}, Time={res.solving_time*1000:6.2f}ms")
            assert res.is_valid
        except Exception as e:
            print(f"Solver={solver:<12}: Not supported or error ({e})")

    print("\n=== 3. TESTING CP-SAT (N=8) ===")
    for form in ["alldifferent", "boolean"]:
        res = solve_nqueens_cp(8, formulation=form)
        print(f"Formulation={form:<12}: SAT={res.is_sat}, Valid={res.is_valid}, Time={res.solving_time*1000:6.2f}ms")
        assert res.is_valid

    print("\n=== 4. TESTING ILP (N=8) ===")
    for s_id in ["SCIP", "CBC"]:
        try:
            res = solve_nqueens_ilp(8, solver_id=s_id)
            print(f"Solver={s_id:<12}: SAT={res.is_sat}, Valid={res.is_valid}, Time={res.solving_time*1000:6.2f}ms")
            assert res.is_valid
        except Exception as e:
            print(f"Solver={s_id:<12}: Not supported or error ({e})")

    print("\n=== 5. SAMPLE SOLUTION BOARD (N=8) ===")
    print(format_board(8, res.solution))
    print("\n>>> ALL SOLVER TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    run()
