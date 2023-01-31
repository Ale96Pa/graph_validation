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

# Dummy weighted set cover with no heuristics
def no_heuristic(universe, sets, weights):
    # lista per mantenere traccia dei set selezionati
    selected_sets = []
    # lista per mantenere traccia degli elementi del universo coperti
    covered_elements = []
    # ordina i set in base al loro peso
    sorted_sets = sorted(zip(sets, weights), key=lambda x: x[1])
    while len(covered_elements) < len(universe):
        # seleziona il set con peso minimo che copre elementi non ancora coperti
        for set_, weight in sorted_sets:
            if set_.issubset(universe) and not set_.intersection(covered_elements):
                selected_sets.append(set_)
                covered_elements.extend(set_)
                break
    # calcola il peso totale dei set selezionati
    total_weight = sum([weights[sets.index(set_)] for set_ in selected_sets])
    return selected_sets, total_weight


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
    sets = [{1, 2}, {2, 3, 4}, {3, 4, 5}, {1, 5}]
    weights = [2, 1, 3, 2]
    selected_sets, total_weight = no_heuristic(universe, sets, weights)
    print("Selected sets:", selected_sets)
    print("Total weight:", total_weight)
