import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow
import config


def main():
    # Create Qt application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Campus Navigator")
    app.setOrganizationName("Campus Navigator")

    try:
        # Create and show main window
        window = MainWindow()
        window.show()

        # Start event loop
        sys.exit(app.exec_())

    except FileNotFoundError as e:
        # Handle missing data file
        error_msg = f"{config.ERROR_LOAD_FAILED}\n\nDetails: {str(e)}"
        QMessageBox.critical(None, "Error", error_msg)
        sys.exit(1)

    except Exception as e:
        # Handle any other errors during startup
        error_msg = f"Failed to start application.\n\nError: {str(e)}"
        QMessageBox.critical(None, "Error", error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()