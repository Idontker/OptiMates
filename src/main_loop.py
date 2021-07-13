import math
import solver
import csv
import numpy as np
from tqdm import tqdm


# TODO: make it fast: https://stackoverflow.com/questions/50615262/what-is-the-fastest-way-to-xor-a-lot-of-binary-arrays-in-python


R = 1
durchmeser = 2 * 8  # deg
r_deg = durchmeser / 2
r = math.radians(r_deg)

# N = 1_000
seperation_step = 1

exploration_factor = 1.8
intersection_bruch = 0.2

# N = 500_000
# step_prct = 0.065
# seperation_step = 0.1

# N = 2_000_000
# seperation_step = 0.065


path = ".\\logs\\testing_count_ " + str(durchmeser) + ".csv"

lens = []
added = []
times = []
Ns = np.linspace(500, 50_000, 41).astype(np.int)
kappenanteil = (1 - np.cos(r))/2 


for n in Ns:
    solutionFilePath = ".\\sols\\solution_" + str(n) + "_" + str(durchmeser) + "_01"
    solution_log_FilePath = (
        ".\\logs\\solution_log" + str(n) + "_" + str(durchmeser) + "_01.csv"
    )

    dichte = n * kappenanteil
    
    intersection_weight = dichte * intersection_bruch

    ret = solver.solve(
        r_deg=r_deg,
        N=n,
        intersection_weight=intersection_weight,
        exploration_factor=exploration_factor,
        seperation_step=seperation_step,
        solutionFilePath=solutionFilePath,
        solution_log_FilePath=solution_log_FilePath,
        save_it = False
    )

    lens.append(ret[0])
    added.append(ret[1])
    times.append(ret[2])


csv_writer = csv.writer(
    open(file=path, mode="w", newline=""), delimiter=";"
)

csv_writer.writerow(["N", "dichte", "size", "added", "time used"])

kappenanteil = (1 - np.cos(r))/2 
for i in range(len(Ns)):
    dichte = Ns[i] * kappenanteil
    csv_writer.writerow([Ns[i], dichte, lens[i], added[i],times[i]])
    # if type(p) is np.ndarray:
    #     writer_solution.writerow([p[0], p[1], p[2]])
    # else:
    #     writer_solution.writerow([p[0], p[1], p[2].replace("\n", "")])
    # pass
