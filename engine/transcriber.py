"""
engine/transcriber.py
Wraps Faster-Whisper: model loading, language detection, and segment-by-
segment transcription with progress callbacks. No UI imports here -
this module is UI-agnostic so it can be reused (CLI, tests, etc).
"""

import sys
import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from faster_whisper import WhisperModel

import config
from engine.romanizer import romanize_text


def _log(msg: str) -> None:
    """Diagnostic logging to the console, per the error-handling requirement."""
    print(f"[AudioScribeAI] {msg}", file=sys.stderr, flush=True)


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class TranscriptionResult:
    text: str
    language: str
    language_probability: float
    # Same transcript, transliterated to Roman/English letters when the
    # detected/selected language has a native-script mapping (see
    # engine/romanizer.py). Computed once here, alongside `text`, so the
    # UI can freely switch between the two without ever re-running
    # Whisper. Equal to `text` for English or unsupported languages.
    romanized_text: str = ""
    segments: List[TranscriptSegment] = field(default_factory=list)
    processing_seconds: float = 0.0
    audio_duration: float = 0.0
    speech_seconds: float = 0.0
    warning: Optional[str] = None  # set when the result looks suspiciously short


# Progress callback signature: (stage: str, percent: int, message: str) -> None
# `percent == -1` means "duration unknown for this stage" - the UI should show
# an indeterminate/busy indicator rather than a specific (and possibly
# misleading) percentage.
ProgressCallback = Callable[[str, int, str], None]

INDETERMINATE = -1


class TranscriberError(Exception):
    """Raised for any failure during model load or transcription."""


