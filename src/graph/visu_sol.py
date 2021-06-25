from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations


fig = plt.figure()
# ax = fig.gca(projection="3d")
ax = None
# ax = fig.add_subplot(1, 2, 1, projection="3d") TODO changed initial picture
# ax.set_aspect("auto")

# # draw cube
# r = [-1, 1]
# for s, e in combinations(np.array(list(product(r, r, r))), 2):
#     if np.sum(np.abs(s-e)) == r[1]-r[0]:
#         ax.plot3D(*zip(s, e), color="b")


def create_subfig(row, col, place):
    global ax
    ax = fig.add_subplot(row, col, place, projection="3d")


def wiresphere_spere(
    resolution_theta: int = 20j, resolution_phi: int = 10j, color="black"
) -> None:
    # draw sphere
    u, v = np.mgrid[0 : 2 * np.pi : resolution_theta, 0 : np.pi : resolution_phi]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color=color)


def surface_spere(
    r=1, alpha=1, resolution_theta=20j, resolution_phi=10j, color="black"
) -> None:
    # draw sphere
    u, v = np.mgrid[0 : 2 * np.pi : resolution_theta, 0 : np.pi : resolution_phi]
    x = r * np.cos(u) * np.sin(v)
    y = r * np.sin(u) * np.sin(v)
    z = r * np.cos(v)
    ax.plot_surface(x, y, z, color=color, alpha=alpha)


def add_point(x, y, z, color="g", size=50,alpha=1):
    ax.scatter(x, y, z, color=color, s=size,alpha=alpha)


def kugelkappe(x, y, z, r, resolution=20j, color="g"):
    M = np.array([x, y, z])
    if y == 0 and z == 0:
        e1 = np.array([0, 1, 0])
        e2 = np.array([0, 0, 1])
    else:
        e1 = np.array([0, z, -y])

        A = np.array([M, e1, [1, 0, 0]])
        B = np.array([0, 0, 1])

        e2 = np.linalg.solve(A, B)

    M = M * np.cos(r)
    e1 = e1 / (np.sum(e1 ** 2) ** 0.5)
    e2 = e2 / (np.sum(e2 ** 2) ** 0.5)

    a = np.sin(r)

    phi_arr = np.mgrid[0 : 2 * np.pi : resolution]

    px = M[0] + a * np.cos(phi_arr) * e1[0] + a * np.sin(phi_arr) * e2[0]
    py = M[1] + a * np.cos(phi_arr) * e1[1] + a * np.sin(phi_arr) * e2[1]
    pz = M[2] + a * np.cos(phi_arr) * e1[2] + a * np.sin(phi_arr) * e2[2]

    # p = [M + a * np.cos(phi) * e1 + a * np.sin(phi) * e2 for phi in phi_arr]
    # print(p[0])
    # print(p[1])
    # print(p[2])
    # print()
    # ax.plot_surface(p, color="g", alpha=0.5)
    ax.scatter(px, py, pz, color=color, s=10)
    # sax.scatter(px, py, pz, color=color, s=10)

    # ax.scatter(x, y, z, color="g", s=10)


# draw a point
# ax.scatter([0], [0], [0], color="g", s=100)
def plot_show():
    plt.show()
