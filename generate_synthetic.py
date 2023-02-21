import csv
import tools
import itertools
import time
import random
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

import sat
import min_set_cover as msc
import weighted_set_cover as wsc

test = [0,5,10,25,50,100,150,250,500,1000,2000,3000]
# test = [5,10]
# test = [2000,2005,2010,2020,2030,2050,2060,2100,2150,2200]
solvers = ['g41','m22','maple','lgl']

def init_file(filename,head):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(head)

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

	B = nx.DiGraph()
	B.add_nodes_from(metrics)
	B.add_nodes_from(meas_settings)
	B.add_nodes_from(instruments)
	B.add_nodes_from(specifications)
	B.add_edges_from(e_mc)
	B.add_edges_from(e_ci)
	B.add_edges_from(e_is)

	#--------------------------#

	metrics2 = prepend(metrics,'M')
	meas_settings2 = prepend(meas_settings,'CL')
	instruments2 = prepend(instruments,'I')
	specifications2 = prepend(specifications,'S')

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
	MGM.add_nodes_from(metrics2)
	for cl in meas_settings2:
		cost = randint(1, 100)
		MGM.add_node(cl, weight=cost)
	MGM.add_nodes_from(instruments2)
	MGM.add_nodes_from(specifications2)
	MGM.add_edges_from(ee_mc)
	MGM.add_edges_from(ee_ci)
	MGM.add_edges_from(ee_is)

	return B, MGM, metrics2, metrics, meas_settings, instruments, specifications


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
		res_mgm = sat.metrics_deployability(MGM_G) #TODO: verificare correttezza
		end = time.time()
		if res_mgm == result: res=1
		else: res=0
		writer.writerow(["MMG",num_nodes,num_edges,end-start,res])

def experiment_msc(G, MGM_G, metrics, set_data, filename):
	num_nodes = len(G.nodes())
	num_edges = len(G.edges())
	
	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)

		start = time.time()
		res_msc = msc.min_set_cover(metrics, set_data)
		end = time.time()
		writer.writerow(["Optimal result",num_nodes,num_edges,end-start,len(res_msc)])

		time_perf, res =  msc.exeMinSetCoverV2(MGM_G,None)
		writer.writerow(["MMG",num_nodes,num_edges,time_perf,len(res)])


def experiment_wsc(MGM_G, metrics, set_data, set_cost, filename):
	num_nodes = len(MGM_G.nodes())
	num_edges = len(MGM_G.edges())
	cl = [node for node in MGM_G.nodes() if 'CL' in node]

	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)

		# dic_set = {}
		# dic_cost = {}
		# for i in range(0,len(set_data)):
		# 	dic_set["S"+str(i+1)] = set_data[i]
		# 	dic_cost["S"+str(i+1)] = set_cost[i]

		# start = time.perf_counter()
		# res_opt = wsc.heuristic_0(metrics,dic_set,dic_cost)
		# res_w = 0
		# end = time.perf_counter()
		# writer.writerow(["Optimal result",num_nodes,num_edges,end-start,res_opt,res_w])
		# print(res_opt)

		start = time.perf_counter()
		res_set, res_w = wsc.heuristic_1(set_data,set_cost)
		end = time.perf_counter()
		
		covCluster	=	[]
		for x in res_set:
			covCluster.append(cl[x])
		m = tools.getListOfMetricsByClusterList(MGM_G,covCluster)
		writer.writerow(["SoA heuristic",num_nodes,num_edges,end-start,len(covCluster),res_w])
		

		start = time.perf_counter()
		clusters, totalCost = wsc.minCostMAXSetCover_fast(MGM_G)
		end = time.perf_counter()
		writer.writerow(["MMG",num_nodes,num_edges,end-start,len(clusters),totalCost])



if __name__ == "__main__":

	filesat = 'sat.csv'
	filemsc = "msc.csv"
	filewsc = "wsc.csv"
	init_file(filesat, ["name","nodes","edges","time","results"])
	init_file(filemsc, ["name","nodes","edges","time","results"])
	init_file(filewsc, ["name","nodes","edges","time","result_set","result_w"])
	
	for n in test:
		G, MGM, m_label, m, c, i, s = generate_graph(n)

		# nx.draw(G, with_labels = True)
		# plt.show()

		# nx.draw(MGM, with_labels = True)
		# plt.show()

		# CNF formula from the graph
		formulaG = sat.convert_graph_to_cnf(G, m, c, i, s)
		experiment_sat(G, MGM, formulaG, filesat)
		
		# Set from the graph
		set_data = tools.getListOfMetricsByCluster(MGM)
		m = [x for x in MGM.nodes if 'M' in x]
		experiment_msc(G, MGM, m, set_data, filemsc)

		# Weighted set from the graph
		set_cost = tools.getCostClList(MGM)
		experiment_wsc(MGM, m, set_data, set_cost, filewsc)
		print(n, "------------------")

 