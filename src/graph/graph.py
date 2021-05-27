from random import random
import numpy as np
import math
from geometrics.ikosaeder import ikosaeder


class Graph:
    def __init__(self, cover_radius: float, number_of_points: int) -> None:
        self.points = None
        self.adj_extensions_dic = {}
        self.adj_neighbour_dic = {}
        self.adj_reach_dic = {}

        self.number_of_points = number_of_points
        self.cover_radius = cover_radius
        pass

    # def create_adjmatrix(self) -> None:
    #     self.adjmatrix = (self.dist < self.cover_radius).astype(np.int8)

    def get_reach_vector(self, label) -> np.array:
        if label not in self.adj_neighbour_dic:
            self.update_vectors(label)
        return self.adj_reach_dic[label]

    def get_neighbour_vector(self, label) -> np.array:
        if label not in self.adj_neighbour_dic:
            self.update_neighbour(label)
        return self.adj_neighbour_dic[label]

    def get_extensions_vector(self, label) -> np.array:
        if label not in self.adj_extensions_dic:
            self.update_vectors(label)
        return self.adj_extensions_dic[label]

    def pop_reach_vector(self, label) -> np.array:
        if label not in self.adj_neighbour_dic:
            self.update_vectors(label)
        return self.adj_reach_dic.pop(label)

    def pop_neighbour_vector(self, label) -> np.array:
        if label not in self.adj_neighbour_dic:
            self.update_neighbour(label)
        return self.adj_neighbour_dic.pop(label)

    def pop_extensions_vector(self, label) -> np.array:
        if label not in self.adj_extensions_dic:
            self.update_vectors(label)
        return self.adj_extensions_dic.pop(label)

    def update_neighbour(self, label) -> None:
        d = self.get_distance_vector(label)
        self.adj_neighbour_dic[label] = (d < self.cover_radius).astype(np.int8)

    def update_vectors(self, label) -> None:
        d = self.get_distance_vector(label)
        # range [0.8, 1.8]
        # self.adj_extensions_dic[label] =  ( (d - 1.3 * self.cover_radius) < 0.5 * self.cover_radius).astype(
        #     np.int8
        # )

        ex_fak = math.sqrt(3) - 0.01
        self.adj_extensions_dic[label] = (d < ex_fak * self.cover_radius).astype(
            np.int8
        )
        self.adj_reach_dic[label] = (d < 2 * self.cover_radius).astype(np.int8)

    def get_distance_vector(self, label) -> np.array:
        cartesian = self.points[:, 3:6]
        other = cartesian[label]
        vec = np.matmul(cartesian, np.transpose(other))
        vec[label] = 1
        return np.arccos(vec)

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

    def _create_random_point_old(self) -> np.array:
        theta = random() * 2 * math.pi
        phi = random() * math.pi

        return self._create_point(1, theta, phi)

    def __len__(self) -> int:
        return int(self.number_of_points)


pass


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
