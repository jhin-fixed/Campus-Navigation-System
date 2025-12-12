from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                             QPushButton, QLabel)
from PyQt5.QtCore import pyqtSignal, Qt
from typing import Dict
from models.graph import Graph
from utils.helpers import format_dropdown_item, parse_dropdown_selection
import config


class ControlPanel(QWidget):
    """Control panel for selecting locations."""

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

        # Build letter to ID mapping
        self.letter_to_id: Dict[str, int] = {}
        for node in graph.get_all_nodes():
            self.letter_to_id[node.letter] = node.id

        # Set fixed width
        self.setFixedWidth(config.CONTROL_PANEL_WIDTH)

        # Setup UI components
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup all UI components and layout."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Set panel background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.BACKGROUND_COLOR};
            }}
            QLabel {{
                color: {config.TEXT_COLOR};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
            }}
            QComboBox {{
                background-color: white;
                border: 2px solid {config.SECONDARY_COLOR};
                border-radius: 6px;
                padding: 6px;
                color: {config.TEXT_COLOR};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }}
            QComboBox:hover {{
                border: 2px solid {config.ACCENT_COLOR};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QPushButton {{
                background-color: {config.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 6px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
                font-weight: bold;
                min-height: 10px;
            }}
            QPushButton:hover {{
                background-color: {config.BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {config.ACCENT_COLOR};
            }}
        """)

        # Start location label
        start_label = QLabel("Starting Location")
        start_label.setWordWrap(True)
        layout.addWidget(start_label)

        # Start location dropdown
        self.start_dropdown = QComboBox()
        self._populate_dropdown(self.start_dropdown)
        layout.addWidget(self.start_dropdown)

        # Add spacing
        layout.addSpacing(8)

        # Destination label
        dest_label = QLabel("Destination")
        dest_label.setWordWrap(True)
        layout.addWidget(dest_label)

        # Destination dropdown
        self.dest_dropdown = QComboBox()
        self._populate_dropdown(self.dest_dropdown)
        layout.addWidget(self.dest_dropdown)

        # Add spacing
        layout.addSpacing(8)

        # Buttons layout (side by side)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_clicked.emit)
        self.calc_button.setCursor(Qt.PointingHandCursor)
        self.calc_button.setMinimumWidth(55)
        buttons_layout.addWidget(self.calc_button)

        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.setMinimumWidth(55)
        buttons_layout.addWidget(self.reset_button)

        layout.addLayout(buttons_layout)

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

        # Add each node in "Letter - Name" format
        for node in nodes:
            item_text = format_dropdown_item(node.letter, node.name)
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
        letter = parse_dropdown_selection(text)
        return self.letter_to_id[letter]

    def get_selected_destination(self) -> int:
        """
        Get the ID of the selected destination.

        Returns:
            Node ID of destination

        Raises:
            ValueError: If selection is invalid
        """
        text = self.dest_dropdown.currentText()
        letter = parse_dropdown_selection(text)
        return self.letter_to_id[letter]