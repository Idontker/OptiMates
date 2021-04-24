import logging
from sphere import pointOnSphere
import setupLogger
import validator

setupLogger.setup("Run main.py")

validator.validateSolutionCSV("/sols/solution.csv", seperator=",", delta=180/2, sampleSize= 1_000_000)


# p = pointOnSphere.point()
# p.testRef()

# pointOnSphere.testRef()
