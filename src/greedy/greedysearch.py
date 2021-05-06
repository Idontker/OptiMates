from typing import Callable, Optional

from numpy.lib.function_base import cov
from graph.graph import Graph
from graph.node import Node
from greedy import prioqueue
from greedy.entry import Entry
from graph.solution import Solution
from greedy.prioqueue import PrioQueue
import graph as graphclass
import numpy as np
import logging


PrinterFunc = Callable[[int, Solution], None]

# BUG: Knoten updatet nur Nachbaren, nicht aber die Knoten die mit seinen Nachbarn benachbart sind
# BUG:


class GreedySearch:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.prioqueue = PrioQueue()
        self.node_to_entry = {}

    def findSolution(self, printer: Optional[PrinterFunc] = None) -> Solution:
        # generate a solution
        sol = Solution(self.graph)
        self.prioqueue = PrioQueue()
        self.node_to_entry = {}

        # insert all nodes with equal weight:
        for node in self.graph.nodes.values():
            self.prioqueue.add_task(Entry(node))

        iteration = 0
        while sol.isFullCover() == False:

            # get best by heuristcs / fittness
            next_entry = self.prioqueue.pop_task()

            ## DEBUG ##
            logging.debug("\t\t\t\t\t\t" + str(next_entry))
            # old = sol.getCoveredNodes()
            # logging.debug(old)
            # logging.debug(np.count_nonzero(old - next_entry.node.getNeighbours() == -1))
            ## DEBUG ##

            sol.addNodeByLabel(next_entry.node.label)

            ## DEBUG ##
            # old = np.apply_along_axis(
            #     arr=old, axis=0, func1d=lambda x: (x != 0) * 1 + (x == 0) * 0
            # )
            # bitsol = np.apply_along_axis(
            #     arr=sol.getCoveredNodes(),
            #     axis=0,
            #     func1d=lambda x: (x != 0) * 1 + (x == 0) * 0,
            # )
            # logging.debug(old)
            # logging.debug(bitsol)
            # logging.debug(old - bitsol)
            ## DEBUG ##

            covered_nodes = np.int8(sol.getCoveredNodes())
            amount_covered = sol.countCoveredNodes()
            # TODO: BUG: hier wird eine falsche annahme getroffen, da der covering vektor nicht nur 0 oder 1 ist
            # not_covered_nodes = np.invert(covered_nodes, dtype=np.int8)

            # updating nodes in the prioqueue

            # extract labels from neighbour vector
            neighbour_labels = np.where(next_entry.node.getNeighbours() != 0)[0]
            for neighbour_label in neighbour_labels:
                neighbour = self.graph.getNode(neighbour_label)
                if sol.containsLabel(neighbour_label):
                    pass
                elif neighbour in self.node_to_entry:
                    entry = self.node_to_entry[neighbour]
                    entry.update(covered_nodes, amount_covered)
                    self.prioqueue.add_task(entry, -entry.getFittness())
                else:
                    self.__addNodeToQueue(neighbour, covered_nodes, amount_covered)
            pass
            iteration = iteration + 1
            if printer is not None:
                printer(iteration, sol)

        return sol

    def __addNodeToQueue(
        self, node: Node, covered_nodes: np.array, amount_covered: int
    ) -> None:
        entry = Entry(node)
        entry.update(covered_nodes, amount_covered)

        self.prioqueue.add_task(entry, -entry.getFittness())
        self.node_to_entry[node] = entry
