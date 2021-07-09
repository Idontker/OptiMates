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



setupLogger.setup("Run main.py")

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

