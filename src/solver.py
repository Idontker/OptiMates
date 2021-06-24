from geometrics.ikosaeder import EPSILON
from greedy.greedysearch import GreedySearch
from graph.graph import Graph
import setupLogger
import logging
import math
import time
import checker.checker as checker
import csv
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

setupLogger.setup("solver loaded - logging setup startet")

solution = None


def get_solution():
    global solution
    return solution


def check_and_extend_solution(solutionFilePath, durchmesser):
    # Lies die Lösung ein
    sol = checker.readSolution(solutionFilePath)
    logging.info("Solution for {}:".format(durchmesser))

    # int um die loecher zu zaehlen
    added = 0

    # looking for missing points with "while"

    while True:
        starttime = time.time()
        arr = checker.checkSolution(sol, durchmesser, printing=False)
        diff = time.time() - starttime
        if arr is None:
            break
        else:
            added = added + 1
            sol.append(arr)
            logging.info("added:{}\ttime used:{}".format(added, diff))

    logging.info("=========DONE=========")
    logging.info("Due to holes additionally added points {}".format(added))
    logging.info("Number of needed shperical caps: {}".format(len(sol)))
    # Überprüfe die Lösung
    checker.checkSolution(sol, durchmesser)

    return sol, len(sol), added


def solve(r_deg, N, intersection_weight, exploration_factor, solutionFilePath):
    R = 1
    durchmesser = 2 * r_deg
    r = math.radians(r_deg)
    logging.info("durchmesser:" + str(math.radians(durchmesser)) + "\tr/2:" + str(r))

    #########################
    #########################
    ##### Create Graph ######
    #########################
    #########################

    starttime = time.time()

    g = Graph(
        cover_radius=r,
        exploration_factor=exploration_factor,
        number_of_points=N,
        intersection_weight=intersection_weight,
    )

    ### Random points version
    # g.gen_random_points()

    ### Archimedische Spirale
    # g.gen_archimedic_spiral(N=N, speed=2000, lower_bound=-1, upper_bound=1)

    ### Bauers spirale Spirale
    g.gen_bauer_spiral(N=N)

    ### Ikosaeder version
    # g.gen_iko_points(divisions=6)
    # N = g.number_of_points
    # print("number of nodes:", g.number_of_points)

    if N <= 15_000:
        steps = 1
    else:
        steps = 1 + int(N / 10_000)

    g.update_all_neighbours(steps=steps)

    timediff = time.time() - starttime
    log_time("graph creation", timediff)

    #########################
    #########################
    ####### SOLVE IT ########
    #########################
    #########################

    starttime = time.time()

    gs = GreedySearch(graph=g)
    s = gs.findSolution(printer=None)

    timediff = time.time() - starttime
    log_time("greedy search", timediff)

    # logging.info(s)
    s.save(solutionFilePath)
    _, len_sol, added = check_and_extend_solution(solutionFilePath, durchmesser)
    return len_sol, added


if __name__ == "__main__":
    # solutionFilePath = "sols\\solution_20000_3.5_01.csv"
    # saveTo = "sols\\complete_3.5_01.csv"
    solutionFilePath = "sols\\solution_10000_74.8_01.csv"
    saveTo = "sols\\complete_74.8_01.csv"
    # durchmesser = 3.5
    durchmesser = 74.8

    try:
        sol, _, added = check_and_extend_solution(solutionFilePath, durchmesser)
    except KeyboardInterrupt:
        print("Got Interrupted - proceeding with saving")

    logging.info("added:{}".format(added))

    if saveTo is not None:
        writer_nodes = csv.writer(
            open(file=saveTo, mode="w", newline=""), delimiter=";"
        )
        for p in sol:
            if type(p) is np.ndarray:
                writer_nodes.writerow([p[0], p[1], p[2]])
            else:
                writer_nodes.writerow([p[0], p[1], p[2].replace("\n", "")])
            pass
