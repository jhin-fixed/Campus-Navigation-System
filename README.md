# Campus-Navigation-System

This a campus navigation app that finds the fastes route between buildings.

The campus is a graph. Buildings are nodes. Path are edges with weights (walking time in minutes). We use Dijkstra Algorithm, Adjacency List, Priority Queue(Min Heap) to find the shortest path, PyQt5 displays it visually.

Probelm it solves: 
New students or visitor don't know which routes are fastest. Some paths look short, some path are longer but faster. This calculates the optional route using measured walking times using average walking healthy speed of a person that ranges from 20yr old to 25yr old.
