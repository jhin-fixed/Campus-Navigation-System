from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint
from typing import List, Tuple, Optional
from models.graph import Graph
import config


class GraphCanvas(QWidget):

    def __init__(self, graph: Graph, parent=None):
        """
        Initialize the canvas.

        Args:
            graph: Graph object containing nodes and edges
            parent: Parent widget
        """
        super().__init__(parent)
        self.graph = graph
        self.highlighted_path: Optional[List[int]] = None

        # Set fixed size
        self.setFixedSize(config.CANVAS_WIDTH, config.CANVAS_HEIGHT)

        # Calculate coordinate scaling parameters
        self._calculate_scaling()

    def _calculate_scaling(self) -> None:
        """
        Calculate scaling parameters to fit graph coordinates onto canvas.
        Maintains aspect ratio and centers the graph with padding.
        """
        # Get coordinate bounds from graph
        min_x, max_x, min_y, max_y = self.graph.get_coordinate_bounds()

        # Calculate coordinate ranges
        coord_width = max_x - min_x
        coord_height = max_y - min_y

        # Avoid division by zero
        if coord_width == 0:
            coord_width = 1
        if coord_height == 0:
            coord_height = 1

        # Available drawing area (accounting for padding)
        draw_width = config.CANVAS_WIDTH - (2 * config.CANVAS_PADDING)
        draw_height = config.CANVAS_HEIGHT - (2 * config.CANVAS_PADDING)

        # Calculate scale factors for each dimension
        scale_x = draw_width / coord_width
        scale_y = draw_height / coord_height

        # Use smaller scale to maintain aspect ratio
        self.scale = scale_x

        # Store bounds for transformation
        self.min_x = min_x
        self.min_y = min_y

        # Calculate offsets to center the graph
        scaled_width = coord_width * self.scale
        scaled_height = coord_height * self.scale
        self.offset_x = config.CANVAS_PADDING + (draw_width - scaled_width) / 2
        self.offset_y = config.CANVAS_PADDING + (draw_height - scaled_height) / 2

    def _scale_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert graph coordinates to canvas pixel coordinates.

        Args:
            x: X coordinate from graph
            y: Y coordinate from graph

        Returns:
            Tuple of (canvas_x, canvas_y) in pixels
        """
        canvas_x = int((x - self.min_x) * self.scale + self.offset_x)
        canvas_y = int((y - self.min_y) * self.scale + self.offset_y)
        return (canvas_x, canvas_y)

    def highlight_path(self, path: List[int]) -> None:
        """
        Highlight a path on the canvas.

        Args:
            path: List of node IDs representing the path
        """
        self.highlighted_path = path
        self.update()  # Trigger repaint

    def clear_highlights(self) -> None:
        """Clear all path highlights."""
        self.highlighted_path = None
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        """
        Paint the graph on the canvas.
        Called automatically by Qt when widget needs to be redrawn.

        Args:
            event: Paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill background
        painter.fillRect(self.rect(), QColor(*config.COLOR_BACKGROUND))

        # Draw edges first (so nodes appear on top)
        self._draw_edges(painter)

        # Draw nodes
        self._draw_nodes(painter)

    def _draw_edges(self, painter: QPainter) -> None:
        """
        Draw all edges in the graph.

        Args:
            painter: QPainter object for drawing
        """
        # Track drawn edges to avoid duplicates (undirected graph)
        drawn_edges = set()

        for node_id, neighbors in self.graph.adjacency.items():
            node = self.graph.get_node(node_id)
            if not node:
                continue

            node_x, node_y = self._scale_coordinates(node.x, node.y)

            for neighbor_id, weight in neighbors:
                # Skip if edge already drawn (avoid drawing twice for undirected)
                edge_key = tuple(sorted([node_id, neighbor_id]))
                if edge_key in drawn_edges:
                    continue
                drawn_edges.add(edge_key)

                neighbor = self.graph.get_node(neighbor_id)
                if not neighbor:
                    continue

                neighbor_x, neighbor_y = self._scale_coordinates(neighbor.x, neighbor.y)

                # Determine if this edge is highlighted
                is_highlighted = False
                if self.highlighted_path and len(self.highlighted_path) >= 2:
                    # Check if both nodes are consecutive in the path
                    for i in range(len(self.highlighted_path) - 1):
                        if ((self.highlighted_path[i] == node_id and
                             self.highlighted_path[i + 1] == neighbor_id) or
                                (self.highlighted_path[i] == neighbor_id and
                                 self.highlighted_path[i + 1] == node_id)):
                            is_highlighted = True
                            break

                # Set pen based on highlight status
                if is_highlighted:
                    pen = QPen(QColor(*config.COLOR_EDGE_HIGHLIGHT),
                               config.EDGE_HIGHLIGHT_WIDTH)
                else:
                    pen = QPen(QColor(*config.COLOR_EDGE_DEFAULT),
                               config.EDGE_WIDTH)

                painter.setPen(pen)
                painter.drawLine(node_x, node_y, neighbor_x, neighbor_y)

    def _draw_nodes(self, painter: QPainter) -> None:
        """
        Draw all nodes in the graph.

        Args:
            painter: QPainter object for drawing
        """
        for node in self.graph.get_all_nodes():
            node_x, node_y = self._scale_coordinates(node.x, node.y)

            # Determine node color based on role in path
            color = config.COLOR_NODE_DEFAULT

            if self.highlighted_path:
                if node.id == self.highlighted_path[0]:
                    # Start node
                    color = config.COLOR_NODE_START
                elif node.id == self.highlighted_path[-1]:
                    # End node
                    color = config.COLOR_NODE_END
                elif node.id in self.highlighted_path:
                    # Intermediate node in path
                    color = config.COLOR_NODE_HIGHLIGHT

            # Draw node circle
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(*color)))
            painter.drawEllipse(QPoint(node_x, node_y),
                                config.NODE_RADIUS,
                                config.NODE_RADIUS)

            # Draw node label (ID)
            painter.setPen(QColor(*config.COLOR_TEXT_NORMAL))
            # Offset text slightly below the node
            text_y = node_y + config.NODE_RADIUS + 12
            painter.drawText(node_x - 10, text_y, 20, 15,
                             Qt.AlignCenter, str(node.id))