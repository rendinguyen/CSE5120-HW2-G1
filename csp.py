"""Executable CSP formulations. Coordinates and time slots are integers."""


def knight_domains(n, k):
    """TODO K1: {K0: [(0,0),...], ..., K{k-1}: [...]} in row-major order.

    n >= 1, 0 <= k <= n*n. Each knight's domain is every board cell. For k=0,
    return {}. Reject other n/k values with ValueError. No knight solver needed.
    """
    raise NotImplementedError("Complete knight_domains")


def knights_consistent(assignment, n, k):
    """TODO K2: bool for a PARTIAL mapping of knight names to (row,col).

    Check names/domains, different cells, and no knight attack: absolute
    coordinate differences may not be (1,2) or (2,1). {} is consistent.
    Invalid n/k or malformed/out-of-domain assignments return False.
    """
    raise NotImplementedError("Complete knights_consistent")


def vehicle_domains():
    """TODO V1: unary-filtered domains for A..E, as lists of (stop, slot).

    A/B/C use CGI, D/E use JB. Slots 1..4. A <= 2, B == 1, D >= 3.
    Do not propagate binary constraints into the returned domains.
    """
    raise NotImplementedError("Complete vehicle_domains")


def vehicles_consistent(assignment):
    """TODO V2: bool for a partial assignment. Check domains and binary rules.

    D.slot < C.slot; same-stop vehicles cannot share a slot. Across different
    stops a shared slot is allowed. Missing variables are unassigned, not bad.
    """
    raise NotImplementedError("Complete vehicles_consistent")


def constraint_edges():
    """TODO V3: undirected graph as alphabetized (smaller_name,larger_name) pairs.

    Return one edge for each nontrivial BINARY constraint in the formulation
    before inference, no self-edges, duplicates, or unary-domain edges.
    """
    raise NotImplementedError("Complete constraint_edges")


def solve_vehicles():
    """TODO V4: list of ALL complete valid assignment dictionaries, no duplicates.

    Write a general backtracking/enumeration procedure using vehicle_domains
    and vehicles_consistent. Do not hard-code solutions. Order is not graded.
    """
    raise NotImplementedError("Complete solve_vehicles")
