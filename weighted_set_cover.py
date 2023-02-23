"""
Weighted Set Cover Heuristics:

[1] Young, N. (2008). Greedy Set-Cover Algorithms. In: Kao, MY. (eds) 
Encyclopedia of Algorithms. Springer, Boston, MA. 
https://doi.org/10.1007/978-0-387-30162-4_175
"""

import itertools
from heapq import *
import networkx as nx

class PriorityQueue:
    def __init__(self):
        self._pq = []
        self._entry_map = {}
        self._counter = itertools.count()

    def addtask(self, task, priority = 0):
        '''Add a new task or update the priority of an existing task'''
        if task in self._entry_map:
            self.removetask(task)
        count = next(self._counter)
        entry = [priority, count, task]
        self._entry_map[task] = entry
        heappush(self._pq, entry)

    def removetask(self, task):
        '''Mark an existing task as REMOVED.'''
        entry = self._entry_map.pop(task)
        entry[-1] = 'removed'

    def poptask(self):
        '''Remove and return the lowest priority task.'''
        while self._pq:
            priority, count, task = heappop(self._pq)
            if task != 'removed':
                del self._entry_map[task]
                return task

    def __len__(self):
        return len(self._entry_map)

# Heuristic for weighted-set-cover as in [1]
MAXPRIORITY = 999999
def heuristic_1(S, w):
    udict = {}
    selected = list()
    scopy = [] # During the process, S will be modified. Make a copy for S.
    for index, item in enumerate(S):
        scopy.append(set(item))
        for j in item:
            if j not in udict:
                udict[j] = set()
            udict[j].add(index)

    pq = PriorityQueue()
    cost = 0
    coverednum = 0
    for index, item in enumerate(scopy): # add all sets to the priorityqueue
        if len(item) == 0:
            pq.addtask(index, MAXPRIORITY)
        else:
            pq.addtask(index, float(w[index]) / len(item))
    while coverednum < len(udict):
        a = pq.poptask() # get the most cost-effective set
        selected.append(a) # a: set id
        cost += w[a]
        coverednum += len(scopy[a])
        # Update the sets that contains the new covered elements
        for m in scopy[a]: # m: element
            for n in udict[m]:  # n: set id
                if n != a:
                    scopy[n].discard(m)
                    if len(scopy[n]) == 0:
                        pq.addtask(n, MAXPRIORITY)
                    else:
                        pq.addtask(n, float(w[n]) / len(scopy[n]))
        scopy[a].clear()
        pq.addtask(a, MAXPRIORITY)                       
    return selected, cost


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
	
	return clusters, totalCost



if __name__ == "__main__":
    U = [1,2,3,4,5]
    S = [[1, 2], [2, 3, 4], [3, 4, 5], [1, 5]]
    w = [2, 1, 3, 2]
    selected, cost = heuristic_1(S, w)

