from random import choices
from graph.graph import Graph
import numpy as np
import csv


class Solution:
    def __init__(self, graph: Graph, sol=None) -> None:
        self.graph = graph

        if sol != None:
            self.genome = sol.genome
            self.covering_vec = sol.covering_vec
        else:
            self.genome = np.zeros(len(self.graph)).astype(int)
            self.covering_vec = np.zeros(len(self.graph)).astype(int)

    def __str__(self) -> str:
        return str(np.where(self.genome != 0)[0])

    def getUsedLabels(self) -> np.array:
        return np.where(self.genome == 1)[0]

    def containsLabel(self, label: int) -> bool:
        return self.genome[label] == 1

    def addNodeByLabel(self, label: int) -> int:
        self.genome[label] = 1
        # actuell nicht mehr gebracuht, da der Graph alle Nachbar Vectoren selbst verwaltet
        # es sparrt auch kaum speicherplatz, da deutlich mehr Knoten betrachtet werden, wie 
        self._updateCoverings(self.graph.get_neighbour_vector(label))
        self.graph.delect_intersects(label)

    def removeNodeByLabel(self, label: int) -> int:
        self.genome[label] = 0

    def initRandomGenome(self) -> None:
        self.genome = np.array(choices((0, 1), k=len(self.graph)))
        # TODO

    def _updateCoverings(self, vec: np.array) -> None:
        self.covering_vec = self.covering_vec + vec
        pass

    def countCoveredNodes(self) -> int:
        # covering_vec[i] = 0 falls nicht überdeckt, andernfalls ist er überdeckt
        return np.count_nonzero(self.covering_vec)

    def isFullCover(self) -> bool:
        return self.countCoveredNodes() == len(self.graph)

    def save(self, filepath: str) -> None:
        writer_nodes = csv.writer(
            open(file=filepath, mode="w", newline=""), delimiter=";"
        )
        for label in np.where(self.genome != 0)[0]:
            point = self.graph.points[label]
            writer_nodes.writerow([point[3], point[4], point[5]])
            pass
