import logging
from sphere.pointOnSphere import Point
from graph.node import Node
from typing import Callable, List
from functools import partial
from tqdm import tqdm

import numpy as np
import sphere.pointOnSphere as pos
import math
import random
import csv
import itertools


class Graph:
    def __init__(self, cover_radius) -> None:
        self.nodes = {}
        self.nextLabel = 0
        self.adjmatrix = None
        self.reach = None
        self.dist = None
        self.cover_radius = cover_radius
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
        rad = random.randint(0, self.nextLabel - 1)
        return self.nodes[rad]

    def getMatrix(self) -> np.array:
        return self.adjmatrix

    def updateAllEdges(self) -> np.array:
        """recalculate all edges
        Runs in O( |V|^2 )
        """

        logging.info("Update all edges")
        # create an emptry quadratic array (uninitialized)
        number_of_nodes = len(self)
        shape_of_matrix = (number_of_nodes, number_of_nodes)
        # matrix = np.empty(shape=shape_of_matrix, dtype=np.int8)
        dist = np.empty(shape=shape_of_matrix, dtype=np.float64)

        # recalculate all edges with the given neighbour_function
        # update neighbours of each node if neighbour_function != 0
        #
        # Runs in O( |V|^2 )
        # for (x,y) in tqdm(matrix.)
        n1, n2 = self.nodes[0], self.nodes[1]

        for i,j in tqdm(np.ndindex(number_of_nodes,number_of_nodes)):
            is_neighbour_value = self.nodes[i].point.dist(self.nodes[j].point)  #self.neighbour_function(
                    #n1,n2 #self.nodes[i], self.nodes[j]
                #)
            dist[i, j] = is_neighbour_value
            dist[j, i] = is_neighbour_value
            pass

        self.dist = dist
        self.adjmatrix = (dist < self.cover_radius).astype(np.int8)

        for i in tqdm(range(number_of_nodes)):
            self.nodes[i].setNeighbourVector(self.dist[i])

        # for i in tqdm(range(number_of_nodes)):
        # # for i in range(number_of_nodes):
        #     for j in range(number_of_nodes):
        #         is_neighbour_value = self.neighbour_function(
        #             self.nodes[i], self.nodes[j]
        #         )
        #         matrix[i, j] = is_neighbour_value
        #         pass
        #     self.nodes[i].setNeighbourVector(matrix[i])
        #     pass

        logging.info("Done")
        return self.dist

    def save(self, filepath: str) -> None:
        writer_nodes = csv.writer(
            open(file=filepath + "-nodes.csv", mode="w", newline="")
        )
        for label, node in self.nodes.items():
            writer_nodes.writerow([label, node.point])
        np.save(file=filepath + "-matrix.npy", arr=self.adjmatrix)
        pass


pass


def load_graph_from(
    path: str, radius: float = math.radians(3.5), neighbour_function=None
) -> Graph:
    if neighbour_function is None:
        neighbour_function = partial(__default_distance, radius=radius)
    g = Graph(neighbour_function)

    try:
        csvfile = open(path + "-nodes.csv", mode="r")
    except:
        print("File cannot be opened:", path + "-nodes.csv")
        return None

    g.adjmatrix = np.load(file=path + "-matrix.npy")

    max_label = -1
    reader_nodes = csv.reader(csvfile, delimiter=",")
    for label, p in reader_nodes:
        label = int(label)
        if label > max_label:
            max_label = label
        node = Node(point=pos.parsePoint(p), label=label)
        node.neighbours = g.adjmatrix[label]
        g.nodes[label] = node
        pass

    g.nextLabel = max_label + 1

    return g


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
    logging.info("Create {} Points".format(number_of_nodes))
    for i in tqdm(range(number_of_nodes)):
        random_point = pos.generateRandomPointOnSphere(sphere_radius)
        list_of_points.append(random_point)
        pass
    logging.info("DONE")

    # Runs in O(number_of_nodes)
    # create graph and add nodes
    logging.info("Create Gaph with {} nodes".format(number_of_nodes))
    # neighbour_function = partial(__default_distance, radius=radius)
    graph = Graph(radius)
    for point in tqdm(list_of_points):
        graph.addNode(point=point)
    logging.info("DONE")

    graph.updateAllEdges()
    return graph


def __default_distance(u: Node, v: Node, radius: float) -> int:
    """radius in radians"""
    if u.dist(v) < radius:
        return 1
    else:
        return 0