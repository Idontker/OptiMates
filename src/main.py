import os
print(os.getcwd())

from functools import partial
from src.graph import solution
from src.greedy.greedysearch import GreedySearch
from src.graph.graph import Graph
from src.graph.solution import Solution
import src.graph.graph as graph
import src.setupLogger
import src.validator
import logging
import math
import time


#########################
#########################
###### Constants ########
#########################
#########################

src.setupLogger.setup("Run main.py")

R = 1
r = 70.6  # deg
r = math.radians(r)
logging.info(r)

N = 1000

#########################
#########################
##### Create Graph ######
#########################
#########################

starttime = time.time()

g = graph.create_default_graph_with_random_points(
    sphere_radius=R, number_of_nodes=N, radius=r
)

timediff = time.time() - starttime
logging.info(
    "time for graph creation: {}::{}::{}    [min:sec:ms]".format(
        math.trunc(timediff / 60),
        math.trunc(timediff % 60),
        math.trunc((timediff - math.trunc(timediff)) * 1000),
    )
)

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

gs = GreedySearch()

s =  gs.findSolution(myPrinter)

logging.info(s)

