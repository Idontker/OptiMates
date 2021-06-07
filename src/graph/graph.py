from random import random
from typing import Tuple
import numpy as np
import math

from tqdm import tqdm
from geometrics.ikosaeder import ikosaeder
import sys
import graph.total_size as total


class Graph:
    def __init__(
        self, cover_radius: float, number_of_points: int, exploration_factor=1.5
    ) -> None:
        self.points = None
        # packed bit Vektoren, welcher die überdeckten Knoten anzeigt
        self.adj_neighbour_dic = {}

        self.number_of_points = number_of_points
        self.cover_radius = cover_radius
        self.exploration_factor = exploration_factor
        pass

    def __len__(self) -> int:
        return int(self.number_of_points)

    def __sizeof__(self) -> int:
        return total.total_size(self.points) + total.total_size(self.adj_neighbour)

    ##############################
    ##############################
    # Updating and Getting Vectors
    ##############################
    ##############################

    def update_all_neighbours(self, steps: int = 1) -> None:
        stepsize = np.linspace(num=steps+1, start=0, stop=len(self.points)).astype(int)

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
        d = self.get_distance_vector(label)
        byte_vector = d < self.cover_radius
        self.adj_neighbour_dic[label] = np.packbits(byte_vector)

        ###  For non packed vectors ###
        # self.adj_neighbour_dic[label] = byte_vector.astype(np.int8)

    def get_extension_and_reach(self, label) -> tuple[np.array, np.array]:
        d = self.get_distance_vector(label)
        byte_extension = d < self.exploration_factor * self.cover_radius
        byte_reach = d < 2 * self.cover_radius
        return byte_extension, byte_reach

    def get_distance_vector(self, label) -> np.array:
        cartesian = self.points[:, 3:6]
        other = cartesian[label]
        vec = np.matmul(cartesian, np.transpose(other))

        # verhindert, dass arccos bei d(label, label) aufgrund Rundungsfehler fehlschlagen würde.
        vec[label] = 1

        return np.arccos(vec)

    ##############################
    ##############################
    ########## Getters ###########
    ##############################
    ##############################

    def get_neighbour_vector(self, label) -> np.array:
        return np.unpackbits(self.adj_neighbour[label])
        if label not in self.adj_neighbour_dic:
            self.update_neighbour(label)
        return np.unpackbits(self.adj_neighbour_dic[label])
        return self.adj_neighbour_dic[label]

    def pop_neighbour_vector(self, label) -> np.array:
        if label not in self.adj_neighbour_dic:
            self.update_neighbour(label)
        return np.unpackbits(self.adj_neighbour_dic.pop(label))
        return self.adj_neighbour_dic.pop(label)

    ### Generating points on graph ###

    def gen_random_points(self) -> None:
        self.points = np.array(
            [self._create_random_point() for _ in range(self.number_of_points)]
        )
        pass

    def gen_iko_points(self, divisions=10):
        iko = ikosaeder()
        iko.subdivide(n=divisions)
        self.points = iko.normalized_points()
        self.number_of_points = len(self.points)
        pass

    def gen_archimedic_spiral(
        self,
        speed=100,
        N=1000,
        lower_bound=0,
        upper_bound=1,
    ):
        """theta in [arccos(lower_bound), arccos(upperbound)]"""

        X = np.linspace(lower_bound, upper_bound, N)
        thetas = np.arccos(X)
        phis = speed * thetas

        arr = np.array(
            [
                np.ones(len(thetas)),
                thetas,
                phis,
                np.sin(thetas) * np.cos(phis),
                np.sin(thetas) * np.sin(phis),
                np.cos(thetas),
            ]
        )
        # np.transpose wechselt die Dimmensionen, sodass bei Iterationen über die Zeilen(einzelne Punkte) und nicht die Spalten(Theta-vektor, Phi-vektor, ...) iteriert wird
        self.points = np.transpose(arr)
        pass

    # sieht für mich nach der archimedischen Spirale aus mit speed L = sqrt(N*pi)
    def gen_bauer_spiral(self, N):
        L = np.sqrt(N * np.pi)
        k = np.array(range(1, N + 1))
        z = 1 - (2 * k - 1) / N
        phi = np.arccos(z)
        theta = L * phi
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)

        arr = np.array(
            [
                np.ones(N),
                phi,
                theta,
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                z,
            ]
        )

        # np.transpose wechselt die Dimmensionen, sodass bei Iterationen über die Zeilen(einzelne Punkte) und nicht die Spalten(Theta-vektor, Phi-vektor, ...) iteriert wird
        self.points = np.transpose(arr)
        pass

    def _create_point(self, r, theta, phi) -> np.array:
        arr = np.array([r, theta, phi, 0, 0, 0])
        arr[3] = r * math.sin(theta) * math.cos(phi)
        arr[4] = r * math.sin(theta) * math.sin(phi)
        arr[5] = r * math.cos(theta)
        return arr

    def _create_random_point(self) -> np.array:
        phi = random() * 2 * math.pi
        x = random() * 2 - 1
        theta = np.arccos(x)

        return self._create_point(1, theta, phi)


pass

#########################
#########################
# Save and Load Operation
#########################
#########################


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
