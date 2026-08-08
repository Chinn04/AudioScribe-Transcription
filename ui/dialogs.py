"""
ui/dialogs.py
Small reusable dialogs: error messages, an export-filename prompt,
and an About box. Kept separate from main_window.py to keep that
file focused on layout/orchestration.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt

import config


def show_error(parent, title: str, message: str):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle(title)
    box.setText(message)
    box.setStyleSheet(f"""
        QMessageBox {{ background-color: {config.COLOR_CARD}; }}
        QLabel {{ color: {config.COLOR_TEXT}; }}
        QPushButton {{
            background-color: {config.COLOR_PRIMARY};
            color: white; border-radius: 8px; padding: 6px 16px;
        }}
    """)
    box.exec()


def show_info(parent, title: str, message: str):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle(title)
    box.setText(message)
    box.setStyleSheet(f"""
        QMessageBox {{ background-color: {config.COLOR_CARD}; }}
        QLabel {{ color: {config.COLOR_TEXT}; }}
        QPushButton {{
            background-color: {config.COLOR_PRIMARY};
            color: white; border-radius: 8px; padding: 6px 16px;
        }}
    """)
    box.exec()


class ExportNameDialog(QDialog):
    """Prompts the user for an output file name before exporting."""

    def __init__(self, parent, default_name: str, format_label: str):
        super().__init__(parent)
        self.setWindowTitle(f"Export as {format_label}")
        self.setFixedSize(380, 150)
        self._result_name = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        label = QLabel(f"File name for {format_label} export:")
        self.input = QLineEdit(default_name)
        self.input.selectAll()

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QPushButton("Export", objectName="primaryButton")
        ok_btn.clicked.connect(self._on_accept)
        ok_btn.setDefault(True)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)

        layout.addWidget(label)
        layout.addWidget(self.input)
        layout.addLayout(btn_row)

    def _on_accept(self):
        name = self.input.text().strip()
        if name:
            self._result_name = name
            self.accept()

    @property
    def file_name(self):
        return self._result_name

    @staticmethod
    def get_name(parent, default_name: str, format_label: str):
        dialog = ExportNameDialog(parent, default_name, format_label)
        if dialog.exec() == QDialog.Accepted:
            return dialog.file_name
        return None
