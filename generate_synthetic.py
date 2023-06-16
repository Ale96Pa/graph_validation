import csv
import tools
import itertools
import time
import random
import networkx as nx
import numpy as np

import sat
import min_set_cover as msc
import weighted_set_cover as wsc

test = [5,10,25,50,100,150,250,500,1000,2000]
testmsc = range(2,32,2)
testwsc = [1000,1005,1010,1020,1030,1050,1060,1100,1150]
solvers = ['g41','lgl','m22','maple']
cost_distro = ["binomial","poisson","geometric","normal"]#,"triangular"]
topologies = ["random","onepath","complete"]
num_experiment = 30

def init_file(filename,head):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(head)

def prepend(list, str):
	str += '{0}'
	list = [str.format(i) for i in list]
	return(list)

def generate_graph(numNodes, distro="random", topology="random"):
	metrics = random.sample(range(1, numNodes*2), numNodes)
	meas_settings = random.sample(range(numNodes*2+1, numNodes*4), numNodes)
	instruments = random.sample(range(numNodes*4+1, numNodes*6), numNodes)
	specifications = random.sample(range(numNodes*6+1, numNodes*8), numNodes)

	e_mc=[]
	e_ci=[]
	e_is=[]
	## Random graph
	if topology == "random":
		e_mc = random.sample(list(itertools.product(metrics,meas_settings)), numNodes*2)
		e_ci = random.sample(list(itertools.product(meas_settings,instruments)), numNodes*2)
		e_is = random.sample(list(itertools.product(instruments,specifications)), numNodes*2)
	## Line shape graph
	elif topology == "onepath":
		for i in range(0,numNodes):
			e_mc.append([metrics[i],meas_settings[i]])
			e_ci.append([meas_settings[i],instruments[i]])
			e_is.append([instruments[i],specifications[i]])
	## Complete graph
	elif topology == "complete":
		for i in range(0,numNodes):
			for j in range(0,numNodes):
				e_mc.append([metrics[i],meas_settings[j]])
				e_ci.append([meas_settings[i],instruments[j]])
				e_is.append([instruments[i],specifications[j]])

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

	if distro == "normal":
		# randomNums = np.random.normal(scale=numNodes, size=len(meas_settings2))
		randomNums = np.random.normal(loc=len(meas_settings2)/2, scale=len(meas_settings2)/4, size=len(meas_settings2))
	elif distro == "lognormal":
		randomNums = np.random.lognormal(size=len(meas_settings2))
	elif distro == "binomial":
		randomNums = np.random.binomial(numNodes, 0.5, size=len(meas_settings2))
	elif distro == "poisson":
		randomNums = np.random.poisson(numNodes,size=len(meas_settings2))
	elif distro == "uniform":
		randomNums = np.random.randint(1, len(meas_settings2), size=len(meas_settings2))
	elif distro == "geometric":
		randomNums = np.random.geometric(0.5, size=len(meas_settings2))
	elif distro == "stdnormal":
		randomNums = np.random.standard_normal(size=len(meas_settings2))
	elif distro == "stdgamma":
		randomNums = np.random.standard_gamma(len(meas_settings2)/2, size=len(meas_settings2))
	elif distro == "triangular":
		randomNums = np.random.triangular(1, len(meas_settings2)/2 ,len(meas_settings2), size=len(meas_settings2))
	else:
		randomNums = np.random.randint(1, 100, size=len(meas_settings2))
	
	MGM = nx.DiGraph()
	MGM.add_nodes_from(metrics2)
	i=0
	for cl in meas_settings2:
		cost = randomNums[i]
		#cost = randomInts[i]
		MGM.add_node(cl, weight=cost)
		i+=1
	MGM.add_nodes_from(instruments2)
	MGM.add_nodes_from(specifications2)
	MGM.add_edges_from(ee_mc)
	MGM.add_edges_from(ee_ci)
	MGM.add_edges_from(ee_is)

	return B, MGM, metrics2, metrics, meas_settings, instruments, specifications


def experiment_sat(G, MGM_G, filename):
	num_nodes = len(G.nodes())
	num_edges = len(G.edges())
	density = nx.density(G)
	
	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)
		
		start1 = time.perf_counter()
		result_paths = sat.solve_sat(MGM_G)
		end1 = time.perf_counter()
		writer.writerow(['path_gen',num_nodes,num_edges,density,end1-start1,len(result_paths)])

		# for s in solvers:
		# 	start = time.time()
		# 	r = sat.solve_sat(formulaG,s)
		# 	end = time.time()
		# 	if r == result: res=1
		# 	else: res=0
		# 	writer.writerow([s,num_nodes,num_edges,density,end-start,res])
		
		start2 = time.perf_counter()
		res_mgm = sat.metrics_deployability(MGM_G)
		end2 = time.perf_counter()
		writer.writerow(["MMG",num_nodes,num_edges,density,end2-start2,len(res_mgm)])

