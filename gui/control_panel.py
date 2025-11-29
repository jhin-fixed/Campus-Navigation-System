from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QPushButton,
                             QLabel, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from models.graph import Graph
from utils.helpers import format_dropdown_item, parse_dropdown_selection
import config


class ControlPanel(QWidget):

    # Signals
    calculate_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()

    def __init__(self, graph: Graph, parent=None):
        """
        Initialize the control panel.

        Args:
            graph: Graph object containing nodes
            parent: Parent widget
        """
        super().__init__(parent)
        self.graph = graph

        # Set fixed width
        self.setFixedWidth(config.PANEL_WIDTH)

        # Setup UI components
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title = QLabel("Campus Navigator")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Add spacing
        layout.addSpacing(10)

        # Start location label
        start_label = QLabel("Start Location:")
        start_label.setWordWrap(True)
        layout.addWidget(start_label)

        # Start location dropdown
        self.start_dropdown = QComboBox()
        self._populate_dropdown(self.start_dropdown)
        layout.addWidget(self.start_dropdown)

        # Add spacing
        layout.addSpacing(5)

        # Destination label
        dest_label = QLabel("Destination:")
        dest_label.setWordWrap(True)
        layout.addWidget(dest_label)

        # Destination dropdown
        self.dest_dropdown = QComboBox()
        self._populate_dropdown(self.dest_dropdown)
        layout.addWidget(self.dest_dropdown)

        # Add spacing
        layout.addSpacing(10)

        # Calculate button
        self.calc_button = QPushButton("Calculate Route")
        self.calc_button.clicked.connect(self.calculate_clicked.emit)
        layout.addWidget(self.calc_button)

        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        layout.addWidget(self.reset_button)

        # Add spacing
        layout.addSpacing(15)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Add spacing
        layout.addSpacing(10)

        # Results section label
        results_label = QLabel("Results:")
        results_font = QFont()
        results_font.setBold(True)
        results_label.setFont(results_font)
        layout.addWidget(results_label)

        # ETA display label
        self.eta_label = QLabel("")
        self.eta_label.setWordWrap(True)
        self.eta_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.eta_label)

        # Path display label
        self.path_label = QLabel("")
        self.path_label.setWordWrap(True)
        self.path_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.path_label)

        # Error/status label
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.status_label.setStyleSheet(f"color: rgb{config.COLOR_ERROR_TEXT};")
        layout.addWidget(self.status_label)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.setLayout(layout)

    def _populate_dropdown(self, dropdown: QComboBox) -> None:
        """
        Populate a dropdown with all nodes from the graph.

        Args:
            dropdown: QComboBox to populate
        """
        # Get all nodes sorted by ID
        nodes = self.graph.get_all_nodes()

        # Add each node in "ID - Name" format
        for node in nodes:
            item_text = format_dropdown_item(node.id, node.name)
            dropdown.addItem(item_text)

    def get_selected_start(self) -> int:
        """
        Get the ID of the selected start location.

        Returns:
            Node ID of start location

        Raises:
            ValueError: If selection is invalid
        """
        text = self.start_dropdown.currentText()
        return parse_dropdown_selection(text)

    def get_selected_destination(self) -> int:
        """
        Get the ID of the selected destination.

        Returns:
            Node ID of destination

        Raises:
            ValueError: If selection is invalid
        """
        text = self.dest_dropdown.currentText()
        return parse_dropdown_selection(text)


    def clear_display(self) -> None:

        self.eta_label.clear()
        self.path_label.clear()
        self.status_label.clear()