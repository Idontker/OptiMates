# Gliederung / Table of Contents
1. Auflistung der Module (Deutsche Version)
2. Listing of modules (English Version)

# Auflistung der Module (Deutsche Version)
* graph.py: Dieses Modul implementiert den Graphen, welcher die Diskretisierung, die Schnittpunkte der Lösungenskappen und die Mittelpunkte der Schnittflächen sowie die dazugehörigen Adjazenzmatrix speichert. 
  Bei der Speicheung der Matrizen ist anzumerken, dass diese mittels ``numpy.packbits`` und ``numpy.unpackbits`` die Vektoren bitweise gespeichert werden.
* solution.py: In diesem Modul wird die Speicherung und Verwaltung einer Teillösung implementiert. Mit Teillösung ist hier eine Menge gemeint, die zu einer dominierenden Teilmenge des Teilgraphen. 
  Unter Teilgraph wird der Graph einer Iteration der adaptiven Lösungsfindung verstanden.
*   