def experiment_msc(G, MGM_G, metrics, set_data, filename):
	num_nodes = len(G.nodes())
	num_edges = len(G.edges())
	density = nx.density(G)
	
	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)

		a=[]
		for elem in set_data:
			a.append(set(elem))

		start = time.time()
		res_msc = msc.setCover(a)
		end = time.time()
		res_msc = set([item for sublist in res_msc for item in sublist])
		writer.writerow(["Set Cover",num_nodes,num_edges,density,end-start,len(res_msc)])

		start = time.time()
		res_msc_opt = msc.greedyMinSetCover(frozenset(metrics), a)
		end = time.time()
		res_msc_opt = set([item for sublist in res_msc_opt for item in sublist])
		writer.writerow(["Greedy Approach",num_nodes,num_edges,density,end-start,len(res_msc_opt)])

def experiment_wsc(G, MGM_G, set_data, set_cost, filename):
	num_nodes = len(G.nodes())
	num_edges = len(G.edges())
	density = nx.density(G)

	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)

		start = time.perf_counter()
		res_set, res_w = wsc.heuristic_1(set_data,set_cost)
		end = time.perf_counter()
		writer.writerow(["SoA heuristic",num_nodes,num_edges,density,end-start,len(res_set),res_w])

		start = time.perf_counter()
		clusters, totalCost = wsc.minCostMAXSetCover_fast(MGM_G)
		end = time.perf_counter()
		writer.writerow(["MMG",num_nodes,num_edges,density,end-start,len(clusters),totalCost])

def experimental_topology(topology):
	filesat = "result/topology_"+topology+"/sat.csv"
	# filemsc = "result/topology_"+topology+"/msc.csv"
	# filewsc = "result/topology_"+topology+"/wsc.csv"
	# filewsc2 = "result/topology_"+topology+"/wsc_cut.csv"
	init_file(filesat, ["name","nodes","edges","density","time","results"])
	# init_file(filemsc, ["name","nodes","edges","density","time","results"])
	# init_file(filewsc, ["name","nodes","edges","density","time","result_set","result_w"])
	# init_file(filewsc2, ["name","nodes","edges","density","time","result_set","result_w"])
	filewsc_distro = []
	# filewsc_distro_cut = []
	# for i in range(0,len(cost_distro)):
	# 	filewsc_distro.append("result/topology_"+topology+"/cost_distribution/wsc_"+cost_distro[i]+".csv")
	# 	# filewsc_distro_cut.append("result/topology_"+topology+"/cost_distribution/wsc_"+cost_distro[i]+"_cut.csv")
	# 	init_file(filewsc_distro[i], ["name","nodes","edges","density","time","result_set","result_w"])
	# 	# init_file(filewsc_distro_cut[i], ["name","nodes","edges","density","time","result_set","result_w"])
	
	for index in range(1,num_experiment):
		for n in test:
			G, MGM, m_label, m, c, i, s = generate_graph(n, topology)

			## CNF formula from the graph
			# formulaG = sat.convert_graph_to_cnf(G, m, c, i, s)
			experiment_sat(G, MGM, filesat)
	
			## Weighted set from the graph
			# set_data = tools.getListOfMetricsByCluster(MGM)
			# set_cost = tools.getCostClList(MGM)
			# experiment_wsc(G, MGM, set_data, set_cost, filewsc)


			# for file_i in range(0,len(cost_distro)):
			# 	G, MGM, m_label, m, c, i, s = generate_graph(n,cost_distro[file_i], topology)
			# 	set_data = tools.getListOfMetricsByCluster(MGM)
			# 	set_cost = tools.getCostClList(MGM)
			# 	experiment_wsc(G, MGM, set_data, set_cost, filewsc_distro[file_i])

			# print("1----",index,n,"----")

		# for n in testmsc:
		# 	G, MGM, m_label, m, c, i, s = generate_graph(n, topology)
		# 	set_data = tools.getListOfMetricsByCluster(MGM)
		# 	m = [x for x in MGM.nodes if 'M' in x]
		# 	experiment_msc(G, MGM, m, set_data, filemsc)
		# 	# print("2----",index,n,"----")
		
		# for n in testwsc:
		# 	G, MGM, m_label, m, c, i, s = generate_graph(n, topology)
		# 	set_data = tools.getListOfMetricsByCluster(MGM)
		# 	set_cost = tools.getCostClList(MGM)
		# 	experiment_wsc(G, MGM, set_data, set_cost, filewsc2)
		# 	# print("3----",index,n,"----")

		## Cost Distribution
		# for file_i in range(0,len(cost_distro)):
		# 	for n in test:
		# 		G, MGM, m_label, m, c, i, s = generate_graph(n,cost_distro[file_i], topology)
		# 		set_data = tools.getListOfMetricsByCluster(MGM)
		# 		set_cost = tools.getCostClList(MGM)
		# 		experiment_wsc(G, MGM, set_data, set_cost, filewsc_distro[file_i])
		# 		# print(cost_distro[file_i]," 1----",index,n,"----")
			
			# for n in testwsc:
			# 	G, MGM, m_label, m, c, i, s = generate_graph(n,cost_distro[file_i], topology)
			# 	set_data = tools.getListOfMetricsByCluster(MGM)
			# 	set_cost = tools.getCostClList(MGM)
			# 	experiment_wsc(G, MGM, set_data, set_cost, filewsc_distro_cut[file_i])
			# 	# print(cost_distro[file_i]," 2----",index,n,"----")
		print(index)
	
if __name__ == "__main__":
	for topology in topologies:
		print("***** ",topology," *****")
		experimental_topology(topology)