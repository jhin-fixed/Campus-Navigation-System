from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
from typing import List, Tuple, Optional
from models.graph import Graph
import config


class GraphCanvas(QWidget):

    def __init__(self, graph: Graph, parent=None):
        """
        Initialize the canvas.
        """
        super().__init__(parent)
        self.graph = graph
        self.highlighted_path: Optional[List[int]] = None

        self.setFixedSize(config.CANVAS_WIDTH, config.CANVAS_HEIGHT)

        self._calculate_scaling()

    def _calculate_scaling(self) -> None:
        """
        Calculate scaling parameters to fit graph coordinates onto canvas.
        Maintains aspect ratio and centers the grap.
        """
        min_x, max_x, min_y, max_y = self.graph.get_coordinate_bounds()

        coord_width = max_x - min_x
        coord_height = max_y - min_y

        if coord_width == 0:
            coord_width = 1
        if coord_height == 0:
            coord_height = 1

        draw_width = config.CANVAS_WIDTH - (2 * config.CANVAS_PADDING)
        draw_height = config.CANVAS_HEIGHT - (2 * config.CANVAS_PADDING)

        # Calculate scale factors for each dimension
        scale_x = draw_width / coord_width
        scale_y = draw_height / coord_height

        # Use smaller scale to maintain aspect ratio
        self.scale = min(scale_x, scale_y)

        self.min_x = min_x
        self.min_y = min_y

        scaled_width = coord_width * self.scale
        scaled_height = coord_height * self.scale
        self.offset_x = config.CANVAS_PADDING + (draw_width - scaled_width) / 2
        self.offset_y = config.CANVAS_PADDING + (draw_height - scaled_height) / 2

    def _scale_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert graph coordinates to canvas pixel coordinates.
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
        self.highlighted_path = None
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        painter.fillRect(self.rect(), QColor(*config.COLOR_CANVAS_BG))

        self._draw_grid(painter)

        self._draw_edges(painter)

        # Draw nodes
        self._draw_nodes(painter)

    def _draw_grid(self, painter: QPainter) -> None:
        """
        Draw grid lines on the canvas background.
        Adds grid line visual appearance.

        """
        # Set grid line color (very light gray)
        grid_color = QColor(220, 220, 220, 100)  # Light gray with transparency
        painter.setPen(QPen(grid_color, 1))

        grid_spacing = 30
        for x in range(0, config.CANVAS_WIDTH, grid_spacing):
            painter.drawLine(x, 0, x, config.CANVAS_HEIGHT)

        for y in range(0, config.CANVAS_HEIGHT, grid_spacing):
            painter.drawLine(0, y, config.CANVAS_WIDTH, y)

    def _draw_edges(self, painter: QPainter) -> None:

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
        for node in self.graph.get_all_nodes():
            node_x, node_y = self._scale_coordinates(node.x, node.y)

            # Determine node color based on role in path
            if node.id == 17:  # Junction node
                color = config.COLOR_NODE_JUNCTION
            else:
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

            # Draw node shadow for depth
            shadow_offset = 2
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(0, 0, 0, 30)))
            painter.drawEllipse(QPoint(node_x + shadow_offset, node_y + shadow_offset),
                                config.NODE_RADIUS,
                                config.NODE_RADIUS)

            # Draw node circle
            painter.setPen(QPen(QColor(255, 255, 255), 2))  # White border
            painter.setBrush(QBrush(QColor(*color)))
            painter.drawEllipse(QPoint(node_x, node_y),
                                config.NODE_RADIUS,
                                config.NODE_RADIUS)

            painter.setPen(QColor(*config.COLOR_TEXT_NORMAL))
            font = QFont()
            font.setPointSize(9)
            font.setFamily("Segoe UI")
            painter.setFont(font)

            # Format: [Building Name]
            name_text = f"[{node.name}]"
            text_width = painter.fontMetrics().horizontalAdvance(name_text)
            text_x = node_x - text_width - config.NODE_RADIUS - 5
            text_y = node_y + 4
            painter.drawText(text_x, text_y, name_text)

            # Draw letter on right side of circle (bold, larger)
            letter_font = QFont()
            letter_font.setPointSize(10)
            letter_font.setBold(True)
            letter_font.setFamily("Segoe UI")
            painter.setFont(letter_font)

            letter_x = node_x + config.NODE_RADIUS + 5
            letter_y = node_y + 5
            painter.drawText(letter_x, letter_y, node.letter)