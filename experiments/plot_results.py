# Plotting scripts for benchmark figures (PDF and PNG)

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# Matplotlib styling for academic publication
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "lines.linewidth": 1.8,
    "lines.markersize": 6,
    "grid.alpha": 0.5,
    "grid.linestyle": "--",
})


def plot_runtime_comparison():
    csv_path = os.path.join(RESULTS_DIR, "benchmark_solvers.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    styles = {
        "SAT (Glucose4)": {"color": "#1f77b4", "marker": "o", "label": "SAT (Glucose4)"},
        "SAT (CaDiCaL)": {"color": "#17becf", "marker": "s", "label": "SAT (CaDiCaL 1.5.3)"},
        "CP-SAT (AllDiff)": {"color": "#2ca02c", "marker": "^", "label": "CP-SAT (AllDifferent)"},
        "CP-SAT (Boolean)": {"color": "#8c564b", "marker": "v", "label": "CP-SAT (Boolean 2D)"},
        "ILP (SCIP)": {"color": "#d62728", "marker": "D", "label": "ILP (SCIP MIP)"},
    }

    for method, style in styles.items():
        sub = df[df["Method"] == method]
        ax.plot(
            sub["N"],
            sub["Time_s"],
            color=style["color"],
            marker=style["marker"],
            label=style["label"],
        )

    # Add timeout line
    ax.axhline(y=20.0, color="#d62728", linestyle=":", linewidth=1.5, alpha=0.8)
    ax.text(65, 22.0, "Timeout threshold (20s)", color="#d62728", fontsize=9, style="italic")

    ax.set_yscale("log")
    ax.set_xlabel("Board Dimension ($N$)")
    ax.set_ylabel("Solving Time (seconds, log scale)")
    ax.set_title("Runtime Comparison across Solving Paradigms (SAT vs CP vs ILP)")
    ax.grid(True, which="both")
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()

    out_png = os.path.join(RESULTS_DIR, "fig1_runtime_comparison.png")
    out_pdf = os.path.join(RESULTS_DIR, "fig1_runtime_comparison.pdf")
    fig.savefig(out_png)
    fig.savefig(out_pdf)
    plt.close(fig)
    print(f"[OK] Generated Fig 1: {out_png}")


def plot_clause_growth():
    csv_path = os.path.join(RESULTS_DIR, "benchmark_amo.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    styles = {
        "pairwise": {"color": "#d62728", "marker": "o", "label": "Pairwise ($O(N^3)$ clauses)"},
        "bitwise": {"color": "#ff7f0e", "marker": "s", "label": "Bitwise / Binary"},
        "commander": {"color": "#9467bd", "marker": "^", "label": "Commander Variable"},
        "seqcounter": {"color": "#2ca02c", "marker": "D", "label": "Sequential Counter (Sinz)"},
        "product": {"color": "#1f77b4", "marker": "*", "label": "2-Product (Chen)"},
    }

    for amo, style in styles.items():
        sub = df[df["AMO_Method"] == amo]
        ax.plot(
            sub["N"],
            sub["Num_Clauses"],
            color=style["color"],
            marker=style["marker"],
            label=style["label"],
        )

    # Highlight clause reduction at N=100
    pw_100 = df[(df["N"] == 100) & (df["AMO_Method"] == "pairwise")]["Num_Clauses"].values[0]
    prod_100 = df[(df["N"] == 100) & (df["AMO_Method"] == "product")]["Num_Clauses"].values[0]
    reduction = (pw_100 - prod_100) / pw_100 * 100

    ax.annotate(
        f"Pairwise: {pw_100:,} clauses\nProduct: {prod_100:,} clauses\n(-{reduction:.1f}% reduction)",
        xy=(100, pw_100),
        xytext=(55, 600000),
        arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=6),
        bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.3),
        fontsize=9,
    )

    ax.set_yscale("log")
    ax.set_xlabel("Board Dimension ($N$)")
    ax.set_ylabel("Number of Generated Clauses (log scale)")
    ax.set_title("Formula Complexity Comparison across AMO Encodings")
    ax.grid(True, which="both")
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()

    out_png = os.path.join(RESULTS_DIR, "fig2_clause_growth.png")
    out_pdf = os.path.join(RESULTS_DIR, "fig2_clause_growth.pdf")
    fig.savefig(out_png)
    fig.savefig(out_pdf)
    plt.close(fig)
    print(f"[OK] Generated Fig 2: {out_png}")


def plot_amo_runtime():
    csv_path = os.path.join(RESULTS_DIR, "benchmark_amo.csv")
    if not os.path.exists(csv_path):
        return

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    styles = {
        "pairwise": {"color": "#d62728", "marker": "o", "label": "Pairwise"},
        "bitwise": {"color": "#ff7f0e", "marker": "s", "label": "Bitwise / Binary"},
        "commander": {"color": "#9467bd", "marker": "^", "label": "Commander Variable"},
        "seqcounter": {"color": "#2ca02c", "marker": "D", "label": "Sequential Counter"},
        "product": {"color": "#1f77b4", "marker": "*", "label": "2-Product"},
    }

    for amo, style in styles.items():
        sub = df[df["AMO_Method"] == amo]
        ax.plot(
            sub["N"],
            sub["Total_Time_s"],
            color=style["color"],
            marker=style["marker"],
            label=style["label"],
        )

    ax.set_yscale("log")
    ax.set_xlabel("Board Dimension ($N$)")
    ax.set_ylabel("Total Execution Time (s, log scale)")
    ax.set_title("End-to-End Runtime across 5 AMO Encodings (PySAT Glucose4)")
    ax.grid(True, which="both")
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()

    out_png = os.path.join(RESULTS_DIR, "fig3_amo_runtime.png")
    out_pdf = os.path.join(RESULTS_DIR, "fig3_amo_runtime.pdf")
    fig.savefig(out_png)
    fig.savefig(out_pdf)
    plt.close(fig)
    print(f"[OK] Generated Fig 3: {out_png}")


if __name__ == "__main__":
    plot_runtime_comparison()
    plot_clause_growth()
    plot_amo_runtime()
    print(">>> ALL FIGURES GENERATED SUCCESSFULLY! <<<")
