import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# goldenratio
PHI = (1 + math.sqrt(5)) / 2
EPSILON = 10 ** -5


class ikosaeder:
    def __init__(self) -> None:
        self.vertices = np.array(
            [
                [0.0, 1.0, PHI],
                [0.0, 1.0, -PHI],
                [0.0, -1.0, PHI],
                [0.0, -1.0, -PHI],
                [1.0, PHI, 0.0],
                [1.0, -PHI, 0.0],
                [-1.0, PHI, 0.0],
                [-1.0, -PHI, 0.0],
                [PHI, 0.0, 1.0],
                [PHI, 0.0, -1.0],
                [-PHI, 0.0, 1.0],
                [-PHI, 0.0, -1.0],
            ]
        )

        tri = []

        n = len(self.vertices)
        for ia in range(n):
            for ib in range(ia + 1, n):
                for ic in range(ib + 1, n):
                    a, b, c = self.vertices[ia], self.vertices[ib], self.vertices[ic]

                    d = np.linalg.norm
                    if (
                        abs(d(a - b) - 2) < EPSILON
                        and abs(d(a - c) - 2) < EPSILON
                        and abs(d(b - c) - 2) < EPSILON
                    ):
                        tri.append(np.array([a, b, c]))
        self.tri = np.array(tri)
        pass

    def _subdived_triangles(self) -> None:
        tri = []
        for t in self.tri:
            a, b, c = t
            # calc midpoints
            mab = (a + b) / 2
            mac = (a + c) / 2
            mbc = (b + c) / 2

            # subdived t into 4 triangles:
            # 1: a,     mab,    mac
            # 2: mab,   b,      mbc
            # 3: mac,   mbc,    mab
            # 4: mac,   mvc,    c
            As = [a, mab, mac, mac]
            Bs = [mab, b, mbc, mbc]
            Cs = [mac, mbc, mab, c]

            # append to vertices
            self.vertices = np.vstack((self.vertices, mab))
            self.vertices = np.vstack((self.vertices, mac))
            self.vertices = np.vstack((self.vertices, mbc))

            # append to triangels
            for i in range(4):
                tri.append(np.array([As[i], Bs[i], Cs[i]]))
        self.tri = np.array(tri)

    def subdivide(self, n=10) -> None:
        for _ in range(n):
            self._subdived_triangles()
        pass

    def normalized_points(self) -> np.array:
        tmp = []
        for v in self.vertices:
            d = np.linalg.norm(v)
            tmp.append(np.array([0, 0, 0, v[0] / d, v[1] / d, v[2] / d]))
        return np.array(tmp)


def plot_scatter3d(ax, points, tris=None, color="r", size=1):
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    ax.scatter(x, y, z, color="r", s=10)


def plot_iko_faces(ax, iko, color="r", size=1):
    for i in range(len(iko.tri)):
        t = iko.tri[i]

        x = t[:, 0] * 0.95
        y = t[:, 1] * 0.95
        z = t[:, 2] * 0.95

        verts = [list(zip(x, y, z))]
        poly = Poly3DCollection(verts)
        poly.set_edgecolor("black")
        ax.add_collection3d(poly)


def _surface_spere(
    ax, r=1, alpha=1, resolution_theta=20j, resolution_phi=10j, color="black"
) -> None:
    # draw sphere
    u, v = np.mgrid[0: 2 * np.pi: resolution_theta, 0: np.pi: resolution_phi]
    x = r * np.cos(u) * np.sin(v)
    y = r * np.sin(u) * np.sin(v)
    z = r * np.cos(v)
    ax.plot_surface(x, y, z, color=color, alpha=alpha)


def _test_subdivision(n=2, size=10):
    base = ikosaeder()
    iko = ikosaeder()

    fig = plt.figure()

    ax = fig.add_subplot(2, 2, 1, projection="3d")
    plot_scatter3d(ax, iko.vertices, size=size)
    plot_iko_faces(ax, base)

    iko.subdivide(n=n)

    ax = fig.add_subplot(2, 2, 2, projection="3d")
    plot_scatter3d(ax, iko.vertices, size=size)
    plot_iko_faces(ax, base)

    ax = fig.add_subplot(2, 2, 3, projection="3d")
    points = iko.normalized_points()

    plot_scatter3d(ax, points, size=size)
    _surface_spere(ax, r=0.98, alpha=0.2, color="gray")

    # gleichschenkelig
    iko.vertices = np.array([[0, 0, 0], [0, 2, 0], [2, 1, 0]])
    iko.tri = np.array([iko.vertices])

    iko.subdivide(n=2 * n)

    ax = fig.add_subplot(2, 2, 4)
    x = iko.vertices[:, 0]
    y = iko.vertices[:, 1]
    ax.scatter(x, y, color="r", s=10)

    plt.show()


if __name__ == "__main__":
    _test_subdivision()
