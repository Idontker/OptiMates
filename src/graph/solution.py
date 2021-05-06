from random import choices
from typing import List
import numpy as np


class Solution:
    def __init__(self, graph, genome: np.array = None) -> None:
        self.graph = graph
        self.matrix = self.graph.getMatrix()

        if genome != None:
            self.genome = genome
        else:
            self.genome = np.zeros(len(self.graph))

    def __str__(self) -> str:
        return str(np.where(self.genome != 0))

    def containsLabel(self, label: int) -> bool:
        return self.genome[label] == 1

    def addNodeByLabel(self, label: int) -> int:
        self.genome[label] = 1

    def removeNodeByLabel(self, label: int) -> int:
        self.genome[label] = 0

    def initRandomGenome(self) -> None:
        self.genome = np.array(choices((0, 1), k=len(self.graph)))

    def updateMatrix(self) -> None:
        self.matrix = self.graph

    def getCoveredNodes(self) -> np.array:
        # Multiplikation des Vektors: Ergebniss beschreibt den Überdeckungsvektor
        # result[i] = 0 falls nicht überdeckt, andernfalls ist er überdeckt
        return self.matrix.dot(self.genome)

    def countCoveredNodes(self) -> int:
        # Multiplikation des Vektors: Ergebniss beschreibt den Überdeckungsvektor
        # result[i] = 0 falls nicht überdeckt, andernfalls ist er überdeckt
        result = self.getCoveredNodes()

        # nodes_covered: anzahl überdeckter Knoten
        return np.count_nonzero(result)

    def isFullCover(self) -> bool:
        return self.countCoveredNodes() == len(self.graph)
