import networkx as nx


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


