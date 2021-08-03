import numpy as np
from random import *
import matplotlib.pyplot as plt
import math
import src.graph.visu_sol as vis


def create_point(r, theta, phi) -> np.array:
    arr = np.array([0.0, 0.0, 0.0])
    arr[0] = r * math.sin(theta) * math.cos(phi)
    arr[1] = r * math.sin(theta) * math.sin(phi)
    arr[2] = r * math.cos(theta)
    return arr


def create_random_point() -> np.array:
    theta = random() * 2 * math.pi
    x = random() * 2 - 1
    phi = np.arccos(x)

    arr = np.array([0.0, 0.0, 0.0])
    arr[0] = np.cos(theta) * np.sin(phi)
    arr[1] = np.sin(theta) * np.sin(phi)
    arr[2] = np.cos(phi)

    # arr[0] = np.cos(phi) * np.sqrt(1 - np.arcsin(x) * np.arcsin(x) / (np.pi * np.pi))
    # arr[1] = np.sin(phi) * np.sqrt(1 - np.arcsin(x) * np.arcsin(x) / (np.pi * np.pi))
    # arr[2] = np.arcsin(x) / np.pi
    return arr


def create_random_point_old() -> np.array:
    theta = random() * 2 * math.pi
    phi = random() * math.pi

    return create_point(1, theta, phi)


def add_points_to_plot(points, color):
    for p in points:
        vis.add_point(p[0], p[1], p[2], color=color, size=10)


def add_sphere():
    vis.surface_spere(
        r=1, alpha=0.2, resolution_theta=40j, resolution_phi=20j, color="silver"
    )


def plot_both_spheres(N=40):
    points_old = [create_random_point_old() for _ in range(N)]
    points = [create_random_point() for _ in range(N)]

    add_sphere()
    add_points_to_plot(points_old, "red")
    vis.ax = vis.fig.add_subplot(1, 2, 2, projection="3d")

    add_sphere()
    add_points_to_plot(points, "yellow")
    # actually showing the plot
    vis.plot_show()


def plot_heat_circle(ax, N=10_000,size=1):
    phi = np.linspace(start=0,stop=2*np.pi,num=N)
    xs = np.cos(phi)
    ys = np.sin(phi)
    ax.scatter(xs,ys,color="gray",s=size,alpha=0.2)


def plot_heat_map(fig, points, i, name, color="r", size=5,alpha =0.5 ):
    arr = np.array(points)
    xs = arr[:, 0]
    ys = arr[:, 1]
    zs = arr[:, 2]

    ax1 = fig.add_subplot(2, 2, i )
    ax1.set_title(name + " y - z")
    ax1.set_xlabel("y")
    ax1.set_ylabel("z")

    ax2 = fig.add_subplot(2, 2, i +1 )
    ax2.set_title(name + " y - x")
    ax2.set_xlabel("y")
    ax2.set_ylabel("x")
    
    
    plot_heat_circle(ax1)
    ax1.scatter(ys,zs, color=color,s=size, alpha= alpha)

    plot_heat_circle(ax2)
    ax2.scatter(ys,xs, color=color,s=size, alpha = alpha)

    # for x in xs:
    #     for y in ys:
    #         print(x,y)

    #         ax1.scatter(x, y, color=color, s=size)
    #         ax2.scatter(y, x, color=color, s=size)
    pass


def plot_heat_maps(N=100, size= 1, alpha= 1):
    points_old = [create_random_point_old() for _ in range(N)]
    points = [create_random_point() for _ in range(N)]

    fig = plt.figure()

    plot_heat_map(fig, points_old, 1, name="Intuitive Verteilung",color="r",size=size, alpha = alpha)
    plot_heat_map(fig, points, 3, name ="Echte Gleichmäßige Verteilung",color="b",size=size, alpha = alpha)
    plt.show()

    pass


# plot_both_spheres()
plot_heat_maps(100_000, size=0.5, alpha=0.1)




# def plot_heat_map(fig, points, row):
#     arr = np.array(points)
#     x = arr[:, 0]
#     y = arr[:, 0]
#     z = arr[:, 0]

#     plt.subplot(row, 1, aspect=1)
#     heatmap, xedges, yedges = np.histogram2d(x, y, bins=(64, 64))
#     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#     # Plot heatmap
#     plt.clf()
#     plt.ylabel("y")
#     plt.xlabel("x")
#     plt.imshow(heatmap, extent=extent)

#     plt.subplot(row, 2, aspect=1)
#     heatmap, xedges, yedges = np.histogram2d(y, z, bins=(64, 64))
#     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#     # Plot heatmap
#     plt.clf()
#     plt.ylabel("z")
#     plt.xlabel("y")
#     plt.imshow(heatmap, extent=extent)

#     pass


# def plot_heat_maps(N=100):
#     points_old = [create_random_point_old() for _ in range(N)]
#     points = [create_random_point() for _ in range(N)]

#     fig = plt.figure(figsize=(2, 2))

#     plot_heat_map(points_old, 1)
#     plot_heat_map(points, 2)
#     plt.show()

#     pass
