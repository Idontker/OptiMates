from sphere import Point
from graph import Node
from typing import Callable, List
from functools import partial

import numpy as np
import sphere.pointOnSphere as pos
import math
import random


class Graph:
    def __init__(self, isNeighbourFunction: Callable[[Point, Point], int]) -> None:
        self.nodes = {}
        self.nextLabel = 0
        self.adjmatrix = np.full((0, 0), 0)
        self.neighbour_function = isNeighbourFunction
        pass

    def __len__(self) -> int:
        return len(self.nodes)

    def __str__(self) -> str:
        return "number of Nodes: " + str(self.nextLabel)

    def addNode(self, point: Point) -> None:
        node = Node(point, self.nextLabel)
        self.nodes[self.nextLabel] = node
        self.nextLabel = self.nextLabel + 1
        pass

    def addNodes(self, points: List[Point]) -> None:
        for point in points:
            self.addNode(point=point)
        pass

    def getNode(self, label: int) -> Node:
        if label < 0 or label >= self.nextLabel:
            return None
        else:
            return self.nodes[label]

    def getRandomNode(self) -> Node:
        rad = random.randint(0,self.nextLabel-1)
        return self.nodes[rad]

    def getMatrix(self) -> np.array:
        return self.adjmatrix

    def updateAllEdges(self) -> np.array:
        """recalculate all edges
        Runs in O( |V|^2 )
        """

        # create an emptry quadratic array (uninitialized)
        number_of_nodes = len(self)
        shape_of_matrix = (number_of_nodes, number_of_nodes)
        matrix = np.empty(shape=shape_of_matrix)

        # recalculate all edges with the given neighbour_function
        # update neighbours of each node if neighbour_function != 0
        #
        # Runs in O( |V|^2 )
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                is_neighbour_value = self.neighbour_function(
                    self.nodes[i], self.nodes[j]
                )
                matrix[i][j] = is_neighbour_value
                if is_neighbour_value != 0:
                    n1 = self.nodes[i]
                    n2 = self.nodes[j]

                    n1.addNeighbour(n2)
                    n2.addNeighbour(n1)
                    pass
                pass
            pass

        self.adjmatrix = matrix
        return matrix


pass


def create_default_graph_with_random_points(
    sphere_radius: float = 1.0,
    number_of_nodes: int = 100_000,
    radius: float = math.radians(3.5),
) -> Graph:
    """Runs in O(|V|^3) = O(number_of_nodes + number_of_nodes + O(Graph.updateAllEdges))

    using the following neighbour function `F`:
    F(u, v) = 1     if arccos(u.point, v.point) < `radius`
    F(u, v) = 0     otherwise
    """

    # Runs in O(number_of_nodes)
    # create random points and add to list
    list_of_points = list()
    for i in range(number_of_nodes):
        random_point = pos.generateRandomPointOnSphere(sphere_radius)
        list_of_points.append(random_point)
        pass

    # Runs in O(number_of_nodes)
    # create graph and add nodes
    neighbour_function = partial(__default_distance, radius=radius)
    graph = Graph(neighbour_function)
    for point in list_of_points:
        graph.addNode(point=point)

    graph.updateAllEdges()
    pass


def __default_distance(u: Node, v: Node, radius: float) -> int:
    """radius in radians"""
    if u.dist(v) < radius:
        return 1
    else:
        return 0
