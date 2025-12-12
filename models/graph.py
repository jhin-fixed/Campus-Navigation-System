import json
from typing import List, Tuple, Dict, Optional
import config


class Node:

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
        self.letter = config.NODE_LETTER_MAP.get(id, '?')  # Get letter from mapping

    def __repr__(self) -> str:
        return f"Node({self.id}, '{self.name}', letter={self.letter}, x={self.x}, y={self.y})"

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

        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = []

    def add_edge(self, from_id: int, to_id: int, weight: float) -> None:

        # Ensure both nodes exist in adjacency list
        if from_id not in self.adjacency:
            self.adjacency[from_id] = []
        if to_id not in self.adjacency:
            self.adjacency[to_id] = []

        # Add edge in both directions (undirected graph)
        self.adjacency[from_id].append((to_id, weight))
        self.adjacency[to_id].append((from_id, weight))

    def get_node(self, node_id: int) -> Optional[Node]:

        return self.nodes.get(node_id)

    def get_node_by_name(self, name: str) -> Optional[Node]:

        for node in self.nodes.values():
            if node.name == name:
                return node
        return None

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:

        return self.adjacency.get(node_id, [])

    def get_all_nodes(self) -> List[Node]:

        return sorted(self.nodes.values(), key=lambda n: n.id)

    def get_coordinate_bounds(self) -> Tuple[float, float, float, float]:

        if not self.nodes:
            return (0, 0, 0, 0)

        x_coords = [node.x for node in self.nodes.values()]
        y_coords = [node.y for node in self.nodes.values()]

        return (min(x_coords), max(x_coords), min(y_coords), max(y_coords))

    def load_from_json(self, filepath: str) -> None:

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
        return f"Graph(nodes={len(self.nodes)}, edges={sum(len(adj) for adj in self.adjacency.values()) // 2})"