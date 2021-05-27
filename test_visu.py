import numpy as np
from random import *
import numpy as np
import math
import src.graph.visu_sol as vis


durchmeser = 15*2  # deg
d = math.radians(durchmeser)
radius = durchmeser / 2
r = math.radians(radius)


def toCart(phi, theta):
    x = np.sin(theta) * np.sin(phi)
    y = np.sin(theta) * np.cos(phi)
    z = np.cos(theta)
    return np.array([x, y, z])


def place_kappe(p, color, res):
    vis.add_point(p[0], p[1], p[2], color=color)
    vis.kugelkappe(p[0], p[1], p[2], r, resolution=res, color=color)


vis.surface_spere(
    r=1, alpha=0.2, resolution_theta=40j, resolution_phi=20j, color="silver"
)
colors = ["royalblue", "indigo", "green", "lime"]
i = 0

resolution = 50j

p = [0, 0, 1]
place_kappe(p, color=colors[i], res=resolution)

theta = math.radians(20) # 2 * np.arcsin(np.sqrt(3) / 2 * r)
phis = np.array([np.pi/2])# np.linspace(0, 2 * np.pi, 6)
i = 1
for phi in phis:
    p = toCart(phi,theta)
    place_kappe(p, color=colors[i], res=resolution)

p = [ 0.17031878, 0.19488153, 0.96592583]
vis.add_point(p[0], p[1], p[2], color="green")
p = [0.17031878, -0.19488153  ,  0.96592583]
vis.add_point(p[0], p[1], p[2], color="green")

# actually showing the plot
vis.plot_show()
