import sys
import time
from faster_whisper import WhisperModel

audio_file = sys.argv[1]
language = sys.argv[2]
model_size = sys.argv[3] if len(sys.argv) > 3 else "small"

print("Loading model:", model_size, "(first time it downloads, please wait)")
start = time.time()
model = WhisperModel(model_size, device="cpu", compute_type="int8")
print("Model loaded in", round(time.time() - start, 1), "seconds")

start = time.time()
segments, info = model.transcribe(audio_file, language=language, beam_size=5)
text = " ".join(segment.text.strip() for segment in segments)
print("Transcribed in", round(time.time() - start, 1), "seconds")

with open("test_audio/result.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("RESULT:", text)
print("Also saved to test_audio/result.txt")