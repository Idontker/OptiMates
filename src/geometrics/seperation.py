import graph.visu_sol as vis
import numpy as np
import logging


def _gen_bauer_spiral(N):
    L = np.sqrt(N * np.pi)
    k = np.array(range(1, N + 1))
    z = 1 - (2 * k - 1) / N
    phi = np.arccos(z)
    theta = L * phi
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    return x, y, z


def _select_strip(arr, upper_z, lower_z, epsi=0, z_index=2):
    """ je upper_z, lower_z und epsi in rad"""

    smaller_than_upper = arr[z_index] <= np.cos(upper_z)
    greater_than_lower = (
        arr[z_index] >= np.cos(lower_z + epsi) if lower_z + epsi < np.pi else -1
    )

    within_bounds = np.logical_and(smaller_than_upper, greater_than_lower)

    return arr[:, within_bounds]


def _get_stripes(arr, Z, epsi, z_index=2):
    s = []
    M = len(Z)
    lens = []

    for i in range(M - 1):
        tmp = _select_strip(arr, Z[i], Z[i + 1], epsi, z_index=z_index)
        lens.append(len(tmp[0]))
        s.append(tmp)

    logging.info(lens)
    return s


def _new_gen(step_prct, epsi=0):
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


def _validate_Z(Z, epsi=0):
    faces = []
    for i in range(len(Z) - 1):
        low = Z[i]
        max = Z[i + 1] + epsi if Z[i + 1] + epsi < np.pi else np.pi
        face = np.cos(low) - np.cos(max)
        faces.append(face)
    logging.info("faces[0]: {}\tavg(faces): {}:".format(faces[0], np.average(faces)))
    pass


def create_stripes(points, r, step_prct, z_index=2):
    epsi = 2 * r
    # append labels to points
    labels = np.array(range(len(points[0])))
    combined = np.vstack((points, labels))

    Z = _new_gen(step_prct, epsi)
    _validate_Z(Z, epsi)

    ### Normale Zerlegung
    # points and labels combined ==> extract them
    combined_stripes = _get_stripes(combined, Z, epsi, z_index)
    ret_labels = []
    stripes = []
    for stripe in combined_stripes:
        ret_labels.append(stripe[-1].astype(int))
        stripes.append(stripe[0:-1])

    ### Delete Zerlegung: Welche Überschnittenen Lösungen sollen in der nächsten Interation
    # erneut berechnet werden?
    # TODO: code doppelung ?
    delete_labels = []
    for i in range(1, len(Z) - 1):
        # Aussname: letzte Stripe soll vollständig übernommen werden
        up_z = Z[i] + epsi / 2
        low_z = Z[i] + epsi
        tmp = labels[
            (points[z_index] <= np.cos(up_z)) & (points[z_index] >= np.cos(low_z))
        ]
        # print(tmp)
        delete_labels.append((tmp[0], tmp[-1]))
        pass
    # print(delete_labels)

    return stripes, ret_labels, delete_labels


if __name__ == "__main__":
    N = 1000
    # step_prct = 0.065
    step_prct = 0.5
    # r = 1.75
    r = 13
    epsi = np.deg2rad(r)

    Z = _new_gen(step_prct, epsi)
    _validate_Z(Z, epsi)

    # print(Z)
    # print("epsi: ", 2 * r, " deg", "  =  ", epsi, "rad")

    x, y, z = _gen_bauer_spiral(N)
    arr = np.array([x, y, z])

    strips = _get_stripes(arr, Z, epsi)

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