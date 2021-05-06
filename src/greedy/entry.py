from graph.node import Node
import numpy as np


class Entry:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.covering_nodes = node.getNeighbours()
        self.covering_uncovered_nodes = len(node.getNeighbours())

    def __str__(self):
        return "covering: {}\tlabel: {}".format(-self.getFittness(), self.node)

    def getFittness(self) -> int:
        return self.covering_uncovered_nodes

    # BUG: ist amount_covered = 0 und covered_nodes = 0, so ist das ergebnis falsch (-|V|)
    def update(self, covered_nodes: np.array, amount_covered: int) -> None:
        # More speedup with JAX ?
        # https://stackoverflow.com/questions/42916330/efficiently-count-zero-elements-in-numpy-array
        amount_covered_with_this = self.__extract_possible_coverings(covered_nodes)

        self.covering_uncovered_nodes = amount_covered_with_this - amount_covered

    def __extract_possible_coverings(self, covered_nodes: np.array):
        return np.count_nonzero(self.covering_nodes + covered_nodes)
