# Deutsche Version
Optimates ist eine fiktive Firma, welche im Rahmen eines Projektseminars gegründet wurde. Ihr Ziel war es, eine Implementierung für das Sphere-Covering Problem für die dreidimensionale Sphäre zu entwickeln. 

## Sphere-Covering Problem
Gegeben ist die Oberfläche der dreidimmensionalen Sphäre. Ziel ist es nun diese Oberfläche mit möglichst wenigen Kugelsegmenten zu überdecken. Diese sollen jeweils den gleichen Öffnungsradius *r* besitzten. 
Mögliche Anwendungen sind die Beobachtung des Sternenhimmels oder die Asteroidenüberwachung.

## Lösungsansatz
Der hier gewählte Lösungsanatz besteht aus vier Phasen:
1. Diskretisierung der Oberfläche der Spähre
2. Generierung eines Graphen *G* aus der Diskretisierung. Dieser ist ungerichtet und ungewichtet. Eine Kante zwischen zwei Knoten *v* und *w* existiert genau dann, wenn *w* im Kugelsegment mit Radius *r* um *v* liegt.
3. Greedy Verfahren zur Bestimmung einer dominierenden Menge *S* auf diesem Graphen *G*
4. Überprüfen und ggf. Erweiteren der Menge *S* zu einer vollständigen Überdeckung der Sphäre

## Beispielswerte für verschiedene Größen
r | untere Schranke | Kleinste Größe der Lösungsmenge | Laufzeit |
---| ---| ---| ---|
70.6° | 3 | 5 | 106 ms |
37.4° | 10 | 14 | 202 ms | 
22.7° | 26 | 45 | 2.52 s | 
13.0° | 79 | 117 | 11.6 s | 
1.75° | 4288 | 6786 | 110 min |

Die Laufzeiten ergeben sich aus der Berechnung mit folgender Hardware Fujitsu Esprimo P758, Intel Core i7-9700, 64 GB RAM. Die untere Schranke ergibt sich durch ein Vergleich der Oberfläche eines Kugelsegments und der Oberfläche der Sphäre dar. Dies ist somit eine theoretische Schranke, die nicht erreichbar ist.


# English Version
Optimates is a fictitious company that was founded during a project seminar. Their goal was to develop an implementation for the sphere-covering problem for the three-dimensional sphere. 

## Sphere-Covering Problem
Given is the surface of the three-dimensional sphere. The goal is to cover this surface with as few sphere-segments as possible. These should each have the same opening radius *r*. 
Possible applications are the observation of the starry sky or asteroid monitoring.

## Solution approach
The solution approach chosen here consists of four phases:
1. discretisation of the surface of the sphere
2. generation of a graph *G* from the discretisation. This is undirected and unweighted. An edge between two nodes *v* and *w* exists exactly when *w* lies in the spherical segment with radius *r* around *v*.
3. Greedy method for determining a dominating set *S* on this graph *G*.
4. check and, if necessary, extend the set *S* to a complete covering of the sphere.

## Example results for diffrent paramters
r | lower limit | smallest resultset | runtimes |
---| ---| ---| ---|
70.6° | 3 | 5 | 106 ms |
37.4° | 10 | 14 | 202 ms | 
22.7° | 26 | 45 | 2.52 s | 
13.0° | 79 | 117 | 11.6 s | 
1.75° | 4288 | 6786 | 110 min |

The runtimes result from the calculation with the following hardware Fujitsu Esprimo P758, Intel Core i7-9700, 64 GB RAM. The lower limit is calculated by comparing the surface of a sphere segment and the surface of the sphere. This is therefore a theoretical barrier that is not achievable.
