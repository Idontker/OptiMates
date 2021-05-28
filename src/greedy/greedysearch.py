from typing import Callable, Optional

from graph.graph import Graph
from graph.solution import Solution
from greedy.entry import Entry
from greedy.prioqueue import PrioQueue
import numpy as np
import logging
from tqdm import tqdm


PrinterFunc = Callable[[int, Solution], None]

# BUG: Knoten updatet nur Nachbaren, nicht aber die Knoten die mit seinen Nachbarn benachbart sind
# BUG:


class GreedySearch:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def findSolution(self, printer: Optional[PrinterFunc] = None) -> Solution:
        # generate a solution
        sol = Solution(self.graph)
        self.prioqueue = PrioQueue()
        self.label_to_entry = {}

        # insert initial
        self.prioqueue.add_task(Entry(graph=self.graph, label=0))

        iteration = 0
        while sol.isFullCover() == False:

            # get best by heuristcs / fittness
            curr_entry = self.prioqueue.pop_task()
            logging.debug("\t\t\t\t\t\t" + str(curr_entry))

            curr_label = curr_entry.label
            sol.addNodeByLabel(curr_label)

            reached_labels = np.where(self.graph.pop_reach_vector(curr_label) != 0)[0]
            extension_vec = self.graph.pop_extensions_vector(curr_label)
            amount_covered = sol.countCoveredNodes()
            covered_nodes = sol.covering_vec

            # update prioqueue
            for reached_label in tqdm(reached_labels):
                if sol.containsLabel(reached_label):
                    pass
                elif reached_label in self.label_to_entry:
                    entry = self.label_to_entry[reached_label]
                    entry.update(covered_nodes, amount_covered)
                    self.prioqueue.add_task(entry, -entry.getFittness())
                elif extension_vec[reached_label] == 1:
                    self.__addLabelToQueue(reached_label, covered_nodes, amount_covered)
            pass
            iteration = iteration + 1
            if printer is not None:
                printer(iteration, sol)

        return sol

    def __addLabelToQueue(
        self, label: int, covered_nodes: np.array, amount_covered: int
    ) -> None:
        entry = Entry(graph=self.graph, label=label)
        entry.update(covered_nodes, amount_covered)

        self.prioqueue.add_task(entry, -entry.getFittness())
        self.label_to_entry[label] = entry
