# N-Queens Problem: Exact Solving with SAT, CP, and ILP

Author: Le Trung Hieu (Student ID: 24021475)  
Faculty of Information Technology, VNU University of Engineering and Technology (VNU-UET)  
Course: Modern Issues in Computer Science (HK I, 2026-2027)  
Email: 24021475@vnu.edu.vn  

---

## Introduction

This repository contains the source code, experimental benchmarks, and scientific paper for Assignment 1. The project investigates exact solving approaches for the generalized N-Queens problem on board sizes up to N = 100 (10,000 Boolean decision variables).

We evaluate three exact combinatorial paradigms:
- SAT Solving (PySAT): CDCL backends including MiniSat 2.2, CaDiCaL 1.5.3, Glucose 3.0, and Glucose 4.0 across five At-Most-One (AMO) cardinality encodings.
- Constraint Programming (Google OR-Tools CP-SAT): Both 1D integer formulation with global AllDifferent constraints and 2D Boolean grid formulation.
- Integer Linear Programming (Google OR-Tools SCIP / CBC): 0-1 binary formulation solved via Branch-and-Bound and LP relaxations.

---

## Implemented AMO Encodings

Five At-Most-One encodings are implemented in `src/sat_encodings.py`:
1. Pairwise: Direct quadratic baseline without auxiliary variables.
2. Sequential Counter (Sinz 2005): Linear clause complexity using k - 1 accumulator variables.
3. Bitwise (Binary): Logarithmic auxiliary variables encoding the binary index of the active literal.
4. Commander Variable (Klieber & Gao 2007): Disjoint group partitioning (group size g = 3) with recursive commander trees.
5. 2-Product (Chen 2010): Square matrix coordinate mapping (p x q), producing 2k + O(sqrt(k)) clauses and 2*sqrt(k) auxiliary variables. For short lines (k <= 3), the implementation falls back to pairwise clauses.

---

## Key Experimental Results

- Scalability: SAT solvers (Glucose 4.0: 2.77s, CaDiCaL: 4.03s) and CP-SAT (1.29s) solve N = 100 within a few seconds. All returned board placements are verified by an independent O(N^2) validator.
- ILP Breakdown: SCIP solves small to medium instances but hits the 20-second timeout at N = 100. Because the uniform fractional assignment x_{r,c} = 1/N satisfies all row, column, and diagonal constraints with zero violation and zero objective cost, the LP relaxation provides no dual bounding cutoffs to prune the Branch-and-Bound search tree.
- Formula Size: At N = 100, the Pairwise encoding requires 1,646,900 clauses (~185 MB memory in PySAT), while 2-Product requires only 116,636 clauses (~14 MB memory), representing a 92.9% reduction in clause count.

---

## Project Structure

```text
├── src/
│   ├── sat_encodings.py         # 5 AMO encodings and CNF generator
│   ├── sat_solver.py            # PySAT wrapper and solution decoder
│   ├── cp_solver.py             # OR-Tools CP-SAT solvers (1D and 2D)
│   ├── ilp_solver.py            # OR-Tools MIP solver (SCIP / CBC)
│   └── utils.py                 # Solution verifier and ASCII board printer
├── experiments/
│   ├── benchmark.py             # Automated benchmark runner across N in [4, 100]
│   ├── plot_results.py          # Script generating figures (PDF / PNG, 300 DPI)
│   └── results/                 # Raw CSV benchmark outputs and LaTeX tables
├── paper/
│   ├── main.tex                 # Elsevier cas-sc LaTeX manuscript
│   ├── references.bib           # BibTeX references
│   ├── cas-sc.cls               # Elsevier single-column class
│   ├── cas-common.sty           # Style package
│   ├── cas-model2-names.bst     # Bibliography style
│   └── figures/                 # Vector PDF figures included in the paper
├── Bai_Bao_BTL_LeTrungHieu_24021475.pdf  # Compiled 9-page research paper
├── test_solvers.py              # Unit tests for all solvers and encodings (N = 8)
├── test_scale.py                # Quick scaling check up to N = 100
├── run_n100.py                  # Standalone solver demonstration on 100x100 board
├── requirements.txt             # Python dependencies
└── README.md
```

---

## Setup and Usage

### Prerequisites
Python 3.10 or later with dependencies:
```bash
pip install python-sat ortools matplotlib pandas numpy
```

### Running Tests
Verify all five AMO encodings, multiple SAT solvers, CP-SAT, and ILP on N = 8:
```bash
python test_solvers.py
```

### Solve N = 100 Directly
```bash
python run_n100.py
```

### Reproduce Benchmarks and Figures
```bash
python experiments/benchmark.py
python experiments/plot_results.py
```

---

## Paper

The paper is typeset using Elsevier's official `cas-sc` (single-column) template:
- Compiled PDF: `Bai_Bao_BTL_LeTrungHieu_24021475.pdf` (9 pages)
- LaTeX source: `paper/main.tex`

---

## References

1. C. Sinz, "Towards an optimal CNF encoding of boolean cardinality constraints," in CP 2005, LNCS 3709, pp. 827-831, 2005.
2. W. Klieber and L. Gao, "A new efficient SAT encoding for at-most-one constraints," in SAT 2007 Workshops, 2007.
3. J. Chen, "A new SAT encoding of the at-most-one constraint," in ISORA 2011, pp. 207-215, 2010.
4. A. Ignatiev, A. Morgado, and J. Marques-Silva, "PySAT: A Python toolkit for prototyping with SAT oracles," in SAT 2018, LNCS 10929, pp. 428-437, 2018.
5. A. Biere, M. Heule, H. van Maaren, and T. Walsh (Eds.), Handbook of Satisfiability, 2nd ed., IOS Press, 2021.
