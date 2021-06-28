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
durchmeser = 2 * 22.7  # deg
r = math.radians(durchmeser / 2)
logging.info("durchmeser:" + str(math.radians(durchmeser)) + "\tr/2:" + str(r))


N = 20_000
seperation_step = 0.4
exploration_factor = 2
intersection_weight = 1
solutionFilePath = ".\\sols\\solution_" + str(N) + "_" + str(durchmeser) + "_01.csv"


#########################
##### Logging setup #####
#########################
import setupLogger

setupLogger.setup("Run main.py")
time_ground_zero = time.time()

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
stripes, labels = seperator.create_stripes(
    points=points, epsi=r, step_prct=seperation_step, z_index=5
)
log_time("stripes generation", time.time() - starttime)


# solve individuals
total_solution = Total_Solution(N, labels)
# current_sol = Solution(N, labels)

# total_solution.used_labels = np.array(range(100, 2000, 50))

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

    if n <= 15_000:
        steps = 1
    else:
        steps = 1 + int(n / 10_000)
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
    pass


total_solution.save(solutionFilePath, points=np.transpose(points))


#########################
#########################
####### CHECK SOL #######
#########################
#########################

# Lies die Lösung ein
solution = checker.readSolution(solutionFilePath)
logging.info("Solution for {}:".format(durchmeser))
# for p in solution:
#     logging.info(p)

# int um die loecher zu zaehlen
added = 0

# looking for missing points with "do while"
while True:
    arr = checker.checkSolution(solution, durchmeser, printing=False)
    if arr is None:
        break
    else:
        added = added + 1
        solution.append(arr)

logging.info("=========DONE=========")
logging.info("Due to holes additionally added points {}".format(added))
logging.info("Number of needed shperical caps: {}".format(len(solution)))
# Überprüfe die Lösung
checker.checkSolution(solution, durchmeser)