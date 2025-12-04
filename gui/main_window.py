from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from models.graph import Graph
from models.pathfinder import PathFinder
from gui.graph_canvas import GraphCanvas
from gui.control_panel import ControlPanel
from utils.helpers import format_eta_display, format_path_display, calculate_eta
import config

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load graph data
        self.graph = Graph()
        try:
            self.graph.load_from_json(config.GRAPH_DATA_FILE)
        except Exception as e:
            print(f"Error loading graph: {e}")
            # You might want to show an error dialog here
            raise

        # Create pathfinder
        self.pathfinder = PathFinder(self.graph)

        # Setup UI
        self._setup_ui()

        # Connect signals
        self._connect_signals()

    def _setup_ui(self) -> None:
        # Set window properties
        self.setWindowTitle("Campus Navigator")
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout (horizontal)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create canvas (left side)
        self.canvas = GraphCanvas(self.graph)
        layout.addWidget(self.canvas)

        # Create control panel (right side)
        self.control_panel = ControlPanel(self.graph)
        layout.addWidget(self.control_panel)

        # Set layout
        central_widget.setLayout(layout)

    def _connect_signals(self) -> None:
        self.control_panel.calculate_clicked.connect(self._on_calculate_clicked)
        self.control_panel.reset_clicked.connect(self._on_reset_clicked)

    def _on_calculate_clicked(self) -> None:
        try:
            # Get selected nodes
            start_id = self.control_panel.get_selected_start()
            dest_id = self.control_panel.get_selected_destination()

            # Validate: check if same location
            if start_id == dest_id:
                self.control_panel.display_error(config.ERROR_SAME_LOCATION)
                self.canvas.clear_highlights()
                return

            # Find shortest path
            path, total_weight = self.pathfinder.find_shortest_path(start_id, dest_id)

            # Check if path exists
            if path is None or total_weight == float('inf'):
                self.control_panel.display_error(config.ERROR_NO_PATH)
                self.canvas.clear_highlights()
                return

            # Calculate ETA
            eta = calculate_eta(total_weight)

            # Get building names for path
            path_names = []
            for node_id in path:
                node = self.graph.get_node(node_id)
                if node:
                    path_names.append(node.name)

            # Format display strings
            eta_text = format_eta_display(eta)
            path_text = format_path_display(path_names)

            # Display results
            self.control_panel.display_result(eta_text, path_text)

            # Highlight path on canvas
            self.canvas.highlight_path(path)

        except ValueError as e:
            # Handle invalid dropdown selection
            self.control_panel.display_error(config.ERROR_INVALID_SELECTION)
            self.canvas.clear_highlights()
        except Exception as e:
            # Handle unexpected errors
            self.control_panel.display_error(f"Error: {str(e)}")
            self.canvas.clear_highlights()

    def _on_reset_clicked(self) -> None:
        # Clear display
        self.control_panel.clear_display()

        # Clear canvas highlights
        self.canvas.clear_highlights()