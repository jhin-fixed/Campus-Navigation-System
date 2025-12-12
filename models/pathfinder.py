import heapq
from typing import List, Tuple, Dict, Optional
from models.graph import Graph


class PathFinder:

    def __init__(self, graph: Graph):

        self.graph = graph

    def find_shortest_path(self, start_id: int, end_id: int) -> Tuple[Optional[List[int]], float]:
        """
        Find the shortest path between two nodes.

        Args:
            start_id: Starting node ID
            end_id: Destination node ID

        Returns:
            Tuple of (path, total_weight) where:
                - path: List of node IDs from start to end, or None if no path exists
                - total_weight: Total weight of the path, or float('inf') if no path
        """
        # Validate nodes exist
        if start_id not in self.graph.nodes or end_id not in self.graph.nodes:
            return (None, float('inf'))

        # Handle same start and end
        if start_id == end_id:
            return ([start_id], 0.0)

        # Run Dijkstra's algorithm
        distances, predecessors = self._dijkstra(start_id)

        # Check if destination is reachable
        if distances[end_id] == float('inf'):
            return (None, float('inf'))

        # Reconstruct path
        path = self._reconstruct_path(predecessors, start_id, end_id)
        total_weight = distances[end_id]

        return (path, total_weight)

    def _dijkstra(self, start_id: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Run Dijkstra's algorithm from a starting node.

        Args:
            start_id: Starting node ID

        Returns:
            Tuple of (distances, predecessors) where:
                - distances: Dict mapping node_id -> shortest distance from start
                - predecessors: Dict mapping node_id -> previous node in shortest path
        """
        # Initialize distances and predecessors
        distances = {node_id: float('inf') for node_id in self.graph.nodes}
        predecessors = {node_id: None for node_id in self.graph.nodes}
        distances[start_id] = 0.0

        # Priority queue: (distance, node_id)
        pq = [(0.0, start_id)]
        visited = set()

        while pq:
            current_dist, current_id = heapq.heappop(pq)

            # Skip if already visited
            if current_id in visited:
                continue

            visited.add(current_id)

            # If we found a shorter path since adding to queue, skip
            if current_dist > distances[current_id]:
                continue

            # Check all neighbors
            for neighbor_id, weight in self.graph.get_neighbors(current_id):
                # Calculate distance through current node
                new_dist = current_dist + weight

                # Update if we found a shorter path
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    predecessors[neighbor_id] = current_id
                    heapq.heappush(pq, (new_dist, neighbor_id))

        return distances, predecessors

    def _reconstruct_path(self, predecessors: Dict[int, Optional[int]],
                          start_id: int, end_id: int) -> List[int]:
        """
        Reconstruct path from predecessors dictionary.

        Args:
            predecessors: Dict mapping node_id -> previous node
            start_id: Starting node ID
            end_id: Ending node ID

        Returns:
            List of node IDs representing the path from start to end
        """
        path = []
        current = end_id

        # Trace back from end to start
        while current is not None:
            path.append(current)
            current = predecessors[current]

        # Reverse to get start -> end order
        path.reverse()

        return path