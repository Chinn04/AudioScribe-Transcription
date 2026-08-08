# 🎙️ AudioScribe AI

> **Offline MP3 Speech-to-Text & Romanization Desktop Application**

AudioScribe AI is a professional Windows desktop application built with **Python, PySide6, and Faster-Whisper** for converting MP3 audio into accurate text.

The application is designed with an **offline-first architecture**, providing speech transcription, language detection, Indic-language romanization, transcript editing, statistics, and document export capabilities through a modern desktop interface.

It is particularly useful for users who need to convert spoken audio into readable text while keeping the complete transcription workflow locally on their system.

---

## ✨ Key Features

### 🎧 MP3 Speech-to-Text

* Upload MP3 audio files through a simple desktop interface.
* Supports drag-and-drop file selection.
* Validates uploaded audio before processing.
* Displays audio metadata including:

  * File name
  * File size
  * Duration
  * Bitrate
  * Sample rate
* Converts MP3 audio into a processing-friendly WAV format using FFmpeg.
* Uses Faster-Whisper for speech recognition.

### 🌍 Multi-Language Transcription

AudioScribe AI supports automatic language detection as well as manual language selection.

Supported languages include:

* English
* Hindi
* Kannada
* Tamil
* Telugu
* Malayalam
* Marathi
* Bengali
* Gujarati
* Punjabi
* Urdu
* Arabic
* Chinese
* Japanese
* Korean
* French
* German
* Spanish
* Italian
* Portuguese
* Russian
* Dutch
* Turkish
* Polish
* Indonesian
* Vietnamese
* Thai
* Ukrainian
* Greek
* Hebrew
* Persian
* Swahili
* Romanian
* Hungarian
* Czech
* Finnish
* Swedish
* Danish
* Norwegian
* Slovak
* Serbian
* Croatian
* Bulgarian
* Lithuanian
* Latvian
* Estonian
* Malay
* Filipino
* Albanian
* Azerbaijani
* Khmer
* Nepali
* Sinhala
* Burmese
* Afrikaans
* Amharic
* Armenian
* Assamese
* Basque
* Belarusian
* Bosnian
* Catalan
* Welsh
* Galician
* Georgian
* Icelandic
* Kazakh
* Lao
* Luxembourgish
* Macedonian
* Malagasy
* Maltese
* Mongolian
* Pashto
* Sindhi
* Somali
* Tajik
* Uzbek
* Yoruba
* Odia

> Language availability depends on the underlying Whisper model.

---

## 🔤 Romanized Output

One of the core features of AudioScribe AI is its **Romanized / English Letters output mode**.

For supported Indic languages, native-script transcription can be converted into easy-to-read Roman characters.

### Example

**Kannada:**

```text
ನೀವು ಊಟ ಮಾಡಿದ್ದೀರಾ?
```

**Romanized:**

```text
Nivu uta madidra?
```

Similarly:

**Hindi:**

```text
क्या तूने खाना खा लिया?
```

can be represented in Roman letters as:

```text
Kya tune khana kha liya?
```

The application uses local transliteration through the `indic-transliteration` library.

Romanization is **transliteration, not translation**.

The meaning and language are preserved while the writing system is changed.

---

## 📝 Original & Romanized Output

Users can choose between:

* **Romanized / English Letters**
* **Original Script**

This makes the application useful for both native-script readers and users who prefer Latin/Roman characters.

---

## 🤖 Faster-Whisper Transcription Engine

AudioScribe AI uses **Faster-Whisper**, an optimized implementation of Whisper designed for efficient speech recognition.

The transcription pipeline includes:

* Beam-search decoding
* Multiple temperature fallbacks
* Voice Activity Detection
* Previous-text contextual processing
* Repetition protection
* Speech coverage analysis
* Suspicious-result detection
* Automatic language detection
* Manual language selection

The application also checks for potentially incomplete transcription results instead of silently presenting questionable output as a successful transcription.

---

## ⚡ Background Processing

Audio transcription can be computationally intensive.

To prevent the desktop interface from freezing, AudioScribe AI runs the transcription workflow in a dedicated **Qt background thread**.

The interface remains responsive while processing.

The application provides progress stages such as:

```text
Loading Model
      ↓
Converting Audio
      ↓
Reading MP3
      ↓
Detecting Language
      ↓
Transcribing
      ↓
Finalizing
      ↓
Done
```

---

## 📊 Transcription Statistics

After processing, the application provides useful statistics including:

* Word count
* Character count
* Audio duration
* Processing time
* Processing speed
* Detected language

This provides a quick overview of the transcription result and processing performance.

---

## 📤 Export Transcripts

Completed transcripts can be exported into multiple formats.

### TXT

Simple plain-text output suitable for notes and further processing.

### DOCX

Professional Microsoft Word-compatible transcription reports containing:

* Application name
* Report title
* Source file
* Detected language
* Export timestamp
* Transcribed content

