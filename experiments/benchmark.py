# Benchmark script for N-Queens solvers (SAT, CP-SAT, ILP) and AMO encodings.

import os
import sys
import time
import pandas as pd

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import (
    solve_nqueens_sat,
    solve_nqueens_cp,
    solve_nqueens_ilp,
    build_nqueens_cnf,
)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_solver_comparison():
    print("=" * 70)
    print("EXPERIMENT 1: Cross-Paradigm Solver Comparison (SAT vs CP vs ILP)")
    print("=" * 70)

    n_values = [4, 8, 12, 16, 24, 32, 40, 50, 64, 80, 100]
    records = []

    for n in n_values:
        print(f"\n>>> Benchmarking N = {n} (board {n}x{n} = {n*n} cells)...")

        # 1. SAT - Glucose4 (Pairwise)
        r_glu = solve_nqueens_sat(n, amo_method="pairwise", solver_name="glucose4")
        print(f"  [SAT Glucose4]  Time={r_glu.solving_time:.4f}s, SAT={r_glu.is_sat}, Valid={r_glu.is_valid}")
        records.append({
            "N": n,
            "Method": "SAT (Glucose4)",
            "Paradigm": "SAT",
            "Time_s": r_glu.solving_time,
            "SAT": r_glu.is_sat,
            "Valid": r_glu.is_valid,
            "Variables": r_glu.num_variables,
            "Constraints": r_glu.num_clauses,
        })

        # 2. SAT - CaDiCaL 1.5.3 (Pairwise)
        r_cad = solve_nqueens_sat(n, amo_method="pairwise", solver_name="cadical153")
        print(f"  [SAT CaDiCaL]   Time={r_cad.solving_time:.4f}s, SAT={r_cad.is_sat}, Valid={r_cad.is_valid}")
        records.append({
            "N": n,
            "Method": "SAT (CaDiCaL)",
            "Paradigm": "SAT",
            "Time_s": r_cad.solving_time,
            "SAT": r_cad.is_sat,
            "Valid": r_cad.is_valid,
            "Variables": r_cad.num_variables,
            "Constraints": r_cad.num_clauses,
        })

        # 3. CP-SAT AllDifferent
        r_cp_diff = solve_nqueens_cp(n, formulation="alldifferent")
        print(f"  [CP-SAT AllDiff] Time={r_cp_diff.solving_time:.4f}s, SAT={r_cp_diff.is_sat}, Valid={r_cp_diff.is_valid}")
        records.append({
            "N": n,
            "Method": "CP-SAT (AllDiff)",
            "Paradigm": "CP",
            "Time_s": r_cp_diff.solving_time,
            "SAT": r_cp_diff.is_sat,
            "Valid": r_cp_diff.is_valid,
            "Variables": r_cp_diff.num_variables,
            "Constraints": r_cp_diff.num_clauses,
        })

        # 4. CP-SAT Boolean 2D
        r_cp_bool = solve_nqueens_cp(n, formulation="boolean")
        print(f"  [CP-SAT Boolean] Time={r_cp_bool.solving_time:.4f}s, SAT={r_cp_bool.is_sat}, Valid={r_cp_bool.is_valid}")
        records.append({
            "N": n,
            "Method": "CP-SAT (Boolean)",
            "Paradigm": "CP",
            "Time_s": r_cp_bool.solving_time,
            "SAT": r_cp_bool.is_sat,
            "Valid": r_cp_bool.is_valid,
            "Variables": r_cp_bool.num_variables,
            "Constraints": r_cp_bool.num_clauses,
        })

        # 5. ILP - SCIP (Timeout 20s)
        r_ilp = solve_nqueens_ilp(n, solver_id="SCIP", time_limit_sec=20.0)
        status_str = f"Time={r_ilp.solving_time:.4f}s" if r_ilp.is_sat else "TIMEOUT (>20s)"
        print(f"  [ILP SCIP]      {status_str}, SAT={r_ilp.is_sat}, Valid={r_ilp.is_valid}")
        records.append({
            "N": n,
            "Method": "ILP (SCIP)",
            "Paradigm": "ILP",
            "Time_s": r_ilp.solving_time if r_ilp.is_sat else 20.0,
            "SAT": r_ilp.is_sat,
            "Valid": r_ilp.is_valid,
            "Variables": r_ilp.num_variables,
            "Constraints": r_ilp.num_clauses,
        })

    df = pd.DataFrame(records)
    csv_path = os.path.join(RESULTS_DIR, "benchmark_solvers.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[OK] Saved solver comparison to: {csv_path}")

    # Generate LaTeX Table
    pivot_time = df.pivot(index="N", columns="Method", values="Time_s")
    tex_path = os.path.join(RESULTS_DIR, "table_solvers.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Table: Solving time comparison (seconds)\n")
        f.write("\\begin{tabular}{r|rrrrr}\n\\hline\n")
        f.write("$N$ & SAT (Glucose4) & SAT (CaDiCaL) & CP-SAT (AllDiff) & CP-SAT (Boolean) & ILP (SCIP) \\\\\n\\hline\n")
        for n in n_values:
            row = pivot_time.loc[n]
            scip_str = f"{row['ILP (SCIP)']:.3f}" if row["ILP (SCIP)"] < 20.0 else "TO (20s)"
            f.write(f"{n:>4} & {row['SAT (Glucose4)']:>10.4f} & {row['SAT (CaDiCaL)']:>10.4f} & {row['CP-SAT (AllDiff)']:>10.4f} & {row['CP-SAT (Boolean)']:>10.4f} & {scip_str:>10} \\\\\n")
        f.write("\\hline\n\\end{tabular}\n")
    print(f"[OK] Generated LaTeX table: {tex_path}")


