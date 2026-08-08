"""
engine/audio_processor.py
Handles MP3 validation, metadata extraction, and any pre-processing
(e.g. converting to a WAV suitable for the model) needed before
transcription. Kept independent of the UI and the transcription engine.
"""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional

from mutagen.mp3 import MP3
from mutagen import MutagenError

import config


class AudioValidationError(Exception):
    """Raised when a selected file is not a usable MP3."""


@dataclass
class AudioInfo:
    file_path: str
    file_name: str
    file_size_bytes: int
    duration_seconds: float
    bitrate_kbps: int
    sample_rate_hz: int
    channels: int

    @property
    def file_size_human(self) -> str:
        size = self.file_size_bytes
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @property
    def duration_human(self) -> str:
        total = int(self.duration_seconds)
        hours, rem = divmod(total, 3600)
        minutes, seconds = divmod(rem, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"


class AudioProcessor:
    """Validates MP3 input and extracts metadata used by the UI."""

    @staticmethod
    def is_ffmpeg_available() -> bool:
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def validate_file(file_path: str) -> None:
        """Raise AudioValidationError if the file is not an acceptable MP3."""
        if not file_path:
            raise AudioValidationError("No file was selected.")

        if not os.path.isfile(file_path):
            raise AudioValidationError("The selected file does not exist.")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in config.ALLOWED_EXTENSIONS:
            raise AudioValidationError(
                f"Unsupported file type '{ext}'. Only .mp3 files are accepted."
            )

        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > config.MAX_FILE_SIZE_MB:
            raise AudioValidationError(
                f"File is too large ({size_mb:.1f} MB). "
                f"Maximum supported size is {config.MAX_FILE_SIZE_MB} MB."
            )

        # Confirm the file actually decodes as MP3 (catches corrupt / renamed files).
        try:
            MP3(file_path)
        except MutagenError as exc:
            raise AudioValidationError(
                "This file could not be read as a valid MP3. It may be corrupted "
                "or renamed from another format."
            ) from exc

    @staticmethod
    def get_audio_info(file_path: str) -> AudioInfo:
        """Extract metadata for display in the UI. Assumes validate_file() passed."""
        try:
            audio = MP3(file_path)
        except MutagenError as exc:
            raise AudioValidationError("Unable to read MP3 metadata.") from exc

        info = audio.info
        return AudioInfo(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            file_size_bytes=os.path.getsize(file_path),
            duration_seconds=float(getattr(info, "length", 0.0)),
            bitrate_kbps=int(getattr(info, "bitrate", 0) / 1000),
            sample_rate_hz=int(getattr(info, "sample_rate", 0)),
            channels=int(getattr(info, "channels", 0)),
        )

    @staticmethod
    def convert_to_wav(file_path: str, out_dir: str = config.TEMP_DIR) -> str:
        """
        Convert the MP3 to a 16kHz mono WAV via ffmpeg for more reliable,
        faster decoding by the Whisper model. Returns the WAV path.
        """
        if not AudioProcessor.is_ffmpeg_available():
            raise AudioValidationError(
                "FFmpeg was not found on this system. Please install FFmpeg "
                "and ensure it is on your PATH."
            )

        os.makedirs(out_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(file_path))[0]
        wav_path = os.path.join(out_dir, f"{base}_16k.wav")

        cmd = [
            "ffmpeg", "-y", "-i", file_path,
            "-ar", "16000", "-ac", "1", "-f", "wav", wav_path,
        ]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0 or not os.path.exists(wav_path):
            raise AudioValidationError(
                "FFmpeg failed to process this MP3 file. It may be corrupted.\n"
                f"Details: {result.stderr[-400:]}"
            )
        return wav_path

    @staticmethod
    def cleanup_temp(path: Optional[str]) -> None:
        if path and os.path.exists(path) and path.startswith(config.TEMP_DIR):
            try:
                os.remove(path)
            except OSError:
                pass