### PDF

Formatted PDF transcription reports containing:

* Application branding
* Source information
* Detected language
* Export timestamp
* Transcribed content

---

## 🖥️ Modern Desktop Interface

AudioScribe AI provides a modern dark desktop interface built using **PySide6 and Qt Style Sheets (QSS)**.

The interface includes:

* Application branding
* Offline-ready indicator
* Drag-and-drop upload area
* Audio information panel
* Language selector
* Output-script selector
* Transcription controls
* Progress tracking
* Editable transcription area
* Export controls
* Processing statistics
* Error dialogs and validation feedback

---

## 🔒 Offline-First Architecture

AudioScribe AI is designed to perform the actual transcription and romanization locally.

Once the required Whisper model has been downloaded and cached, transcription can operate without an active internet connection.

### Important

The first model download requires internet access unless the required model has already been provided locally.

After the model is available locally, the core transcription workflow does not require an online API.

No external cloud transcription API is required by the application.

---

# 🏗️ Technology Stack

| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| **Python**                | Core application development    |
| **PySide6**               | Desktop GUI                     |
| **Faster-Whisper**        | Speech-to-text engine           |
| **CTranslate2**           | Efficient model inference       |
| **FFmpeg**                | Audio conversion and processing |
| **indic-transliteration** | Indic-language romanization     |
| **python-docx**           | DOCX generation                 |
| **ReportLab**             | PDF generation                  |
| **Qt QThread**            | Background processing           |
| **PyInstaller**           | Windows executable packaging    |

---

# 📂 Project Structure

```text
AudioScribeAI/
│
├── app.py
│   └── Application entry point
│
├── config.py
│   └── Application configuration,
│      paths, language list and constants
│
├── requirements.txt
│   └── Python dependencies
│
├── assets/
│   ├── logo.png
│   └── icons/
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   │   └── Main application window,
│   │       controls and background worker
│   │
│   ├── upload_widget.py
│   │   └── MP3 upload and drag/drop handling
│   │
│   ├── styles.py
│   │   └── Application QSS styling
│   │
│   └── dialogs.py
│       └── Application dialogs and
│           export-name handling
│
├── engine/
│   ├── __init__.py
│   ├── audio_processor.py
│   │   └── MP3 validation, metadata,
│   │       FFmpeg conversion and cleanup
│   │
│   ├── transcriber.py
│   │   └── Faster-Whisper transcription engine
│   │
│   ├── romanizer.py
│   │   └── Indic-language transliteration
│   │
│   └── exporter.py
│       └── TXT, DOCX and PDF export
│
├── outputs/
│   └── Default transcript export directory
│
└── temp/
    └── Temporary audio-processing files
```

---

# ⚙️ Requirements

### Operating System

The application is primarily designed for:

* Windows 10
* Windows 11

It may also be adaptable to other operating systems where the required Python dependencies and FFmpeg are available.

### Python

Recommended:

```text
Python 3.10+
```

For the current project configuration, use the Python version supported by the installed Faster-Whisper/CTranslate2 dependencies.

### FFmpeg

FFmpeg is required for audio processing and MP3-to-WAV conversion.

Verify that FFmpeg is installed:

```bash
ffmpeg -version
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AudioScribeAI.git
```

Move into the project:

