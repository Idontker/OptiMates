from typing import Callable, Optional
from graph import Graph, Node
from greedy import prioqueue
from sphere import Point, Solution
from greedy.prioqueue import PrioQueue
import graph as graphclass


PrinterFunc = Callable[[int, Solution], None]


class GreedySearch:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.prioqueue = PrioQueue()
        self.node_to_entry = {}

    def findSolution(self, printer: Optional[PrinterFunc] = None) -> Solution:
        # generate a solution
        sol = Solution(self.graph)
        self.prioqueue = []
        self.node_to_entry = {}

        # insert a random node
        initial_node = self.graph.getRandomNode()
        self.__addNodeToQueue(initial_node, initial=True)

        iteration = 0
        while sol.isFullCover() == False:
            # get best by heuristcs / fittness
            next_entry = self.prioqueue.pop_task()

            # updating nodes in the prioqueue
            for neighbour in next_entry.getNeighbours():
                if neighbour in self.node_to_entry:
                    entry = self.node_to_entry[neighbour]
                    entry.update()
                    prioqueue.add_task(entry, entry.getFittness)
                else:
                    self.__addNodeToQueue(neighbour)
            pass
            
            if printer is not None:
                printer(iteration, sol)

        return sol

    def __addNodeToQueue(self, node: Node, initial: bool = False) -> None:
        entry = Entry(node)
        if initial == False:
            entry.update()

        prioqueue.add_task(entry, entry.getFittness)
        self.node_to_entry[node] = entry


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