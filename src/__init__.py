"""
N-Queens Solvers Package for Advanced Computer Science Assignment.
Includes SAT, CP-SAT, and ILP solvers with multiple encodings.
"""

from src.utils import SolverResult, is_valid_nqueens_solution, format_board
from src.sat_encodings import build_nqueens_cnf
from src.sat_solver import solve_nqueens_sat
from src.cp_solver import solve_nqueens_cp
from src.ilp_solver import solve_nqueens_ilp

__all__ = [
    "SolverResult",
    "is_valid_nqueens_solution",
    "format_board",
    "build_nqueens_cnf",
    "solve_nqueens_sat",
    "solve_nqueens_cp",
    "solve_nqueens_ilp",
]
