"""
Weighted Set Cover Heuristics:

[1] Young, N. (2008). Greedy Set-Cover Algorithms. In: Kao, MY. (eds) 
Encyclopedia of Algorithms. Springer, Boston, MA. 
https://doi.org/10.1007/978-0-387-30162-4_175
"""

import itertools
from heapq import *
from collections import defaultdict

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

def heuristic_0(universe, subsets):
    # universe: a set of elements
    # subsets: a list of sets containing elements of universe, each with an associated cost

    # Create a dictionary to store the cost of each subset
    subset_costs = {frozenset(s): c for s, c in subsets}

    # Create a dictionary to store the sets that cover each element of the universe
    element_cover = {}
    for elem in universe:
        element_cover[elem] = set(s for s in subsets if elem in s)

    # Initialize an empty list to store the chosen subsets
    chosen_subsets = []

    # Loop until all elements are covered
    while element_cover:
        # Find the subset with the smallest cost-to-cover ratio
        best_subset = min(subsets, key=lambda s: subset_costs[frozenset(s)] / len(element_cover & set(s)))

        # Add the best subset to the chosen set
        chosen_subsets.append(best_subset)

        # Remove the chosen subset and update element_cover
        for elem in best_subset:
            for subset in element_cover[elem]:
                subset_costs[frozenset(subset)] -= subset_costs[frozenset(best_subset)]
            del element_cover[elem]

    # Return the list of chosen subsets
    return chosen_subsets


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

if __name__ == "__main__":
    S = [[1, 2], [2, 3, 4], [3, 4, 5], [1, 5]]
    w = [2, 1, 3, 2]
    selected, cost = heuristic_1(S, w)
    print("selected:", selected)
    print("cost:", cost)

    universe = set([1, 2, 3, 4, 5])
    # sets = [{1, 2}, {2, 3, 4}, {3, 4, 5}, {1, 5}]
    f = []
    for s in S:       
        f1 = set()
        f1.update(s)
        f.append(f1)
    print(f)

    universe = set([1, 2, 3, 4, 5])
    subsets = [({1, 2, 3}, 5), ({2, 4}, 10), ({3, 4}, 7), ({4, 5}, 8)]
    selected_sets, total_weight = heuristic_0(universe, subsets)
    print("Selected sets:", selected_sets)
    print("Total weight:", total_weight)
