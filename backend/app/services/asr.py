# backend/app/services/asr.py - empty for now, filled in during Phase 1
import os
import tempfile

from faster_whisper import WhisperModel

# Model size can be changed later by setting WHISPER_MODEL (small or medium).
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")

_model = None


def get_model():
    # Load the model only once, the first time it is needed.
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model


def transcribe(audio_bytes, language):
    # audio_bytes: the recording as bytes. language: "hi" or "mr".
    with tempfile.NamedTemporaryFile(suffix=".audio", delete=False) as f:
        f.write(audio_bytes)
        path = f.name
    try:
        segments, info = get_model().transcribe(
            path, language=language, beam_size=1, vad_filter=True
        )
        return " ".join(s.text.strip() for s in segments).strip()
    finally:
        os.remove(path)