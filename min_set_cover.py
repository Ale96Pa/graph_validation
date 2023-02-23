def greedyMinSetCover(universe, subsets):
    selected_subsets = []
    while universe:
        best_subset = max(subsets, key=lambda s: len(s & universe))
        selected_subsets.append(best_subset)
        oldLen = len(universe)
        universe -= best_subset
        if oldLen == len(universe):
            break

    return selected_subsets

def setCover(setList,target=None):
    if not setList: return None
    if target is None: target  = set.union(*setList)
    bestCover = []
    for i,values in enumerate(setList):
        remaining = target - values
        if remaining == target: continue
        if not remaining: return [values]
        subCover = setCover(setList[i+1:],remaining)
        if not subCover: continue
        if not bestCover or len(subCover)<len(bestCover)-1:
            bestCover = [values] + subCover
    return bestCover

if __name__ == "__main__":

    universe = range(1,10)
    subsets = [[1, 2, 3],
        [2, 4],
        [3, 5],
        [1, 4, 5],
        [1, 4, 5],
        [4, 4, 5],
        [5, 4, 5],
        [6, 4, 5],
        [7, 4, 5],
        [8, 4, 5],
        [1, 2, 5],
        [1, 4, 5],
        [1, 9, 10],
        [1, 7, 5],
        [1, 6, 5],
        [1, 3, 5],
    ]
    a=[]
    for elem in subsets:
        a.append(set(elem))
    minimal_covering = setCover(a)
    print("Minimal Covering:", minimal_covering)

    minimal_covering = greedyMinSetCover(set(universe), a)
    print("Minimal Covering:", minimal_covering)