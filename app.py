"""
app.py
Entry point for AudioScribe AI. Run this file to launch the desktop app:

    python app.py

To package as a Windows .exe (after installing pyinstaller):

    pyinstaller --noconsole --onefile --name AudioScribeAI ^
        --add-data "assets;assets" app.py
"""

import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

import config
from ui.main_window import MainWindow


def main():
    # Ensure the working directory is the app root regardless of how it's launched,
    # so relative asset/output paths resolve correctly.
    os.chdir(config.BASE_DIR)

    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setOrganizationName(config.ORG_NAME)

    if os.path.exists(config.LOGO_PATH):
        app.setWindowIcon(QIcon(config.LOGO_PATH))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
