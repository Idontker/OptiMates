import numpy as np
from random import *
import numpy as np
import math
import src.graph.visu_sol as vis
import src.checker.checker as checker
from matplotlib import pyplot as plt


durchmeser = 2*1.75  # deg
d = math.radians(durchmeser)
radius = durchmeser / 2
r = math.radians(radius)

N = 20000
solutionFilePath = ".\\sols\\solution_" + str(N) + "_" + str(durchmeser) + "_01.csv"
# solutionFilePath = ".\\sols\\solution_10000_180_optimal.csv"
# solutionFilePath = ".\\sols\\solution_" + str(10000) + "_" + str(180) + "_02.csv"

# Lies die Lösung ein
solution = np.genfromtxt(solutionFilePath, delimiter=";")

vis.surface_spere(
    r=1, alpha=0.2, resolution_theta=40j, resolution_phi=20j, color="silver"
)
# colors = ["royalblue", "indigo", "green", "lime"]
colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
]

colors = [
    "black",
    "gray",
    "silver",
    "rosybrown",
    "firebrick",
    "red",
    "darkred"
]


i = 0
# for p in solution:
#     # print(i)
#     vis.add_point(p[0], p[1], p[2], color=colors[i % len(colors)])
#     # vis.kugelkappe(p[0],p[1],p[2],math.radians(30))
#     vis.kugelkappe(p[0], p[1], p[2], r, resolution=100j, color=colors[i % len(colors)])
#     i = i + 1

# # Überprüfe die Lösung

# Lies die Lösung ein
check_solution = checker.readSolution(solutionFilePath)
print("Durchmesser:", durchmeser)
for p in check_solution:
    print(p)
missing = checker.checkSolution(check_solution, durchmeser)
if missing is not None:
    print(missing)
    vis.add_point(missing[0], missing[1], missing[2], color="b", size=100)

# actually showing the plot
# vis.plot_show()

#############################################
#############################################
#############################################


def check_distances(missing: np.array):

    dist = np.dot(solution, np.transpose(missing))
    raddist = np.arccos(dist)
    winkeldist = np.degrees(raddist)

    print("Öffnungswinkel: ", durchmeser, "° == ", d)
    print("Öffnungsradius: ", radius, "° == ", r)
    print()
    print("rad distanzen: ")
    print(raddist)
    print()
    print("winkel distanzen: ")
    print(winkeldist)
    print()
    print("distances: ")
    print(dist)

    print(solution)


# missing = np.array([-0.6941044750530672, 0.2631523439968591, -0.670052528029299])
# check_distances(missing)
