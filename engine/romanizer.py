"""
engine/romanizer.py
Optional, fully-local Roman-alphabet TRANSLITERATION layer for Indic
languages.

IMPORTANT: this is transliteration, not translation. Meaning, word order
and language are all preserved - only the writing system changes (native
script -> Roman/English letters), e.g.:

    "ನೀವು ಊಟ ಮಾಡಿದ್ದೀರಾ?"  ->  "Nivu uta madidra?"

It never calls out to the network - it uses the local, offline
'indic-transliteration' library (pure-Python Unicode mapping tables), so
the application stays fully offline. If that optional dependency isn't
installed, or the language has no script mapping here (e.g. English),
romanize_text() simply hands the text back unchanged - it never raises,
so this feature can never break the core transcription pipeline.
"""

import re
import sys
from typing import Optional

try:
    from indic_transliteration import sanscript
    _SANSCRIPT_AVAILABLE = True
except Exception:
    _SANSCRIPT_AVAILABLE = False


def _log(msg: str) -> None:
    print(f"[AudioScribeAI] {msg}", file=sys.stderr, flush=True)


# Whisper language code -> the Brahmic script that language is written in.
# (A few languages share a script family, e.g. Hindi/Marathi/Nepali all
# use Devanagari.) Only languages with a well-defined native script are
# listed - everything else (English, "auto", etc.) is left untouched by
# romanize_text().
LANGUAGE_TO_SCRIPT = {
    "hi": "devanagari",   # Hindi
    "mr": "devanagari",   # Marathi
    "ne": "devanagari",   # Nepali
    "kn": "kannada",      # Kannada
    "te": "telugu",       # Telugu
    "ta": "tamil",        # Tamil
    "ml": "malayalam",    # Malayalam
    "bn": "bengali",      # Bengali
    "as": "assamese",     # Assamese (falls back to the Bengali-script
                           # mapping below if 'assamese' isn't available
                           # in the installed library version)
    "gu": "gujarati",     # Gujarati
    "pa": "gurmukhi",     # Punjabi (Gurmukhi script)
    "or": "oriya",        # Odia
}

# Preferred ASCII-only (no diacritics) output scheme first, then fallbacks,
# in case an installed library version only ships some of these.
_TARGET_SCHEME_CANDIDATES = ("optitrans", "itrans", "hk")

_SENTENCE_END_RE = re.compile(r"([.!?]+\s*)")


def is_romanizable(language_code: Optional[str]) -> bool:
    """True if we have a native-script mapping for this language code."""
    return bool(language_code) and language_code in LANGUAGE_TO_SCRIPT


def romanize_text(text: str, language_code: Optional[str]) -> str:
    """
    Transliterate `text` (written in the native script for
    `language_code`) into simple, keyboard-friendly Roman letters.

    Any characters that are already Latin script (numbers, punctuation,
    or code-switched English words like "office") are left untouched by
    the underlying transliteration engine, since it only maps characters
    that belong to the source script's Unicode block.

    Returns the original text unchanged if romanization isn't applicable
    or fails for any reason - this function never raises.
    """
    if not text or not text.strip():
        return text

    if not _SANSCRIPT_AVAILABLE:
        _log("Romanization skipped: 'indic-transliteration' is not installed.")
        return text

    source_scheme = LANGUAGE_TO_SCRIPT.get(language_code)
    if not source_scheme:
        # English, or a language without a script mapping here - nothing
        # to transliterate.
        return text

    sources_to_try = (
        [source_scheme] if source_scheme != "assamese"
        else ["assamese", "bengali"]
    )

    romanized = None
    for src in sources_to_try:
        for target in _TARGET_SCHEME_CANDIDATES:
            try:
                romanized = sanscript.transliterate(text, src, target)
                break
            except Exception as exc:
                _log(f"Romanization attempt ({src} -> {target}) failed: {exc}")
        if romanized is not None:
            break

    if romanized is None:
        _log("Romanization failed for all scheme combinations; keeping "
             "original-script text.")
        return text

    return _casualize(romanized)


def _casualize(romanized: str) -> str:
    """
    Formal transliteration schemes (ITRANS/OPTITRANS/HK) use mixed
    capitalization to mark linguistic distinctions (retroflex consonants,
    vowel length, etc). For a normal reader that just looks like random
    mid-word capitals, so this normalizes to simple, keyboard-friendly
    casing: lowercase throughout, with each sentence capitalized at its
    start - ordinary English sentence casing.
    """
    lowered = romanized.lower()
    parts = _SENTENCE_END_RE.split(lowered)
    out = []
    capitalize_next = True
    for part in parts:
        if not part:
            continue
        if _SENTENCE_END_RE.fullmatch(part):
            out.append(part)
            capitalize_next = True
        else:
            if capitalize_next:
                part = part[:1].upper() + part[1:]
                capitalize_next = False
            out.append(part)
    return "".join(out).strip()
