from typing import Callable, Optional

from graph.graph import Graph
from graph.solution import Solution
from greedy.entry import Entry
from greedy.prioqueue import PrioQueue
import numpy as np
import logging
from tqdm import tqdm
from geometrics import three_sphere_intersection as intersect


PrinterFunc = Callable[[int, Solution], None]

class GreedySearch:
    def __init__(self, graph: Graph, initial_sol: Solution = None) -> None:
        self.graph = graph
        self.sol = initial_sol

    def findSolution(
        self, curr_sol=None, printer: Optional[PrinterFunc] = None
    ) -> Solution:
        # generate a solution
        sol = None
        if self.sol is not None:
            sol = self.sol
            # TODO: build the prioqueue
        else:
            sol = Solution(self.graph)

        # setup datastructures
        self.prioqueue = PrioQueue()
        self.label_to_entry = {}

        # insert initial
        self.prioqueue.add_task(Entry(graph=self.graph, label=0))

        iteration = 0
        while sol.isFullCover() == False:

            # get best by heuristcs / fittness
            curr_entry = self.prioqueue.pop_task()
            logging.debug(
                "\titer:"
                + str(iteration)
                + "\tcovered:"
                + str(sol.countCoveredNodes())
                + "\t"
                + str(curr_entry)
            )

            curr_label = curr_entry.label
            sol.addNodeByLabel(curr_label)
            sol_labels = sol.getUsedLabels()

            # fuege Schnittpunkte zu den Punkten hinzu
            p1 = self.graph.points[curr_label]
            p1 = p1[3:6]  # extrahiere karthesische Koordinaten
            for sol_label in sol_labels:
                if sol_label == curr_entry:
                    continue  # skip Identitaet

                p2 = self.graph.points[sol_label]
                p2 = p2[3:6]  # extrahiere karthesische Koordinaten
                # find intersections
                s = intersect.find_aequidist_points_on_sphere(
                    p1, p2, self.graph.cover_radius, deg=False
                )

                # teste, ob auch wirklich Schnittpunkte vorhanden sind
                if s is not None:
                    # einfuegen dieser in den Algo
                    self.graph.add_intersection_point(s[0], s[1])
                    self.graph.add_mid_point(p1, p2)
                pass

            reached_vec, extension_vec = self.graph.get_extension_and_reach(curr_label)
            # where gibt nen array von arrays, daher braucht es das [0]
            reached_labels = np.where(reached_vec != 0)[0]
            amount_covered = sol.countCoveredNodes()
            covered_nodes = sol.covering_vec

            # update prioqueue
            # for reached_label in tqdm(reached_labels):
            for reached_label in reached_labels:
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
