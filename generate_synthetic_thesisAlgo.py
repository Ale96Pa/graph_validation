import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import random
from random import randint 
import itertools
import time

from MGM_set_cover import MGMminSetCover 
from tools import getListOfMetrics
from tools import getCostClList

def prepend(list, str):
 
	# Using format()
	str += '{0}'
	list = [str.format(i) for i in list]
	return(list)

test = [5,10,25,50,100,150,250,500,1000,2000,5000,10000]

def generate_graph(numNodes,draw=False):
	
	metrics = prepend(random.sample(range(1, numNodes*2), numNodes),'M')
	meas_settings = prepend(random.sample(range(numNodes*2+1, numNodes*4), numNodes),'CL')
	instruments = prepend(random.sample(range(numNodes*4+1, numNodes*6), numNodes),'I')
	specifications = prepend(random.sample(range(numNodes*6+1, numNodes*8), numNodes),'S')

	e_mc = random.sample(list(itertools.product(metrics,meas_settings)), numNodes*3)
	e_ci = random.sample(list(itertools.product(meas_settings,instruments)), numNodes*3)
	e_is = random.sample(list(itertools.product(instruments,specifications)), numNodes*3)

	B = nx.DiGraph()
	B.add_nodes_from(metrics, bipartite=0)
	for cl in meas_settings:
		cost = randint(1, 100)
		B.add_node(cl, weight=cost, bipartite=1)
	#B.add_nodes_from(meas_settings, bipartite=1)
	B.add_nodes_from(instruments, bipartite=2)
	B.add_nodes_from(specifications, bipartite=3)
	B.add_edges_from(e_mc)
	B.add_edges_from(e_ci)
	B.add_edges_from(e_is)


	#nx.write_gpickle(B, "test_"+str(numNodes)+".gpickle")
	return B, metrics, meas_settings, instruments, specifications

if __name__ == "__main__":
	
	for n in test:
		B, metrics, meas_settings, instruments, specifications = generate_graph(n)
		outputFile='output/MGM_'+str(n)+'.pdf'
		#MGMminSetCover(B,outputFile,draw=False,saveFig=False)
		getCostClList(B)
		exit(1)
		
