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




def maxSetCovByATTRv3(G,cost,outputFile,pos,config):
	targetCost = cost
	setOfCluster = []
	g_c = G.copy()

	while targetCost > 0:
		minCost = 99999
		maxNumbMetrics = 0
		fistCluster = ''
		
		cl = [x for x in G.nodes if 'C' in x]

		for c in cl:
			actClCost = getClusterCost(G,c)
			totMetrics = len(set([m[0] for m in G.in_edges(nbunch=c)]))
			if actClCost <= targetCost and actClCost <= minCost and totMetrics > maxNumbMetrics:
				minCost = actClCost
				maxNumbMetrics = totMetrics
				fistCluster = c

		print(minCost,maxNumbMetrics,fistCluster)
	
		#2 remove cluster node
		G.remove_node(fistCluster)
		setOfCluster.append(fistCluster)
		targetCost = cost - getClusterCost(g_c,setOfCluster)
	
	print(setOfCluster)
	listOfMetrics = [x for x in g_c.nodes if 'M' in x and g_c.out_degree(x) > 0]
	listOfSources = [x for x in g_c.nodes if 'S' in x]
	listOfInputs = [x for x in g_c.nodes if 'I' in x]

	subGraph	=	g_c.subgraph(listOfMetrics+setOfCluster+listOfInputs+listOfSources)

	return MGMminSetCover(subGraph,outputFile,pos,config)