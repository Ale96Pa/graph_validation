import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import random
import itertools
import time

test = [5,10,25,50,100,150]

def generate_graph(numNodes):
    metrics = random.sample(range(0, numNodes*2), numNodes)
    meas_settings = random.sample(range(numNodes*2+1, numNodes*4), numNodes)
    instruments = random.sample(range(numNodes*4+1, numNodes*6), numNodes)
    specifications = random.sample(range(numNodes*6+1, numNodes*8), numNodes)

    e_mc = random.sample(list(itertools.product(metrics,meas_settings)), numNodes*3)
    e_ci = random.sample(list(itertools.product(meas_settings,instruments)), numNodes*3)
    e_is = random.sample(list(itertools.product(instruments,specifications)), numNodes*3)

    B = nx.Graph()
    B.add_nodes_from(metrics, bipartite=0)
    B.add_nodes_from(meas_settings, bipartite=1)
    B.add_nodes_from(instruments, bipartite=2)
    B.add_nodes_from(specifications, bipartite=3)
    B.add_edges_from(e_mc)
    B.add_edges_from(e_ci)
    B.add_edges_from(e_is)

    color_map = []
    for node in B:
        if node <= numNodes:
            color_map.append('blue')
        elif node > numNodes and node <= numNodes*4: 
            color_map.append('green')
        elif node > numNodes*4 and node <= numNodes*6:
            color_map.append('red')
        else:
            color_map.append('yellow')
    nx.draw(B, node_color=color_map, with_labels=True)
    plt.show()    

if __name__ == "__main__":
    
    for n in test:
        start = time.time()
        generate_graph(4)
        end = time.time()
        print(end - start)
    