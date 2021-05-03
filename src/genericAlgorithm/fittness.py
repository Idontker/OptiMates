from genericAlgorithm.basic_genetic_algorithm import Genome
from sphere.solution import Solution
from sphere.graphOnSphere import Graph
from nptyping import NDArray
import numpy as np


def fittness(genome: Genome, graph: Graph) -> int:
    if len(genome) != graph.size():
        raise ValueError("genome and things must be of same length")

    labels = list()
    for i in range(0, len(genome) - 1):
        if genome[i] == 1:
            labels.append(i)

    sol = Solution(graph)
    sol.addNodesByLabels(labels)
    return sol.fittness()


def fittnessFast(genome: Genome, adjmatrix: NDArray[int]) -> int:
    # ueberpruefe Inputs
    if adjmatrix.ndim != 2:
        raise ValueError("adjacenzmatrix must have exaclty 2 dimmensions")

    if len(genome) != adjmatrix.shape[0] or len(genome) != adjmatrix.shape[1]:
        raise ValueError("genome and matrix must be of same length")

    # Umwandlung des Types
    vec = np.array(genome)

    # Multiplikation des Vektors: Ergebniss beschreibt den Überdeckungsvektor
    # result[i] = 0 falls nicht überdeckt, andernfalls ist er überdeckt
    result = adjmatrix.dot(vec)

    # nodes_covered: anzahl überdeckter Knoten
    nodes_covered = np.count_nonzero(result)

    # dominating_set_size: anzahl von
    dominating_set_size = np.sum(vec)

    return fittnessFunction_paperHybird(
        nodes_total=len(genome),
        nodes_covered=nodes_covered,
        dominating_set_size=dominating_set_size,
    )


def fittnessFunction_paperHybird(
    nodes_total: int, nodes_covered: int, dominating_set_size: int
) -> int:
    return (nodes_covered + 1 / dominating_set_size) / nodes_total
