from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx

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
            pneg = [-x for x in p]
            graph.append(pneg)

    return graph.negate()

def solve_sat(cnf, solv_type):
    with Solver(name=solv_type, bootstrap_with=cnf) as solver:
        return not solver.solve()
    

# TODO: controllare correttezza
def metrics_deployability(MGM):
    wrongCL = set()
    wrongIN = set()
    vIN = [node for node in MGM.nodes() if 'I' in node]
    vM	= [node for node in MGM.nodes() if 'M' in node]
    vCL = [node for node in MGM.nodes() if 'CL' in node]

    for inp in vIN:
        if MGM.out_degree(inp) == 0:
            wrongIN = wrongIN.union({inp})
            wrongCL = wrongCL.union(set([edge[0] for edge in MGM.in_edges(inp) ]))

    for wrong in wrongIN:
        MGM.remove_node(wrong)
    for wrong in wrongCL:
        MGM.remove_node(wrong)

    for mt in vM:
        if MGM.out_degree(mt) == 0:
            MGM.remove_node(mt)
            # TODO: almeno una metrica non è implementabile
            return 0
    
    for cl in vCL:
        if MGM.in_degree(cl) == 0:
            MGM.remove_node(cl)
    return 1