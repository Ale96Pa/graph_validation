# the standard way to import PySAT:
from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import generate_synthetic as gs

def convert_graph_to_cnf(G, M, S):
    paths = []
    neg_paths = []
    for m in M:
        for s in S:
            allP = list(nx.all_simple_paths(G, source=m, target=s, cutoff=4))
            for p in allP:
                if p not in paths:
                    paths.append(p)
                    pneg = [ -x for x in p]
                    neg_paths.append(pneg)
                    pos = CNF(from_clauses=[pneg])
                    neg = pos.negate()
    # print(paths)
    print(neg_paths)

def foo():
    # create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
    cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

    # create a SAT solver for this formula:
    with Solver(bootstrap_with=cnf) as solver:
        # 1.1 call the solver for this formula:
        print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

        # 1.2 the formula is satisfiable and so has a model:
        print('and the model is:', solver.get_model())

        # 2.1 apply the MiniSat-like assumption interface:
        print('formula is',
            f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
            'assuming x1 and x2')

        # 2.2 the formula is unsatisfiable,
        # i.e. an unsatisfiable core can be extracted:
        print('and the unsatisfiable core is:', solver.get_core())

if __name__ == "__main__":
    G, m, s = gs.generate_graph(5)
    convert_graph_to_cnf(G, m, s)