import math
import numpy as np
import argparse

# Setup the parser of the arguments

parser = argparse.ArgumentParser()

# required arguments
parser.add_argument("N", help="integer - number of nodes to be used")
parser.add_argument(
    "radian", help="float within 0 and 360° - radian of a spherical segment in degree"
)
parser.add_argument(
    "stepsize",
    help="float within 0 and 1 - step size of the adaptive solution generation in percent",
)

# optional
parser.add_argument(
    "-w",
    "--weight",
    default=100 / 513,
    help="float greater or equal to zero - intersection weight in percent of the pointdensity of a spherical segment",
)
parser.add_argument(
    "-e",
    "--exploration",
    default=1.8,
    help="float greater or equal to zero - exploration factor that is mutiplied with the radius to determine how large the distance of the surrounding nodes under consideration is",
)
parser.add_argument(
    "-p", "--path", default=".\\", help="path to the save location (excluding filename)"
)
parser.add_argument(
    "-l",
    "--logpath",
    default=".\\",
    help="path to the save location of the log file (excluding filename)",
)

# activate arg parsing - if -h is set, it prints out the help
args = parser.parse_args()


# set required params
N = int(args.N)
r_deg = float(args.radian)
seperation_step = float(args.stepsize)

# set optional params
exploration_factor = float(args.exploration)
intersection_bruch = float(args.weight)

solutionFilePath = args.path + "solution_" + str(N) + "_" + str(r_deg * 2)
solution_log_FilePath = (
    args.logpath + "\\solution_log" + str(N) + "_" + str(r_deg * 2) + ".csv"
)


### Fixed Paramas

R = 1
durchmeser = 2 * r_deg  # deg
r = math.radians(r_deg)

kappenanteil = (1 - np.cos(r)) / 2
dichte = N * kappenanteil
intersection_weight = dichte * intersection_bruch
# imports solver and triggers the logging setup

import solver

ret = solver.solve(
    r_deg=r_deg,
    N=N,
    intersection_weight=intersection_weight,
    exploration_factor=exploration_factor,
    seperation_step=seperation_step,
    solutionFilePath=solutionFilePath,
    solution_log_FilePath=solution_log_FilePath,
    save_it=True,
)
