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


#########################
##### Logging setup #####
#########################
setupLogger.setup("Run main.py")

time_ground_zero = time.time()


R = 1
durchmeser = 2 * 13  # deg
r = math.radians(durchmeser / 2)


# N = 500_000
# step_prct = 0.065
# seperation_step = 0.1

N = 2_000_000
seperation_step = 0.065


exploration_factor = 1.8
intersection_weight = 10

solutionFilePath = ".\\sols\\solution_" + str(N) + "_" + str(durchmeser) + "_01"
solution_log_FilePath = (
    ".\\logs\\solution_log" + str(N) + "_" + str(durchmeser) + "_01.csv"
)

logging.info(
    "Start greedy for r={}°    N={}    sep_step={} explor={}   inter_weight={}:".format(
        durchmeser / 2, N, seperation_step, exploration_factor, intersection_weight
    )
)



#########################
###### Run Prog #########
#########################

##### Build Points ######

starttime = time.time()
# ## random
# points = factory.gen_random_points(N)

# ## iko
# points = factory.gen_iko_points(divisions=5)

# ## alchimeds
# points = factory.gen_archimedic_spiral(speed=500, N=N)

# ## bauer
points = factory.gen_bauer_spiral(N)

log_time("point factory", time.time() - starttime)


##### Gen Stripes ######
# Seperation of points into stripes / chunks

starttime = time.time()
stripes, labels, delete_parts = seperator.create_stripes(
    points=points, r=r, step_prct=seperation_step, z_index=5
)
log_time("stripes generation", time.time() - starttime)


# solve individuals
total_solution = Total_Solution(N, labels, delete_parts)

print(total_solution.ranges)
print(total_solution.delete_parts)

i = 0
for stripe in stripes:
    n = len(stripe[0])

    # build subgraph
    starttime = time.time()
    graph = Graph(
        cover_radius=r,
        number_of_points=n,
        exploration_factor=exploration_factor,
        intersection_weight=intersection_weight,
        points=np.transpose(
            stripe
        ),  # graph iteriert über Zeilen und nicht Spalten => transposes
    )

    if n <= 10_000:
        steps = 1
    else:
        old_steps = 1 + int(n / 10_000)
        steps = 1 + int(n / 10_000) * int(n / 10_000)
    graph.update_all_neighbours(steps=steps)

    # build sol for current subgraph on stripe
    tmp_sol = total_solution.create_initial_solution(i, graph)

    log_time("graph and initial sol build", time.time() - starttime)

    # solve
    starttime = time.time()

    gs = GreedySearch(graph=graph, initial_sol=tmp_sol)
    tmp_sol = gs.findSolution()

    log_time("greadysearch", time.time() - starttime)

    # include in solution
    total_solution.include_solution(iteration=i, solution=tmp_sol)

    # incremennt iteration count
    i = i + 1
    
    total_solution.save_logs(solution_log_FilePath, points=np.transpose(points))
    pass


total_solution.save(solutionFilePath + "_tmp", points=np.transpose(points))
total_solution.save_logs(solution_log_FilePath, points=np.transpose(points))


#########################
#########################
####### CHECK SOL #######
#########################
#########################

# Lies die Lösung ein
logging.info("Loaded solution from \"{}\"".format(solutionFilePath+ "_tmp.csv"))
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
    if type(p) is np.ndarray:
        writer_nodes.writerow([p[0], p[1], p[2]])
    else:
        writer_nodes.writerow([p[0], p[1], p[2].replace("\n", "")])
    pass
