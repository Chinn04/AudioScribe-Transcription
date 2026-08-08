# 🎙️ AudioScribe AI

### Offline AI-Powered Speech-to-Text & Romanization Desktop Application

**AudioScribe AI** is a professional Windows desktop application built with **Python, PySide6, Faster-Whisper, FFmpeg, and Indic Transliteration**.

The application converts MP3 audio into editable text, automatically detects or allows manual selection of the spoken language, and provides both **Original Script** and **Romanized / English Letters** output.

It is designed with an **offline-first architecture**, allowing transcription and processing to be performed locally without depending on a cloud transcription API.

---

## 🚀 Key Features

* 🎙️ MP3 speech-to-text transcription
* 🤖 Faster-Whisper AI transcription engine
* 🌍 80+ configured language options
* 🔎 Automatic language detection
* 🌐 Manual language selection
* 🔤 Romanized / English Letters output
* 📝 Original Script output
* 🇮🇳 Indic-language transliteration
* ⚡ Background transcription processing
* 📊 Transcription statistics
* 📈 Processing speed monitoring
* 🎧 Audio metadata detection
* 🔄 MP3-to-WAV conversion using FFmpeg
* 📄 TXT export
* 📝 DOCX export
* 📕 PDF export
* ✏️ Editable transcript
* 🎨 Modern PySide6 desktop interface
* 🖱️ Drag-and-drop MP3 upload
* 🔒 Offline-first local processing
* 🖥️ Windows executable support
* 🧹 Temporary audio cleanup
* ⚠️ Transcription validation and error handling

---

# 🌍 Supported Languages

AudioScribe AI provides the following language options in its application:

### 🇮🇳 Indian & Indic Languages

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
* Nepali
* Assamese
* Odia

### 🌎 International Languages

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
* Sinhala
* Burmese
* Afrikaans
* Amharic
* Armenian
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

### 🔍 Detection

The application also provides:

**Auto Detect**

When Auto Detect is selected, Faster-Whisper analyzes the audio and identifies the most likely spoken language.

---

# 🔤 Romanized / English Letters Output

One of the main features of AudioScribe AI is its Romanized output.

The application can convert supported native scripts into readable Roman/English letters.

### Example — Kannada

**Original Script**

```text
ನೀವು ಊಟ ಮಾಡಿದ್ದೀರಾ?
```

**Romanized**

```text
Nivu uta madidra?
```

### Example — Hindi

**Original Script**

```text
क्या तूने खाना खा लिया?
```

**Romanized**

```text
Kya tune khana kha liya?
```

### Example — Telugu

**Original Script**

```text
మీరు భోజనం చేశారా?
```

**Romanized**

```text
Meeru bhojanam chesara?
```

The Romanization feature currently provides native-script mappings for:

* Hindi
* Marathi
* Nepali
* Kannada
* Telugu
* Tamil
* Malayalam
* Bengali
* Assamese
* Gujarati
* Punjabi
* Odia

For languages without a configured transliteration mapping, the original transcription is retained.

> **Important:** Romanization is transliteration, not translation. The spoken language and meaning remain the same; only the writing system changes.

---

# 🎧 Audio Processing

AudioScribe AI accepts MP3 files and processes them through a structured audio pipeline.

### Processing Flow

```text
MP3 File
   │
   ▼
Audio Validation
   │
   ▼
Metadata Extraction
   │
   ▼
FFmpeg Conversion
   │
   ▼
WAV Processing
   │
   ▼
Faster-Whisper
   │
   ▼
Language Detection
   │
   ▼
Speech Transcription
   │
   ▼
Romanization
   │
   ▼
Transcript Validation
   │
   ▼
Editable Result
   │
   ├── TXT
   ├── DOCX
   └── PDF
```

---

# 🤖 Faster-Whisper

AudioScribe AI uses **Faster-Whisper** as its speech recognition engine.

The application supports:

* Automatic language detection
* Manual language selection
* Beam-search transcription
* Voice Activity Detection
* Temperature fallback
* Context-aware transcription
* Repetition protection
* Speech coverage analysis
* Suspicious transcription detection

This provides a robust local speech-to-text workflow while avoiding the need for an external transcription API.

---

# ⚡ Background Processing

Transcription can require significant CPU/GPU resources.

AudioScribe AI uses **PySide6/Qt background processing** so that the main user interface remains responsive during transcription.

