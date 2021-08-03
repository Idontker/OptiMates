import numpy as np
from random import *
import numpy as np
import math
import src.graph.visu_sol as vis
import three_sphere_intersection as intersect
import timeit


durchmeser = 20 * 2  # deg
d = math.radians(durchmeser)
radius = durchmeser / 2
r = math.radians(radius)
dist = 2 * np.arcsin(np.sqrt(3) / 2 * r)

# angels of the secound point
p0 = np.array([0, 0, 1])
# theta, phi = math.radians(45), np.pi / 2
theta, phi = dist, np.pi / 2


def toCart(phi, theta):
    x = np.sin(theta) * np.sin(phi)
    y = np.sin(theta) * np.cos(phi)
    z = np.cos(theta)
    return np.array([x, y, z])


def place_kappe(p, color, res):
    vis.add_point(p[0], p[1], p[2], color=color)
    vis.kugelkappe(p[0], p[1], p[2], r, resolution=res, color=color)


# colors for plotting
colors = ["royalblue", "indigo", "green", "lime"]
i = 0


ps = [p0, toCart(phi, theta)]


# Wiederhole n mal:
#   Zeichne alle bereits bekannten Knoten in grau
#   > berechne alle Kinder aus den Eltern
#   > füge alle neuen Paare zur neuen Elternliste hinzu (je ein Elterknoten und ein Kind)
#   zeichne die Kinder in rot
#   aktualisiere die Listen ps mit allen gefunden Knoten und die Elternpaareliste
n = 3
resolution = 40j

parent_list = [[ps[0], ps[1]]]
for i in range(n):
    vis.create_subfig(1, n, i + 1)
    # plot sphere
    vis.surface_spere(
        r=1, alpha=0.2, resolution_theta=40j, resolution_phi=20j, color="silver"
    )
    # plot old points
    for p in ps:
        place_kappe(p, "gray", resolution)

    new_parents = []
    kids = []

    # vis.plot_show()
    dic = {}

    for parents in parent_list:
        u, v = intersect.find_aequidist_points_on_sphere(
            parents[0], parents[1], dist, deg=False
        )
        dic[sum(u)] = parents
        dic[sum(v)] = parents
        # print(parents[0], parents[1], "\tu:", u, "\tv:", v)
        kids.append(u)
        kids.append(v)
        new_parents.append([parents[0], u])
        new_parents.append([parents[1], u])
        new_parents.append([parents[0], v])
        new_parents.append([parents[1], v])
    parent_list = new_parents
    # plot kids and sort out duplicates
    tmp = []
    for kid in kids:
        duplicate = False
        for p in ps:
            if np.linalg.norm(p - kid) < 1e-4:
                # print("kid: ", kid, "\tp:", p)
                # print("dist:", np.linalg.norm(p - kid))
                duplicate = True
            pass
        if duplicate is not True:
            tmp.append(kid)
            parents = dic[sum(kid)]
            print("parents:\t", parents[0], parents[1])
            print("kid:\t\t", kid)
            print(
                "distance:\t",
                np.linalg.norm(parents[0] - kid),
                np.linalg.norm(parents[1] - kid),
            )
            place_kappe(kid, "red", resolution)
    # now add all new kids to ps
    for kid in tmp:
        ps.append(kid)
        print(kid)

    print(40 * "===")
    pass

# p = [ 0.17031878, 0.19488153, 0.96592583]
# vis.add_point(p[0], p[1], p[2], color="green")
# p = [0.17031878, -0.19488153  ,  0.96592583]
# vis.add_point(p[0], p[1], p[2], color="green")


# actually showing the plot
vis.plot_show()
