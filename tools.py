import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from random import randint

def genPosNodes(G,prt=False):
	if prt:
		print('Start the positioning of nodes according to AS algo')
	delta = [3,10,8,7]
	pos = [0,15,30,45]
	
	#1/03/2023 ho cambiato la sequenza del for che prima era I S CL ad CL I S
	d = {}
	find = 0
	i=1
	for el in G.nodes:
		if 'CL' in el and find == 0:
			find = 1
			i=1
			delta.pop(0)
			pos.pop(0)
		if 'I' in el and find == 1:
			find = 2
			i=1
			delta.pop(0)
			pos.pop(0)
		if 'S' in el and find == 2:
			find = 3
			i=1
			delta.pop(0)
			pos.pop(0)
		
		aaaa=str((i*4)+((i-1)*delta[0]))
		d[str(el)] = (int(pos[0]),int(aaaa))

		i+=1

	if prt:
		print(d)
		print('END - the positioning of nodes')
	return d

def drawGraph(G,outputFileName,pos,saveFig=True,show=False,fontSize=5,nodeSize=400):
	print('START drawing...')
	plt.figure(figsize=(21,30), frameon=False)

	options = {
		"font_size": fontSize,
		"node_size": nodeSize,
		"node_color": "white",
		"edgecolors": "black",
		"linewidths": 1,
		"width": 1
	}
	
	
	nx.draw_networkx(G, pos, **options)



	# Set margins for the axes so that nodes aren't clipped
	ax = plt.gca()
	ax.margins()

	plt.axis("off")
	
	if saveFig:
		plt.savefig(outputFileName)
	
	if show:
		plt.show()

	print('END Draw phase')


def getListOfMetrics(G):
	metrics = []

	for node in G.nodes():
		if 'CL' in node:
			#questo è il controllo per prendere tutti i nodi cluster
			#e da quelli estrarre la lista di metriche
			nodes = [edge[0] for edge in G.in_edges(node)]	
			metrics.append(nodes)
	
	#print(metrics)
	return metrics

def getCostClList(G):
	costList = []
	weight = nx.get_node_attributes(G, "weight")
	for key, val in weight.items():
		costList.append(val)

	#print(costList)
	return costList

	