The application provides processing stages such as:

```text
Loading Model
      ↓
Reading MP3
      ↓
Detecting Language
      ↓
Transcribing
      ↓
Romanizing
      ↓
Finalizing
      ↓
Completed
```

---

# 📊 Transcription Statistics

After transcription, the application provides useful statistics including:

* Word count
* Character count
* Audio duration
* Processing time
* Processing speed
* Detected language
* Language confidence

This allows users to quickly understand the generated transcript and processing performance.

---

# 📤 Export Options

Users can export completed transcripts into multiple formats.

## 📄 TXT

Simple plain-text transcript suitable for notes and further processing.

## 📝 DOCX

Professional Word document containing:

* Application name
* Transcript title
* Source MP3
* Detected language
* Export information
* Transcript content

## 📕 PDF

Formatted PDF report containing:

* Audio source
* Detected language
* Export information
* Transcript
* Application branding

---

# 🎨 Desktop Interface

The application is built using **PySide6** and provides a modern desktop interface.

### Interface Features

* Application branding
* Offline status indicator
* MP3 upload section
* Drag-and-drop support
* Audio information panel
* Language selector
* Output-script selector
* Start Transcription button
* Progress indicator
* Transcript editor
* Export controls
* Statistics panel
* Error and validation dialogs

---

# 🔒 Offline-First Architecture

AudioScribe AI is designed around local processing.

The core transcription workflow does not require a cloud speech-recognition API.

Once the required Faster-Whisper model has been downloaded and cached locally, transcription can be performed without an active internet connection.

### First-Time Setup

Internet access may be required initially to download the selected Whisper model and required Python packages.

After the model is available locally:

```text
MP3
 ↓
Local Audio Processing
 ↓
Local Whisper Model
 ↓
Local Transcription
 ↓
Local Romanization
 ↓
Local Export
```

No cloud transcription service is required for the core workflow.

---

# 🏗️ Technology Stack

| Technology                | Purpose                   |
| ------------------------- | ------------------------- |
| **Python**                | Application development   |
| **PySide6**               | Desktop GUI               |
| **Faster-Whisper**        | Speech recognition        |
| **CTranslate2**           | Efficient model inference |
| **FFmpeg**                | Audio conversion          |
| **Indic Transliteration** | Romanization              |
| **python-docx**           | DOCX generation           |
| **ReportLab**             | PDF generation            |
| **PyInstaller**           | Windows EXE packaging     |
| **Qt QThread**            | Background processing     |

---

# 📂 Project Structure

```text
AudioScribeAI/
│
├── app.py
│
├── config.py
│
├── requirements.txt
│
├── assets/
│   ├── logo.png
│   └── icons/
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── upload_widget.py
│   ├── styles.py
│   └── dialogs.py
│
├── engine/
│   ├── __init__.py
│   ├── audio_processor.py
│   ├── transcriber.py
│   ├── romanizer.py
│   └── exporter.py
│
├── outputs/
│   └── .gitkeep
│
├── temp/
│   └── .gitkeep
│
└── README.md
```

---

# ⚙️ Requirements

### Operating System

Recommended:

* Windows 10
* Windows 11

### Python

The project is configured for modern Python environments and has been updated for the project's Python 3.14 setup.

### FFmpeg

FFmpeg is required for audio conversion.

Verify installation:

```bash
ffmpeg -version
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AudioScribeAI.git
```

