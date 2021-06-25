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


def printer(index: int, sol: Solution, stepsize: int = 100, stepsize_ram: int = 10):
    g = sol.graph

    if index % stepsize == 0:
        logging.debug(
            "step: {}\tcovered: {}\t of {}".format(
                index, sol.countCoveredNodes(), len(g.points)
            )
        )
        # intersects = g.intersection_neighbours
        # mids = g.mid_neighbours
        # if intersects is not None:
        #     logging.debug(
        #         "\t inter shape:{}".format(
        #             intersects.shape,
        #         )
        #     )
        # if mids is not None:
        #     logging.debug(
        #         "\t mids shape:{}".format(
        #             mids.shape,
        #         )
        #     )

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


#########################
#########################
###### Constants ########
#########################
#########################

setupLogger.setup("Run main.py")

R = 1
durchmeser = 2 * 1.75  # deg
r = math.radians(durchmeser / 2)
logging.info("durchmeser:" + str(math.radians(durchmeser)) + "\tr/2:" + str(r))


N = 20_000

intersection_weight = 1

#########################
#########################
###### Run Prog #########
#########################
#########################

# Build Points

# Seperation of points into stripes

# solve individuals