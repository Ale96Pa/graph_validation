import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

#from tools
from tools import drawGraph
from tools import genPosNodes


def correctnessMGM(MGM,outputFile,pos,drw=False):
    wrongCL = set()
    wrongIN = set()
    vIN = [node for node in MGM.nodes() if 'I' in node]
    vM	= [node for node in MGM.nodes() if 'M' in node]
    vCL = [node for node in MGM.nodes() if 'CL' in node]
    vSRC = [node for node in MGM.nodes() if 'S' in node]

    for inp in vIN:
        if MGM.out_degree(inp) == 0:
            # print(inp,MGM.out_degree(inp))
            wrongIN = wrongIN.union({inp})
            wrongCL = wrongCL.union(set([edge[0] for edge in MGM.in_edges(inp) ]))



    for wrong in wrongIN:
        MGM.remove_node(wrong)
    for wrong in wrongCL:
        MGM.remove_node(wrong)

    for mt in vM:
        if MGM.out_degree(mt) == 0:
            MGM.remove_node(mt)
    
    for cl in vCL:
        if MGM.in_degree(cl) == 0:
            MGM.remove_node(cl)

def correctnessMGM(MGM,outputFile,pos):
	wrongCL = set()
	wrongIN = set()
	vIN = [node for node in MGM.nodes() if 'I' in node]
	vM	= [node for node in MGM.nodes() if 'M' in node]
	vCL = [node for node in MGM.nodes() if 'CL' in node]
	vSRC = [node for node in MGM.nodes() if 'S' in node]

	for inp in vIN:
		if MGM.out_degree(inp) == 0:
			# print(inp,MGM.out_degree(inp))
			wrongIN = wrongIN.union({inp})
			wrongCL = wrongCL.union(set([edge[0] for edge in MGM.in_edges(inp) ]))



	for wrong in wrongIN:
		MGM.remove_node(wrong)
	for wrong in wrongCL:
		MGM.remove_node(wrong)

	for mt in vM:
		if MGM.out_degree(mt) == 0:
			MGM.remove_node(mt)
	
	for cl in vCL:
		if MGM.in_degree(cl) == 0:
			MGM.remove_node(cl)

	for inp in vIN:
		if MGM.in_degree(inp) == 0:
			MGM.remove_node(inp)
	
	for src in vSRC:
		if MGM.in_degree(src) == 0:
			MGM.remove_node(src)

	#drawGraph(MGM, outputFile,pos,)
	return True #TODO:modificare

#create X from edge to respect the paper S is a subSet of X
def makeXForAlgo(listoOfNodes,Graph):
    X = []
    for node in listoOfNodes:
        #uso > 0 di zero perché devo prendermi solo le metriche 
        # da cui parte almeno 1 arco
        if len(Graph.out_edges(node)) > 0:
            X.append(node)

    return set(X)

#create S
def makeSForAlgo(listoOfNodes,Graph):
    S = []
    for node in listoOfNodes:
        tmpList = []
        for el in Graph.in_edges(node):
            tmpList.append(el[0])
        S.append(tmpList)
    return S

def greedyMinSetCover(X,S):
    I = set({})
    while X != set():
        valMax = 0
        index = 0
        for s in S:
            d = len(set(s).intersection(X))
            if d > valMax:
                valMax = d
                index = S.index(s)
        
        #print(valMax,index)
    
        I = I.union(set({index}))
        X = X.difference(set(S[index]))
        
    return I

def exeMinSetCoverV1(MGM,results={}):
    listOfMetrics = [node for node in MGM.nodes() if 'M' in node]
    listOfClusters = []
    listOfInputs = []
    listOfCovMetrics	=	[]

    for node in MGM.nodes():
        if 'M' in node and MGM.out_degree(node) > 0:
            listOfCovMetrics.append(node)
        elif 'CL' in node:
            listOfClusters.append(node)
        elif 'I' in node:
            listOfInputs.append(node)
    
    subMGM = MGM.subgraph(listOfCovMetrics+listOfClusters)
    
    #SICCOME POSSO AVERE METRICHE CHE NON SONO COLLEGATE A NULLA
    #PRENDO SOLO LE METRICHE CON UN ARCO USCENTE
    #PERCIò creo X e S

    S = makeSForAlgo(listOfClusters,subMGM)
    X = makeXForAlgo(listOfCovMetrics,subMGM)
    
    I = greedyMinSetCover(X, S)

    listOfCovCluster = [listOfClusters[el] for el in I]

    # print('[V1] METRICS COV: {}'.format(len(listOfCovMetrics)), '\t/\tALL METRICS: {}'.format(len(listOfMetrics)))
    # print('[V1] MIN CLUSTERS COV: {}'.format(len(listOfCovCluster)), '\t/\tALL CLASTERS: {}'.format(len(listOfClusters)))
    results['M_T']= str(len(listOfMetrics))
    results['M_C']= str(len(listOfCovMetrics))
    results['C_T']= str(len(listOfClusters))
    results['C_C']= str(len(listOfCovCluster))


    
    covGraph_v1 = MGM.subgraph(listOfCovMetrics+listOfCovCluster)

    return listOfCovCluster,covGraph_v1,results

