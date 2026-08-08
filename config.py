"""
config.py
Central configuration for AudioScribe AI.
All constants, paths, and app-wide settings live here so nothing
is hard-coded inside the UI or engine modules.
"""

import os
import sys


def _base_dir() -> str:
    """Return the directory the app is running from (handles PyInstaller .exe)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = _base_dir()
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

for _d in (ASSETS_DIR, ICONS_DIR, OUTPUTS_DIR, TEMP_DIR):
    os.makedirs(_d, exist_ok=True)

# ---------------------------------------------------------------------------
# Application identity
# ---------------------------------------------------------------------------
APP_NAME = "AudioScribe AI"
APP_SUBTITLE = "Offline MP3 Speech-to-Text Converter"
APP_VERSION = "1.0.0"
ORG_NAME = "AudioScribeAI"

# ---------------------------------------------------------------------------
# Whisper / Faster-Whisper settings
# ---------------------------------------------------------------------------
# Model size options: tiny, base, small, medium, large-v2, large-v3
DEFAULT_MODEL_SIZE = "small"
AVAILABLE_MODEL_SIZES = ["tiny", "base", "small", "medium", "large-v3"]

# "auto" runs on GPU if CUDA is available, otherwise CPU.
DEVICE = "auto"
COMPUTE_TYPE_GPU = "float16"
COMPUTE_TYPE_CPU = "int8"

# Full language list supported by Whisper (code -> display name).
# This drives the manual-language dropdown; "Auto Detect" is always first.
WHISPER_LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English", "hi": "Hindi", "kn": "Kannada", "ta": "Tamil",
    "te": "Telugu", "ml": "Malayalam", "mr": "Marathi", "bn": "Bengali",
    "gu": "Gujarati", "pa": "Punjabi", "ur": "Urdu", "ar": "Arabic",
    "zh": "Chinese", "ja": "Japanese", "ko": "Korean", "fr": "French",
    "de": "German", "es": "Spanish", "it": "Italian", "pt": "Portuguese",
    "ru": "Russian", "nl": "Dutch", "tr": "Turkish", "pl": "Polish",
    "id": "Indonesian", "vi": "Vietnamese", "th": "Thai", "uk": "Ukrainian",
    "el": "Greek", "he": "Hebrew", "fa": "Persian", "sw": "Swahili",
    "ro": "Romanian", "hu": "Hungarian", "cs": "Czech", "fi": "Finnish",
    "sv": "Swedish", "da": "Danish", "no": "Norwegian", "sk": "Slovak",
    "sr": "Serbian", "hr": "Croatian", "bg": "Bulgarian", "lt": "Lithuanian",
    "lv": "Latvian", "et": "Estonian", "ms": "Malay", "tl": "Filipino",
    "sq": "Albanian", "az": "Azerbaijani", "km": "Khmer", "ne": "Nepali",
    "si": "Sinhala", "my": "Burmese", "af": "Afrikaans", "am": "Amharic",
    "hy": "Armenian", "as": "Assamese", "eu": "Basque", "be": "Belarusian",
    "bs": "Bosnian", "ca": "Catalan", "cy": "Welsh", "gl": "Galician",
    "ka": "Georgian", "gu": "Gujarati", "is": "Icelandic", "kk": "Kazakh",
    "lo": "Lao", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy",
    "mt": "Maltese", "mn": "Mongolian", "ps": "Pashto", "sd": "Sindhi",
    "so": "Somali", "tg": "Tajik", "uz": "Uzbek", "yo": "Yoruba",
    "or": "Odia",
}

# ---------------------------------------------------------------------------
# Output script (Original vs. Romanized transliteration)
# ---------------------------------------------------------------------------
# Purely a display/export choice - both versions are produced from the same
# single transcription pass, never from re-running Whisper.
OUTPUT_SCRIPT_ORIGINAL = "Original Script"
OUTPUT_SCRIPT_ROMANIZED = "Romanized / English Letters"
OUTPUT_SCRIPT_OPTIONS = [OUTPUT_SCRIPT_ROMANIZED, OUTPUT_SCRIPT_ORIGINAL]
DEFAULT_OUTPUT_SCRIPT = OUTPUT_SCRIPT_ROMANIZED

# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------
ALLOWED_EXTENSIONS = (".mp3",)
MAX_FILE_SIZE_MB = 500

# ---------------------------------------------------------------------------
# Pipeline stages shown in the progress UI
# ---------------------------------------------------------------------------
STAGE_LOADING_MODEL = "Loading Model"
STAGE_CONVERTING_AUDIO = "Converting Audio"
STAGE_READING_AUDIO = "Reading MP3"
STAGE_DETECTING_LANGUAGE = "Detecting Language"
STAGE_TRANSCRIBING = "Transcribing"
STAGE_FINALIZING = "Finalizing"
STAGE_DONE = "Done"

# ---------------------------------------------------------------------------
# UI palette (used by ui/styles.py)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = "#0F172A"
COLOR_BACKGROUND_ALT = "#111827"
COLOR_CARD = "#1E293B"
COLOR_CARD_LIGHT = "#273449"
COLOR_BORDER = "#334155"
COLOR_PRIMARY = "#3B82F6"
COLOR_PRIMARY_DARK = "#2563EB"
COLOR_ACCENT = "#06B6D4"
COLOR_SUCCESS = "#22C55E"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
COLOR_TEXT = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"
