import logging
from sphere import solution
import random


class Simple_GA:
    def __init__(self, graph, population_size=25) -> None:
        self.population_size = population_size
        self.population = list()
        self.node_size = graph.size()

        for i in range(0, population_size):
            sol = solution.Solution(graph)
            sol.randomSolution(random.randint(1, self.node_size))
            self.population.append(sol)

        self.population.sort()
        for sol in self.population:
            logging.info(sol)