def exeMinSetCoverV2(MGM,listOfCovCluster,results={}):
    listOfClusters = []
    listOfInputs = []
    listOfCovMetrics	=	[]

    for node in MGM.nodes():
        if 'M' in node and MGM.out_degree(node) > 0:
            listOfCovMetrics.append(node)
        elif 'CL' in node:
            listOfClusters.append(node)
        elif 'I' in node:
            listOfInputs.append(node)
    
    subMGM = MGM.subgraph(listOfCovMetrics+listOfCovCluster+listOfInputs)

    
    listOfCovInput = []
    for covCluster in listOfCovCluster:
        for el in subMGM.out_edges(covCluster):
            listOfCovInput.append(el[1])
    
    listOfCovInput    =   list(set(listOfCovInput))

    covGraph_v2 = MGM.subgraph(listOfCovMetrics+listOfCovCluster+listOfCovInput)

    # if len(listOfCovInput) > 9:
    #     print('[V2] MIN INPUTS COV: {}'.format(len(listOfCovInput)), '\t/\tALL INPUTS: {}'.format(len(listOfInputs)))
    # else:
    #     print('[V2] MIN INPUTS COV: {}'.format(len(listOfCovInput)), '\t\t/\tALL INPUTS: {}'.format(len(listOfInputs)))

    
    results['I_T']= str(len(listOfInputs)+6)
    results['I_C']= str(len(listOfCovInput))

    return listOfCovInput,covGraph_v2,results

def MGMminSetCover(MGM,outputFile,draw=True,saveFig=True,color=True,show=False):
    # print('START TASK: MGMminSetCover()')
    # print(outputFile.split('.')[0])


    # pos = genPosNodes(MGM)

    # st = time.time()
    
    results = {}
    # outputFile_BASE	=	outputFile.split('.')[0]+"_START."+outputFile.split('.')[1]

    # outputFile_CORRECT	=	outputFile.split('.')[0]+"_CORRECT."+outputFile.split('.')[1]
    # MGM = correctnessMGM(MGM, outputFile_CORRECT, pos)

    # outputFile_v1	=	outputFile.split('.')[0]+"_v1."+outputFile.split('.')[1]
    listOfCovCluster,covGraph_v1,results	=	exeMinSetCoverV1(MGM,results)


    # outputFile_v2	=	outputFile.split('.')[0]+"_v2."+outputFile.split('.')[1]
    #listOfCovInput,covGraph_v2,results    =   exeMinSetCoverV2(MGM,listOfCovCluster,results)
    
    


    # outputFile_COMPLETE	=	outputFile.split('.')[0]+"_COVERED."+outputFile.split('.')[1]
    
    # listOfMinCostSources,covGraph_v3,results	=	exeMinSetCoverV3(MGM,listOfCovCluster,listOfCovInput,results)
    #listOfMetrics = [x for x in MGM.nodes if 'M' in x and MGM.out_degree(x) > 0]
    #listOfSources = [x for x in MGM.nodes if 'S' in x]
    #covGraph_v3 = MGM.subgraph(listOfMetrics+listOfCovCluster+listOfCovInput+listOfSources)
    

    # # get the end time
    # et = time.time()

    # # get the execution time
    # elapsed_time = et - st
    # print('Execution time:', elapsed_time, 'seconds')
    # #print(results)

    # """
    # if draw:
    #     drawGraph(MGM, outputFile_BASE,pos,saveFig=saveFig,show=show)
    #     drawGraph(covGraph_v1, outputFile_v1,pos,saveFig=saveFig,show=show)
    #     drawGraph(covGraph_v2, outputFile_v2,pos,saveFig=saveFig,show=show)
    #     drawGraph(covGraph_v3, outputFile_COMPLETE,pos,saveFig=saveFig,show=show)
    # """

    # print('END TASK: MGMminSetCover()')
    # print('----------------------------------------')
    return results