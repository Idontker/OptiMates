from src.sphere import Point
from typing import List
import src.sphere.pointOnSphere as pos
import random
import logging
import numpy as np
import math


class Graph:
    def __init__(self, R: float, r: float, radial:bool = False) -> None:
        self.nodes = {}
        self.R = R
        self.label = 0
        if radial:
            self.r = r
        else:
            self.r = math.radians(r)

    def getNode(self, label):
        return self.nodes[label]

    def getRandomNode(self) :
        return random.choice(list(self.nodes.values()))

    def addPointsToGraph(self, points:List[Point]) -> None :
        # add to nodes
        for p in points:
                self.nodes[self.label] = Node(p, self.label)
                self.label = self.label + 1
        # TODO: update neighbours
 
    def initRandomSet(self, n:int) -> None:
        # create n random Points and add to nodes (dict)
        points = list()
        for i in range(0, n):
            point = pos.generateRandomPointOnSphere(self.R)
            points.append(point)
        
        # add to Graph
        self.addPointsToGraph()

    # removed .size() with __len__
    def __len__(self) -> int:
      return len(self.nodes)

    def createMatrix(self) -> np.array:
        # Anzahl Knoten
        N = len(self.nodes)
        # create N x N matrix
        matrix = np.full((N, N), 0)

        # fill each field 
        for node in self.nodes.values():
            for neighbour in node.neighbours:
                matrix[node.label, neighbour.label] = 1
        return matrix



    #### Methods for debugging 

    def __str__(self) -> str:
        s = "Graph:\n"
        for v in self.nodes.values():
            s = s + "\tnode: " + str(v) + "\n"
        return s

    def strStruct(self) -> str:
        s = ""
        for v in self.nodes.values():
            s = s + v.strStruct() + "\n"
        return s

    def fullstr(self) -> str:
        s = ""
        for v in self.nodes.values():
            s = s + v.fullstr() + "\n"
        return s


class Node:
    def __init__(self, point, label) -> None:
        self.point = point
        self.neighbours = set()
        self.label = label

    def __str__(self) -> str:
        return str(self.label)

    def strStruct(self) -> str:
        s = "[Node:" + str(self.label) + ", ( "
        for v in self.neighbours:
            s = s + str(v.label) + ", "
        s = s + ")]"
        return s

    def fullstr(self) -> str:
        s = "[Node:" + str(self.label) + ", "
        for v in self.neighbours:
            s = (
                s
                + "("
                + str(pos.dist(self.point, v.point))
                + ", "
                + str(v.label)
                + "), "
            )
        s = s + "]"
        return s

    def findNeighbours(self, nodes, distance):
        self.n = len(nodes)
        for v in nodes:
            # if np.isnan(pos.dist(self.point, v.point)):
            #     logging.debug(self.point)
            #     logging.debug(
            #         "Distance: "
            #         + str(pos.dist(self.point, v.point))
            #         + "\t to point:"
            #         + str(v.point)
            #     )
            if pos.dist(self.point, v.point) < distance:
                self.neighbours.add(v)

    def hasAsNeighbours(self, other):
        return other in self.neighbours

    def weight(self):
        return len(self.neighbours) / self.n
