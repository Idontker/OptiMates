import logging
from sphere.solution import Solution
from genericAlgorithm.basic_genetic_algorithm import print_stats, run_evolution
from sphere import pointOnSphere as pos
from sphere import graphOnSphere as gos
import setupLogger
import validator
from sphere import solution as sol
from genericAlgorithm import gericAlgo
from genericAlgorithm import fittness
from genericAlgorithm import basic_genetic_algorithm as bga
import math
from functools import partial
import time
import numpy as np


setupLogger.setup("Run main.py")

R = 1
r = 70.6  # deg
r = math.radians(r)
logging.info(r)

N = 10000
population_size = 25
goal_size = 4
generation_limit = 500


starttime = time.time()
g1 = gos.Graph(R, r, radial=True)
g1.initRandomSet(N)
# logging.info(g1.strStruct())
# ga = gericAlgo.Simple_GA(g1)
adjmatrix = g1.createMatrix()
mat = adjmatrix
nonzero = np.count_nonzero(mat)
print(mat)
print(np.shape(mat))
print(nonzero/(np.shape(mat)[0] * np.shape(mat)[1]))
quit()

timediff = time.time() - starttime
logging.info(
    "time for graph creation: {}::{}::{}    [min:sec:ms]".format(
        math.trunc(timediff / 60),
        math.trunc(timediff % 60),
        math.trunc((timediff - math.trunc(timediff)) * 1000),
    )
)
# f = partial(fittness.fittness, graph=g1)
f = partial(fittness.fittnessFast, adjmatrix=adjmatrix)


starttime = time.time()
population, generations = bga.run_evolution(
    populate_func=partial(
        bga.generate_population, size=population_size, genome_length=len(g1)
    ),
    fitness_func=f,
    fitness_limit=1 + 1 / (N * goal_size),
    generation_limit=generation_limit,
    printer=bga.print_stats,
)
timediff = time.time() - starttime
logging.info(
    "time for training: {}::{}::{}    [min:sec:ms]".format(
        math.trunc(timediff / 60),
        math.trunc(timediff % 60),
        math.trunc((timediff - math.trunc(timediff)) * 1000),
    )
)

logging.info("generations: " + str(generations))
# logging.info("Best: " + str(population[0]))


s = Solution(g1)
s.addNodesByGenome(population[0])
logging.info(s)

# s1 = sol.Solution(g1)
# s2 = sol.Solution(g1)
# s3 = sol.Solution(g1)

# s1.randomSolution(3)
# logging.info(s1)
# s2.randomSolution(3)
# logging.info(s2)
# s3.randomSolution(3)
# logging.info(s3)


# validator.validateSolutionCSV("/sols/solution.csv", seperator=",", delta=180/2, sampleSize= 1_000_000)


# p = pointOnSphere.point()
# p.testRef()

# pointOnSphere.testRef()
