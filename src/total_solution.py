import logging
from graph.solution import Solution
from graph.graph import Graph
import numpy as np
import csv


class Total_Solution:
    def __init__(self, N, labels, delete_parts) -> None:
        self.N = N
        self.labels = labels
        self.delete_parts = delete_parts

        self.used_labels = np.array([]).astype(int)

        # list von tupeln (a,b).
        self.ranges = []
        # a stellt dabei jeweils das erste und b das letzte Label dar,
        # die in einer iteration genutzt werden
        self._setup_ranges(self.labels)

    def _setup_ranges(self, labels):
        for stripe in labels:
            self.ranges.append((stripe[0], stripe[-1]))
        pass

    def create_initial_solution(self, iteration: int, graph: Graph) -> Solution:
        sol = Solution(graph=graph)

        # setup sol.genome with previous sol
        start, end = self.ranges[iteration]

        tmp = self.used_labels[(self.used_labels >= start) & (self.used_labels <= end)]
        tmp = tmp - start
        logging.info("{}:reused labels: start={}\tend={}".format(iteration, start, end))
        logging.info(
            "{}:reused labels: count={}\tlabels={}\tlabels-start={}".format(
                iteration, len(tmp), tmp + start, tmp
            )
        )

        for label in tmp:
            sol.addNodeByLabel(label)
        return sol

    def include_solution(self, iteration: int, solution: Solution) -> None:
        start, end = self.ranges[iteration]
        if end < self.N - 1:
            end, _ = self.delete_parts[iteration]

        sol_labels = solution.getUsedLabels()
        sol_labels = sol_labels + start
        sol_labels = sol_labels[sol_labels <= end]
        self.used_labels = np.append(self.used_labels, sol_labels)

        arr, c = np.unique(self.used_labels, return_counts=True)
        self.used_labels = arr[c > 0]

        pass

    pass

    def save(self, filepath: str, points) -> None:
        # TODO: anpassen an cart only
        writer_nodes = csv.writer(
            open(file=filepath, mode="w", newline=""), delimiter=";"
        )
        for label in self.used_labels:
            point = points[label]
            writer_nodes.writerow([point[3], point[4], point[5]])
            pass