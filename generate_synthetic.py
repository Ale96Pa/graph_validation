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
import csv
import tools


test = [0,5,10,25,50,100,150,250,500,1000, 2000, 3000, 4000]
solvers = ['g41','m22','maple','lgl']

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


def init_file(filename,head):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(head)

def experiment_sat(G, formulaG, filename):
    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        
        start = time.time()
        result = sat.solve_sat(formulaG,'cdl')
        end = time.time()
        writer.writerow(['cdl',num_nodes,num_edges,end-start,1])

        for s in solvers:
            start = time.time()
            r = sat.solve_sat(formulaG,s)
            end = time.time()
            if r == result: res=1
            else: res=0
            writer.writerow([s,num_nodes,num_edges,end-start,res])
        
        start = time.time()
        r = mgm.correctnessMGM(G,None,None)
        end = time.time()
        if r == result: res=1
        else: res=0
        writer.writerow(["mmg",num_nodes,num_edges,end-start,res])
        
def experiment_wsc(G, metrics, set_data, set_cost, filename):
    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
    
        # set_data_t = []
        # for s in set_data:       
        #     set_data_t.append(set(s))
        # start = time.time()
        # res_set, res_w = wsc.heuristic_0(set(metrics),set_data_t,set_cost)
        # end = time.time()
        # writer.writerow(["h0",num_nodes,num_edges,end-start,res_set, res_w])
        # print("h0")

        start = time.time()
        res_set, res_w = wsc.heuristic_1(set_data,set_cost)
        print(res_set)
        end = time.time()
        writer.writerow(["h1",num_nodes,num_edges,end-start,res_set, res_w])

        start = time.time()
        res= tt.MGMminSetCover(G,None)
        end = time.time()
        # print(res)
        writer.writerow(["mmg",num_nodes,num_edges,end-start,res_set, res_w])


if __name__ == "__main__":

    filesat = 'sat.csv'
    filewsc = "wsc.csv"
    init_file(filesat, ["name","nodes","edges","time","results"])
    init_file(filewsc, ["name","nodes","edges","time","result_set","result_w"])
    
    for n in test:
        # Graph
        # G, m, c, i, s = generate_graph(n)
        G, m, c, i, s = tt.generate_graph(n)

        # # CNF formula from the graph
        # formulaG = sat.convert_graph_to_cnf(G, m, c, i, s)
        # experiment_sat(G, formulaG, filesat)

        # Weighted setd from the graph
        set_data = tools.getListOfMetrics(G)
        set_cost = tools.getCostClList(G)
        experiment_wsc(G, m, set_data, set_cost, filewsc)
        print(n)

    