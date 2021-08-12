# Gliederung / Table of Contents
1. Auflistung der Module (Deutsche Version)
2. Listing of modules (English Version)

# Auflistung der Module (Deutsche Version)
* entry.py: Dieses Modul beschreibt einen Eintrag in der PrioQueue. 
* greadysearch.py: Dieses Modul implementiert das Greedyverfahren zur Suche nach einer dominierenden Menge auf einem Graphen.
* prioqueue.py: In diesem Modul wird eine Prioritätswarteschlange (PrioQueue) implementiert. Dazu werden die Einträge in einem Heap gespeichert. Bei einer Aktualisierung 
  einzelner Gewichte, werden alte Einträge als ungültig markiert und ein neuer Eintrag eingefügt. Bei der Entnahme von Elementen werden Einträge, die als ungültig markiert wurden,
  aus dem Heap entnommen, aber nicht weitergegeben. Stattdessen werden solange Einträge entnommen, bis ein gültuger Eintrag weitergegeben werden kann.

# Listing of modules (English Version)
* entry.py: This module describes an entry in the PrioQueue. 
* greadysearch.py: This module implements the greedy procedure to search for a dominating set on a graph.
* prioqueue.py: This module implements a priority queue. For this purpose, the entries are stored in a heap. When individual weights are updated 
  When updating individual weights, old entries are marked as invalid and a new entry is inserted. When elements are removed, entries that have been marked as invalid,
  from the heap but are not passed on. Instead, entries are removed until a valid entry can be passed on.

