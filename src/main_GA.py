import logging
from src.sphere.solution import Solution
from src.genericAlgorithm.basic_genetic_algorithm import print_stats, run_evolution
from src.sphere import pointOnSphere as pos
from src.sphere import graphOnSphere as gos
import src.setupLogger
import src.validator
from src.sphere import solution as sol
from src.genericAlgorithm import gericAlgo
from src.genericAlgorithm import fittness
from src.genericAlgorithm import basic_genetic_algorithm as bga
import math
from functools import partial
import time


src.setupLogger.setup("Run main.py")

R = 1
r = 70.6  # deg
r = math.radians(r)
logging.info(r)

N = 1000
population_size = 25
goal_size = 4
generation_limit = 500


starttime = time.time()
g1 = gos.Graph(R, r, radial=True)
g1.initRandomSet(N)
# logging.info(g1.strStruct())
# ga = gericAlgo.Simple_GA(g1)
adjmatrix = g1.createMatrix()

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
        bga.generate_population, size=population_size, genome_length=g1.size()
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
