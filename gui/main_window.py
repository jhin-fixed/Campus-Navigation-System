from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from models.graph import Graph
from models.pathfinder import PathFinder
from gui.graph_canvas import GraphCanvas
from gui.control_panel import ControlPanel
from gui.results_panel import ResultsPanel
from utils.helpers import format_eta_display, format_path_display, calculate_eta
import config


class MainWindow(QMainWindow):

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # Load graph data
        self.graph = Graph()
        try:
            self.graph.load_from_json(config.GRAPH_DATA_FILE)
        except Exception as e:
            print(f"Error loading graph: {e}")
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

        self.setStyleSheet(f"background-color: {config.BACKGROUND_COLOR};")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.canvas = GraphCanvas(self.graph)
        # Add subtle shadow/border around canvas
        self.canvas.setStyleSheet("""
            border: 2px solid #B0BEC5;
            background-color: white;
        """)
        main_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        bottom_wrapper = QHBoxLayout()
        bottom_wrapper.setContentsMargins(0, 0, 0, 0)
        bottom_wrapper.setSpacing(0)

        bottom_wrapper.addStretch()

        # Create bottom panel layout (horizontal: controls left, results right)
        bottom_panel_layout = QHBoxLayout()
        bottom_panel_layout.setContentsMargins(0, 0, 0, 0)
        bottom_panel_layout.setSpacing(0)

        # Create control panel (bottom-left)
        self.control_panel = ControlPanel(self.graph)
        bottom_panel_layout.addWidget(self.control_panel)

        # Create results panel (bottom-right)
        self.results_panel = ResultsPanel()
        bottom_panel_layout.addWidget(self.results_panel)

        # Create bottom panel widget (centered, ~450px wide)
        bottom_panel_widget = QWidget()
        bottom_panel_widget.setLayout(bottom_panel_layout)
        bottom_panel_widget.setFixedSize(470, config.BOTTOM_PANEL_HEIGHT)
        # Add subtle shadow/border around bottom panel
        bottom_panel_widget.setStyleSheet(f"""
            border: 2px solid #B0BEC5;
            border-radius: 8px;
            background-color: {config.BACKGROUND_COLOR};
        """)

        bottom_wrapper.addWidget(bottom_panel_widget)

        bottom_wrapper.addStretch()

        bottom_wrapper_widget = QWidget()
        bottom_wrapper_widget.setLayout(bottom_wrapper)
        bottom_wrapper_widget.setFixedHeight(config.BOTTOM_PANEL_HEIGHT)

        main_layout.addWidget(bottom_wrapper_widget)

        central_widget.setLayout(main_layout)

    def _connect_signals(self) -> None:
        """Connect signals from control panel to handler methods."""
        self.control_panel.calculate_clicked.connect(self._on_calculate_clicked)
        self.control_panel.reset_clicked.connect(self._on_reset_clicked)

    def _on_calculate_clicked(self) -> None:
        """Handle calculate button click."""
        try:
            # Get selected nodes
            start_id = self.control_panel.get_selected_start()
            dest_id = self.control_panel.get_selected_destination()

            # Validate: check if same location
            if start_id == dest_id:
                self.results_panel.display_error(config.ERROR_SAME_LOCATION)
                self.canvas.clear_highlights()
                return

            # Find shortest path
            path, total_weight = self.pathfinder.find_shortest_path(start_id, dest_id)

            # Check if path exists
            if path is None or total_weight == float('inf'):
                self.results_panel.display_error(config.ERROR_NO_PATH)
                self.canvas.clear_highlights()
                return

            # Calculate ETA
            eta = calculate_eta(total_weight)

            # Get building names for path (using letters)
            path_names = []
            for node_id in path:
                node = self.graph.get_node(node_id)
                if node:
                    path_names.append(node.letter)

            # Format display strings
            eta_text = format_eta_display(eta)
            path_text = format_path_display(path_names)

            # Display results
            self.results_panel.display_result(eta_text, path_text)

            # Highlight path on canvas
            self.canvas.highlight_path(path)

        except ValueError as e:
            # Handle invalid dropdown selection
            self.results_panel.display_error(config.ERROR_INVALID_SELECTION)
            self.canvas.clear_highlights()
        except Exception as e:
            # Handle unexpected errors
            self.results_panel.display_error(f"Error: {str(e)}")
            self.canvas.clear_highlights()

    def _on_reset_clicked(self) -> None:
        """Handle reset button click."""
        # Clear display
        self.results_panel.clear_display()

        # Clear canvas highlights
        self.canvas.clear_highlights()