```bash
cd AudioScribeAI
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
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

Run:

```bash
python app.py
```

The AudioScribe AI desktop application will launch.

---

# 🎯 How to Use

### 1. Upload MP3

Drag and drop an MP3 file into the application or select it using the file browser.

### 2. Review Audio Information

The application displays information such as:

```text
File Name
File Size
Duration
Bitrate
Sample Rate
```

### 3. Select Language

Choose a language manually or select:

```text
Auto Detect
```

### 4. Select Output Format

Choose between:

```text
Romanized / English Letters
```

or:

```text
Original Script
```

### 5. Start Transcription

Click:

```text
Start Transcription
```

The transcription runs in the background.

### 6. Review Transcript

The generated transcript is displayed in the application and can be reviewed or edited.

### 7. Export

Export the result as:

```text
TXT
DOCX
PDF
```

---

# 🧠 Whisper Model

The project uses a configurable Faster-Whisper model.

Typical model options include:

```text
tiny
base
small
medium
large-v3
```

### Model Comparison

| Model    | Speed | Accuracy | Resource Usage |
| -------- | ----: | -------: | -------------: |
| Tiny     | ⭐⭐⭐⭐⭐ |       ⭐⭐ |            Low |
| Base     |  ⭐⭐⭐⭐ |      ⭐⭐⭐ |            Low |
| Small    |   ⭐⭐⭐ |     ⭐⭐⭐⭐ |         Medium |
| Medium   |    ⭐⭐ |     ⭐⭐⭐⭐ |           High |
| Large-v3 |     ⭐ |    ⭐⭐⭐⭐⭐ |      Very High |

The appropriate model can be selected based on the available hardware and required accuracy.

---

# 🖥️ CPU & GPU

AudioScribe AI supports automatic hardware selection.

Typical configuration:

```text
Device: Auto
```

CPU processing can use:

```text
int8
```

GPU processing can use:

```text
float16
```

Performance depends on:

* CPU
* GPU
* RAM
* VRAM
* Audio duration
* Selected Whisper model
* Audio quality

---

# 📦 Windows EXE

The project can be packaged into a standalone Windows executable using PyInstaller.

Install:

```bash
pip install pyinstaller
```

Example:

```bash
pyinstaller --noconsole --onefile --name AudioScribeAI --add-data "assets;assets" app.py
```

The generated application will be available inside:

```text
dist/
```

Example:

```text
dist/AudioScribeAI.exe
```

> Whisper model files are large and may need to be downloaded or supplied separately rather than being embedded directly into the executable.

---

# 🛡️ Error Handling

AudioScribe AI includes handling for common application and transcription issues, including:

* Invalid MP3 files
* Unsupported audio
* Missing FFmpeg
* Transcription failures
* Model-loading failures
* Export errors
* Missing dependencies
* Low-quality audio
* Suspicious or incomplete transcription results

The application attempts to display meaningful feedback instead of silently failing.

---

# 🔐 Privacy

AudioScribe AI is designed for local processing.

The application does not require a third-party cloud transcription API for its core speech-to-text workflow.

Temporary converted audio files are used during processing and can be cleaned after transcription.

For sensitive recordings, users should still review their own system, model, dependency, and storage configuration.

---

# 🔮 Future Enhancements

Potential future improvements include:

* 🎬 Video transcription
* 🎞️ SRT subtitle generation
* 📝 VTT subtitle generation
* 👥 Speaker identification
* ⏱️ Timestamped transcript editing
* 📚 Batch audio processing
* 🔍 Transcript search
* 🎨 Advanced transcript formatting
* ⚙️ Application settings
* 🚀 Improved GPU acceleration
* 📦 Portable Windows distribution

---

# 🤝 Contributing

Contributions and suggestions are welcome.

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Stage changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Add your feature"
```

Push:

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 🐛 Reporting Issues

When reporting an issue, provide:

* Operating system
* Python version
* Application version
* Whisper model
* Approximate audio duration
* Error message
* Steps to reproduce

Do not upload private or sensitive audio recordings to public issues.

---

# 📄 License

Add the appropriate license before publishing the repository.

For an open-source project, you may use:

```text
MIT License
```

If the project is proprietary, replace this section with the appropriate proprietary license notice.

---

# 👨‍💻 Designed & Developed By

## **Chinmayee**

**Python Developer | AI/ML | Desktop Application Development | Speech Processing**

---

# ⭐ Project Highlights

```text
✓ Offline-first AI transcription
✓ Faster-Whisper speech recognition
✓ 80+ configured language options
✓ Automatic language detection
✓ Manual language selection
✓ Indic-language Romanization
✓ Original Script support
✓ Romanized / English Letters output
✓ MP3 processing
✓ FFmpeg audio conversion
✓ Background transcription
✓ Real-time progress tracking
✓ Transcript editing
✓ Processing statistics
✓ TXT export
✓ DOCX export
✓ PDF export
✓ Modern PySide6 interface
✓ Windows EXE support
✓ Local processing architecture
✓ Modular Python architecture
```

---

## ⭐ Support the Project

If you find **AudioScribe AI** useful, consider giving the repository a ⭐ **Star** on GitHub.

### Designed & Developed with ❤️ by **Chinmayee**
