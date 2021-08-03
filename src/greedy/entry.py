from graph.graph import Graph
import numpy as np
from graph.solution import Solution
import logging


class Entry:
    def __init__(self, graph: Graph, label: int) -> None:
        self.graph = graph
        self.label = label
        self.covering_uncovered_nodes = 0
        self.covered_intersections = 0
        self.covered_mids = 0

    def __str__(self):
        return "label: {}\tfittness: {}\tnew_coverings:{} \tcovered intersections:{}\t covered mid:{}".format(
            self.label,
            self.getFittness(),
            self.covering_uncovered_nodes,
            self.covered_intersections,
            self.covered_mids,
        )

    def savetycheck_coverings(self, current_solution: Solution):
        # überprüft, on der Knoten auch wirklich eine akkurate Fitness
        covered_nodes = current_solution.covering_vec
        amount_covered = current_solution.countCoveredNodes()
        amount_covered_with_this = self.__extract_possible_coverings(covered_nodes)

        curr_potential = amount_covered_with_this - amount_covered

        if curr_potential != self.covering_uncovered_nodes:
            logging.error(
                "label{} has {} new coverings but should have {} new coverings".format(
                    self.label, self.covering_uncovered_nodes, curr_potential
                )
            )

    def getFittness(self) -> int:
        if self.covering_uncovered_nodes == 0:
            return 0

        return (
            self.covering_uncovered_nodes
            + self.graph.intersection_weight * self.covered_intersections
            + self.graph.mid_neg_weight * self.covered_mids
        )

    def update(self, covered_nodes: np.array, amount_covered: int) -> None:
        # TODO: More speedup with JAX ?
        # https://stackoverflow.com/questions/42916330/efficiently-count-zero-elements-in-numpy-array
        amount_covered_with_this = self.__extract_possible_coverings(covered_nodes)

        self.covering_uncovered_nodes = amount_covered_with_this - amount_covered
        self.covered_intersections = self.graph.count_intersections_next_to(self.label)
        self.covered_mids = self.graph.count_mid_next_to(self.label)

    def __extract_possible_coverings(self, covered_nodes: np.array):
        my_covered_nodes = self.graph.get_neighbour_vector(self.label)
        return np.count_nonzero(my_covered_nodes + covered_nodes)