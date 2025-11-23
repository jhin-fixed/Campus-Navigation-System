"""
Configuration constants for Campus Navigator application.
All dimensions, colors, and application settings.
"""

# Window dimensions (pixels at 96 DPI)
WINDOW_WIDTH = 528
WINDOW_HEIGHT = 528
CANVAS_WIDTH = 384
PANEL_WIDTH = 144

# Canvas drawing settings
CANVAS_PADDING = 30  # Padding around graph in pixels
NODE_RADIUS = 8  # Circle radius for nodes
EDGE_WIDTH = 2  # Default edge line width
EDGE_HIGHLIGHT_WIDTH = 4  # Highlighted path edge width

# Colors (R, G, B) tuples
COLOR_NODE_DEFAULT = (100, 100, 100)  # Gray
COLOR_NODE_HIGHLIGHT = (255, 0, 0)  # Red
COLOR_NODE_START = (0, 200, 0)  # Green
COLOR_NODE_END = (255, 0, 0)  # Red (same as highlight)
COLOR_EDGE_DEFAULT = (150, 150, 150)  # Light gray
COLOR_EDGE_HIGHLIGHT = (255, 100, 0)  # Orange
COLOR_BACKGROUND = (255, 255, 255)  # White
COLOR_ERROR_TEXT = (200, 0, 0)  # Red for error messages

# Text colors (Qt uses different format, we'll convert as needed)
COLOR_TEXT_NORMAL = (0, 0, 0)  # Black
COLOR_TEXT_SUCCESS = (0, 150, 0)  # Green

# Data file path
GRAPH_DATA_FILE = "data/campus_graph.json"

# Error messages
ERROR_SAME_LOCATION = "Start and destination cannot be the same"
ERROR_NO_PATH = "No path found between selected locations"
ERROR_INVALID_SELECTION = "Please select both start and destination"
ERROR_LOAD_FAILED = "Failed to load campus map data"