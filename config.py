WINDOW_WIDTH = 600
WINDOW_HEIGHT = 520
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 320  # Canvas on top
CONTROL_PANEL_WIDTH = 135  # 30% of 450px centered panel
RESULTS_PANEL_WIDTH = 315  # 70% of 450px centered panel
BOTTOM_PANEL_HEIGHT = 200

# Canvas drawing settings
CANVAS_PADDING = 30
NODE_RADIUS = 8  # Circle radius for nodes
EDGE_WIDTH = 2  # Default edge line width
EDGE_HIGHLIGHT_WIDTH = 4  # Highlighted path edge width

# Colors (R, G, B) tuples
COLOR_NODE_DEFAULT = (84, 110, 122)  # Blue-gray (buildings)
COLOR_NODE_HIGHLIGHT = (38, 166, 154)  # Teal (path)
COLOR_NODE_START = (67, 160, 71)  # Green (start)
COLOR_NODE_END = (244, 67, 54)  # Red (end)
COLOR_NODE_JUNCTION = (158, 158, 158)  # Gray (junction)
COLOR_EDGE_DEFAULT = (176, 190, 197)  # Light blue-gray
COLOR_EDGE_HIGHLIGHT = (38, 166, 154)  # Teal
COLOR_BACKGROUND = (236, 239, 241)  # Light gray
COLOR_CANVAS_BG = (255, 255, 255)  # White canvas
COLOR_ERROR_TEXT = (211, 47, 47)  # Red for errors

# Text colors (Qt uses different format, we'll convert as needed)
COLOR_TEXT_NORMAL = (55, 71, 79)  # Dark blue-gray
COLOR_TEXT_SUCCESS = (67, 160, 71)  # Green
COLOR_TEXT_HEADER = (55, 71, 79)  # Dark blue-gray

# UI Colors (for Qt stylesheets - RGB format)
PRIMARY_COLOR = "#37474F"  # Dark blue-gray
SECONDARY_COLOR = "#546E7A"  # Blue-gray
ACCENT_COLOR = "#26A69A"  # Teal
BACKGROUND_COLOR = "#ECEFF1"  # Light gray
BUTTON_HOVER = "#455A64"  # Darker blue-gray
TEXT_COLOR = "#37474F"  # Dark blue-gray
SUCCESS_COLOR = "#43A047"  # Green
ERROR_COLOR = "#D32F2F"  # Red

# Data file path
GRAPH_DATA_FILE = "data/campus_graph.json"

# Node ID to Letter mapping
NODE_LETTER_MAP = {
    0: 'A',
    1: 'B',
    5: 'C',
    16: 'D',
    16.1: 'E',
    17: 'F',
    18: 'G',
    19: 'H',
    20: 'I',
    41: 'J',
    42: 'K'

}

# Error messages
ERROR_SAME_LOCATION = "Start and destination cannot be the same"
ERROR_NO_PATH = "No path found between selected locations"
ERROR_INVALID_SELECTION = "Please select both start and destination"
ERROR_LOAD_FAILED = "Failed to load campus map data"