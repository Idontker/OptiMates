# Gliederung / Table of Contents
1. Auflistung der Module (Deutsche Version)
2. Listing of modules (English Version)

# Auflistung der Module (Deutsche Version)
* graph.py: Dieses Modul implementiert den Graphen, welcher die Diskretisierung, die Schnittpunkte der Lösungenskappen und die Mittelpunkte der Schnittflächen sowie die dazugehörigen Adjazenzmatrix speichert. 
  Bei der Speicheung der Matrizen ist anzumerken, dass diese mittels ``numpy.packbits`` und ``numpy.unpackbits`` die Vektoren bitweise gespeichert werden.
* solution.py: In diesem Modul wird die Speicherung und Verwaltung einer Teillösung implementiert. Mit Teillösung ist hier eine Menge gemeint, die zu einer dominierenden Teilmenge des Teilgraphen. 
  Unter Teilgraph wird der Graph einer Iteration der adaptiven Lösungsfindung verstanden.
*  total_solution.py: Dieses Modul beschreibt eine Schnittstelle, die die einzelnen Teillösungen zusammenführt. 
*  total_size.py: Dieses Modul gibt einem die Möglichkeit, akurate den aktuellen Speicherverbrauch zu bestimmen.
*  visu_sol.py: Mit diesem Modul, kann die resultierende Lösung abgebildet werden.


# Listing of modules (English Version)
* graph.py: This module implements the graph, which stores the discretisation, the intersections of the solution caps and the centres of the intersections as well as the corresponding adjacency matrix. 
  When storing the matrices, it should be noted that they are stored bitwise by means of ``numpy.packbits`` and ``numpy.unpackbits`` the vectors.
* solution.py: This module implements the storage and management of a partial solution. By partial solution is meant here a set that becomes a dominant subset of the subgraph. 
  By subgraph is meant the graph of an iteration of adaptive solution finding.
* total_solution.py: This module describes an interface that assembles the individual partial solutions. 
* total_size.py: This module gives you the possibility to accurately determine the current memory consumption.
* visu_sol.py: With this module, the resulting solution can be displayed.
