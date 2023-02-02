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

    return covering

if __name__ == "__main__":
    universe = [1, 2, 3, 4, 5]
    subsets = [    [1, 2, 3],
        [2, 4],
        [3, 5],
        [1, 4, 5],
    ]

    minimal_covering = min_set_cover(universe, subsets)
    print("Minimal Covering:", minimal_covering)
