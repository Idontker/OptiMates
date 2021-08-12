from graph.total_solution import Total_Solution
from greedy.greedysearch import GreedySearch
from graph.graph import Graph
import geometrics.seperation as seperator
import setupLogger
import logging
import math
import time
import checker.checker as checker
import csv
import numpy as np
import geometrics.point_factory as factory
import os


def log_time(tastname, timediff, time_ground_zero):
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


#########################
#########################
###### Constants ########
#########################
#########################

setupLogger.log_level = logging.INFO

setupLogger.setup("solver loaded - logging setup startet")

solution = None


def solve(
    r_deg,
    N,
    intersection_weight,
    exploration_factor,
    seperation_step,
    solutionFilePath,
    solution_log_FilePath,
    save_it
):
    R = 1
    durchmeser = 2 * r_deg
    r = math.radians(r_deg)
    logging.info("durchmesser:" +
                 str(math.radians(durchmeser)) + "\tr/2:" + str(r))

    #########################
    ##### Logging setup #####
    #########################

    logging.info(
        "Start greedy for r={}deg    N={}    sep_step={} explor={}   inter_weight={}:".format(
            durchmeser / 2, N, seperation_step, exploration_factor, intersection_weight
        )
    )

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

    log_time("point factory", time.time() - starttime, time_ground_zero)

    ##### Gen Stripes ######
    # Seperation of points into stripes / chunks

    starttime = time.time()
    stripes, labels, delete_parts = seperator.create_stripes(
        points=points, r=r, step_prct=seperation_step, z_index=5
    )
    log_time("stripes generation", time.time() - starttime, time_ground_zero)

    # solve individuals
    total_solution = Total_Solution(N, labels, delete_parts)

    # print(total_solution.ranges)
    # print(total_solution.delete_parts)

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
            steps = 1 + int(n / 10_000) * int(n / 10_000)
        graph.update_all_neighbours(steps=steps)

        # build sol for current subgraph on stripe
        tmp_sol = total_solution.create_initial_solution(i, graph)

        log_time(
            "graph and initial sol build", time.time() - starttime, time_ground_zero
        )

        # solve
        starttime = time.time()

        gs = GreedySearch(graph=graph, initial_sol=tmp_sol)
        tmp_sol = gs.findSolution()

        log_time("greadysearch", time.time() - starttime, time_ground_zero)

        # include in solution
        total_solution.include_solution(iteration=i, solution=tmp_sol)

        # incremennt iteration count
        i = i + 1
        if save_it:
            total_solution.save_logs(
                solution_log_FilePath, points=np.transpose(points))
        pass

    total_solution.save("tmp_calculation", points=np.transpose(points))
    if save_it:
        total_solution.save_logs(
            solution_log_FilePath, points=np.transpose(points))

    #########################
    #########################
    ####### CHECK SOL #######
    #########################
    #########################

    # Lies die Lösung ein
    logging.info('Loaded solution from "{}"'.format("tmp_calculation.csv"))
    solution = checker.readSolution("tmp_calculation.csv")
    logging.info(
        "Solution for r={}    N={}    sep_step={} explor={}   inter_weight={}:".format(
            durchmeser / 2, N, seperation_step, exploration_factor, intersection_weight
        )
    )

    # custom printer for checker
    def collect_printer(i, length, timediff):
        if i % 10 == 0:
            log_time(
                "collecting missing - so far: {}   (added={})".format(
                    length, i),
                timediff=timediff,
                time_ground_zero=time_ground_zero,
            )
            return True
        return False

    added = checker.collect_missing(
        solution=solution, alpha=durchmeser, n=3, printer=collect_printer
    )
    for a in added:
        solution.append(a)
    time_ground_end = time.time()
    logging.info("=========DONE=========")
    logging.info(
        "Due to holes additionally added points {}".format(len(added)))
    logging.info("Number of needed shperical caps: {}".format(len(solution)))
    # Überprüfe die Lösung
    checker.checkSolution(solution, durchmeser)

    # save solution and added
    if save_it:
        writer_solution = csv.writer(
            open(file=solutionFilePath + ".csv", mode="w", newline=""), delimiter=";"
        )

        for p in solution:
            if type(p) is np.ndarray:
                writer_solution.writerow([p[0], p[1], p[2]])
            else:
                writer_solution.writerow([p[0], p[1], p[2].replace("\n", "")])
        pass

    # remove tmp file
    try:
        os.remove("tmp_calculation.csv")
    except OSError:
        pass

    return len(solution), len(added), time_ground_end - time_ground_zero
