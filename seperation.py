from numpy.core.function_base import linspace
import src.graph.visu_sol as vis
import numpy as np
import math


def gen_bauer_spiral(N):
    L = np.sqrt(N * np.pi)
    k = np.array(range(1, N + 1))
    z = 1 - (2 * k - 1) / N
    phi = np.arccos(z)
    theta = L * phi
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    return x, y, z


def select_strip(arr, upper_z, lower_z, epsi=0):
    """ je upper_z, lower_z und epsi in rad"""

    smaller_than_upper = arr[2] <= np.cos(upper_z)
    greater_than_lower = (
        arr[2] >= np.cos(lower_z + epsi) if lower_z + epsi < np.pi else -1
    )

    within_bounds = np.logical_and(smaller_than_upper, greater_than_lower)

    return arr[:, within_bounds]


def get_strips(arr, Z, epsi):
    s = []
    M = len(Z)
    lens = []

    for i in range(M - 1):
        tmp = select_strip(arr, Z[i], Z[i + 1], epsi)
        lens.append(len(tmp[0]))
        s.append(tmp)

    print(lens)
    return s


def new_gen(step_prct, epsi=0):
    """ 0 < step_prct < 1 """

    Z = np.array([0])

    last = 0
    while last < np.pi - 1e-10:
        if np.cos(last) - 2 * step_prct < -1:
            last = np.pi
        else:
            last = np.arccos(np.cos(last) - 2 * step_prct) - epsi
        Z = np.append(Z, last)
        pass
    return Z


def validate_Z(Z, epsi=0):

    faces = []
    for i in range(len(Z) - 1):
        low = Z[i]
        max = Z[i + 1] + epsi if Z[i + 1] + epsi < np.pi else np.pi
        face = np.cos(low) - np.cos(max)
        faces.append(face)
    print("faces[0]:", faces[0], "avg(faces)", np.average(faces))

    for i in range(len(Z) - 1):
        d = Z[i + 1] - Z[i] - epsi
        if d < -1e-11:
            print(
                "i:{}\tZ[i+1]-Z[i] - epsi >0 ? {}\t Z[i+1]-Z[i] - epsi = {}".format(
                    i, d > -1e-11, d
                )
            )
    pass


if __name__ == "__main__":
    N = 1000
    # step_prct = 0.065
    step_prct = 0.5
    # r = 1.75
    r = 13
    epsi = np.deg2rad(2 * r)
    M = math.floor(180 / epsi)

    Z = new_gen(step_prct, epsi)
    validate_Z(Z, epsi)

    # print(Z)
    # print("epsi: ", 2 * r, " deg", "  =  ", epsi, "rad")

    x, y, z = gen_bauer_spiral(N)
    arr = np.array([x, y, z])

    strips = get_strips(arr, Z, epsi)

    ##########
    ## PLOT ##
    ##########

    size = 10
    alpha_sphere = 0.8
    alpha = 0.4

    s = strips[0]
    vis.create_subfig(2, 2, 1)
    vis.ax.view_init(0, 0)

    vis.surface_spere(r=1, alpha=alpha_sphere, color="gray")
    vis.add_point(s[0], s[1], s[2], color="r", size=size, alpha=alpha)
    s = strips[1]
    vis.add_point(s[0], s[1], s[2], color="b", size=size, alpha=alpha)
    s = strips[2]
    vis.add_point(s[0], s[1], s[2], color="g", size=size, alpha=alpha)

    s = strips[0]
    vis.create_subfig(2, 2, 2)
    vis.ax.view_init(0, 0)
    vis.surface_spere(r=1, alpha=alpha_sphere, color="gray")
    vis.add_point(s[0], s[1], s[2], color="r", size=size, alpha=alpha)

    s = strips[1]
    vis.create_subfig(2, 2, 3)
    vis.ax.view_init(0, 0)

    vis.surface_spere(r=1, alpha=alpha_sphere, color="gray")
    vis.add_point(s[0], s[1], s[2], color="b", size=size, alpha=alpha)

    s = strips[2]
    vis.create_subfig(2, 2, 4)
    vis.ax.view_init(0, 0)

    vis.surface_spere(r=1, alpha=alpha_sphere, color="gray")
    vis.add_point(s[0], s[1], s[2], color="g", size=size, alpha=alpha)

    vis.plot_show()
    pass