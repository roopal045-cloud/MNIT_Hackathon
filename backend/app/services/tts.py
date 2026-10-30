# backend/app/services/tts.py
# Text to speech (voice out) for Hindi and Marathi, using gTTS (needs internet).

import hashlib
from pathlib import Path

from gtts import gTTS

# backend/generated/ is already ignored by Git (.gitignore).
AUDIO_DIR = Path(__file__).resolve().parents[2] / "generated"
SUPPORTED = {"hi", "mr"}


def make_speech(text, language):
    # text: what to say. language: "hi" or "mr".
    # Returns a URL like "/audio/ab12cd34ef56ab78.mp3", or None if it fails.
    if not text or not text.strip():
        return None

    lang = language if language in SUPPORTED else "hi"
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # Same text + language always gives the same file name, so we reuse it.
    key = (lang + ":" + text).encode("utf-8")
    name = hashlib.sha1(key).hexdigest()[:16] + ".mp3"
    path = AUDIO_DIR / name

    if not path.exists():
        try:
            gTTS(text=text, lang=lang).save(str(path))
        except Exception:
            # No internet or the service is down: answer without audio.
            return None

    return "/audio/" + name