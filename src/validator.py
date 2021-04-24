from numpy import genfromtxt
from sphere import pointOnSphere as pos
import numpy as np
import math
import os
import time
import logging
from tqdm import tqdm


# TODO: return a list with points read in the solutionFile
def load_data(path, seperator, radial, polar):
    input = genfromtxt(os.getcwd() + "/" + path, delimiter=seperator)

    sols = list()
    for row in input:
        if np.size(row) != 3:
            logging.warning("Solution contains wrongly formated inputs: " + str(row))
            continue
        elif radial:
            if polar:
                theta = math.radians(row[1])
            else:
                theta = row[1]
            if polar:
                phi = math.radians(row[2])
            else:
                phi = row[2]
            p = pos.point(row[0], theta, phi)
        else:
            p = pos.point(row[0], row[1], row[2], polar=False)
        sols.append(p)
        logging.debug("Added to solution: " + str(p))
    return sols


def validate(solution, r, R, n):
    starttime = time.time()
    #logging.info("starttime: " + str(time))

    pointsCovered = 0
    for i in tqdm(range(0, n), mininterval=0.1, miniters=0):
    # for i in range(0, n):
        p = pos.generateRandomPointOnSphere(R)

        covered = False

        for v in solution:
            if pos.dist(v, p) < r:
                covered = True
                # logging.debug("covered" + str(p))
                pointsCovered = pointsCovered + 1
                break
        if covered == False:
            logging.warning("NOT covered" + str(p))
    percent = pointsCovered / n
    timediff = time.time() - starttime
    logging.info(
        "accurcy: {}\t covered: {} out of {} points".format(percent, pointsCovered, n)
    )
    logging.info("time of validation: " + str(timediff))

def validateSolutionCSV(
    solutionPath="solution.csv",
    seperator=" ",
    R=1,
    delta=3.5 / 2,
    radial=False,
    polar=False,
    sampleSize=1_000,
):
    sol = load_data(solutionPath, seperator, radial=radial, polar=polar)
    if radial == False:
        delta = math.radians(delta)

    validate(solution=sol, r=delta, R=R, n=sampleSize)
