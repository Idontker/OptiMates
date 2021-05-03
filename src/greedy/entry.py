from graph.node import Node

class Entry:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.covering_uncovered_nodes = len(node.getNeighbours)

    def getNode(self) -> Node:
        return self.node

    def getFittness(self) -> int:
        return self.covering_uncovered_nodes

    def update(self) -> None:
        self.covering_uncovered_nodes = self.covering_uncovered_nodes - 1