def run_amo_ablation():
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: Ablation Study of 5 AMO Encodings")
    print("=" * 70)

    n_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    amo_methods = ["pairwise", "seqcounter", "bitwise", "commander", "product"]
    records = []

    for n in n_values:
        print(f"\n>>> Benchmarking AMO encodings for N = {n}...")
        for amo in amo_methods:
            # Measure encoding time
            t0_enc = time.perf_counter()
            cnf, n_base, n_total = build_nqueens_cnf(n, amo_method=amo)
            t_enc = time.perf_counter() - t0_enc

            # Measure solve time with Glucose4
            res = solve_nqueens_sat(n, amo_method=amo, solver_name="glucose4")

            num_clauses = len(cnf.clauses)
            aux_vars = n_total - n_base

            print(f"  {amo:<12}: Clauses={num_clauses:>9,}, AuxVars={aux_vars:>6,}, SolveTime={res.solving_time:>7.4f}s, Valid={res.is_valid}")
            records.append({
                "N": n,
                "AMO_Method": amo,
                "Base_Vars": n_base,
                "Aux_Vars": aux_vars,
                "Total_Vars": n_total,
                "Num_Clauses": num_clauses,
                "Encoding_Time_s": t_enc,
                "Solving_Time_s": res.solving_time,
                "Total_Time_s": t_enc + res.solving_time,
                "Valid": res.is_valid,
            })

    df = pd.DataFrame(records)
    csv_path = os.path.join(RESULTS_DIR, "benchmark_amo.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[OK] Saved AMO ablation to: {csv_path}")

    # Generate LaTeX Table for Clauses and Vars
    tex_path = os.path.join(RESULTS_DIR, "table_amo.tex")
    pivot_clauses = df.pivot(index="N", columns="AMO_Method", values="Num_Clauses")
    pivot_time = df.pivot(index="N", columns="AMO_Method", values="Total_Time_s")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Table: Formula Size and Runtime across AMO Encodings\n")
        f.write("\\begin{tabular}{r|rrrrr|rrrrr}\n\\hline\n")
        f.write(" & \\multicolumn{5}{c|}{Number of Clauses} & \\multicolumn{5}{c}{Total Runtime (s)} \\\\\n")
        f.write("$N$ & Pairwise & SeqCounter & Bitwise & Commander & Product & Pairwise & SeqCounter & Bitwise & Commander & Product \\\\\n\\hline\n")
        for n in n_values:
            cl = pivot_clauses.loc[n]
            tm = pivot_time.loc[n]
            f.write(f"{n:>3} & {int(cl['pairwise']):>9} & {int(cl['seqcounter']):>9} & {int(cl['bitwise']):>9} & {int(cl['commander']):>9} & {int(cl['product']):>9} & ")
            f.write(f"{tm['pairwise']:>8.3f} & {tm['seqcounter']:>8.3f} & {tm['bitwise']:>8.3f} & {tm['commander']:>8.3f} & {tm['product']:>8.3f} \\\\\n")
        f.write("\\hline\n\\end{tabular}\n")
    print(f"[OK] Generated LaTeX table: {tex_path}")


if __name__ == "__main__":
    t_start = time.time()
    run_solver_comparison()
    run_amo_ablation()
    print("\n" + "=" * 70)
    print(f">>> ALL BENCHMARKS COMPLETED IN {time.time() - t_start:.2f} SECONDS! <<<")
    print("=" * 70)
