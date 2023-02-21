import time
from itertools import chain, combinations

def min_set_cover(universe, subsets):
    universe = set(universe)
    subsets = [set(s) for s in subsets]

    covered = set()
    covering = []
    for s in sorted(subsets, key=lambda x: len(x - covered)):
        covered |= s
        covering.append(s)
        if covered == universe:
            break

    res = []
    for elem in covering:
        st = "("
        for e in list(elem):
            st+=str(e)+" "
        st+=")"
        res.append(st)
    covering = [ele for ele in covering if ele != set()]
    return covering

def makeSForAlgo(listOfNodes, Graph):
    S = []
    for node in listOfNodes:
        tmpSet = set()
        for el in Graph.in_edges(node):
            tmpSet.add(el[0])
        S.append(tmpSet)
    return S

def makeXForAlgo(listOfNodes, Graph):
    X = [node for node in listOfNodes if Graph.out_degree(node) > 0]
    return set(X)

def greedyMinSetCover(U, S):
    C = []
    while U:
        i = max(range(len(S)), key=lambda j: len(S[j] & U))
        C.append(i)
        U -= S[i]
    return C

def exeMinSetCoverV2(MGM, results={}):
    listOfMetrics = [node for node in MGM.nodes() if 'M' in node]
    listOfClusters = [node for node in MGM.nodes() if 'CL' in node]
    listOfCovMetrics = [node for node in listOfMetrics if MGM.out_degree(node) > 0]

    subMGM = MGM.subgraph(listOfCovMetrics + listOfClusters)

    S = makeSForAlgo(listOfClusters, subMGM)
    X = set(makeXForAlgo(listOfCovMetrics, subMGM))
    start = time.perf_counter()
    I = greedyMinSetCover(X, S)
    end = time.perf_counter()

    listOfCovCluster = [listOfClusters[i] for i in I]

    if results:
        results['M_T'] = str(len(listOfMetrics))
        results['M_C'] = str(len(listOfCovMetrics))
        results['C_T'] = str(len(listOfClusters))
        results['C_C'] = str(len(listOfCovCluster))

    covGraph = MGM.subgraph(listOfCovMetrics + listOfCovCluster)

    return end-start, listOfCovCluster#, covGraph, results


if __name__ == "__main__":
    universe = [1, 2, 3, 4, 5]
    subsets = [[1, 2, 3],
        [2, 4],
        [3, 5],
        [1, 4, 5],
    ]

    minimal_covering = min_set_cover(universe, subsets)
    print("Minimal Covering:", minimal_covering)
