import numpy as np
from random import *
import numpy as np
import math
import src.graph.visu_sol as vis
from matplotlib import pyplot as plt


durchmeser = 70.6 * 2  # deg
d = math.radians(durchmeser)
radius = durchmeser / 2
r = math.radians(radius)


def gen_archimedic_spiral(speed=100, N=1000, low=0, up=1):
    """theta in [arccos(lower_bound), arccos(upperbound)]"""

    X = np.linspace(low, up, N)
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
    return np.transpose(arr)


def toCart(phi, theta):
    x = np.sin(theta) * np.sin(phi)
    y = np.sin(theta) * np.cos(phi)
    z = np.cos(theta)
    return np.array([x, y, z])


def place_kappe(p, color, res):
    vis.add_point(p[0], p[1], p[2], color=color)
    vis.kugelkappe(p[0], p[1], p[2], r, resolution=res, color=color)


def plot_spiral(N, speed, size, color, low=-1):
    spiral = gen_archimedic_spiral(N=N, speed=speed, up=1, low=low)
    ps = np.transpose(spiral)
    vis.add_point(ps[3], ps[4], ps[5], color, size=size)


# sphere
ps = np.array(
    [
        [0.1005812632962995, 0.7690139849453359, -0.6312692772757241],
        [-0.45155342746778837, -0.1889429789446743, -0.872009204567019],
        [-0.055515123319415716, 0.5012889255406199, 0.8634972404201191],
        [0.782218307120611, -0.5812840531298045, 0.2241503280888788],
        [-0.8673569914683484, -0.14379031019924424, 0.4764621664348392],
    ]
)

colors = ["royalblue", "indigo", "green", "lime", "red"]
i = 0
resolution = 50j

# vis.create_subfig(2, 1, 1)
vis.create_subfig(1, 1, 1)
vis.surface_spere(
    r=1, alpha=0.5, resolution_theta=40j, resolution_phi=20j, color="silver"
)
for p in ps:
    vis.add_point(p[0], p[1], p[2], color=colors[i])
    place_kappe(p, color=colors[i], res=resolution)
    i = i + 1

vis.plot_show()


# for t in thetas:
#     p = toCart(10*t, t)
#     vis.add_point(p[0],p[1],p[2], "red")
# for theta in thetas:
#     p = toCart(10 * theta,theta)
#     vis.add_point(p[0], p[1], p[2], color=colors[i])
# place_kappe(p, color=colors[i], res=resolution)


vis.fig = plt.figure()

N = 10_000
ts = [10, 100, 1000]
size = 0.05
for i in range(len(ts)):
    vis.create_subfig(2, 3, i + 1)
    vis.surface_spere(
        r=1, alpha=0.5, resolution_theta=40j, resolution_phi=20j, color="silver"
    )
    plot_spiral(N, ts[i], size, "red")

for i in range(len(ts)):
    vis.create_subfig(2, 3, i + 4)
    vis.surface_spere(
        r=1, alpha=0.5, resolution_theta=40j, resolution_phi=20j, color="silver"
    )
    p = np.array([0, 0, 1])
    place_kappe(p, color="blue", res=resolution)
    plot_spiral(N, ts[i], size, "red", low=0.3)

vis.plot_show()
