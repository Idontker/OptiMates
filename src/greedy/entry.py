from graph.graph import Graph
import numpy as np


class Entry:
    def __init__(self, graph: Graph, label: int) -> None:
        self.graph = graph
        self.label = label
        self.covering_uncovered_nodes = 0

    def __str__(self):
        return "covering: {}\tlabel: {}".format(-self.getFittness(), self.label)

    def getFittness(self) -> int:
        return self.covering_uncovered_nodes

    # BUG: ist amount_covered = 0 und covered_nodes = 0, so ist das ergebnis falsch (-|V|)
    def update(self, covered_nodes: np.array, amount_covered: int) -> None:
        # More speedup with JAX ?
        # https://stackoverflow.com/questions/42916330/efficiently-count-zero-elements-in-numpy-array
        amount_covered_with_this = self.__extract_possible_coverings(covered_nodes)

        self.covering_uncovered_nodes = amount_covered_with_this - amount_covered

    def __extract_possible_coverings(self, covered_nodes: np.array):
        my_covered_nodes = self.graph.get_neighbour_vector(self.label)
        return np.count_nonzero(my_covered_nodes + covered_nodes)
