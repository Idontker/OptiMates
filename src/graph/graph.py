import numpy as np
from tqdm import tqdm
import graph.total_size as total


class Graph:
    def __init__(
        self,
        cover_radius: float,
        number_of_points: int,
        exploration_factor=1.5,
        intersection_weight=1000,
        points=None,
    ) -> None:
        # graphs attributes
        self.points = points
        self.adj_neighbour = None

        # settings for the graph
        self.number_of_points = number_of_points
        self.cover_radius = cover_radius
        self.exploration_factor = exploration_factor

        # attributes for the weighted intersection search
        self.intersection_points = None
        self.mid_points = None
        self.intersection_weight = intersection_weight
        self.mid_neg_weight = -intersection_weight
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

    def add_intersection_point(self, p1, p2):
        if self.intersection_points is None:
            self.intersection_points = p1
        else:
            self.intersection_points = np.vstack(
                (self.intersection_points, p1))
        self.intersection_points = np.vstack(
            (self.intersection_points, p2))

    def add_mid_point(self, m1, m2):
        """m1 und m2 sind die Mittelpunkte, zwischen denen der Mittelpunkt gelegt werden soll"""
        mid = m1 + m2
        mid = mid / np.linalg.norm(mid)

        if self.mid_points is None:
            self.mid_points = np.array(mid)
        else:
            self.mid_points = np.vstack((self.mid_points, mid))

    def count_intersections_next_to(self, label):
        if self.intersection_points is None:
            return 0
        vec = self.points[label][3:6]
        vec = np.matmul(self.intersection_points, np.transpose(vec))
        dist = np.arccos(vec) < self.cover_radius

        return np.sum(dist.astype(np.int8))

    def count_mid_next_to(self, label):
        if self.mid_points is None:
            return 0
        vec = self.points[label][3:6]
        vec = np.matmul(self.mid_points, np.transpose(vec))
        dist = np.arccos(vec) < self.cover_radius

        return np.sum(dist.astype(np.int8))

    def delect_intersects(self, label):
        if self.intersection_points is None:
            return
        vec = self.points[label][3:6]
        vec = np.matmul(self.intersection_points, np.transpose(vec))
        dist = np.arccos(vec) < self.cover_radius

        indices = np.where(dist == True)[0]
        self.intersection_points = np.delete(
            self.intersection_points, indices, axis=0
        )

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

            # ugly bugfix, da die diagonale auf 1 zu setzten nicht so trivial ist (diagonale nach dem zweiten slice fängt in der mitte an)
            matrix[np.where(matrix > 1)] = 1

            dist = np.arccos(matrix)
            # transform to bit vector
            byte_matrix = dist < self.cover_radius
            # -1 zeigt an, dass es vectorweise geht und nicht erst gefattend wird
            packed = np.packbits(byte_matrix, axis=-1)

            # zur temporären Lösung hinzufügen
            if arr is None:
                arr = packed
            else:
                arr = np.vstack((arr, packed))

            pass
        self.adj_neighbour = arr
        pass

    ##############################
    ##############################
    ########## Getters ###########
    ##############################
    ##############################

    def get_extension_and_reach(self, label):
        d = self._get_distance_vector_label(label)
        byte_extension = d < self.exploration_factor * self.cover_radius
        byte_reach = d < 2 * self.cover_radius
        return byte_extension, byte_reach

    def _get_distance_vector_label(self, label) -> np.array:
        cartesian = self.points[:, 3:6]
        # ermöglicht auch beliebig distanzvektoren zu generieren
        other = cartesian[label]
        vec = np.matmul(cartesian, np.transpose(other))

        # verhindert, dass arccos bei d(label, label) aufgrund Rundungsfehler fehlschlagen würde.
        vec[label] = 1

        return np.arccos(vec)

    def get_neighbour_vector(self, label) -> np.array:
        return np.unpackbits(self.adj_neighbour[label])[0:self.number_of_points]


pass
