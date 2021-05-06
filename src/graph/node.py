from sphere.pointOnSphere import Point
from typing import Set, Any
import numpy as np


class Node:
    def __init__(self, point: Point, label: int) -> None:
        # repräsentierter Punkt
        self.point = point

        # label für eindeutigen Zugriff
        self.label = label

        # Vektor der Nachbarn, woebi nur die Labels der Nachbaren gespeichert werden
        self.neighbours = None
        pass

    ## Getter ##

    def __str__(self) -> str:
        return str(self.label)

    def getPoint(self) -> Point:
        return self.point

    def getLabel(self) -> int:
        return self.label

    def getNeighbours(self) -> np.array:
        return self.neighbours

    def setNeighbourVector(self, vector: np.array) -> None:
        self.neighbours = vector
        pass

    # TODO: other should get the Node typing
    def isNeighbourOf(self, other) -> bool:
        return self.neighbours[other.label] == 1

    def dist(self, other):
        return self.point.dist(other.point)