class Transcriber:
    """
    Loads a Faster-Whisper model once and reuses it across transcriptions.
    Designed to run inside a worker thread - all methods are blocking.
    """

    def __init__(self, model_size: str = config.DEFAULT_MODEL_SIZE):
        self.model_size = model_size
        self._model: Optional[WhisperModel] = None

    def load_model(self, progress_cb: Optional[ProgressCallback] = None) -> None:
        if self._model is not None:
            # Model already loaded/cached in memory - reuse it, do not reload.
            _log(f"Reusing already-loaded '{self.model_size}' model.")
            return

        device, compute_type = self._pick_device_and_compute_type()

        # Model loading (and, on first run, downloading the model weights)
        # is a single blocking call whose duration we cannot predict, so we
        # report it as indeterminate instead of freezing on a fixed percent.
        if progress_cb:
            progress_cb(
                config.STAGE_LOADING_MODEL, INDETERMINATE,
                f"Loading Whisper model ({self.model_size}) on {device.upper()} "
                f"({compute_type})... this can take a while on first run "
                f"while the model is downloaded and cached."
            )
        _log(f"Loading WhisperModel(size={self.model_size!r}, device={device!r}, "
             f"compute_type={compute_type!r})")

        t0 = time.time()
        try:
            self._model = WhisperModel(
                self.model_size, device=device, compute_type=compute_type
            )
        except Exception as exc:
            _log(f"Model load failed: {exc}")
            raise TranscriberError(f"Failed to load Whisper model: {exc}") from exc

        _log(f"Model loaded in {time.time() - t0:.1f}s.")
        if progress_cb:
            progress_cb(config.STAGE_LOADING_MODEL, 15, "Whisper model ready.")

    @staticmethod
    def _pick_device_and_compute_type():
        """
        Try GPU first, fall back to CPU (int8) if CUDA isn't usable.

        We deliberately do NOT depend on torch here (it isn't a project
        dependency and pulling it in just for a CUDA check would add an
        unnecessary, heavy install). faster-whisper's own backend
        (ctranslate2) already knows how to enumerate CUDA devices, so we
        ask it directly. Any failure here just means "no usable GPU" and
        we transparently fall back to CPU - the app must keep working on
        CPU-only Windows systems either way.
        """
        if config.DEVICE == "cpu":
            return "cpu", config.COMPUTE_TYPE_CPU
        if config.DEVICE == "cuda":
            return "cuda", config.COMPUTE_TYPE_GPU

        try:
            import ctranslate2
            if ctranslate2.get_cuda_device_count() > 0:
                _log("CUDA device detected via ctranslate2 - using GPU.")
                return "cuda", config.COMPUTE_TYPE_GPU
        except Exception as exc:
            _log(f"CUDA probe failed/unavailable, using CPU. ({exc})")
        return "cpu", config.COMPUTE_TYPE_CPU

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        progress_cb: Optional[ProgressCallback] = None,
    ) -> TranscriptionResult:
        """
        Transcribe the given audio file (a WAV path is recommended).
        `language` should be a Whisper language code, or None/"auto" for
        automatic detection.
        """
        if self._model is None:
            self.load_model(progress_cb)

        lang_arg = None if (language in (None, "auto", "")) else language

        if progress_cb:
            progress_cb(config.STAGE_READING_AUDIO, INDETERMINATE,
                        "Reading audio stream...")

        start_time = time.time()
        segments, text_parts, info = self._run_transcription_pass(
            audio_path, lang_arg, progress_cb, use_vad=True
        )
        total_duration = max(info.duration, 0.001)
        speech_seconds = sum(max(s.end - s.start, 0.0) for s in segments)

        # --- Safety net against an over-aggressive VAD -----------------
        # If Voice Activity Detection classified almost the entire file as
        # "non-speech" (e.g. quiet recordings, background noise/music
        # confusing the detector), we can end up with a technically-valid
        # but essentially empty/partial transcript even though the pipeline
        # "worked". Detect that case and automatically retry once WITHOUT
        # the VAD filter so we fall back to transcribing the raw audio.
        coverage = speech_seconds / total_duration
        if coverage < 0.15 and total_duration > 5.0:
            _log(
                f"VAD kept only {coverage * 100:.1f}% of {total_duration:.1f}s "
                f"of audio as speech - retrying WITHOUT vad_filter."
            )
            if progress_cb:
                progress_cb(
                    config.STAGE_TRANSCRIBING, INDETERMINATE,
                    "Initial pass looked suspiciously short - retrying without "
                    "voice-activity filtering..."
                )
            retry_segments, retry_text_parts, info = self._run_transcription_pass(
                audio_path, lang_arg, progress_cb, use_vad=False
            )
            retry_speech = sum(max(s.end - s.start, 0.0) for s in retry_segments)
            if retry_speech > speech_seconds:
                segments, text_parts = retry_segments, retry_text_parts
                speech_seconds = retry_speech

        full_text = self._format_transcript(text_parts)

        # Romanize using whichever language actually drove the
        # transcription: an explicit user selection (lang_arg) takes
        # priority, exactly as it does for the transcription pass above;
        # otherwise fall back to what Whisper auto-detected. This is a
        # pure post-processing step on the already-complete transcript -
        # it never touches the audio or re-runs the model.
        romanization_language = lang_arg or info.language
        romanized_text = romanize_text(full_text, romanization_language)

        elapsed = time.time() - start_time
        _log(
            f"Transcription pass complete: {len(segments)} segments, "
            f"{len(full_text.split())} words, "
            f"{speech_seconds:.1f}s of speech in {total_duration:.1f}s of audio, "
            f"took {elapsed:.1f}s."
        )

        if progress_cb:
            progress_cb(config.STAGE_FINALIZING, 98, "Finalizing transcript...")

        # --- Suspicious-result validation -------------------------------
        # Never silently report success on an obviously incomplete result.
        # We do NOT invent or pad missing text - we just flag it honestly
        # so the UI/user is told the truth instead of "Completed".
        warning = None
        word_count = len(full_text.split())
        coverage = speech_seconds / total_duration
        if total_duration > 20.0 and (word_count < 3 or coverage < 0.05):
            warning = (
                f"This result looks incomplete: only {word_count} word(s) were "
                f"recognized from {self._format_time(total_duration)} of audio "
                f"({coverage * 100:.1f}% detected as speech). This may indicate "
                f"very quiet audio, background noise, or an unsupported "
                f"language - it is NOT a confirmed complete transcription."
            )
            _log(f"WARNING: {warning}")

        return TranscriptionResult(
            text=full_text,
            language=info.language,
            language_probability=info.language_probability,
            romanized_text=romanized_text,
            segments=segments,
            processing_seconds=elapsed,
            audio_duration=total_duration,
            speech_seconds=speech_seconds,
            warning=warning,
        )

    def _run_transcription_pass(
        self,
        audio_path: str,
        lang_arg: Optional[str],
        progress_cb: Optional[ProgressCallback],
        use_vad: bool,
    ):
        """
        Runs one full model.transcribe() pass and FULLY consumes the
        segment iterator (faster-whisper streams segments lazily - the
        transcription for segment N doesn't happen until it's iterated).
        Every segment's text is collected here; nothing is returned early.
        """
        try:
            segments_iter, info = self._model.transcribe(
                audio_path,
                language=lang_arg,
                task="transcribe",
                # Decoding search width. beam_size=5 / best_of=5 / patience=1.0
                # mirror Whisper's own recommended "high accuracy" settings -
                # wide enough to meaningfully improve word choice over greedy
                # decoding, without the runtime blowing up on CPU.
                beam_size=5,
                best_of=5,
                patience=1.0,
                # Fallback temperature ladder: if a segment's decode looks
                # unreliable (see thresholds below), retry it at increasing
                # temperature instead of silently keeping a bad guess.
                temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                # Let the model use prior segments as context, which helps
                # resolve ambiguous/similar-sounding words (e.g. "meeting"
                # vs "meaning") using surrounding speech.
                condition_on_previous_text=True,
                # Guard against condition_on_previous_text's main failure
                # mode - the model looping on / duplicating a phrase. This
                # discourages immediate repeats without discarding valid
                # repeated words that legitimately occur in speech.
                repetition_penalty=1.1,
                no_repeat_ngram_size=3,
                vad_filter=use_vad,
                vad_parameters={
                    # Slightly more sensitive than the library default (0.5)
                    # so quieter-but-real speech isn't classified as
                    # silence and dropped.
                    "threshold": 0.35,
                    "min_silence_duration_ms": 500,
                    "speech_pad_ms": 400,
                } if use_vad else None,
            )
        except Exception as exc:
            raise TranscriberError(f"Transcription failed to start: {exc}") from exc

        if progress_cb:
            detected = config.WHISPER_LANGUAGES.get(info.language, info.language)
            progress_cb(
                config.STAGE_DETECTING_LANGUAGE, 30,
                f"Detected language: {detected} "
                f"({info.language_probability * 100:.0f}% confidence)"
            )

        segments: List[TranscriptSegment] = []
        text_parts: List[str] = []
        total_duration = max(info.duration, 0.001)

        # This loop MUST run to completion - segments_iter is a generator,
        # and every iteration performs real decoding work for that chunk of
        # audio. Stopping early (break/return) or only reading the first
        # item would silently truncate the transcript.
        for seg in segments_iter:
            clean_text = seg.text.strip()
            segments.append(TranscriptSegment(seg.start, seg.end, clean_text))
            if clean_text:
                text_parts.append(clean_text)

            if progress_cb:
                # Map transcription progress into the 30-95% range.
                frac = min(seg.end / total_duration, 1.0)
                percent = int(30 + frac * 65)
                progress_cb(
                    config.STAGE_TRANSCRIBING, percent,
                    f"Transcribing... {self._format_time(seg.end)} / "
                    f"{self._format_time(total_duration)}"
                )

        return segments, text_parts, info

    @staticmethod
    def _format_transcript(parts: List[str]) -> str:
        """
        Join segments into readable paragraphs. Faster-Whisper already
        applies punctuation and capitalization per segment; here we just
        join them cleanly and avoid duplicated spacing.
        """
        joined = " ".join(p for p in parts if p)
        # Collapse accidental double spaces from segment joins.
        while "  " in joined:
            joined = joined.replace("  ", " ")
        return joined.strip()

    @staticmethod
    def _format_time(seconds: float) -> str:
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
