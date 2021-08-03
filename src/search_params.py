import solver
import numpy as np
import matplotlib.pyplot as plt
import math
import time


def log_time(tastname, timediff):
    print(
        'time for "{}": {}::{}::{}    [min:sec:ms]'.format(
            tastname,
            math.trunc(timediff / 60),
            math.trunc(timediff % 60),
            math.trunc((timediff - math.trunc(timediff)) * 1000),
        )
    )


def linear_testing(start, stop, steps, N, r_deg, exploration_factor):
    results = np.array([])
    added = np.array([])
    values = np.linspace(start, stop, steps)
    print(values)
    i = 0
    starttime = time.time()
    for weight in values:
        print("\n\n\n")
        print(i, "weight", weight)
        print(40 * "=")
        i = i + 1
        res, add = solver.solve(
            r_deg=r_deg,
            N=N,
            intersection_weight=weight,
            exploration_factor=exploration_factor,
            solutionFilePath=".\\sols\\solution_tmp.csv",
        )
        # print("weight: {}   res:{}".format(weight, res))
        results = np.append(results, res)
        added = np.append(added, add)
    print(results)
    print(added)
    timediff = time.time() - starttime
    log_time("testing params", timediff)

    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    ax.scatter(x=values, y=results, color="blue", s=5)

    ax = fig.add_subplot(2, 1, 2)
    ax.scatter(x=values, y=added, color="blue", s=5)
    plt.show()


def binary_search(start, end, steps, N, r_deg, exploration_factor):
    results = np.array([])
    added = np.array([])
    weights = np.array([])

    # left side
    lw = start  # left weight
    left = solver.solve(
        r_deg=r_deg,
        N=N,
        intersection_weight=lw,
        exploration_factor=exploration_factor,
        solutionFilePath=".\\sols\\solution_tmp.csv",
    )
    # print("weight: {}   res:{}".format(weight, res))
    results = np.append(results, left[0])
    added = np.append(added, left[1])
    weights = np.append(weights, lw)

    # right side
    rw = end
    right = solver.solve(
        r_deg=r_deg,
        N=N,
        intersection_weight=rw,
        exploration_factor=exploration_factor,
        solutionFilePath=".\\sols\\solution_tmp.csv",
    )
    # print("weight: {}   res:{}".format(weight, res))
    results = np.append(results, right[0])
    added = np.append(added, right[1])
    weights = np.append(weights, rw)

    for i in range(steps):
        print("\n\n")
        print(lw, rw)
        print(left, right)
        print()

        if left[0] < right[0]:
            # new boarder
            rw = rw - (rw - lw) / 4
            # update
            right = solver.solve(
                r_deg=r_deg,
                N=N,
                intersection_weight=rw,
                exploration_factor=exploration_factor,
                solutionFilePath=".\\sols\\solution_tmp.csv",
            )
            # print("weight: {}   res:{}".format(weight, res))
            results = np.append(results, right[0])
            added = np.append(added, right[1])
            weights = np.append(weights, rw)
        else:
            # new boarder
            lw = lw + (rw - lw) / 4
            left = solver.solve(
                r_deg=r_deg,
                N=N,
                intersection_weight=lw,
                exploration_factor=exploration_factor,
                solutionFilePath=".\\sols\\solution_tmp.csv",
            )
            # print("weight: {}   res:{}".format(weight, res))
            results = np.append(results, left[0])
            added = np.append(added, left[1])
            weights = np.append(weights, lw)
        pass

    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    ax.scatter(x=weights, y=results, color="blue", s=5)

    ax = fig.add_subplot(2, 1, 2)
    ax.scatter(x=weights, y=added, color="blue", s=5)
    plt.show()
    pass


N = 10_000
r_deg = 22.7
exploration_factor = 1.8

binary_search(5, 15, 10, N, r_deg, exploration_factor)
