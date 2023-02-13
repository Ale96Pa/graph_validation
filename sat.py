# the standard way to import PySAT:
from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import generate_synthetic as gs
import re

def convert_graph_to_cnf(G, M, C, I, S):
    paths = []
    allP = []
    graph = CNF()
    for m in M:
        all2P = list(nx.all_simple_paths(G, source=m, target=C))
        all3P = list(nx.all_simple_paths(G, source=m, target=I))
        all4P = list(nx.all_simple_paths(G, source=m, target=S))
        for p in all2P:
            allP.append(p)
        for p in all3P:
            allP.append(p)
        for p in all4P:
            allP.append(p)
    for p in allP:
        if p not in paths:
            paths.append(p)
            # pneg = [-(int(''.join(c for c in x if c.isdigit()))) for x in p]
            pneg = [-x for x in p]
            graph.append(pneg)

    return graph.negate()

def solve_sat(cnf, solv_type):
    with Solver(name=solv_type, bootstrap_with=cnf) as solver:
        # # call the solver for this formula:
        # print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

        # # # the formula is satisfiable and so has a model
        # # print('and the model is:', solver.get_model())

        # if not solver.solve():
        #     print('and the unsatisfiable core is:', solver.get_core())
        return solver.solve()

if __name__ == "__main__":
    G, m, c, i, s = gs.generate_graph(3)
    graph_formula = convert_graph_to_cnf(G, m, c, i, s)
    solve_sat(graph_formula, "m22")