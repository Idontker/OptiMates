import math
import solver
import csv
import numpy as np
from tqdm import tqdm


# TODO: make it fast: https://stackoverflow.com/questions/50615262/what-is-the-fastest-way-to-xor-a-lot-of-binary-arrays-in-python


R = 1
durchmeser = 2 * 1.75  # deg
r_deg = durchmeser / 2
r = math.radians(r_deg)

N = 220_000
seperation_step = 0.8

exploration_factor = 1.8
intersection_weight = 10

# N = 500_000
# step_prct = 0.065
# seperation_step = 0.1

# N = 2_000_000
# seperation_step = 0.065

solutionFilePath = ".\\sols\\solution_" + str(N) + "_" + str(durchmeser) + "_01"
solution_log_FilePath = (
    ".\\logs\\solution_log" + str(N) + "_" + str(durchmeser) + "_01.csv"
)

ret = solver.solve(
    r_deg=r_deg,
    N=N,
    intersection_weight=intersection_weight,
    exploration_factor=exploration_factor,
    seperation_step=seperation_step,
    solutionFilePath=solutionFilePath,
    solution_log_FilePath=solution_log_FilePath,
    save_it = True
)
