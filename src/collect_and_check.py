from graph.solution import Solution
from graph.graph import Graph
from greedy.greedysearch import GreedySearch
import setupLogger
import logging
import math
import sys
import geometrics.point_factory as factory
import geometrics.seperation as seperator
from total_solution import Total_Solution
import numpy as np
import time
import checker.checker as checker
import csv


# TODO: make it fast: https://stackoverflow.com/questions/50615262/what-is-the-fastest-way-to-xor-a-lot-of-binary-arrays-in-python


def log_time(tastname, timediff):
    total_diff = time.time() - time_ground_zero
    logging.info(
        'time for "{}": {}::{}::{}    [min:sec:ms]'.format(
            tastname,
            math.trunc(timediff / 60),
            math.trunc(timediff % 60),
            math.trunc((timediff - math.trunc(timediff)) * 1000),
        )
    )
    logging.info(
        "total time: {}::{}::{}    [min:sec:ms]".format(
            math.trunc(total_diff / 60),
            math.trunc(total_diff % 60),
            math.trunc((total_diff - math.trunc(total_diff)) * 1000),
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
###### Constants ########
#########################

setupLogger.setup("Run main.py")

R = 1
durchmeser = 2 * 1.75  # deg
r = math.radians(durchmeser / 2)
logging.info("durchmeser:" + str(math.radians(durchmeser)) + "\tr/2:" + str(r))


N = 50_000
step_prct = 0.065

seperation_step = 0.6
exploration_factor = 1.8
intersection_weight = 0.5

solutionFilePath = ".\\sols\\solution_" + str(N) + "_" + str(durchmeser) + "_01"
solution_log_FilePath = (
    ".\\logs\\solution_log" + str(N) + "_" + str(durchmeser) + "_01.csv"
)


#########################
##### Logging setup #####
#########################
import setupLogger

setupLogger.setup("Run main.py")
time_ground_zero = time.time()




#########################
#########################
####### CHECK SOL #######
#########################
#########################

# Lies die Lösung ein
solution = checker.readSolution(solutionFilePath+ "_tmp.csv")
logging.info(
    "Solution for r={}°    N={}    sep_step={} explor={}   inter_weight={}:".format(
        durchmeser / 2, N, seperation_step, exploration_factor, intersection_weight
    )
)
# custom printer for checker
def collect_printer(i, length, timediff):
    if i % 10 == 0:
        log_time("collecting missing - so far: {}   (added={})".format(length,i), timediff=timediff)
        return True
    return False

added = checker.collect_missing(solution=solution, alpha=durchmeser,n=3,printer=collect_printer)
for a in added:
    solution.append(a)

logging.info("=========DONE=========")
logging.info("Due to holes additionally added points {}".format(len(added)))
logging.info("Number of needed shperical caps: {}".format(len(solution)))
# Überprüfe die Lösung
checker.checkSolution(solution, durchmeser)

# save solution and added


writer_solution = csv.writer(
    open(file=solutionFilePath + ".csv", mode="w", newline=""), delimiter=";"
)
for p in solution:
    writer_solution.writerow([p[0], p[1], p[2]])
    pass