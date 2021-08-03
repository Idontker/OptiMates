import math
import solver
import numpy as np



### Paramas to set

durchmeser = 2 * 13  # deg
N = 20_000
seperation_step = 0.8
intersection_bruch = 0.2

### Fixed Paramas

R = 1
r_deg = durchmeser / 2
r = math.radians(r_deg)

exploration_factor = 1.8

kappenanteil = (1 - np.cos(r)) / 2
dichte = N * kappenanteil
intersection_weight = dichte * intersection_bruch

# intersection_weight = 10

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
    save_it=True,
)
