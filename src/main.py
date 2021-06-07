from functools import partial
from geometrics.ikosaeder import EPSILON
from greedy.greedysearch import GreedySearch
from graph.graph import Graph
from graph.solution import Solution
import graph.graph as graph
import setupLogger
import logging
import math
import time
import numpy as np
import checker.checker as checker
import graph.visu_sol as vis
import sys


# TODO: make it fast: https://stackoverflow.com/questions/50615262/what-is-the-fastest-way-to-xor-a-lot-of-binary-arrays-in-python


def log_time(tastname, timediff):
    logging.info(
        'time for "{}": {}::{}::{}    [min:sec:ms]'.format(
            tastname,
            math.trunc(timediff / 60),
            math.trunc(timediff % 60),
            math.trunc((timediff - math.trunc(timediff)) * 1000),
        )
    )


#########################
#########################
###### Constants ########
#########################
#########################

setupLogger.setup("Run main.py")

R = 1
durchmeser = 2 * 70.6  # deg
r = math.radians(durchmeser / 2)
logging.info("durchmeser:" + str(math.radians(durchmeser)) + "\tr/2:" + str(r))


N = 40_000

save = False
# graph_path = None
graph_path = ".\\graphsave\\graphsave_" + str(N) + "_" + str(durchmeser) + "_01"
solutionFilePath = ".\\sols\\solution_" + str(N) + "_" + str(durchmeser) + "_01.csv"

# savety first
# EPSILON = 0.01
# r = math.radians(durchmeser * (1 - EPSILON) / 2)

## Berechne Besetzungsgrad
# g = graph.load_graph_from(path=graph_path, radius=r)
# mat = g.adjmatrix
# nonzero = np.count_nonzero(mat)
# print(g.nodes)
# print(mat)
# print(np.shape(mat))
# print(nonzero/(np.shape(mat)[0] * np.shape(mat)[1]))
# quit()


#########################
#########################
##### Create Graph ######
#########################
#########################

starttime = time.time()

g = graph.load_graph_from(filepath=graph_path)

if g is None:
    g = Graph(cover_radius=r, exploration_factor=math.sqrt(3), number_of_points=N)
    ### Random points version
    # g.gen_random_points()

    ### Archimedische Spirale
    # g.gen_archimedic_spiral(N=N, speed=2000, lower_bound=-1, upper_bound=1)

    ### Bauers spirale Spirale
    g.gen_bauer_spiral(N=N)

    ####Ikosaeder version
    # g.gen_iko_points(divisions=6)
    # N = g.number_of_points
    # print("number of nodes:", g.number_of_points)
    
    if N <= 15_000: 
        steps = 1
    else: 
        steps = 1 + int(N/10_000)
    print("Steps used:", steps)
    g.update_all_neighbours(steps=steps)
    if save:
        graph.save(g2=g, filepath=graph_path)

timediff = time.time() - starttime
log_time("graph creation", timediff)

# vis.surface_spere()
# for p in g.points:
#     vis.add_point(p[3],p[4],p[5])
# vis.plot_show()

#########################
#########################
####### SOLVE IT ########
#########################
#########################


def printer(index: int, sol: Solution, stepsize: int = 100, stepsize_ram: int = 10):
    if index % stepsize == 0:
        logging.debug(
            "step: "
            + str(index)
            + "\t"
            + "covered: "
            + str(sol.countCoveredNodes())
            + "\tof "
            + str(N)
        )
    if index % stepsize_ram == 1:
        g_size = sys.getsizeof(g)
        logging.debug(
            # "used spac: {:.3e} MB|\t{:.3e} MB per individual|\t{:.3e} MB/N".format(
            "used spac: {:.3e} MB|\t{:.3e} MB/N".format(
                g_size / (1024 ** 2),
                # sys.getsizeof(g) / (1024 ** 2) / len(g.adj_neighbour_dic),
                g_size / (1024 ** 2) / N,
            )
        )


myPrinter = partial(printer, stepsize=1)


starttime = time.time()

gs = GreedySearch(graph=g)
s = gs.findSolution(myPrinter)

timediff = time.time() - starttime
log_time("greedy search", timediff)


logging.info(s)
s.save(solutionFilePath)

#########################
#########################
####### CHECK SOL #######
#########################
#########################

# Lies die Lösung ein
solution = checker.readSolution(solutionFilePath)
print("Durchmesser:", durchmeser)
logging.info("Solution for {}:".format(durchmeser))
# for p in solution:
#     logging.info(p)

# int um die loecher zu zaehlen
added = 0

# looking for missing points with "do while"
while True:
    arr = checker.checkSolution(solution, durchmeser, printing=False)
    if arr is None:
        break
    else:
        added = added + 1
        solution.append(arr)

logging.info("=========DONE=========")
logging.info("Due to holes additionally added points {}".format(added))
logging.info("Number of needed shperical caps: {}".format(len(solution)))
# Überprüfe die Lösung
checker.checkSolution(solution, durchmeser)