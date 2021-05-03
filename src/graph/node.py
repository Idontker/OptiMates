from src.sphere import Point
from typing import Any, Set


class Node:
    def __init__(self, point: Point, label: int) -> None:
        # repräsentierter Punkt
        self.point = point

        # label für eindeutigen Zugriff
        self.label = label

        # Menge der Nachbarn, woebi nur die Labels der Nachbaren gespeichert werden
        self.neighbours = set()
        pass

    ## Getter ##

    def __str__(self) -> str:
        return str(self.label)

    def getPoint(self) -> Point:
        return self.point

    def getLabel(self) -> int:
        return self.label

    def getNeighbours(self) -> Set[Point]:
        return self.neighbours

    ## public methods

    def addNeighbour(self, other: Node):
        self.neighbours.add(other.label)
        pass

    def isNeighbourOf(self, other: Node) -> bool:
        """isNeighbourOf(self, other: Node) -> bool
        
        Returns true if self.neighbours contains the label of the Node
        Returns false otherwise"""
        return other.label in self.neighbours
