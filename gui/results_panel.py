from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config


class ResultsPanel(QWidget):
    """Panel for displaying calculation results."""

    def __init__(self, parent=None):
        """
        Initialize the results panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Set fixed width
        self.setFixedWidth(config.RESULTS_PANEL_WIDTH)

        # Setup UI components
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup all UI components and layout."""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        # Set panel background and styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.BACKGROUND_COLOR};
            }}
            QLabel {{
                color: {config.TEXT_COLOR};
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: transparent;
                border: none;
            }}
        """)

        # ETA section
        eta_header = QLabel("ETA :")
        eta_font = QFont()
        eta_font.setBold(True)
        eta_font.setPointSize(11)
        eta_font.setFamily("Segoe UI")
        eta_header.setFont(eta_font)
        layout.addWidget(eta_header)

        # ETA display label
        self.eta_label = QLabel("")
        self.eta_label.setWordWrap(True)
        self.eta_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        eta_display_font = QFont()
        eta_display_font.setPointSize(11)
        eta_display_font.setFamily("Segoe UI")
        self.eta_label.setFont(eta_display_font)
        layout.addWidget(self.eta_label)

        # Add spacing
        layout.addSpacing(10)

        # Path sequence header
        path_header = QLabel("Path Sequence :")
        path_header.setFont(eta_font)
        layout.addWidget(path_header)

        # Path display label
        self.path_label = QLabel("")
        self.path_label.setWordWrap(True)
        self.path_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        path_display_font = QFont()
        path_display_font.setPointSize(11)
        path_display_font.setFamily("Segoe UI")
        self.path_label.setFont(path_display_font)
        layout.addWidget(self.path_label)

        # Error/status label (only shows when there's an error)
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        status_font = QFont()
        status_font.setPointSize(11)
        status_font.setFamily("Segoe UI")
        self.status_label.setFont(status_font)
        layout.addWidget(self.status_label)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.setLayout(layout)

    def display_result(self, eta_text: str, path_text: str) -> None:
        """
        Display calculation results.

        Args:
            eta_text: Formatted ETA string (e.g., "ETA: 8.5 min")
            path_text: Formatted path string (e.g., "START: X | VIA: Y | END: Z")
        """
        # Clear any previous error
        self.status_label.clear()

        # Display results with success color
        self.eta_label.setText(eta_text)
        self.eta_label.setStyleSheet(f"color: {config.SUCCESS_COLOR}; font-weight: bold;")

        self.path_label.setText(path_text)
        self.path_label.setStyleSheet(f"color: {config.TEXT_COLOR};")

    def display_error(self, message: str) -> None:
        """
        Display an error message.

        Args:
            message: Error message to display
        """
        # Clear results
        self.eta_label.clear()
        self.path_label.clear()

        # Show error with error color
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {config.ERROR_COLOR}; font-weight: bold;")

    def clear_display(self) -> None:
        """Clear all display labels (results and errors)."""
        self.eta_label.clear()
        self.path_label.clear()
        self.status_label.clear()