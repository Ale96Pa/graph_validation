import networkx as nx
import networkx as nx
from operator import itemgetter


def makeClusterXY(G):
	listOfCluster   =   [x for x in G.nodes if 'CL' in x]
	weight = nx.get_node_attributes(G, "weight")
	res	=	[]

	for key, val in weight.items():
		metricsCovered	=	[x for x,y in G.in_edges(key)]
		clusterCost		= 	val
		res.append([key,metricsCovered,clusterCost])
	
	return res



def searchMinCostMaxMetrics(clusterXY):
	metricCov = 0
	costCluster = 999999
	cluster	=	[]

	for xyz in clusterXY:
		if xyz[2] < costCluster and len(xyz[1]) > metricCov:
			metricCov = len(xyz[1])
			costCluster = xyz[2]
			cluster = xyz[0]

	
	return cluster,costCluster

def searchMinCostMaxMetrics_fast(clusterCost,clusterMetrics):
	#clusterMax = min(clusterCost.items(), key=lambda x: (x[1], -clusterMetrics[x[0]]))[0]
	clusterMax = max(clusterMetrics.items(), key=lambda x: (x[1], -clusterMetrics[x[0]]))[0]
	clusterMaxCost = clusterCost[clusterMax]
	clusterMaxCover	=	clusterMetrics[clusterMax]
	bestCluster = clusterMax
	for x,y in clusterMetrics.items():
		if y == clusterMaxCover and clusterCost[x] < clusterMaxCost:
		#if clusterCost[x] == clusterMaxCost and y > clusterMaxCover:
			clusterMaxCost = clusterCost[x]
			#clusterMaxCover = y
			bestCluster = x
	
	return bestCluster

def minCostMAXSetCover(G):
	listOfMetrics   =   [x for x in G.nodes if 'M' in x and G.out_degree(x) > 0]
	listOfCluster   =   [x for x in G.nodes if 'CL' in x]


	metricsCovered = set({})
	clusters = []
	totalCost = 0


	while set(metricsCovered) != set(listOfMetrics):
		clusterXY	=	makeClusterXY(G)
		

		removeCluster,costCluster	=	searchMinCostMaxMetrics(clusterXY)
		clusters.append(removeCluster)

		G.remove_node(removeCluster)
		metricsToCover = [x[1] for x in clusterXY if x[0]==removeCluster]
		for xx in metricsToCover[0]:
			G.remove_node(xx)
			metricsCovered.add(xx)
		
		totalCost += costCluster

	return listOfMetrics,list(metricsCovered),clusters,totalCost


def searchMinCostMaxMetrics(clusterXY):
	metricCov = 0
	costCluster = 999999
	cluster	=	[]

	for xyz in clusterXY:
		if xyz[2] < costCluster and len(xyz[1]) > metricCov:
			metricCov = len(xyz[1])
			costCluster = xyz[2]
			cluster = xyz[0]

	
	return cluster,costCluster

def minCostMAXSetCover_fast(G):
	listOfMetrics = [x for x in G.nodes if 'M' in x and G.out_degree(x) > 0]
	listOfCluster = [x for x in G.nodes if 'CL' in x]

	metricsCovered = set()

	clusters = []
	totalCost = 0

	while len(metricsCovered) != len(listOfMetrics):
		clusterCost = nx.get_node_attributes(G, "weight")
		clusterCost = {c: clusterCost[c] for c in listOfCluster}

		# clusterMetrics = {c: len([x for x, y in G.in_edges(c) ]) for c in listOfCluster}
		clusterMetrics = {c: G.in_degree(c) for c in listOfCluster}
		clusterToRemove = {x for x,y in clusterMetrics.items() if y==0}
		
		clusterMetrics = {x:y for x,y in clusterMetrics.items() if y!=0}
		
		for x in clusterToRemove:
			clusterCost.pop(x,None)

		try:
			bestCluster = searchMinCostMaxMetrics_fast(clusterCost,clusterMetrics)
			clusters.append(bestCluster)
			totalCost += clusterCost[bestCluster]
			metricsToCover = [x[0] for x in G.in_edges(bestCluster)]
			metricsCovered	=	metricsCovered.union(set(metricsToCover))

			G.remove_node(bestCluster)
			listOfCluster.remove(bestCluster)
			for m in metricsToCover:
				if m in listOfMetrics:
					G.remove_node(m)
			
		except Exception as e:
			print(e)
	
	return listOfMetrics, list(metricsCovered), clusters, totalCost
