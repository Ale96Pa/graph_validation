import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import random
from random import randint
import itertools
import time
import weighted_set_cover as wsc
import min_set_cover as msc
#import sat

import MGM_set_cover as mgm
import generate_synthetic_thesisAlgo as tt
import csv
import tools

import algorithms as algo


test = [0,5,10,25,50,100,150,250,500,1000, 2000, 3000, 4000]
test = [0,5,10]
solvers = ['g41','m22','maple','lgl']

def prepend(list, str):
	str += '{0}'
	list = [str.format(i) for i in list]
	return(list)

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

	#--------------------------#

	metrics = prepend(metrics,'M')
	meas_settings = prepend(meas_settings,'CL')
	instruments = prepend(instruments,'I')
	specifications = prepend(specifications,'S')

	ee_mc = []
	ee_ci = []
	ee_is = []
	for x in e_mc:
		ee_mc.append(('M'+str(x[0]),'CL'+str(x[1])))
	for x in e_ci:
		ee_ci.append(('CL'+str(x[0]),'I'+str(x[1])))
	for x in e_is:
		ee_is.append(('I'+str(x[0]),'S'+str(x[1])))


	MGM = nx.DiGraph()
	MGM.add_nodes_from(metrics, bipartite=0)
	for cl in meas_settings:
		cost = randint(1, 100)
		MGM.add_node(cl, weight=cost, bipartite=1)
	MGM.add_nodes_from(instruments, bipartite=2)
	MGM.add_nodes_from(specifications, bipartite=3)
	MGM.add_edges_from(ee_mc)
	MGM.add_edges_from(ee_ci)
	MGM.add_edges_from(ee_is)


	#--------------------------#

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

	return B, MGM, metrics, meas_settings, instruments, specifications


def init_file(filename,head):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(head)

def experiment_sat(G, MGM_G, formulaG, filename):
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
		r = mgm.correctnessMGM(MGM_G,None,None)
		end = time.time()
		writer.writerow(["mmg",num_nodes,num_edges,end-start,res])
		
def experiment_wsc(G, MGM_G, metrics, set_data, set_cost, filename):
	num_nodes = len(MGM_G.nodes())
	num_edges = len(MGM_G.edges())
	cl = [node for node in MGM_G.nodes() if 'CL' in node]
	
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
		end = time.time()
		
		covCluster	=	[]
		for x in res_set:
			covCluster.append(cl[x])
		tools.printGraph(MGM_G)
		m = tools.getListOfMetricsByClusterList(MGM_G,covCluster)
	
		writer.writerow(["h1",str(len(m)),num_edges,end-start,covCluster, res_w])


		start = time.time()
		listOfMetrics,metricsCovered,clusters,totalCost = algo.minCostMAXSetCover(MGM_G)
		end = time.time()
		writer.writerow(["mmg",str(len(metricsCovered)),num_edges,end-start,clusters, totalCost])

def experiment_msc(G, MGM_G, metrics, set_data, filename):
	num_nodes = len(G.nodes())
	num_edges = len(G.edges())
	
	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)

		start = time.time()
		res_set = msc.min_set_cover(metrics, set_data)
		end = time.time()
		writer.writerow(["msc",num_nodes,num_edges,end-start,"todo1"])

		start = time.time()
		res = tt.MGMminSetCover(MGM_G,None)
		end = time.time()
		writer.writerow(["mmg",num_nodes,num_edges,end-start,"todo2"])



if __name__ == "__main__":

	filesat = 'sat.csv'
	filemsc = "msc.csv"
	filewsc = "wsc.csv"
	init_file(filesat, ["name","nodes","edges","time","results"])
	init_file(filemsc, ["name","nodes","edges","time","results"])
	init_file(filewsc, ["name","nodes","edges","time","result_set","result_w"])
	
	for n in test:
		# Graph
		# G, m, c, i, s = generate_graph(n)
		G, MGM, m, c, i, s = generate_graph(n)

		# CNF formula from the graph
		#formulaG = sat.convert_graph_to_cnf(G, m, c, i, s)
		#experiment_sat(G, formulaG, filesat)

		# Set from the graph
		set_data = tools.getListOfMetricsByCluster(MGM)
		m = [x for x in MGM.nodes if 'M' in x]
		#experiment_msc(G, MGM, m, set_data, filemsc)

		# Weighted set from the graph
		set_cost = tools.getCostClList(MGM)
		experiment_wsc(G, MGM, m, set_data, set_cost, filewsc)
		print(n)

 