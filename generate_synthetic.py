import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import random
import itertools
import time
import weighted_set_cover as wsc
import sat
import MGM_set_cover as mgm
import generate_synthetic_thesisAlgo as tt

test = [5,10,25,50,100,150,250]
solvers = ['cdl','gc41','g41','m22','maple','lgl']

def generate_graph(numNodes):
    metrics = random.sample(range(1, numNodes*2), numNodes)
    meas_settings = random.sample(range(numNodes*2+1, numNodes*4), numNodes)
    instruments = random.sample(range(numNodes*4+1, numNodes*6), numNodes)
    specifications = random.sample(range(numNodes*6+1, numNodes*8), numNodes)

    e_mc = random.sample(list(itertools.product(metrics,meas_settings)), numNodes*2)
    e_ci = random.sample(list(itertools.product(meas_settings,instruments)), numNodes*2)
    e_is = random.sample(list(itertools.product(instruments,specifications)), numNodes*2)

    # e_mc = []
    # e_ci = []
    # e_is = []
    # for i in range(1,numNodes*2):
    #     m = random.sample(metrics, 1)[0]
    #     c = random.sample(meas_settings, 1)[0]
    #     i = random.sample(instruments, 1)[0]
    #     s = random.sample(specifications, 1)[0]
    #     e_mc.append((m,c))
    #     e_ci.append((c,i))
    #     e_is.append((i,s))

    B = nx.DiGraph()
    B.add_nodes_from(metrics)
    B.add_nodes_from(meas_settings)
    B.add_nodes_from(instruments)
    B.add_nodes_from(specifications)
    B.add_edges_from(e_mc)
    B.add_edges_from(e_ci)
    B.add_edges_from(e_is)

    # color_map = []
    # for node in B:
    #     if node <= numNodes*2:
    #         color_map.append('blue')
    #     elif node > numNodes*2 and node <= numNodes*4: 
    #         color_map.append('green')
    #     elif node > numNodes*4+1 and node <= numNodes*6:
    #         color_map.append('red')
    #     else:
    #         color_map.append('yellow')
    # nx.draw(B, node_color=color_map, with_labels=True)
    # plt.show()

    return B, metrics, meas_settings, instruments, specifications


def experiment_sat(G, formulaG):
    for s in solvers:
        start = time.time()
        sat.solve_sat(formulaG,s)
        end = time.time()
        print("Solver: ", s)
        print(end - start)
    
    start = time.time()
    mgm.correctnessMGM(G,"null","null")
    end = time.time()
    print("HEURISTIC-SAT: ")
    print(end - start)



if __name__ == "__main__":
    
    for n in test:
        # Graph
        # G, m, c, i, s = generate_graph(n)
        G, m, c, i, s = tt.generate_graph(n)

        # Weighted setd from the graph

        # CNF formula from the graph
        formulaG = sat.convert_graph_to_cnf(G, m, c, i, s)

        experiment_sat(G, formulaG)

        print("--------------------")
    