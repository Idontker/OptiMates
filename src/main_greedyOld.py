from functools import partial
from graph import solution
from greedy.greedysearch import GreedySearch
from graph.graph import Graph
from graph.graph2 import Graph2
from graph.solution import Solution
import graph.graph as graph
import setupLogger
import validator
import logging
import math
import time
import numpy as np


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
durchmeser = 70.6  # deg
durchmeser = 360  # deg
r = math.radians(durchmeser / 2)
logging.info("durchmeser:" + str(math.radians(durchmeser)) +"\tr/2:" + str(r))

N = 10_000

# graph_path = None
graph_path = ".\\graphsave\\graphsave_" + str(N) +"_" + str(durchmeser) + "_01"

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

g = graph.load_graph_from(path=graph_path, radius=r)

if g is None:
    g = graph.create_default_graph_with_random_points(
        sphere_radius=R, number_of_nodes=N, radius=r
    )
    g.save(graph_path)

timediff = time.time() - starttime
log_time("graph creation", timediff)

#########################
#########################
####### SOLVE IT ########
#########################
#########################


def printer(index: int, sol: Solution, stepsize: int = 100):
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


myPrinter = partial(printer, stepsize=1)


starttime = time.time()

gs = GreedySearch(graph=g)
s = gs.findSolution(myPrinter)

timediff = time.time() - starttime
log_time("greedy search", timediff)


logging.info(s)
