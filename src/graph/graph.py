from random import random
from typing import Tuple
import numpy as np
import math
from numpy.core.numeric import indices

from tqdm import tqdm
from geometrics.ikosaeder import ikosaeder
import sys
import graph.total_size as total


class Graph:
    def __init__(
        self,
        cover_radius: float,
        number_of_points: int,
        exploration_factor=1.5,
        intersection_weight=1000,
    ) -> None:
        # graphs attributes
        self.points = None
        self.adj_neighbour = None

        # settings for the graph
        self.number_of_points = number_of_points
        self.cover_radius = cover_radius
        self.exploration_factor = exploration_factor

        # attributes for the weighted intersection search
        # TODO: rename - neighbours macht keinen Sinn, da es echte Puntke sind
        self.intersection_neighbours = None
        self.mid_neighbours = None
        self.intersection_weight = intersection_weight
        self.mid_neg_weight = -intersection_weight

        # TODO: Schnittpunkte hinzufuegbar machen
        # es ist nicht möglich Punkte zur Packed matrix hinzufügen, die nicht nur 0 und 1 Einträge haben
        # die Idee ist es eine zweite und dritte Matrix zu erstellen. Hier kann man die Vektoren so anlegen,
        # dass man mit dem Zugriff einen Vektor erhält, der angibt wie viele Schnittpunkte und wie viele
        # Wenn man die Schnittpunkte nicht als mögliche positionen betrachtet sollte es nicht zu viel aufwand sein
        # Man müsste nur die drei Punkte hinzufügen: 2 Schnittpunkte der Kugeln um zwei Mittelpunkte mit der Sphere
        # und den Punkt zwischen den Mittelpunkten (M1 + M2) / ||M1+M2||. Die Schnittpunkte können mit *alpha* bewertet werden
        # die Mittelpunkte haben einen negativen Einfluss auf die Knoten. Die Mittelpunkte verhindern, dass man genau zwischen
        # die gesamte Schnittfläche doppelt überdeckt wird

        pass

    def __len__(self) -> int:
        return int(self.number_of_points)

    def __sizeof__(self) -> int:
        return total.total_size(self.points) + total.total_size(self.adj_neighbour)

    ##############################
    ##############################
    ##############################
    # Intersection Part
    ##############################
    ##############################

    # TODO: Wahrscheinlich macht es für die Laufzeit keinen Sinn ALLES im voraus zu berechnen
    # es sparrt zwar später Zeit, aber die kann ich mir auch sparen, da ich alles nur einmal brauche

    # def add_intersection_point(self, p1, p2=None):
    #     # Wiederhole für beide Knoten
    #     if p2 is not None:
    #         self.add_intersection_point(p2)

    #     # generiere nachbarvektor
    #     # label sollte nicht genutzt werden, daher -1, sodass andernfalls ein Fehler fliegt
    #     neigbours = self.get_distance_vector(label=-1, vector=p1) < self.cover_radius
    #     neigbours = neigbours.astype(np.int8)

    #     if self.intersection_neighbours is None:
    #         self.intersection_neighbours = neigbours
    #     else:
    #         self.intersection_neighbours = np.vstack(
    #             (self.intersection_neighbours, neigbours)
    #         )
    #     print(self.intersection_neighbours.shape)
    #     print(self.intersection_neighbours)

    def add_intersection_point(self, p1, p2):
        if self.intersection_neighbours is None:
            self.intersection_neighbours = p1
        else:
            self.intersection_neighbours = np.vstack((self.intersection_neighbours, p1))
        self.intersection_neighbours = np.vstack((self.intersection_neighbours, p2))
        # print("shape intersections: ", self.intersection_neighbours.shape)
        # print(self.intersection_neighbours)

    def add_mid_point(self, m1, m2):
        """m1 und m2 sind die Mittelpunkte, zwischen denen der Mittelpunkt gelegt werden soll"""
        mid = m1 + m2
        mid = mid / np.linalg.norm(mid)

        # print(m1, m2, "mid:", mid)
        if self.mid_neighbours is None:
            self.mid_neighbours = np.array(mid)
        else:
            self.mid_neighbours = np.vstack((self.mid_neighbours, mid))
        # print("shape mids: ", self.mid_neighbours.shape)

    def count_intersections_next_to(self, label):
        if self.intersection_neighbours is None:
            return 0
        vec = self.points[label][3:6]
        vec = np.matmul(self.intersection_neighbours, np.transpose(vec))
        dist = np.arccos(vec) < self.cover_radius

        return np.sum(dist.astype(np.int8))

    def count_mid_next_to(self, label):
        if self.mid_neighbours is None:
            return 0
        vec = self.points[label][3:6]
        vec = np.matmul(self.mid_neighbours, np.transpose(vec))
        dist = np.arccos(vec) < self.cover_radius

        return np.sum(dist.astype(np.int8))

    def delect_intersects(self, label):
        if self.intersection_neighbours is None:
            return
        vec = self.points[label][3:6]
        vec = np.matmul(self.intersection_neighbours, np.transpose(vec))
        dist = np.arccos(vec) < self.cover_radius

        indices = np.where(dist == True)[0]
        # print(np.arccos(vec))
        # print(dist)
        # print(self.cover_radius)
        # print(self.intersection_neighbours)
        self.intersection_neighbours = np.delete(
            self.intersection_neighbours, indices, axis=0
        )
        # print(self.intersection_neighbours)

        pass

    ##############################
    ##############################
    ##############################
    # Updating and Getting Vectors
    ##############################
    ##############################

    def update_all_neighbours(self, steps: int = 1) -> None:
        stepsize = np.linspace(num=steps + 1, start=0, stop=len(self.points)).astype(
            int
        )

        arr = None
        other = self.points[:, 3:6]
        for i in tqdm(range(len(stepsize) - 1)):
            a, b = stepsize[i], stepsize[i + 1]
            cartesian_slice = self.points[a:b, 3:6]

            matrix = np.matmul(cartesian_slice, np.transpose(other))

            # verhindert, dass arccos bei d(label, label) aufgrund Rundungsfehler fehlschlagen würde.
            # np.fill_diagonal(matrix, 1)

            # ugly bugfix, da die diagonale auf 1 zu setzten nicht so trivial ist (diagonale nach dem zweiten slice fängt in der mitte an)
            matrix[np.where(matrix > 1)] = 1

            dist = np.arccos(matrix)
            # transform to bit vector
            byte_matrix = dist < self.cover_radius
            # -1 zeigt an, dass es vectorweise geht und nicht erst gefattend wird
            packed = np.packbits(byte_matrix, axis=-1)
            # packed = byte_matrix

            # zur temporären Lösung hinzufügen
            if arr is None:
                arr = packed
            else:
                arr = np.vstack((arr, packed))

            pass
        self.adj_neighbour = arr
        pass

    def update_neighbour(self, label) -> None:
        # TODO: wie kann ich einzelne Knoten zur adj matrix hinzufuegen?
        d = self.get_distance_vector(label)
        byte_vector = d < self.cover_radius
        self.adj_neighbour_dic[label] = np.packbits(byte_vector)

        ###  For non packed vectors ###
        # self.adj_neighbour_dic[label] = byte_vector.astype(np.int8)

    ##############################
    ##############################
    ########## Getters ###########
    ##############################
    ##############################

    def get_extension_and_reach(self, label) -> tuple[np.array, np.array]:
        d = self.get_distance_vector(label)
        byte_extension = d < self.exploration_factor * self.cover_radius
        byte_reach = d < 2 * self.cover_radius
        return byte_extension, byte_reach

    def get_distance_vector(self, label, vector=None) -> np.array:
        cartesian = self.points[:, 3:6]
        # TODO: sinnvoller trennen durch zwei Funktionen: z.B. get_distance_vector(label) ruft get_distance_vector_by_vec(vec) auf
        # ermöglicht auch beliebig distanzvektoren zu generieren
        other = cartesian[label] if vector is None else vector
        vec = np.matmul(cartesian, np.transpose(other))

        # verhindert, dass arccos bei d(label, label) aufgrund Rundungsfehler fehlschlagen würde.
        vec[label] = 1

        return np.arccos(vec)

    def get_neighbour_vector(self, label) -> np.array:
        return np.unpackbits(self.adj_neighbour[label])


pass

#########################
#########################
# Save and Load Operation
#########################
#########################

# TODO: adjust graph saving
def save(g: Graph, filepath: str) -> None:
    np.save(file=filepath + "-points.npy", arr=g.points)
    f = open(file=filepath + "-settings.txt", mode="w", newline="")
    f.write("number of points:" + str(g.number_of_points) + "\n")
    f.write("cover radius:" + str(g.cover_radius))
    f.flush()
    f.close()
    pass


def load_graph_from(filepath: str) -> Graph:
    try:
        f = open(file=filepath + "-settings.txt", mode="r", newline="")
    except:
        print("File cannot be opened:", str(filepath) + "-settings.txt")
        return None
    line = f.readline()
    N = int(line.split(":")[1])
    line = f.readline()
    r = float(line.split(":")[1])

    g = Graph(cover_radius=r, number_of_points=N)
    g.points = np.load(file=filepath + "-points.npy")
    return g
