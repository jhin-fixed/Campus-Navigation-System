"""
Graph data structures for Campus Navigator.
Defines Node and Graph classes for representing the campus map.
"""

import json
from typing import List, Tuple, Dict, Optional


class Node:
    """Represents a location (building or junction) on campus."""

    def __init__(self, id: int, name: str, x: float, y: float):
        """
        Initialize a node.

        Args:
            id: Unique identifier for the node
            name: Display name (e.g., "Entrance", "Main Gym")
            x: X coordinate from JSON (will be scaled for display)
            y: Y coordinate from JSON (will be scaled for display)
        """
        self.id = id
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Node({self.id}, '{self.name}', x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        """Two nodes are equal if they have the same ID."""
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets and dicts."""
        return hash(self.id)


class Graph:
    """
    Represents the campus map as an undirected weighted graph.
    Uses adjacency list representation.
    """

    def __init__(self):
        """Initialize an empty graph."""
        self.nodes: Dict[int, Node] = {}  # Maps node_id -> Node object
        self.adjacency: Dict[int, List[Tuple[int, float]]] = {}  # Maps node_id -> [(neighbor_id, weight), ...]

    def add_node(self, node: Node) -> None:
        """
        Add a node to the graph.

        Args:
            node: Node object to add
        """
        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = []

    def add_edge(self, from_id: int, to_id: int, weight: float) -> None:
        """
        Add a bidirectional edge between two nodes.

        Args:
            from_id: Source node ID
            to_id: Destination node ID
            weight: Edge weight (time in minutes)
        """
        # Ensure both nodes exist in adjacency list
        if from_id not in self.adjacency:
            self.adjacency[from_id] = []
        if to_id not in self.adjacency:
            self.adjacency[to_id] = []

        self.adjacency[from_id].append((to_id, weight))
        self.adjacency[to_id].append((from_id, weight))


    def get_node(self, node_id: int) -> Optional[Node]:
        """
        Get a node by its ID.

        Args:
            node_id: ID of the node to retrieve

        Returns:
            Node object or None if not found
        """
        return self.nodes.get(node_id)

    def get_node_by_name(self, name: str) -> Optional[Node]:
        """
        Get a node by its name.

        Args:
            name: Name of the node to retrieve

        Returns:
            Node object or None if not found
        """
        for node in self.nodes.values():
            if node.name == name:
                return node
        return None

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        """
        Get all neighbors of a node with their edge weights.

        Args:
            node_id: ID of the node

        Returns:
            List of (neighbor_id, weight) tuples
        """
        return self.adjacency.get(node_id, [])

    def get_all_nodes(self) -> List[Node]:
        """
        Get all nodes in the graph.

        Returns:
            List of all Node objects, sorted by ID
        """
        return sorted(self.nodes.values(), key=lambda n: n.id)

    def get_coordinate_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the bounding box of all node coordinates.

        Returns:
            Tuple of (min_x, max_x, min_y, max_y)
        """
        if not self.nodes:
            return (0, 0, 0, 0)

        x_coords = [node.x for node in self.nodes.values()]
        y_coords = [node.y for node in self.nodes.values()]

        return (min(x_coords), max(x_coords), min(y_coords), max(y_coords))

    def load_from_json(self, filepath: str) -> None:
        """
        Load graph data from a JSON file.

        Args:
            filepath: Path to the JSON file

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is malformed
            KeyError: If required fields are missing
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Load nodes
        for node_data in data['nodes']:
            node = Node(
                id=node_data['id'],
                name=node_data['name'],
                x=node_data['x'],
                y=node_data['y']
            )
            self.add_node(node)

        # Load edges (automatically creates bidirectional connections)
        for edge_data in data['edges']:
            self.add_edge(
                from_id=edge_data['from'],
                to_id=edge_data['to'],
                weight=edge_data['weight']
            )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Graph(nodes={len(self.nodes)}, edges={sum(len(adj) for adj in self.adjacency.values()) // 2})"