```bash
cd AudioScribeAI
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

From the project directory:

```bash
python app.py
```

The AudioScribe AI desktop application should open.

---

# 🎯 How to Use

### Step 1 — Upload Audio

Drag an MP3 file into the upload area or use the file browser.

### Step 2 — Review Audio Information

The application displays:

```text
File Name
File Size
Duration
Bitrate
Sample Rate
Detected Language
```

### Step 3 — Select Language

Choose:

```text
Auto Detect
```

or manually select the spoken language.

### Step 4 — Select Output Script

Choose:

```text
Romanized / English Letters
```

or:

```text
Original Script
```

### Step 5 — Start Transcription

Click:

```text
▶ Start Transcription
```

The application processes the audio in the background.

### Step 6 — Review

The completed transcription appears in the editable text area.

### Step 7 — Export

Use one of the available export options:

```text
Copy Text
Export TXT
Export DOCX
Export PDF
```

---

# 🧠 Model Configuration

The default Whisper model is:

```python
DEFAULT_MODEL_SIZE = "small"
```

Available model sizes include:

```text
tiny
base
small
medium
large-v3
```

### General trade-off

| Model    | Speed | Accuracy | Resource Usage |
| -------- | ----- | -------- | -------------- |
| tiny     | ⭐⭐⭐⭐⭐ | ⭐⭐       | Low            |
| base     | ⭐⭐⭐⭐  | ⭐⭐⭐      | Low            |
| small    | ⭐⭐⭐   | ⭐⭐⭐⭐     | Medium         |
| medium   | ⭐⭐    | ⭐⭐⭐⭐     | High           |
| large-v3 | ⭐     | ⭐⭐⭐⭐⭐    | Very High      |

For everyday usage, `small` provides a practical balance between performance and accuracy.

---

# 🖥️ CPU & GPU

The application supports automatic device selection.

Configuration includes:

```python
DEVICE = "auto"
```

CPU processing uses:

```text
int8
```

GPU processing can use:

```text
float16
```

Actual performance depends on:

* CPU
* GPU
* available RAM/VRAM
* audio duration
* selected Whisper model
* audio quality

---

# 📦 Windows EXE Packaging

The application can be packaged as a Windows executable using PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

Then build:

```bash
pyinstaller --noconsole --onefile --name AudioScribeAI --add-data "assets;assets" app.py
```

The executable will be generated inside:

```text
dist/
```

Result:

```text
dist/AudioScribeAI.exe
```

### Model Packaging Note

Whisper model files are large and are not automatically embedded into the executable by the standard PyInstaller command.

The required model should therefore be downloaded/cached before using the application completely offline.

---

# 🔍 Accuracy Considerations

Speech recognition accuracy depends on several factors.

For best results:

* Use clear audio.
* Minimize background noise.
* Use high-quality recordings.
* Select the spoken language manually when possible.
* Use a larger Whisper model when accuracy is more important than processing speed.
* Avoid heavily distorted or extremely quiet recordings.

The application includes Voice Activity Detection to help reduce unnecessary processing of silent sections.

---

# 🛡️ Error Handling

AudioScribe AI includes validation and error handling for common processing problems.

Examples include:

* Invalid MP3 files
* Unsupported audio input
* FFmpeg unavailable
* Transcription failures
* Export failures
* Missing optional dependencies
* Suspiciously incomplete transcription results

The application attempts to surface meaningful error messages instead of silently failing.

---

# 🔄 Processing Architecture

The application follows a modular processing pipeline:

```text
                MP3 Input
                   │
                   ▼
          Audio Validation
                   │
                   ▼
          Audio Metadata Read
                   │
                   ▼
          FFmpeg Audio Convert
                   │
                   ▼
        Faster-Whisper Engine
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Language Detection   Manual Language
          │                 │
          └────────┬────────┘
                   ▼
             Transcription
                   │
                   ▼
          Romanization Layer
                   │
                   ▼
          Result Validation
                   │
                   ▼
          Editable Transcript
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
       TXT        DOCX       PDF
```

---

# 🔐 Privacy

AudioScribe AI is designed around local processing.

The application does not require a third-party cloud transcription API for its core functionality.

Audio files are processed locally and temporary converted audio files are cleaned up after processing.

Users should still review their own deployment environment, dependencies, logs, and model distribution strategy when processing sensitive recordings.

---

# 🧪 Future Improvements

Potential future enhancements include:

* Support for additional audio formats
* Video transcription
* Subtitle generation
* SRT/VTT export
* Speaker identification
* Timestamped transcript editing
* Batch transcription
* Custom model selection from the UI
* GPU acceleration improvements
* Search and highlight within transcripts
* Advanced transcript formatting
* Application settings panel
* Portable Windows distribution

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

A typical contribution workflow:

```bash
git checkout -b feature/your-feature
```

Make your changes, test the application, then commit:

```bash
git add .
git commit -m "Add your feature"
```

Push your branch:

```bash
git push origin feature/your-feature
```

Then create a Pull Request.

---

# 🐛 Reporting Issues

When reporting an issue, please include:

* Operating system
* Python version
* Application version
* Whisper model used
* Audio format and approximate duration
* Full error message
* Steps to reproduce the issue

Avoid uploading private or sensitive audio files to public issue trackers.

---

# 📄 License

Add your preferred open-source license before publishing this repository.

For example:

```text
MIT License
```

If this project is intended to remain proprietary, replace this section with the appropriate proprietary license notice.

---

# 👨‍💻 Author

**Chinmayee**

Software Developer | Python | Desktop Applications | AI/ML

---

## ⭐ Project Highlights

```text
✓ Offline-first speech recognition
✓ Faster-Whisper transcription
✓ Multi-language support
✓ Indic-language romanization
✓ Original-script output
✓ Romanized output
✓ Automatic language detection
✓ Manual language selection
✓ MP3 validation and processing
✓ Background transcription
✓ Real-time progress tracking
✓ Transcript editing
✓ TXT export
✓ DOCX export
✓ PDF export
✓ Processing statistics
✓ Windows EXE packaging
✓ Modular application architecture
✓ Modern PySide6 desktop UI
```

---

## 📌 Project Status

**Version:** `1.0.0`

**Status:** Active Development

AudioScribe AI is a desktop speech-to-text application focused on accurate local transcription, multilingual support, and accessible Romanized output.

---

### Designed & Developed by Chinmayee

⭐ **If you find this project useful, consider giving the repository a star!**
