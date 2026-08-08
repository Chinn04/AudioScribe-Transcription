"""
ui/main_window.py
The main application window. Wires the upload widget, audio-info panel,
controls, progress bar, output editor and stats panel together, and
runs transcription on a background QThread so the UI never freezes.
"""

import os
import time

from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QPixmap, QIcon, QTextCursor
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QTextEdit, QProgressBar, QComboBox, QFrame, QSizePolicy,
    QScrollArea, QApplication,
)

import config
from engine.audio_processor import AudioProcessor, AudioInfo, AudioValidationError
from engine.transcriber import Transcriber, TranscriptionResult, TranscriberError
from engine.exporter import Exporter, ExportError
from ui.upload_widget import UploadWidget
from ui.dialogs import show_error, show_info, ExportNameDialog
from ui.styles import get_stylesheet


# =============================================================================
# Background worker
# =============================================================================
class TranscriptionWorker(QObject):
    """
    Runs the full pipeline (convert -> load model -> transcribe) off the
    UI thread. Lives inside a QThread owned by MainWindow.
    """

    progress = Signal(str, int, str)          # stage, percent, message
    finished = Signal(object)                 # TranscriptionResult
    failed = Signal(str)                      # error message

    def __init__(self, transcriber: Transcriber, mp3_path: str, language: str):
        super().__init__()
        self.transcriber = transcriber
        self.mp3_path = mp3_path
        self.language = language
        self._wav_path = None

    def run(self):
        try:
            # ffmpeg conversion time depends on file size/length and cannot be
            # estimated in advance, so this is reported as indeterminate
            # rather than a fixed, misleading percentage.
            self.progress.emit(
                config.STAGE_CONVERTING_AUDIO, -1, "Converting MP3 to WAV..."
            )
            self._wav_path = AudioProcessor.convert_to_wav(self.mp3_path)

            def cb(stage, percent, message):
                self.progress.emit(stage, percent, message)

            result = self.transcriber.transcribe(
                self._wav_path, language=self.language, progress_cb=cb
            )
            self.progress.emit(config.STAGE_DONE, 100, "Transcription complete.")
            self.finished.emit(result)
        except (AudioValidationError, TranscriberError) as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # noqa: BLE001 - surface anything unexpected
            self.failed.emit(f"Unexpected error: {exc}")
        finally:
            AudioProcessor.cleanup_temp(self._wav_path)


