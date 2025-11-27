from models.graph import Graph
from models.pathfinder import PathFinder

graph = Graph()
graph.load_from_json("data/campus_graph.json")
pf = PathFinder(graph)

# This will fail or give wrong results due to one-way edges
path, dist = pf.find_shortest_path(0, 41)
print(f"Path: {path}, Distance: {dist}")
