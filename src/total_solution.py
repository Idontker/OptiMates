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

        self.logs = []

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
        self.__log_all_labels(iteration, start, end, sol_labels, solution.label_logs)

        sol_labels = sol_labels + start
        sol_labels = sol_labels[sol_labels <= end]
        self.used_labels = np.append(self.used_labels, sol_labels)

        arr, c = np.unique(self.used_labels, return_counts=True)
        self.used_labels = arr[c > 0]

        pass

    pass

    def __log_all_labels(
        self, iteration: int, start: int, end: int, sol_labels: int, label_logs
    ):
        for label in label_logs.keys():
            t = label_logs[label]

            keep_label = label + start <= end

            self.logs.append(
                [
                    iteration,
                    t[0],  # specific iteration
                    t[1],  # % covered
                    t[2],  # covered
                    t[3] + start,  # label
                    t[4],  # fittness
                    t[5],  # new coverings
                    t[6],  # covered intersection
                    t[7],  # covered mid
                    keep_label,
                ]
            )

        pass

    def save_logs(self, filepath: str, points):
        # TODO: anpassen an cart only
        writer_nodes = csv.writer(
            open(file=filepath, mode="w", newline=""), delimiter=";"
        )
        # header
        writer_nodes.writerow(
            [
                "slice",
                "slice_i",
                "'%' covered",
                "# covered",
                "label",
                "fittness",
                "new coverings",
                "covered intersection",
                "mid",
                "keep",
                "x",
                "y",
                "z",
            ]
        )
        for t in self.logs:
            label = t[4]
            point = points[label]
            writer_nodes.writerow(
                [
                    t[0],
                    t[1],
                    t[2],
                    t[3],
                    t[4],
                    t[5],
                    t[6],
                    t[7],
                    t[8],
                    t[9],
                    point[3],
                    point[4],
                    point[5],
                ]
            )
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
