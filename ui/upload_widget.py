"""
ui/upload_widget.py
A drag-and-drop + browse-button widget for selecting a single MP3 file.
Emits fileSelected(path) once a valid file is chosen; emits
validationFailed(message) if the drop/selection is rejected.
"""

import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QSizePolicy,
)

from engine.audio_processor import AudioProcessor, AudioValidationError
import config


class UploadWidget(QWidget):
    fileSelected = Signal(str)
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.drop_area = QWidget(objectName="uploadArea")
        self.drop_area.setProperty("dragActive", "false")
        self.drop_area.setMinimumHeight(190)
        self.drop_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        inner = QVBoxLayout(self.drop_area)
        inner.setAlignment(Qt.AlignCenter)
        inner.setSpacing(10)

        icon = QLabel("🎧")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 42px;")

        title = QLabel("Drag & drop an MP3 file here", objectName="uploadTitle")
        title.setAlignment(Qt.AlignCenter)

        hint = QLabel("or click Browse below  •  .mp3 only  •  up to "
                      f"{config.MAX_FILE_SIZE_MB} MB", objectName="uploadHint")
        hint.setAlignment(Qt.AlignCenter)

        browse_row = QHBoxLayout()
        browse_row.setAlignment(Qt.AlignCenter)
        self.browse_btn = QPushButton("Browse MP3 File")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setFixedWidth(190)
        self.browse_btn.clicked.connect(self._on_browse_clicked)
        browse_row.addWidget(self.browse_btn)

        inner.addWidget(icon)
        inner.addWidget(title)
        inner.addWidget(hint)
        inner.addLayout(browse_row)

        outer.addWidget(self.drop_area)

    # -- Drag & drop events ------------------------------------------------
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_drag_active(True)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._set_drag_active(False)

    def dropEvent(self, event: QDropEvent):
        self._set_drag_active(False)
        urls = event.mimeData().urls()
        if not urls:
            return
        path = urls[0].toLocalFile()
        self._handle_candidate_path(path)

    def _set_drag_active(self, active: bool):
        self.drop_area.setProperty("dragActive", "true" if active else "false")
        self.drop_area.style().unpolish(self.drop_area)
        self.drop_area.style().polish(self.drop_area)

    # -- Browse button -------------------------------------------------------
    def _on_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select MP3 File", os.path.expanduser("~"),
            "MP3 Audio Files (*.mp3)"
        )
        if path:
            self._handle_candidate_path(path)

    # -- Shared validation ---------------------------------------------------
    def _handle_candidate_path(self, path: str):
        try:
            AudioProcessor.validate_file(path)
        except AudioValidationError as exc:
            self.validationFailed.emit(str(exc))
            return
        self.fileSelected.emit(path)
