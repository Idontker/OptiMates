from genericAlgorithm.basic_genetic_algorithm import Genome
from sphere import graphOnSphere as gos
import logging


class Solution:
    def __init__(self, graph) -> None:
        self.dominatingSet = set()
        self.graph = graph

    def addNodesByGenome(self, genome: Genome):
        labels = list()
        for i in range(0, len(genome) - 1):
            if genome[i] == 1:
                labels.append(i)
        self.addNodesByLabels(labels)

    def addNodesByLabels(self, labels):
        for label in labels:
            self.dominatingSet.add(self.graph.getNode(label))
        self.coveredSet = self.calcCoveredSet()

    def randomSolution(self, N):
        s = "Solution: ("
        for i in range(0, N):
            node = self.graph.getRandomNode()
            self.dominatingSet.add(node)
            s = s + str(node) + ", "
        logging.debug(s + ")")
        self.coveredSet = self.calcCoveredSet()

    def calcCoveredSet(self):
        coveredSet = set()
        for v in self.dominatingSet:
            coveredSet = coveredSet.union(v.neighbours)
        return coveredSet

    def fittness(self):
        s = "\tCovered: ("
        for v in self.coveredSet:
            s = s + str(v) + ", "
        logging.debug(s + ")")

        if len(self.dominatingSet) == 0:
            return 0
        fit = len(self.coveredSet) + 1.0 / len(self.dominatingSet)
        return fit / self.graph.size()

    def _cmp(self, other):
        return self.fittness() - other.fittness()

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __str__(self) -> str:
        return (
            " n: "
            + str(self.graph.size())
            + "\tdom size: "
            + str(len(self.dominatingSet))
            + "\tcovered: "
            + str(len(self.coveredSet))
            + "\tfittness: "
            + str(self.fittness())
        )
