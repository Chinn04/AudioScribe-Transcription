# AudioScribe AI

Offline MP3 → text transcription desktop app, built with **PySide6** and
**Faster-Whisper**. Auto-detects the spoken language (Whisper's full
language set) or lets you pick one manually, and exports the result to
TXT, DOCX, or PDF.

---

## 1. Prerequisites

- **Python 3.10–3.11** (Faster-Whisper/ctranslate2 wheels target these)
- **FFmpeg** installed and on your system `PATH`
  - Windows: `winget install ffmpeg` (or download from ffmpeg.org and add to PATH)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- (Optional, for GPU speed) a CUDA-capable GPU + `torch` with CUDA installed.
  Without it, the app automatically runs on CPU using an `int8` model.

## 2. Setup

```bash
cd AudioScribeAI
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

The first time you transcribe a file, Faster-Whisper will download the
selected model (default: `small`) from Hugging Face and cache it locally.
After that first download, the app runs **fully offline**.

To change the default model size (`tiny`/`base`/`small`/`medium`/`large-v3`),
edit `DEFAULT_MODEL_SIZE` in `config.py`. Larger models are more accurate
but slower and use more RAM/VRAM.

## 3. Run

```bash
python app.py
```

## 4. Using the app

1. Drag an `.mp3` file onto the upload area, or click **Browse MP3 File**.
2. Review the file's duration, bitrate, and sample rate in the info card.
3. Pick a language from the dropdown, or leave it on **Auto Detect**.
4. Click **Start Transcription** — the progress bar walks through
   Loading Model → Reading MP3 → Detecting Language → Transcribing → Finalizing.
5. Edit the result freely in the text area if needed.
6. Use **Copy Text**, **Export TXT**, **Export DOCX**, or **Export PDF**.
   Exported files are saved to the `outputs/` folder by default (you can
   type a full path in the export dialog too).

## 5. Project structure

```
AudioScribeAI/
├── app.py                 # Entry point
├── config.py               # Paths, palette, language list, constants
├── requirements.txt
├── assets/
│   ├── logo.png
│   └── icons/
├── ui/
│   ├── main_window.py      # Layout + orchestration + worker thread
│   ├── upload_widget.py    # Drag & drop / browse widget
│   ├── styles.py            # QSS dark/glassmorphism theme
│   └── dialogs.py           # Error / export-name / info dialogs
├── engine/
│   ├── audio_processor.py  # MP3 validation, metadata, ffmpeg conversion
│   ├── transcriber.py       # Faster-Whisper wrapper + progress callbacks
│   └── exporter.py          # TXT / DOCX / PDF writers
├── outputs/                 # Default export destination
└── temp/                    # Scratch WAV files (auto-cleaned)
```

## 6. Packaging as a Windows .exe

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name AudioScribeAI ^
    --add-data "assets;assets" app.py
```

The built executable will be in `dist/AudioScribeAI.exe`. Note that
Faster-Whisper model files are downloaded/cached separately (under the
user's Hugging Face cache directory) and are not bundled into the .exe —
run the app once with an internet connection first so the chosen model
is cached, after which it works fully offline.

## 7. Notes on accuracy & formatting

- Faster-Whisper applies punctuation and capitalization per segment as
  part of its decoding; the app joins segments into clean paragraphs
  without altering the model's own formatting choices.
- Voice-activity detection (VAD) is enabled by default to skip silent
  stretches and reduce hallucinated text on quiet audio.
- For best accuracy on non-English audio, try manually selecting the
  language instead of Auto Detect — it skips the detection pass and
  avoids occasional misdetection on short clips.
