import math
from typing import List, Tuple
from pysat.card import CardEnc, EncType
from pysat.formula import CNF


def encode_amo_pairwise(lits: List[int], top_id: int) -> Tuple[List[List[int]], int]:
    # Pairwise: for each pair (u, v), add (~u \/ ~v)
    clauses = []
    n = len(lits)
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([-lits[i], -lits[j]])
    return clauses, top_id


def encode_amo_seqcounter(lits: List[int], top_id: int) -> Tuple[List[List[int]], int]:
    # Sequential counter encoding (Sinz 2005)
    if len(lits) <= 1:
        return [], top_id
    cnf = CardEnc.atmost(lits=lits, bound=1, encoding=EncType.seqcounter, top_id=top_id)
    new_top = max(top_id, cnf.nv)
    return cnf.clauses, new_top


def encode_amo_bitwise(lits: List[int], top_id: int) -> Tuple[List[List[int]], int]:
    # Bitwise/binary encoding
    if len(lits) <= 1:
        return [], top_id
    cnf = CardEnc.atmost(lits=lits, bound=1, encoding=EncType.bitwise, top_id=top_id)
    new_top = max(top_id, cnf.nv)
    return cnf.clauses, new_top


def encode_amo_commander(lits: List[int], top_id: int, group_size: int = 3) -> Tuple[List[List[int]], int]:
    # Commander variable encoding (Klieber & Gao 2007)
    if len(lits) <= group_size:
        return encode_amo_pairwise(lits, top_id)

    clauses = []
    curr_id = top_id
    commanders = []
    groups = [lits[i:i + group_size] for i in range(0, len(lits), group_size)]

    for grp in groups:
        if len(grp) == 1:
            commanders.append(grp[0])
            continue
        curr_id += 1
        c = curr_id
        commanders.append(c)

        # At most one in group
        pw, _ = encode_amo_pairwise(grp, curr_id)
        clauses.extend(pw)

        # Literal implies commander
        for x in grp:
            clauses.append([-x, c])

        # Commander implies at least one literal
        clauses.append([-c] + grp)

    # Recursive step on commanders
    rec_clauses, curr_id = encode_amo_commander(commanders, curr_id, group_size)
    clauses.extend(rec_clauses)
    return clauses, curr_id


def encode_amo_product(lits: List[int], top_id: int) -> Tuple[List[List[int]], int]:
    # 2-Product encoding (Chen 2010)
    k = len(lits)
    if k <= 3:
        return encode_amo_pairwise(lits, top_id)

    p = int(math.ceil(math.sqrt(k)))
    q = int(math.ceil(k / p))

    u = [top_id + i + 1 for i in range(p)]
    v = [top_id + p + j + 1 for j in range(q)]
    curr_id = top_id + p + q

    clauses = []
    # AMO on row and col variables
    u_amo, _ = encode_amo_pairwise(u, curr_id)
    v_amo, _ = encode_amo_pairwise(v, curr_id)
    clauses.extend(u_amo)
    clauses.extend(v_amo)

    # Map literals to grid coordinates
    for idx, x in enumerate(lits):
        r = idx // q
        c = idx % q
        clauses.append([-x, u[r]])
        clauses.append([-x, v[c]])

    return clauses, curr_id


def build_nqueens_cnf(n: int, amo_method: str = "pairwise") -> Tuple[CNF, int, int]:
    amo_dispatch = {
        "pairwise": encode_amo_pairwise,
        "seqcounter": encode_amo_seqcounter,
        "bitwise": encode_amo_bitwise,
        "commander": encode_amo_commander,
        "product": encode_amo_product,
    }
    if amo_method not in amo_dispatch:
        raise ValueError(f"Unknown AMO method: {amo_method}. Supported: {list(amo_dispatch.keys())}")

    amo_func = amo_dispatch[amo_method]

    def var_id(r: int, c: int) -> int:
        return r * n + c + 1

    cnf = CNF()
    num_base_vars = n * n
    top_id = num_base_vars

    def add_amo(lits: List[int]):
        nonlocal top_id
        if len(lits) <= 1:
            return
        clauses, new_top = amo_func(lits, top_id)
        top_id = max(top_id, new_top)
        for cl in clauses:
            cnf.append(cl)

    # 1. Row constraints (1 queen per row)
    for r in range(n):
        row_lits = [var_id(r, c) for c in range(n)]
        cnf.append(row_lits)
        add_amo(row_lits)

    # 2. Column constraints (1 queen per column)
    for c in range(n):
        col_lits = [var_id(r, c) for r in range(n)]
        cnf.append(col_lits)
        add_amo(col_lits)

    # 3. Diagonals (falling and rising)
    diags = {}
    anti_diags = {}
    for r in range(n):
        for c in range(n):
            diags.setdefault(r - c, []).append(var_id(r, c))
            anti_diags.setdefault(r + c, []).append(var_id(r, c))

    for d_lits in diags.values():
        if len(d_lits) > 1:
            add_amo(d_lits)

    for ad_lits in anti_diags.values():
        if len(ad_lits) > 1:
            add_amo(ad_lits)

    return cnf, num_base_vars, top_id