# =============================================================================
# Main window
# =============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} — {config.APP_SUBTITLE}")
        self.resize(1180, 800)
        self.setMinimumSize(980, 680)
        self.setStyleSheet(get_stylesheet())

        self._audio_info: AudioInfo | None = None
        self._current_result: TranscriptionResult | None = None
        self._transcriber = Transcriber(config.DEFAULT_MODEL_SIZE)
        self._thread: QThread | None = None
        self._worker: TranscriptionWorker | None = None
        self._transcribe_start_time = 0.0

        self._build_ui()
        self._reset_stats()

    # -------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        outer = QVBoxLayout(central)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(16)

        outer.addWidget(self._build_header())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.addWidget(self._build_upload_card())
        content_layout.addWidget(self._build_info_card())
        content_layout.addWidget(self._build_controls_card())
        content_layout.addWidget(self._build_progress_card())
        content_layout.addWidget(self._build_output_card(), stretch=1)
        content_layout.addWidget(self._build_stats_card())

        scroll.setWidget(content)
        outer.addWidget(scroll, stretch=1)

    def _build_header(self) -> QWidget:
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(4, 0, 4, 0)

        logo = QLabel()
        if os.path.exists(config.LOGO_PATH):
            pix = QPixmap(config.LOGO_PATH).scaledToHeight(
                44, Qt.SmoothTransformation
            )
            logo.setPixmap(pix)
        else:
            logo.setText("🎙️")
            logo.setStyleSheet("font-size: 32px;")
        logo.setFixedWidth(50)

        text_col = QVBoxLayout()
        text_col.setSpacing(0)
        title = QLabel(config.APP_NAME, objectName="appTitle")
        subtitle = QLabel(config.APP_SUBTITLE, objectName="appSubtitle")
        text_col.addWidget(title)
        text_col.addWidget(subtitle)

        layout.addWidget(logo)
        layout.addLayout(text_col)
        layout.addStretch(1)

        badge = QLabel("● Offline Ready")
        badge.setStyleSheet(
            f"color: {config.COLOR_SUCCESS}; font-weight: 600; font-size: 12px;"
        )
        layout.addWidget(badge, alignment=Qt.AlignRight | Qt.AlignVCenter)
        return header

    def _build_upload_card(self) -> QWidget:
        card = QFrame(objectName="card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        self.upload_widget = UploadWidget()
        self.upload_widget.fileSelected.connect(self._on_file_selected)
        self.upload_widget.validationFailed.connect(self._on_validation_failed)

        self.selected_file_label = QLabel("No file selected.", objectName="uploadHint")
        self.selected_file_label.setWordWrap(True)

        layout.addWidget(self.upload_widget)
        layout.addWidget(self.selected_file_label)
        return card

    def _build_info_card(self) -> QWidget:
        card = QFrame(objectName="card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("Audio Information")
        title.setStyleSheet("font-weight: 700; font-size: 14px;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(6)

        self._info_labels = {}
        fields = [
            ("File Name", "file_name"), ("File Size", "file_size"),
            ("Duration", "duration"), ("Bitrate", "bitrate"),
            ("Sample Rate", "sample_rate"), ("Detected Language", "detected_language"),
        ]
        for idx, (label_text, key) in enumerate(fields):
            row, col = divmod(idx, 3)
            box = QVBoxLayout()
            lbl = QLabel(label_text, objectName="statLabel")
            val = QLabel("—", objectName="statValue")
            val.setWordWrap(True)
            box.addWidget(lbl)
            box.addWidget(val)
            wrapper = QWidget()
            wrapper.setLayout(box)
            grid.addWidget(wrapper, row, col)
            self._info_labels[key] = val

        layout.addLayout(grid)
        return card

    def _build_controls_card(self) -> QWidget:
        card = QFrame(objectName="card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        lang_label = QLabel("Language:")
        self.language_combo = QComboBox()
        for code, name in config.WHISPER_LANGUAGES.items():
            self.language_combo.addItem(name, userData=code)
        self.language_combo.setFixedWidth(220)

        script_label = QLabel("Output Script:")
        self.output_script_combo = QComboBox()
        for option in config.OUTPUT_SCRIPT_OPTIONS:
            self.output_script_combo.addItem(option)
        self.output_script_combo.setCurrentText(config.DEFAULT_OUTPUT_SCRIPT)
        self.output_script_combo.setFixedWidth(220)
        self.output_script_combo.currentTextChanged.connect(
            self._on_output_script_changed
        )

        top_row.addWidget(lang_label)
        top_row.addWidget(self.language_combo)
        top_row.addSpacing(16)
        top_row.addWidget(script_label)
        top_row.addWidget(self.output_script_combo)
        top_row.addStretch(1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.start_btn = QPushButton("▶  Start Transcription", objectName="primaryButton")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self._on_start_clicked)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._on_clear_clicked)

        self.copy_btn = QPushButton("Copy Text")
        self.copy_btn.clicked.connect(self._on_copy_clicked)
        self.copy_btn.setEnabled(False)

        self.export_txt_btn = QPushButton("Export TXT")
        self.export_txt_btn.clicked.connect(lambda: self._on_export_clicked("txt"))
        self.export_txt_btn.setEnabled(False)

        self.export_docx_btn = QPushButton("Export DOCX")
        self.export_docx_btn.clicked.connect(lambda: self._on_export_clicked("docx"))
        self.export_docx_btn.setEnabled(False)

        self.export_pdf_btn = QPushButton("Export PDF")
        self.export_pdf_btn.clicked.connect(lambda: self._on_export_clicked("pdf"))
        self.export_pdf_btn.setEnabled(False)

        for b in (self.start_btn, self.clear_btn, self.copy_btn,
                  self.export_txt_btn, self.export_docx_btn, self.export_pdf_btn):
            btn_row.addWidget(b)
        btn_row.addStretch(1)

        layout.addLayout(top_row)
        layout.addLayout(btn_row)
        return card

    def _build_progress_card(self) -> QWidget:
        card = QFrame(objectName="card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(6)

        row = QHBoxLayout()
        self.stage_label = QLabel("Ready", objectName="stageLabel")
        self.eta_label = QLabel("", objectName="statLabel")
        row.addWidget(self.stage_label)
        row.addStretch(1)
        row.addWidget(self.eta_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        self.status_message = QLabel("", objectName="statLabel")

        layout.addLayout(row)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_message)
        return card

    def _build_output_card(self) -> QWidget:
        card = QFrame(objectName="card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("Transcribed Text")
        title.setStyleSheet("font-weight: 700; font-size: 14px;")

        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText(
            "Your transcription will appear here once processing completes..."
        )
        self.output_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.output_text.setMinimumHeight(260)
        self.output_text.textChanged.connect(self._update_word_char_stats)

        layout.addWidget(title)
        layout.addWidget(self.output_text)
        return card

    def _build_stats_card(self) -> QWidget:
        card = QFrame(objectName="card")
        layout = QGridLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setHorizontalSpacing(28)

        self._stat_labels = {}
        fields = [
            ("Word Count", "word_count"), ("Character Count", "char_count"),
            ("Audio Duration", "audio_duration"), ("Processing Time", "processing_time"),
            ("Processing Speed", "processing_speed"), ("Detected Language", "language"),
        ]
        for idx, (label_text, key) in enumerate(fields):
            box = QVBoxLayout()
            lbl = QLabel(label_text, objectName="statLabel")
            val = QLabel("0", objectName="statValue")
            box.addWidget(lbl)
            box.addWidget(val)
            wrapper = QWidget()
            wrapper.setLayout(box)
            layout.addWidget(wrapper, 0, idx)
            self._stat_labels[key] = val
        return card

    # -------------------------------------------------------------------
    # Upload handling
    # -------------------------------------------------------------------
    def _on_file_selected(self, path: str):
        try:
            info = AudioProcessor.get_audio_info(path)
        except AudioValidationError as exc:
            self._on_validation_failed(str(exc))
            return

        self._audio_info = info
        self.selected_file_label.setText(f"Selected: {info.file_name}")
        self._info_labels["file_name"].setText(info.file_name)
        self._info_labels["file_size"].setText(info.file_size_human)
        self._info_labels["duration"].setText(info.duration_human)
        self._info_labels["bitrate"].setText(f"{info.bitrate_kbps} kbps")
        self._info_labels["sample_rate"].setText(f"{info.sample_rate_hz} Hz")
        self._info_labels["detected_language"].setText("—")
        self._stat_labels["audio_duration"].setText(info.duration_human)

        self.start_btn.setEnabled(True)
        self.status_message.setText("Ready to transcribe.")
        self.stage_label.setText("Ready")
        self.progress_bar.setValue(0)

    def _on_validation_failed(self, message: str):
        show_error(self, "Invalid File", message)

    # -------------------------------------------------------------------
    # Transcription lifecycle
    # -------------------------------------------------------------------
    def _on_start_clicked(self):
        if not self._audio_info:
            return
        if not AudioProcessor.is_ffmpeg_available():
            show_error(
                self, "FFmpeg Not Found",
                "FFmpeg is required for audio processing but was not found on "
                "your system PATH. Please install FFmpeg and try again."
            )
            return

        self._set_busy(True)
        self.output_text.clear()
        self._transcribe_start_time = time.time()

        language_code = self.language_combo.currentData()

        self._thread = QThread(self)
        self._worker = TranscriptionWorker(
            self._transcriber, self._audio_info.file_path, language_code
        )
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_transcription_finished)
        self._worker.failed.connect(self._on_transcription_failed)
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup_thread)

        self._thread.start()

    def _on_progress(self, stage: str, percent: int, message: str):
        self.stage_label.setText(stage)
        self.status_message.setText(message)

        if percent < 0:
            # Duration for this stage (e.g. model loading/download, ffmpeg
            # conversion) can't be predicted - show a busy/indeterminate
            # bar instead of freezing on a fixed, misleading percentage.
            if self.progress_bar.maximum() != 0:
                self.progress_bar.setRange(0, 0)
            self.eta_label.setText("")
            return

        if self.progress_bar.maximum() == 0:
            self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(percent)

        if 0 < percent < 100:
            elapsed = time.time() - self._transcribe_start_time
            if percent > 30:
                estimated_total = elapsed / (percent / 100)
                remaining = max(estimated_total - elapsed, 0)
                self.eta_label.setText(f"ETA: {int(remaining)}s")
        else:
            self.eta_label.setText("")

    def _on_transcription_finished(self, result: TranscriptionResult):
        self._current_result = result
        self.output_text.setPlainText(self._text_for_current_script())

        lang_name = config.WHISPER_LANGUAGES.get(result.language, result.language)
        self._info_labels["detected_language"].setText(
            f"{lang_name} ({result.language_probability * 100:.0f}%)"
        )
        self._stat_labels["language"].setText(lang_name)
        self._stat_labels["processing_time"].setText(f"{result.processing_seconds:.1f}s")

        if result.processing_seconds > 0 and result.audio_duration > 0:
            speed = result.audio_duration / result.processing_seconds
            self._stat_labels["processing_speed"].setText(f"{speed:.2f}x realtime")
        else:
            self._stat_labels["processing_speed"].setText("—")

        self._set_busy(False)
        self._set_output_actions_enabled(True)
        self.eta_label.setText("")

        if result.warning:
            # Honest reporting: a suspiciously short result is NOT presented
            # as a normal success, even though the pipeline technically ran
            # to completion.
            self.stage_label.setText("Completed with warning")
            self.status_message.setText(result.warning)
            show_error(self, "Transcription Looks Incomplete", result.warning)
        else:
            self.stage_label.setText(config.STAGE_DONE)
            self.status_message.setText("Transcription complete.")

    def _on_transcription_failed(self, message: str):
        self._set_busy(False)
        self.stage_label.setText("Failed")
        self.status_message.setText(message)
        show_error(self, "Transcription Failed", message)

    def _cleanup_thread(self):
        if self._worker:
            self._worker.deleteLater()
        if self._thread:
            self._thread.deleteLater()
        self._worker = None
        self._thread = None

    def _set_busy(self, busy: bool):
        self.start_btn.setEnabled(not busy and self._audio_info is not None)
        self.upload_widget.setEnabled(not busy)
        self.language_combo.setEnabled(not busy)
        self.output_script_combo.setEnabled(not busy)
        self.clear_btn.setEnabled(not busy)
        if busy:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)

    # -------------------------------------------------------------------
    # Output script (Original vs. Romanized)
    # -------------------------------------------------------------------
    def _text_for_current_script(self) -> str:
        """
        Returns the transcript text matching the currently selected
        'Output Script' option, from the already-computed result. Both
        versions were produced in the same transcription pass (see
        engine/transcriber.py), so switching here never re-runs Whisper.
        """
        if not self._current_result:
            return ""
        if self.output_script_combo.currentText() == config.OUTPUT_SCRIPT_ROMANIZED:
            return self._current_result.romanized_text or self._current_result.text
        return self._current_result.text

    def _on_output_script_changed(self, _text: str):
        # Only swap the display if we already have a finished result -
        # otherwise this is just the combo initializing/being restored
        # and there's nothing to redisplay yet.
        if self._current_result:
            self.output_text.setPlainText(self._text_for_current_script())

    # -------------------------------------------------------------------
    # Output actions
    # -------------------------------------------------------------------
    def _on_copy_clicked(self):
        QApplication.clipboard().setText(self.output_text.toPlainText())
        self.status_message.setText("Text copied to clipboard.")

    def _on_clear_clicked(self):
        self._audio_info = None
        self._current_result = None
        self.output_text.clear()
        self.selected_file_label.setText("No file selected.")
        for lbl in self._info_labels.values():
            lbl.setText("—")
        self._reset_stats()
        self.progress_bar.setValue(0)
        self.stage_label.setText("Ready")
        self.status_message.setText("")
        self.eta_label.setText("")
        self.start_btn.setEnabled(False)
        self._set_output_actions_enabled(False)

    def _set_output_actions_enabled(self, enabled: bool):
        self.copy_btn.setEnabled(enabled)
        self.export_txt_btn.setEnabled(enabled)
        self.export_docx_btn.setEnabled(enabled)
        self.export_pdf_btn.setEnabled(enabled)

    def _on_export_clicked(self, fmt: str):
        if not self._current_result:
            return
        text = self.output_text.toPlainText()
        base_name = "transcript"
        if self._audio_info:
            base_name = os.path.splitext(self._audio_info.file_name)[0]

        format_labels = {"txt": "TXT", "docx": "DOCX", "pdf": "PDF"}
        name = ExportNameDialog.get_name(self, base_name, format_labels[fmt])
        if not name:
            return

        try:
            lang_name = config.WHISPER_LANGUAGES.get(
                self._current_result.language, self._current_result.language
            )
            source_name = self._audio_info.file_name if self._audio_info else ""

            if fmt == "txt":
                path = Exporter.export_txt(text, name)
            elif fmt == "docx":
                path = Exporter.export_docx(
                    text, name, source_file=source_name, language=lang_name
                )
            else:
                path = Exporter.export_pdf(
                    text, name, source_file=source_name, language=lang_name
                )
        except ExportError as exc:
            show_error(self, "Export Failed", str(exc))
            return

        show_info(self, "Export Complete", f"Saved to:\n{path}")

    # -------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------
    def _update_word_char_stats(self):
        text = self.output_text.toPlainText()
        words = len(text.split())
        chars = len(text)
        self._stat_labels["word_count"].setText(str(words))
        self._stat_labels["char_count"].setText(str(chars))

    def _reset_stats(self):
        for key in self._stat_labels:
            self._stat_labels[key].setText("0")
        self._stat_labels["language"].setText("—")
        self._stat_labels["processing_speed"].setText("—")

    # -------------------------------------------------------------------
    def closeEvent(self, event):
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(2000)
        event.accept()
